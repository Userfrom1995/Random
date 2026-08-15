module Halcyon.Pretty (prettyProgram, prettyStmt, prettyExpr) where

import Halcyon.AST

-- | Precedence of binary operators (higher binds tighter).
opPrec :: Name -> Int
opPrec op = case op of
  "||" -> 2
  "&&" -> 3
  "==" -> 4
  "/=" -> 4
  "<" -> 4
  "<=" -> 4
  ">" -> 4
  ">=" -> 4
  ":" -> 5
  "+" -> 6
  "-" -> 6
  "++" -> 6
  "*" -> 7
  "/" -> 7
  "%" -> 7
  _ -> 6

prettyProgram :: [Stmt] -> String
prettyProgram = unlines . map prettyStmt

prettyStmt :: Stmt -> String
prettyStmt st = case st of
  SDef n ann params body ->
    "let " ++ joinBinding n ann params ++ " = " ++ prettyExpr body
  SPrint e -> "print " ++ prettyExpr e
  SExpr e -> prettyExpr e

-- | 'name :: type params...', spaced correctly whether or not the annotation
-- and the parameter list are present.
joinBinding :: Name -> Maybe Type -> [Name] -> String
joinBinding n ann params = unwords (n : annParts ++ params)
  where
    annParts = maybe [] (\t -> [":: " ++ prettyType t]) ann

prettyType :: Type -> String
prettyType t = case t of
  TyInt -> "Int"
  TyFloat -> "Float"
  TyBool -> "Bool"
  TyString -> "String"
  TyList inner -> "[" ++ prettyType inner ++ "]"
  TyFun a b -> prettyTypeAtom a ++ " -> " ++ prettyType b
  TyVar n -> n
  where
    prettyTypeAtom x = case x of
      TyFun _ _ -> "(" ++ prettyType x ++ ")"
      _ -> prettyType x

-- | Pretty-print an expression, wrapping in parentheses if its binding
-- strength is looser than @ctx@.
prettyExpr :: Expr -> String
prettyExpr e = prettyP 1 e

prettyP :: Int -> Expr -> String
prettyP ctx e = wrap (precOf e < ctx) (pretty e)
  where
    wrap True s = "(" ++ s ++ ")"
    wrap False s = s

precOf :: Expr -> Int
precOf e = case exprK e of
  EInt _ -> 10
  EFloat _ -> 10
  EBool _ -> 10
  EString _ -> 10
  EVar _ -> 10
  EApp _ _ -> 9
  EUnary _ _ -> 8
  EList _ -> 10
  ECons _ _ -> 5
  EOp op _ _ -> opPrec op
  ELam _ _ -> 1
  EIf _ _ _ -> 1
  ELet _ _ _ _ _ -> 1
  ELetRec _ _ _ _ _ -> 1

pretty :: Expr -> String
pretty e = case exprK e of
  EInt n -> show n
  EFloat d -> showFloatLit d
  EBool True -> "true"
  EBool False -> "false"
  EString s -> showStringLit s
  EVar n -> n
  EApp f a -> prettyP 9 f ++ " " ++ prettyP 10 a
  EUnary "-" inner -> "-" ++ prettyP 8 inner
  EUnary "not" inner -> "not " ++ prettyP 8 inner
  EUnary op inner -> op ++ prettyP 8 inner
  EList es -> "[" ++ commaSep (map prettyExpr es) ++ "]"
  ECons l r -> prettyP 6 l ++ " : " ++ prettyP 5 r
  EOp op l r -> prettyP (opPrec op) l ++ " " ++ op ++ " " ++ prettyP (opPrec op + 1) r
  ELam params body -> "\\" ++ unwords params ++ " -> " ++ prettyExpr body
  EIf c t f -> "if " ++ prettyExpr c ++ " then " ++ prettyExpr t ++ " else " ++ prettyExpr f
  ELet n ann params def body ->
    "let " ++ joinBinding n ann params ++ " = " ++ prettyExpr def
      ++ " in " ++ prettyExpr body
  ELetRec n ann params def body ->
    "letrec " ++ joinBinding n ann params ++ " = " ++ prettyExpr def
      ++ " in " ++ prettyExpr body

commaSep :: [String] -> String
commaSep [] = ""
commaSep [x] = x
commaSep (x : xs) = x ++ ", " ++ commaSep xs

-- | Render a Double literal the way the lexer accepts it: at least one digit
-- before and after the dot.
showFloatLit :: Double -> String
showFloatLit d
  | isNaN d = "0.0"
  | isInfinite d = if d > 0 then "1.0e999" else "-1.0e999"
  | otherwise =
      let base = show d
      in if '.' `elem` base then base else base ++ ".0"

showStringLit :: String -> String
showStringLit s = "\"" ++ concatMap esc s ++ "\""
  where
    esc '\n' = "\\n"
    esc '\t' = "\\t"
    esc '\r' = "\\r"
    esc '"' = "\\\""
    esc '\\' = "\\\\"
    esc c = [c]