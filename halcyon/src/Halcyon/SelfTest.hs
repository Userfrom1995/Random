module Halcyon.SelfTest (runSelfTests) where

import Halcyon.AST
import Halcyon.Errors
import Halcyon.Lexer (Tok, lexer)
import Halcyon.Parser (parseProgram)
import Halcyon.Pretty (prettyProgram)

-- | A single self-test case: a name and a check that returns True on pass.
type Case = (String, Bool)

-- | Run every self-test and report. Exits non-zero via main if any fail.
runSelfTests :: IO Int
runSelfTests = do
  let cases = parserCases
  let fails = [name | (name, ok) <- cases, not ok]
  mapM_ (\(n, _) -> putStrLn ("  ok   " ++ n)) [c | c@(n, _) <- cases, n `notElem` fails]
  mapM_ (\n -> putStrLn ("  FAIL " ++ n)) fails
  putStrLn ("  " ++ show (length cases - length fails) ++ " passed, "
            ++ show (length fails) ++ " failed")
  pure (length fails)

-- | Round-trip: parse a program, pretty-print it, parse it again, and check
-- the two ASTs are structurally identical (ignoring source positions).
roundTrip :: String -> String -> Bool
roundTrip _name src =
  case parseProgram (unsafeLex src) of
    Left _err -> False
    Right ast1 ->
      case parseProgram (unsafeLex (prettyProgram ast1)) of
        Left _err2 -> False
        Right ast2 -> map stripStmt ast1 == map stripStmt ast2

-- | Position-insensitive view of the AST, used so round-trip tests compare
-- structure rather than byte offsets.
stripStmt :: Stmt -> Stmt
stripStmt st = case st of
  SDef n a ps e -> SDef n a ps (stripPos e)
  SPrint e -> SPrint (stripPos e)
  SExpr e -> SExpr (stripPos e)

stripPos :: Expr -> Expr
stripPos (Expr _ k) = Expr originPos (stripK k)

stripK :: ExprK -> ExprK
stripK k = case k of
  EApp f a -> EApp (stripPos f) (stripPos a)
  EIf c t e -> EIf (stripPos c) (stripPos t) (stripPos e)
  ELet n a ps d b -> ELet n a ps (stripPos d) (stripPos b)
  ELetRec n a ps d b -> ELetRec n a ps (stripPos d) (stripPos b)
  EList es -> EList (map stripPos es)
  ECons l r -> ECons (stripPos l) (stripPos r)
  EOp op l r -> EOp op (stripPos l) (stripPos r)
  EUnary op e -> EUnary op (stripPos e)
  ELam ps b -> ELam ps (stripPos b)
  _ -> k

unsafeLex :: String -> [Tok]
unsafeLex src = case lexer src of
  Left e -> error (formatError "<selftest>" e)
  Right toks -> toks

parserCases :: [Case]
parserCases =
  [ ("parse arithmetic precedence", roundTrip "arith" "1 + 2 * 3 - 4 / 2\n")
  , ("parse application binds tight", roundTrip "app" "f x y + 1\n")
  , ("parse cons right assoc", roundTrip "cons" "1 : 2 : []\n")
  , ("parse lambda", roundTrip "lam" "\\x -> \\y -> x + y\n")
  , ("parse if", roundTrip "if" "if x > 0 then 1 else -1\n")
  , ("parse let expr", roundTrip "let" "let x = 5 in x + 1\n")
  , ("parse letrec expr", roundTrip "letrec" "letrec f n = if n == 0 then 1 else n * f (n - 1) in f 5\n")
  , ("parse def", roundTrip "def" "let square x = x * x\n")
  , ("parse def with annotation", roundTrip "annot" "let x :: Int = 5\n")
  , ("parse def with fn annotation", roundTrip "annotfn" "let id :: a -> a = \\x -> x\n")
  , ("parse list literal", roundTrip "list" "[1, 2, 3]\n")
  , ("parse string escapes", roundTrip "str" "print \"a\\n\\t\\\"\\\\\"\n")
  , ("parse comparison chain", roundTrip "cmp" "a < b && b <= c || d >= e\n")
  , ("parse unary minus", roundTrip "neg" "-x + -(y * z)\n")
  , ("parse nested parens", roundTrip "parens" "((x + y) * (z - w))\n")
  , ("parse multiple defs", roundTrip "defs" "let a = 1\nlet b = 2\nprint a + b\n")
  , ("parse comments", roundTrip "comments" "-- a comment\n{- block {- nested -} comment -}\nlet x = 1\n")
  , ("parse bool literals", roundTrip "bool" "let t = true\nlet f = false\n")
  , ("parse not", roundTrip "not" "not x && not (y || z)\n")
  , ("parse mod", roundTrip "mod" "10 % 3\n")
  , ("parse floats", roundTrip "float" "3.14 + 1.5\n")
  , ("parse string concat", roundTrip "concat" "\"foo\" ++ \"bar\"\n")
  , ("parse print stmt", roundTrip "print" "print \"hello\"\n")
  , ("parse list of apps", roundTrip "listapp" "[f 1, g 2, h 3]\n")
  , ("parse param primes", roundTrip "prime" "let foldl' f acc xs = xs\n")
  ]