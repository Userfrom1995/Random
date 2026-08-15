module Halcyon.Parser (parseProgram, describeTok) where

import Control.Monad.State.Strict (StateT, evalStateT, lift, modify, gets)
import Halcyon.AST
import Halcyon.Errors
import Halcyon.Lexer

type P = StateT [Tok] (Either HErr)

-- | Parse a whole program (a list of statements). The token stream must end
-- with TEOF.
parseProgram :: [Tok] -> Either HErr [Stmt]
parseProgram toks = evalStateT go toks
  where
    go :: P [Stmt]
    go = do
      mt <- peekTok
      case mt of
        Just (Tok _ TEOF) -> pure []
        _ -> do
          st <- parseStmt
          rest <- go
          pure (st : rest)

-- | Human-readable description of a token kind, for error messages.
describeTok :: TokKind -> String
describeTok k = case k of
  TInt _ -> "an integer literal"
  TFloat _ -> "a float literal"
  TStr _ -> "a string literal"
  TIdent n -> "identifier '" ++ n ++ "'"
  TOp o -> "'" ++ o ++ "'"
  TLparen -> "'('"
  TRparen -> "')'"
  TLbrack -> "'['"
  TRbrack -> "']'"
  TComma -> "','"
  TEquals -> "'='"
  TDoubleColon -> "'::'"
  TBackslash -> "'\\'"
  TArrow -> "'->'"
  TEOF -> "end of input"

peekTok :: P (Maybe Tok)
peekTok = gets (\toks -> case toks of t : _ -> Just t; [] -> Nothing)

peekKind :: P (Maybe TokKind)
peekKind = fmap tokK <$> peekTok

advance :: P ()
advance = modify (drop 1)

errAt :: Tok -> String -> P a
errAt t m = lift (Left (HErr (tokPos t) m))

errEof :: String -> P a
errEof m = lift (Left (HErr originPos m))

expectKind :: TokKind -> P ()
expectKind k = do
  mt <- peekTok
  case mt of
    Just (Tok _ k') | k' == k -> advance
    Just t -> errAt t ("expected " ++ describeTok k ++ " but found " ++ describeTok (tokK t))
    Nothing -> errEof ("expected " ++ describeTok k ++ " but reached end of input")

expectOp :: Name -> P ()
expectOp op = do
  mt <- peekTok
  let matches t = case tokK t of
        TOp o -> o == op
        TEquals -> op == "="
        _ -> False
  case mt of
    Just t | matches t -> advance
    Just t -> errAt t ("expected '" ++ op ++ "' but found " ++ describeTok (tokK t))
    Nothing -> errEof ("expected '" ++ op ++ "' but reached end of input")

expectIdent :: P Name
expectIdent = do
  mt <- peekTok
  case mt of
    Just (Tok _ (TIdent n)) -> advance >> pure n
    Just t -> errAt t ("expected an identifier but found " ++ describeTok (tokK t))
    Nothing -> errEof "expected an identifier but reached end of input"

isKw :: Name -> Bool
isKw n = n `elem` ["let", "in", "letrec", "if", "then", "else", "print"]

-- | Keywords that may never appear as a standalone expression.
reserved :: [Name]
reserved = ["let", "in", "letrec", "if", "then", "else", "not"]

parseStmt :: P Stmt
parseStmt = do
  mt <- peekTok
  case mt of
    Just t@(Tok _ (TIdent "let")) -> do
      advance
      (name, ann, params, def) <- parseLetBind
      hasIn <- afterLetIsIn
      if hasIn
        then do
          advance
          body <- parseExpr
          pure (SExpr (at (tokPos t) (ELet name ann params def body)))
        else pure (SDef name ann params def)
    Just t@(Tok _ (TIdent "letrec")) -> do
      advance
      (name, ann, params, def) <- parseLetBind
      hasIn <- afterLetIsIn
      if hasIn
        then do
          advance
          body <- parseExpr
          pure (SExpr (at (tokPos t) (ELetRec name ann params def body)))
        else pure (SDef name ann params def)
    Just (Tok _ (TIdent "print")) -> do
      advance
      e <- parseExpr
      pure (SPrint e)
    Just (Tok _ (TIdent "if")) -> do
      e <- parseExpr
      pure (SExpr e)
    _ -> SExpr <$> parseExpr
  where
    -- After 'let name ... = def', an 'in' means this is a let-expression,
    -- not a top-level definition.
    afterLetIsIn :: P Bool
    afterLetIsIn = do
      mt <- peekTok
      pure $ case mt of
        Just (Tok _ (TIdent "in")) -> True
        _ -> False

-- | Parse the binder of a let/letrec/definition:
--   name (:: type)? params* = expr
parseLetBind :: P (Name, Maybe Type, [Name], Expr)
parseLetBind = do
  name <- expectIdent
  ann <- parseMaybeAnnotation
  params <- parseParams
  expectOp "="
  def <- parseExpr
  pure (name, ann, params, def)

parseMaybeAnnotation :: P (Maybe Type)
parseMaybeAnnotation = do
  mt <- peekTok
  case mt of
    Just (Tok _ TDoubleColon) -> advance >> (Just <$> parseType)
    _ -> pure Nothing

parseParams :: P [Name]
parseParams = go []
  where
    go acc = do
      mt <- peekTok
      case mt of
        Just (Tok _ (TIdent n)) | not (isKw n) && n /= "true" && n /= "false" && n /= "not" -> do
          advance
          go (n : acc)
        _ -> pure (reverse acc)

-- | Surface type syntax, right-associative arrows.
parseType :: P Type
parseType = do
  t <- parseTypeAtom
  mt <- peekTok
  case mt of
    Just (Tok _ TArrow) -> do
      advance
      t2 <- parseType
      pure (TyFun t t2)
    _ -> pure t

parseTypeAtom :: P Type
parseTypeAtom = do
  mt <- peekTok
  case mt of
    Just t@(Tok _ (TIdent n)) -> case n of
      "Int" -> advance >> pure TyInt
      "Float" -> advance >> pure TyFloat
      "Bool" -> advance >> pure TyBool
      "String" -> advance >> pure TyString
      _ -> if n == "let" || n == "if" || n == "in" || n == "print"
        then errAt t ("expected a type but found " ++ describeTok (tokK t))
        else advance >> pure (TyVar n)
    Just (Tok _ TLbrack) -> do
      advance
      inner <- parseType
      expectKind TRbrack
      pure (TyList inner)
    Just (Tok _ TLparen) -> do
      advance
      inner <- parseType
      expectKind TRparen
      pure inner
    Just t -> errAt t ("expected a type but found " ++ describeTok (tokK t))
    Nothing -> errEof "expected a type but reached end of input"

parseExpr :: P Expr
parseExpr = do
  mt <- peekTok
  case mt of
    Just t@(Tok _ (TIdent "if")) -> parseIf t
    Just t@(Tok _ (TIdent "let")) -> parseLetExpr t False
    Just t@(Tok _ (TIdent "letrec")) -> parseLetExpr t True
    Just t@(Tok _ TBackslash) -> parseLambda t
    _ -> parseOr

parseIf :: Tok -> P Expr
parseIf t = do
  advance
  cond <- parseExpr
  mt <- peekTok
  case mt of
    Just (Tok _ (TIdent "then")) -> advance
    Just other -> errAt other "expected 'then'"
    Nothing -> errEof "expected 'then'"
  thenE <- parseExpr
  mt2 <- peekTok
  case mt2 of
    Just (Tok _ (TIdent "else")) -> advance
    Just other -> errAt other "expected 'else'"
    Nothing -> errEof "expected 'else'"
  elseE <- parseExpr
  pure (at (tokPos t) (EIf cond thenE elseE))

parseLetExpr :: Tok -> Bool -> P Expr
parseLetExpr t recK = do
  advance
  (name, ann, params, def) <- parseLetBind
  mt <- peekTok
  case mt of
    Just (Tok _ (TIdent "in")) -> advance
    Just other -> errAt other "expected 'in'"
    Nothing -> errEof "expected 'in'"
  body <- parseExpr
  pure $ if recK
    then at (tokPos t) (ELetRec name ann params def body)
    else at (tokPos t) (ELet name ann params def body)

parseLambda :: Tok -> P Expr
parseLambda t = do
  advance
  params <- parseParams
  case params of
    [] -> do
      mt <- peekTok
      case mt of
        Just other -> errAt other "expected a parameter name after '\\'"
        Nothing -> errEof "expected a parameter name after '\\'"
    _ -> pure ()
  mt <- peekTok
  case mt of
    Just (Tok _ TArrow) -> advance
    Just other -> errAt other "expected '->' after parameters"
    Nothing -> errEof "expected '->' after parameters"
  body <- parseExpr
  pure (at (tokPos t) (ELam params body))

parseOr :: P Expr
parseOr = do
  lhs <- parseAnd
  go lhs
  where
    go lhs = do
      mt <- peekKind
      case mt of
        Just (TOp "||") -> do
          advance
          rhs <- parseAnd
          go (binOp lhs "||" rhs)
        _ -> pure lhs

parseAnd :: P Expr
parseAnd = do
  lhs <- parseCmp
  go lhs
  where
    go lhs = do
      mt <- peekKind
      case mt of
        Just (TOp "&&") -> do
          advance
          rhs <- parseCmp
          go (binOp lhs "&&" rhs)
        _ -> pure lhs

parseCmp :: P Expr
parseCmp = do
  lhs <- parseCons
  mt <- peekKind
  case mt of
    Just (TOp op) | op `elem` ["==", "/=", "<", "<=", ">", ">="] -> do
      advance
      rhs <- parseCons
      pure (binOp lhs op rhs)
    _ -> pure lhs

parseCons :: P Expr
parseCons = do
  lhs <- parseAdd
  mt <- peekKind
  case mt of
    Just (TOp ":") -> do
      advance
      rhs <- parseCons
      pure (at (exprPos lhs) (ECons lhs rhs))
    _ -> pure lhs

parseAdd :: P Expr
parseAdd = do
  lhs <- parseMul
  go lhs
  where
    go lhs = do
      mt <- peekKind
      case mt of
        Just (TOp op) | op `elem` ["+", "-", "++"] -> do
          advance
          rhs <- parseMul
          go (binOp lhs op rhs)
        _ -> pure lhs

parseMul :: P Expr
parseMul = do
  lhs <- parseUnary
  go lhs
  where
    go lhs = do
      mt <- peekKind
      case mt of
        Just (TOp op) | op `elem` ["*", "/", "%"] -> do
          advance
          rhs <- parseUnary
          go (binOp lhs op rhs)
        _ -> pure lhs

binOp :: Expr -> Name -> Expr -> Expr
binOp l op r = at (exprPos l) (EOp op l r)

parseUnary :: P Expr
parseUnary = do
  mt <- peekTok
  case mt of
    Just t@(Tok _ (TOp "-")) -> do
      advance
      e <- parseUnary
      pure (at (tokPos t) (EUnary "-" e))
    Just t@(Tok _ (TIdent "not")) -> do
      advance
      e <- parseUnary
      pure (at (tokPos t) (EUnary "not" e))
    _ -> parseApp

parseApp :: P Expr
parseApp = do
  first <- parseAtom
  go first
  where
    go lhs = do
      mt <- peekKind
      case mt of
        Just (TIdent n) | not (isKw n) -> do
          rhs <- parseAtom
          go (at (exprPos lhs) (EApp lhs rhs))
        Just (TInt _) -> do
          rhs <- parseAtom
          go (at (exprPos lhs) (EApp lhs rhs))
        Just (TFloat _) -> do
          rhs <- parseAtom
          go (at (exprPos lhs) (EApp lhs rhs))
        Just (TStr _) -> do
          rhs <- parseAtom
          go (at (exprPos lhs) (EApp lhs rhs))
        Just TLparen -> do
          rhs <- parseAtom
          go (at (exprPos lhs) (EApp lhs rhs))
        Just TLbrack -> do
          rhs <- parseAtom
          go (at (exprPos lhs) (EApp lhs rhs))
        _ -> pure lhs

parseAtom :: P Expr
parseAtom = do
  mt <- peekTok
  case mt of
    Just t@(Tok _ (TInt n)) -> advance >> pure (at (tokPos t) (EInt n))
    Just t@(Tok _ (TFloat d)) -> advance >> pure (at (tokPos t) (EFloat d))
    Just t@(Tok _ (TStr s)) -> advance >> pure (at (tokPos t) (EString s))
    Just t@(Tok _ (TIdent "true")) -> advance >> pure (at (tokPos t) (EBool True))
    Just t@(Tok _ (TIdent "false")) -> advance >> pure (at (tokPos t) (EBool False))
    Just t@(Tok _ (TIdent n))
      | n `elem` reserved -> errAt t ("unexpected keyword '" ++ n ++ "' in expression")
      | otherwise -> advance >> pure (at (tokPos t) (EVar n))
    Just (Tok _ TLparen) -> do
      advance
      e <- parseExpr
      expectKind TRparen
      pure e
    Just (Tok _ TLbrack) -> do
      advance
      mt2 <- peekTok
      case mt2 of
        Just tb -> parseListElems tb
        Nothing -> errEof "unexpected end of input in list literal"
    Just t -> errAt t ("unexpected " ++ describeTok (tokK t) ++ " in expression")
    Nothing -> errEof "unexpected end of input in expression"

parseListElems :: Tok -> P Expr
parseListElems t = do
  mt <- peekKind
  case mt of
    Just TRbrack -> advance >> pure (at (tokPos t) (EList []))
    _ -> do
      first <- parseExpr
      rest <- go
      pure (at (tokPos t) (EList (first : rest)))
  where
    go :: P [Expr]
    go = do
      mt <- peekKind
      case mt of
        Just TComma -> do
          advance
          e <- parseExpr
          rest <- go
          pure (e : rest)
        Just TRbrack -> advance >> pure []
        _ -> do
          t' <- peekTok
          case t' of
            Just tk -> errAt tk "expected ',' or ']' in list literal"
            Nothing -> errEof "expected ',' or ']' in list literal"
