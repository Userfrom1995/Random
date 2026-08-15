module Main (main) where

import System.Environment (getArgs)
import System.Exit (exitWith, ExitCode (ExitSuccess, ExitFailure))
import System.IO
import System.Directory (doesFileExist)

import Halcyon.AST (Stmt)
import Halcyon.Errors (formatError)
import Halcyon.Lexer (Tok, lexer)
import Halcyon.Parser (parseProgram)
import Halcyon.SelfTest (runSelfTests)
import Halcyon.Type (Scheme, builtins, inferProgram, showScheme)

version :: String
version = "0.1.0"

usage :: String
usage = unlines
  [ "Halcyon - a small functional programming language and VM in Haskell"
  , ""
  , "Usage: halcyon <command> [args]"
  , ""
  , "  run <file>       parse, typecheck, and evaluate a program (tree-walking interpreter)"
  , "  vm <file>        parse, typecheck, compile to bytecode, and run the bytecode VM"
  , "  check <file>     parse and typecheck only; exit non-zero on error"
  , "  parse <file>     parse and print the token stream"
  , "  ast <file>       parse and print the AST"
  , "  types <file>     typecheck and print the inferred type of every top-level binding"
  , "  bytecode <file>  compile and print the disassembled bytecode (without running)"
  , "  eval '<expr>'    typecheck and evaluate a one-line expression"
  , "  repl [--vm]      start the REPL (tree-walking interpreter, or --vm for the bytecode VM)"
  , "  selftest         run the built-in self-test suite"
  , "  --version        print the version"
  , "  --help | -h      print this help"
  ]

die :: String -> IO a
die msg = putStrLn msg >> exitWith (ExitFailure 1)

readSource :: FilePath -> IO String
readSource f = do
  exists <- doesFileExist f
  if not exists then die ("halcyon: no such file: " ++ f) else readFile f

lexOrDie :: FilePath -> String -> IO [Tok]
lexOrDie file src = case lexer src of
  Left e -> die (formatError file e)
  Right toks -> pure toks

cmdParse :: FilePath -> IO ()
cmdParse file = do
  src <- readSource file
  toks <- lexOrDie file src
  mapM_ putStrLn (map show toks)

cmdAst :: FilePath -> IO ()
cmdAst file = do
  src <- readSource file
  toks <- lexOrDie file src
  case parseProgram toks of
    Left e -> die (formatError file e)
    Right stmts -> mapM_ (putStrLn . show) stmts

-- | Typecheck a parsed program; dies with the first type error.
typecheckOrDie :: FilePath -> [Stmt] -> IO [(String, Scheme)]
typecheckOrDie file stmts = case inferProgram builtins stmts of
  Left e -> die (formatError file e)
  Right pairs -> pure pairs

cmdCheck :: FilePath -> IO ()
cmdCheck file = do
  src <- readSource file
  toks <- lexOrDie file src
  case parseProgram toks of
    Left e -> die (formatError file e)
    Right stmts -> do
      _ <- typecheckOrDie file stmts
      putStrLn (file ++ ": OK")

cmdTypes :: FilePath -> IO ()
cmdTypes file = do
  src <- readSource file
  toks <- lexOrDie file src
  case parseProgram toks of
    Left e -> die (formatError file e)
    Right stmts -> do
      pairs <- typecheckOrDie file stmts
      mapM_ (\(n, sch) -> putStrLn (n ++ " :: " ++ showScheme sch)) pairs

selftest :: IO ()
selftest = do
  putStrLn "Halcyon self-test suite"
  n <- runSelfTests
  putStrLn ("Halcyon self-test suite: " ++ (if n == 0 then "all green" else show n ++ " failures"))
  exitWith (if n == 0 then ExitSuccess else ExitFailure 1)

main :: IO ()
main = do
  hSetBuffering stdout NoBuffering
  args <- getArgs
  case args of
    [] -> putStr usage >> exitWith ExitSuccess
    ["--version"] -> putStrLn ("halcyon " ++ version)
    ["--help"] -> putStr usage >> exitWith ExitSuccess
    ["-h"] -> putStr usage >> exitWith ExitSuccess
    ["selftest"] -> selftest
    ["parse", f] -> cmdParse f
    ["ast", f] -> cmdAst f
    ["check", f] -> cmdCheck f
    ["types", f] -> cmdTypes f
    ["run", _] -> die "halcyon: interpreter not yet implemented"
    ["vm", _] -> die "halcyon: VM not yet implemented"
    ["bytecode", _] -> die "halcyon: VM not yet implemented"
    ["eval", _] -> die "halcyon: interpreter not yet implemented"
    ["repl"] -> die "halcyon: REPL not yet implemented"
    ["repl", "--vm"] -> die "halcyon: REPL not yet implemented"
    cmd : _ -> die ("halcyon: unknown command '" ++ cmd ++ "'\n\n" ++ usage)