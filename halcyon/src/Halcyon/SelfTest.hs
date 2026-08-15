module Halcyon.SelfTest (runSelfTests) where

import Halcyon.AST
import Halcyon.Errors
import Halcyon.Lexer (Tok, lexer)
import Halcyon.Parser (parseProgram)
import Halcyon.Pretty (prettyProgram)
import Halcyon.Type (builtins, inferProgram, showScheme)

-- | A single self-test case: a name and a check that returns True on pass.
type Case = (String, Bool)

-- | Run every self-test and report. Exits non-zero via main if any fail.
runSelfTests :: IO Int
runSelfTests = do
  let cases = parserCases ++ typeCases
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

-- | Parse a source string into a program, crashing on lex/parse errors.
parseOf :: String -> [Stmt]
parseOf src = case parseProgram (unsafeLex src) of
  Left e -> error (formatError "<selftest>" e)
  Right stmts -> stmts

-- | Typecheck a program and check the named top-level bindings have exactly
-- the given rendered schemes.
inferOK :: String -> [(String, String)] -> Bool
inferOK src expected =
  case inferProgram builtins (parseOf src) of
    Left _ -> False
    Right pairs ->
      let rendered = map (\(n, sch) -> (n, showScheme sch)) pairs
      in all (`elem` rendered) expected

-- | Typechecking must fail for this program.
inferFails :: String -> Bool
inferFails src = case inferProgram builtins (parseOf src) of
  Left _ -> True
  Right _ -> False

typeCases :: [Case]
typeCases =
  [ ("type int literal", inferOK "let x = 5\n" [("x", "Int")])
  , ("type float literal", inferOK "let x = 3.14\n" [("x", "Float")])
  , ("type bool literal", inferOK "let x = true\n" [("x", "Bool")])
  , ("type string literal", inferOK "let x = \"hi\"\n" [("x", "String")])
  , ("type list literal", inferOK "let xs = [1, 2, 3]\n" [("xs", "[Int]")])
  , ("type empty list polymorphic", inferOK "let xs = []\n" [("xs", "forall a. [a]")])
  , ("type cons", inferOK "let xs = 1 : []\n" [("xs", "[Int]")])
  , ("type cons mixed list", inferOK "let xs = 1 : 2 : []\n" [("xs", "[Int]")])
  , ("type id", inferOK "let id x = x\n" [("id", "forall a. a -> a")])
  , ("type const", inferOK "let k x y = x\n" [("k", "forall a b. a -> b -> a")])
  , ("type apply", inferOK "let apply f x = f x\n" [("apply", "forall a b. (a -> b) -> a -> b")])
  , ("type compose", inferOK "let comp f g x = f (g x)\n" [("comp", "forall a b c. (a -> b) -> (c -> a) -> c -> b")])
  , ("type lambda", inferOK "let f = \\x y -> x\n" [("f", "forall a b. a -> b -> a")])
  , ("type numeric op", inferOK "let x = 5 + 2 * 3\n" [("x", "Int")])
  , ("type float op", inferOK "let x = 1.5 + 2.5\n" [("x", "Float")])
  , ("type numeric promotion", inferOK "let x = 5 + 3.14\n" [("x", "Float")])
  , ("type division always float", inferOK "let x = 10 / 4\n" [("x", "Float")])
  , ("type mod", inferOK "let x = 10 % 3\n" [("x", "Int")])
  , ("type unary minus", inferOK "let x = -5\n" [("x", "Int")])
  , ("type unary minus float", inferOK "let x = -3.5\n" [("x", "Float")])
  , ("type comparison int", inferOK "let x = 1 < 2\n" [("x", "Bool")])
  , ("type comparison float", inferOK "let x = 1.5 >= 2.5\n" [("x", "Bool")])
  , ("type comparison string", inferOK "let x = \"a\" < \"b\"\n" [("x", "Bool")])
  , ("type equality int", inferOK "let x = 5 == 5\n" [("x", "Bool")])
  , ("type equality string", inferOK "let x = \"a\" == \"a\"\n" [("x", "Bool")])
  , ("type equality list", inferOK "let x = [1, 2] == [1, 2]\n" [("x", "Bool")])
  , ("type bool ops", inferOK "let x = true && false || not true\n" [("x", "Bool")])
  , ("type append string", inferOK "let x = \"a\" ++ \"b\"\n" [("x", "String")])
  , ("type append list", inferOK "let x = [1] ++ [2]\n" [("x", "[Int]")])
  , ("type if branches unify", inferOK "let x = if true then 1 else 2\n" [("x", "Int")])
  , ("type if branches promote", inferOK "let x = if true then 1 else 2.5\n" [("x", "Float")])
  , ("type numeric lambda generalized", inferOK "let double x = x + x\n" [("double", "forall a. (Num a) => a -> a")])
  , ("type annotation int", inferOK "let x :: Int = 5\n" [("x", "Int")])
  , ("type annotation fn", inferOK "let f :: Int -> Int = \\x -> x\n" [("f", "Int -> Int")])
  , ("type annotation list", inferOK "let xs :: [Float] = []\n" [("xs", "[Float]")])
  , ("type recursive fn", inferOK "let fact n = if n == 0 then 1 else n * fact (n - 1)\n" [("fact", "Int -> Int")])
  , ("type let polymorphism", inferOK "let id x = x\nlet a = id 5\nlet b = id \"s\"\n" [("a", "Int"), ("b", "String")])
  , ("type letrec expr", inferOK "letrec f n = if n == 0 then 1 else n * f (n - 1) in f 5\n" [])
  , ("type head builtin", inferOK "let x = head [1, 2]\n" [("x", "Int")])
  , ("type tail builtin", inferOK "let x = tail [1, 2]\n" [("x", "[Int]")])
  , ("type null builtin", inferOK "let x = null []\n" [("x", "Bool")])
  , ("type head polymorphic", inferOK "let f = head\n" [("f", "forall a. [a] -> a")])
  , ("type print polymorphic", inferOK "let f = print\n" [("f", "forall a. a -> a")])
  , ("type nested let", inferOK "let y = let x = 5 in x + 1\n" [("y", "Int")])
  , ("type deeply nested lists", inferOK "let m = [[1, 2], [3]]\n" [("m", "[[Int]]")])
  , ("type app of generic", inferOK "let apply f x = f x\nlet y = apply (\\x -> x * 2) 3\n" [("y", "Int")])
  , ("fail add int bool", inferFails "let x = 1 + true\n")
  , ("fail add int string", inferFails "let x = 1 + \"a\"\n")
  , ("fail comparison mismatch", inferFails "let x = 1 < \"a\"\n")
  , ("fail eq function", inferFails "let x = (\\y -> y) == (\\y -> y)\n")
  , ("fail head on int", inferFails "let x = head 5\n")
  , ("fail if condition not bool", inferFails "let x = if 1 then 2 else 3\n")
  , ("fail unbound variable", inferFails "let x = nope\n")
  , ("fail annotation mismatch", inferFails "let x :: Int = \"s\"\n")
  , ("fail annotation fn mismatch", inferFails "let f :: Int -> Int = \\x -> x + \"s\"\n")
  , ("fail mod on float", inferFails "let x = 5.5 % 2\n")
  , ("fail occurs check", inferFails "let f x = x x\n")
  , ("fail no eq for functions", inferFails "let x = (\\a b -> a) == (\\a b -> b)\n")
  , ("fail and on int", inferFails "let x = 1 && true\n")
  ]