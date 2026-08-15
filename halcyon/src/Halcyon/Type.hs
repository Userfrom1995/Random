module Halcyon.Type
  ( MonoT (..)
  , Scheme (..)
  , Class (..)
  , Env
  , inferProgram
  , inferOneExpr
  , showType
  , showScheme
  , emptyEnv
  , builtins
  ) where

import qualified Data.Map.Strict as Map
import qualified Data.Set as Set
import Control.Monad (forM_, when)
import Data.Maybe (fromMaybe)

import Halcyon.AST
import Halcyon.Errors

-- | Monomorphic types. Type variables are de Bruijn-like integer ids.
data MonoT
  = TInt
  | TFloat
  | TBool
  | TString
  | TList MonoT
  | TVar Int
  | TFun MonoT MonoT
  deriving (Eq, Show)

-- | Constraint classes for overloaded operators.
data Class = NumC | OrdC | EqC | AppC
  deriving (Eq, Show)

-- | A type scheme: quantified variables, the constraints on those variables,
-- and the body type.
data Scheme = Scheme
  { schVars :: [Int]
  , schCons :: [(Int, Class)]
  , schType :: MonoT
  }
  deriving (Eq, Show)

type Env = [(Name, Scheme)]

-- | Inference state: fresh-variable counter, substitution, and the set of
-- outstanding overload constraints (var, class).
data TCState = TCState
  { stNext   :: !Int
  , stSubst  :: Map.Map Int MonoT
  , stCons   :: [(Int, Class)]
  , stErrPos :: Maybe Pos
  }

initState :: TCState
initState = TCState 0 Map.empty [] Nothing

type Subst = Map.Map Int MonoT

newtype TC a = TC { runTC :: TCState -> Either HErr (a, TCState) }

instance Functor TC where
  fmap f (TC g) = TC $ \s -> do
    (a, s') <- g s
    pure (f a, s')

instance Applicative TC where
  pure a = TC $ \s -> Right (a, s)
  TC f <*> TC g = TC $ \s -> do
    (fn, s') <- f s
    (a, s'') <- g s'
    pure (fn a, s'')

instance Monad TC where
  TC g >>= f = TC $ \s -> do
    (a, s') <- g s
    runTC (f a) s'

get :: TC TCState
get = TC $ \s -> Right (s, s)

modify :: (TCState -> TCState) -> TC ()
modify f = TC $ \s -> Right ((), f s)

throwType :: String -> TC a
throwType m = TC $ \s -> Left (HErr (fromMaybe originPos (stErrPos s)) m)

-- | Make the given position the error position for any error thrown while
-- running the computation.
withPos :: Pos -> TC a -> TC a
withPos p (TC g) = TC $ \s -> g s { stErrPos = Just p }

freshVar :: TC Int
freshVar = TC $ \s -> Right (stNext s, s { stNext = stNext s + 1 })

fresh :: TC MonoT
fresh = TVar <$> freshVar

-- | Substitute a type fully (top-level chains are collapsed).
prune :: Subst -> MonoT -> MonoT
prune s t = case t of
  TVar a -> case Map.lookup a s of
    Just u -> prune s u
    Nothing -> t
  TList inner -> TList (prune s inner)
  TFun a b -> TFun (prune s a) (prune s b)
  _ -> t

ftv :: MonoT -> Set.Set Int
ftv t = case t of
  TVar a -> Set.singleton a
  TList inner -> ftv inner
  TFun a b -> ftv a `Set.union` ftv b
  _ -> Set.empty

ftvScheme :: Scheme -> Set.Set Int
ftvScheme (Scheme vs _ t) = ftv t `Set.difference` Set.fromList vs

-- | Check a concrete type against a class, transferring list constraints to
-- the element type.
checkClass :: Class -> MonoT -> TC ()
checkClass c t = do
  s <- get
  let t' = prune (stSubst s) t
  case (c, t') of
    (_, TVar y) -> addConstraint y c
    (NumC, TInt) -> pure ()
    (NumC, TFloat) -> pure ()
    (OrdC, TInt) -> pure ()
    (OrdC, TFloat) -> pure ()
    (OrdC, TString) -> pure ()
    (EqC, TInt) -> pure ()
    (EqC, TFloat) -> pure ()
    (EqC, TBool) -> pure ()
    (EqC, TString) -> pure ()
    (EqC, TList e) -> checkClass EqC e
    (AppC, TString) -> pure ()
    (AppC, TList _) -> pure ()
    (cl, TFun _ _) -> throwType ("type error: functions have no instance of " ++ show cl)
    (_, _) -> throwType ("type error: no instance of " ++ show c ++ " for " ++ showType t')

-- | Record that a type variable must be an instance of a class. If the
-- variable is already bound, check immediately.
addConstraint :: Int -> Class -> TC ()
addConstraint y c = do
  s <- get
  case Map.lookup y (stSubst s) of
    Just t -> checkClass c t
    Nothing -> modify (\st -> st { stCons = (y, c) : stCons st })

-- | Constrain a monotype against a class: variables get the constraint,
-- ground types are checked immediately.
constrain :: MonoT -> Class -> TC ()
constrain t c = case t of
  TVar x -> addConstraint x c
  _ -> checkClass c t

-- | Bind a variable to a type, discharging all constraints on it.
bindVar :: Int -> MonoT -> TC ()
bindVar x t = do
  s <- get
  let t' = prune (stSubst s) t
  if TVar x == t'
    then pure ()
    else do
      when (x `Set.member` ftv t') (throwType ("type error: infinite type (" ++ showType t' ++ " contains itself)"))
      let consX = [c | (y, c) <- stCons s, y == x]
      modify (\st -> st { stSubst = Map.insert x t' (stSubst st) })
      forM_ consX (\c -> checkClass c t')

-- | Numeric promotion: when Int and Float meet, both become Float. Rewrites
-- any substitution entry that resolves to a numeric type.
promoteFloat :: TC ()
promoteFloat = do
  s <- get
  let subst' = Map.map (\v -> if prune (stSubst s) v `elem` [TInt, TFloat] then TFloat else v) (stSubst s)
  modify (\st -> st { stSubst = subst' })

-- | Unify two types. Returns the unified type (after numeric promotion the
-- two types join to Float, so the result may differ from both inputs).
unify :: MonoT -> MonoT -> TC MonoT
unify a b = do
  s <- get
  let a' = prune (stSubst s) a
      b' = prune (stSubst s) b
  case (a', b') of
    (TVar x, TVar y) | x == y -> pure a'
    (TVar x, t) -> bindVar x t >> pure t
    (t, TVar x) -> bindVar x t >> pure t
    (TInt, TInt) -> pure TInt
    (TFloat, TFloat) -> pure TFloat
    (TInt, TFloat) -> promoteFloat >> pure TFloat
    (TFloat, TInt) -> promoteFloat >> pure TFloat
    (TBool, TBool) -> pure TBool
    (TString, TString) -> pure TString
    (TList x, TList y) -> TList <$> unify x y
    (TFun a1 b1, TFun a2 b2) -> do
      u1 <- unify a1 a2
      u2 <- unify b1 b2
      pure (TFun u1 u2)
    _ -> throwType ("type error: cannot unify " ++ showType a' ++ " with " ++ showType b')

-- | Unify and discard the resulting type.
unify_ :: MonoT -> MonoT -> TC ()
unify_ a b = unify a b >> pure ()

-- | Instantiate a scheme: fresh variables for the quantified ones, and the
-- scheme's constraints re-emitted on those fresh variables.
instantiate :: Scheme -> TC MonoT
instantiate (Scheme vs cons body) = do
  mp <- Map.fromList <$> mapM (\x -> (,) x <$> fresh) vs
  let body' = substTy mp body
  forM_ cons $ \(x, c) ->
    case Map.lookup x mp of
      Just y -> constrain y c
      Nothing -> pure ()
  pure body'

substTy :: Map.Map Int MonoT -> MonoT -> MonoT
substTy mp t = case t of
  TVar a -> Map.findWithDefault (TVar a) a mp
  TList inner -> TList (substTy mp inner)
  TFun a b -> TFun (substTy mp a) (substTy mp b)
  _ -> t

-- | Generalize a type over everything not free in the environment. Constraints
-- on the quantified variables travel with the scheme.
generalize :: Env -> MonoT -> TC Scheme
generalize env t = do
  s <- get
  let t' = prune (stSubst s) t
      envVars = Set.unions (map (ftvScheme . snd) env)
      quant = Set.toList (ftv t' `Set.difference` envVars)
      qcons = [(x, c) | (x, c) <- stCons s, x `elem` quant]
  modify (\st -> st { stCons = [c | c <- stCons st, c `notElem` qcons] })
  pure (Scheme quant qcons t')

-- | Default any remaining constraints on free variables (they are
-- unconstrained by context) to Int, like Haskell's defaulting rule.
finalize :: TC ()
finalize = do
  s <- get
  let unresolved = [(x, c) | (x, c) <- stCons s, not (Map.member x (stSubst s))]
  forM_ unresolved $ \(x, _c) -> bindVar x TInt

lookupEnv :: Env -> Name -> Pos -> TC Scheme
lookupEnv env n p = case lookup n env of
  Just sch -> pure sch
  Nothing -> withPos p (throwType ("type error: unbound variable '" ++ n ++ "'"))

emptyEnv :: Env
emptyEnv = []

-- | The built-in environment.
builtins :: Env
builtins = map (\(n, vs, t) -> (n, Scheme vs [] t))
  [ ("head", [0], TFun (TList (TVar 0)) (TVar 0))
  , ("tail", [0], TFun (TList (TVar 0)) (TList (TVar 0)))
  , ("null", [0], TFun (TList (TVar 0)) TBool)
  , ("print", [0], TFun (TVar 0) (TVar 0))
  , ("show", [0], TFun (TVar 0) TString)
  ]

-- | Turn a surface annotation into a monotype.
fromAnn :: Type -> TC MonoT
fromAnn ty = case ty of
  TyInt -> pure TInt
  TyFloat -> pure TFloat
  TyBool -> pure TBool
  TyString -> pure TString
  TyList inner -> TList <$> fromAnn inner
  TyFun a b -> TFun <$> fromAnn a <*> fromAnn b
  TyVar _ -> fresh

-- | Infer the type of a definition body, applying an annotation if present.
inferDef :: Env -> Name -> Maybe Type -> [Name] -> Expr -> TC MonoT
inferDef env _n ann params def = do
  let body = case params of
        [] -> def
        _ -> at (exprPos def) (ELam params def)
  t <- withPos (exprPos def) (infer env body)
  case ann of
    Nothing -> pure t
    Just ty -> do
      aty <- fromAnn ty
      withPos (exprPos def) (unify_ t aty)
      pure aty

-- | Infer the type of an expression.
infer :: Env -> Expr -> TC MonoT
infer env e = withPos (exprPos e) $ case exprK e of
  EInt _ -> pure TInt
  EFloat _ -> pure TFloat
  EBool _ -> pure TBool
  EString _ -> pure TString
  EVar n -> instantiate =<< lookupEnv env n (exprPos e)
  EList es -> do
    case es of
      [] -> TList <$> fresh
      _ -> do
        ts <- mapM (infer env) es
        a <- fresh
        mapM_ (unify_ a) ts
        pure (TList a)
  ECons x xs -> do
    tx <- infer env x
    txs <- infer env xs
    a <- fresh
    unify_ txs (TList a)
    unify_ tx a
    pure (TList a)
  EApp f a -> do
    tf <- infer env f
    ta <- infer env a
    b <- fresh
    unify_ tf (TFun ta b)
    pure b
  ELam params body -> do
    pvs <- mapM (const fresh) params
    let env' = extendParams env (zip params (map (\v -> Scheme [] [] v) pvs))
    tb <- infer env' body
    pure (foldr TFun tb pvs)
  EIf c t f -> do
    tc <- infer env c
    unify_ tc TBool
    tt <- infer env t
    tf <- infer env f
    u <- unify tt tf
    pure u
  ELet n ann params def body -> do
    td <- inferDef env n ann params def
    gen <- generalize env td
    infer (extendParams env [(n, gen)]) body
  ELetRec n ann params def body -> do
    a <- fresh
    let env' = extendParams env [(n, Scheme [] [] a)]
    td <- inferDef env' n ann params def
    unify_ a td
    gen <- generalize env td
    infer (extendParams env [(n, gen)]) body
  EOp op l r -> do
    tl <- infer env l
    tr <- infer env r
    case op of
      "+" -> numeric tl tr False
      "-" -> numeric tl tr False
      "*" -> numeric tl tr False
      "/" -> numeric tl tr True
      "%" -> do
        u1 <- unify tl TInt
        u2 <- unify tr TInt
        when (u1 == TFloat || u2 == TFloat) (throwType "type error: '%' requires Int operands")
        pure TInt
      "<" -> cmp tl tr OrdC
      "<=" -> cmp tl tr OrdC
      ">" -> cmp tl tr OrdC
      ">=" -> cmp tl tr OrdC
      "==" -> cmp tl tr EqC
      "/=" -> cmp tl tr EqC
      "&&" -> boolOp tl tr
      "||" -> boolOp tl tr
      "++" -> do
        a <- fresh
        constrain a AppC
        unify_ tl a
        unify_ tr a
        pure a
      other -> throwType ("type error: unknown operator '" ++ other ++ "'")
  EUnary "-" inner -> do
    a <- fresh
    constrain a NumC
    te <- infer env inner
    unify_ te a
    pure a
  EUnary "not" inner -> do
    te <- infer env inner
    unify_ te TBool
    pure TBool
  EUnary op _ -> throwType ("type error: unknown unary operator '" ++ op ++ "'")

-- | A numeric operator: both operands share a Num-constrained variable; for
-- integer division the result is always Float.
numeric :: MonoT -> MonoT -> Bool -> TC MonoT
numeric tl tr alwaysFloat = do
  a <- fresh
  constrain a NumC
  unify_ tl a
  unify_ tr a
  pure (if alwaysFloat then TFloat else a)

-- | A comparison operator: both operands share a class-constrained variable,
-- result is Bool.
cmp :: MonoT -> MonoT -> Class -> TC MonoT
cmp tl tr c = do
  a <- fresh
  constrain a c
  unify_ tl a
  unify_ tr a
  pure TBool

boolOp :: MonoT -> MonoT -> TC MonoT
boolOp tl tr = do
  unify_ tl TBool
  unify_ tr TBool
  pure TBool

extendParams :: Env -> [(Name, Scheme)] -> Env
extendParams env = foldr (\(n, sch) acc -> (n, sch) : acc) env

-- | Infer the types of all top-level statements. Returns the type of every
-- top-level binding (in order) together with the final environment.
inferProgram :: Env -> [Stmt] -> Either HErr [(Name, Scheme)]
inferProgram start stmts = do
  (pairs, _) <- runTC (go stmts start [] >>= \acc -> finalize >> pure acc) initState
  pure pairs
  where
    go [] _env acc = pure (reverse acc)
    go (st : rest) env acc = case st of
      SDef n ann params def -> do
        a <- fresh
        let envR = extendParams env [(n, Scheme [] [] a)]
        td <- inferDef envR n ann params def
        unify_ a td
        gen <- generalize env td
        go rest (extendParams env [(n, gen)]) ((n, gen) : acc)
      SPrint e -> do
        _ <- infer env e
        go rest env acc
      SExpr e -> do
        _ <- infer env e
        go rest env acc

-- | Infer the type of a single expression (used by the REPL and eval).
inferOneExpr :: Env -> Expr -> Either HErr (MonoT, Env)
inferOneExpr start e = do
  (t, _) <- runTC (infer start e >>= \t -> finalize >> pure t) initState
  pure (t, start)

-- | Render a monotype with readable variable names.
showType :: MonoT -> String
showType = go
  where
    go ty = case ty of
      TInt -> "Int"
      TFloat -> "Float"
      TBool -> "Bool"
      TString -> "String"
      TVar a -> "t" ++ show a
      TList inner -> "[" ++ go inner ++ "]"
      TFun a b -> paren (isFun a) (go a) ++ " -> " ++ go b
    isFun TFun {} = True
    isFun _ = False
    paren True s = "(" ++ s ++ ")"
    paren False s = s

-- | Render a scheme. Quantified variables are renumbered to a, b, c, ... in
-- order of first appearance so output is stable and readable.
showScheme :: Scheme -> String
showScheme (Scheme vs cons body) =
  let ordered = firstOrder vs (body, cons)
      names = Map.fromList (zip ordered ['a' .. 'z'])
      showT = showTypeWith names
      quant = case vs of
        [] -> ""
        _ -> "forall " ++ unwords [letter names v | v <- ordered] ++ ". "
      consStr = case cons of
        [] -> ""
        _ -> "(" ++ intercalateC [className c ++ " " ++ letter names x | (x, c) <- cons] ++ ") => "
  in quant ++ consStr ++ showT body
  where
    letter names x = maybe (show x) (: []) (Map.lookup x names)
    className c = case c of
      NumC -> "Num"
      OrdC -> "Ord"
      EqC -> "Eq"
      AppC -> "App"

-- | The quantified variables in order of first occurrence in the type and
-- its constraints.
firstOrder :: [Int] -> (MonoT, [(Int, Class)]) -> [Int]
firstOrder vs (ty, cons) =
  reverse (foldl go (seenFromType ty) (map fst cons))
  where
    seenFromType t = collectType [] t
    go acc x = if x `elem` vs && x `notElem` acc then x : acc else acc
    collectType acc t = case t of
      TVar a -> if a `elem` vs && a `notElem` acc then a : acc else acc
      TList inner -> collectType acc inner
      TFun a b -> collectType (collectType acc a) b
      _ -> acc

-- | Render a monotype, using a fixed mapping for type variable names.
showTypeWith :: Map.Map Int Char -> MonoT -> String
showTypeWith names = go
  where
    go ty = case ty of
      TInt -> "Int"
      TFloat -> "Float"
      TBool -> "Bool"
      TString -> "String"
      TVar a -> maybe (show a) (: []) (Map.lookup a names)
      TList inner -> "[" ++ go inner ++ "]"
      TFun a b -> paren (isFun a) (go a) ++ " -> " ++ go b
    isFun TFun {} = True
    isFun _ = False
    paren True s = "(" ++ s ++ ")"
    paren False s = s

intercalateC :: [String] -> String
intercalateC [] = ""
intercalateC [x] = x
intercalateC (x : xs) = x ++ ", " ++ intercalateC xs