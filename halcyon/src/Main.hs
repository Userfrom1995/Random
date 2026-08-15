module Main (main) where

import System.Environment (getArgs)
import System.Exit (exitWith, ExitCode (ExitSuccess, ExitFailure))

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

selftest :: IO ()
selftest = do
  putStrLn "Halcyon self-test suite"
  putStrLn "  (suite not yet implemented)"
  putStrLn "  0 tests, 0 failures"

main :: IO ()
main = do
  args <- getArgs
  case args of
    [] -> putStr usage >> exitWith ExitSuccess
    ["--version"] -> putStrLn ("halcyon " ++ version)
    ["--help"] -> putStr usage >> exitWith ExitSuccess
    ["-h"] -> putStr usage >> exitWith ExitSuccess
    ["selftest"] -> selftest
    cmd : _ -> die ("halcyon: unknown command '" ++ cmd ++ "'\n\n" ++ usage)
