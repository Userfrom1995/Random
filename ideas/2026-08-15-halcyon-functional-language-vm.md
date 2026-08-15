# Halcyon: a small functional programming language and VM in Haskell

**Halcyon** is the factory's first Haskell project and its first
compiler/language project: a complete, small functional programming
language written from scratch in Haskell. The full pipeline is visible and
readable: a hand-written lexer and recursive-descent parser, a real
Hindley-Milner type inference engine (with `let` polymorphism, constraint
classes for overloaded operators, numeric promotion, and type annotations),
a tree-walking interpreter, a real bytecode compiler and stack VM, a REPL,
and a statically-hostable web playground that runs Halcyon programs in the
browser via a faithful JavaScript mirror of the entire core.

## What it is

- **The language.** ML-flavored and minimal: integers, floats, booleans and
  strings; lists (`[]`, `x : xs`); lambdas (`\x -> e`); function
  application by juxtaposition; `if/then/else`; `let` and `letrec ... in`;
  top-level recursive definitions; `print`; and a small standard prelude
  (written in Halcyon itself) with `map`, `filter`, `foldl`, `foldr`,
  `reverse`, `sum`, and friends.
- **A real lexer and parser.** Hand-written, position-tracking, with
  line-and-column error messages, operator precedence climbing, and a pretty
  printer that round-trips the AST.
- **Real Hindley-Milner type inference.** Algorithm W with fresh-variable
  counters, occurs-check unification, generalization at `let`, and
  instantiation at use. Overloaded operators get a small constraint-class
  system (`Num`, `Ord`, `Eq`, `App`) resolved by a constraint set carried
  through inference, plus Int/Float promotion, so `5 + 3.14` and
  `10 / 4 = 2.5` work naturally and `let double x = x + x` generalizes to
  `forall a. Num a => a -> a -> a`. Optional `::` type annotations are
  checked against the inferred type.
- **Two evaluators.** A readable tree-walking interpreter, and a real
  bytecode compiler + stack VM. The VM runs on an explicit, heap-allocated
  call-frame stack, so Halcyon recursion never grows the Haskell call stack.
  Bytecode can be disassembled and inspected.
- **A REPL and CLI.** `halcyon run`, `halcyon vm`, `halcyon check`,
  `halcyon parse`, `halcyon ast`, `halcyon types`, `halcyon bytecode`,
  `halcyon eval`, `halcyon repl`, `halcyon selftest`. The REPL is fully
  headless-testable (batch mode over piped stdin, `:type`, `:bytecode`,
  `:help`, `:quit`).
- **A statically-hostable web playground.** `halcyon/index.html` runs Halcyon
  in the browser on GitHub Pages with no backend: an editor with
  lexer-based syntax highlighting, a runnable interpreter and VM, type /
  bytecode / AST inspectors, and a sample catalog. The browser engine is a
  faithful JavaScript mirror of the Haskell core, differentially tested
  against it.
- **Fully headless-testable core.** The entire language logic (lexer/parser/
  typechecker/interpreter/VM) is exercised by a self-test suite that runs
  `.hcy` programs through both evaluators and checks exact output, plus
  negative type-checking tests and differential tests between the Haskell
  core and the JavaScript mirror.

## Why it fits

A brand-new language (Haskell, first in the factory) and a completely
untouched category (compilers and programming languages). Compilers are the
classic "learn how the machine thinks" project, and Haskell is the language
they are built in: the type checker, evaluator, and VM are each a few
hundred readable lines that demystify how `map`, closures, and type
inference actually work. The result is a real artifact: a working language
you can write programs in, plus a VM to run them and a browser playground to
watch the machinery.

## Key files

- `src/Main.hs` - CLI dispatcher and self-test runner
- `src/Halcyon/{Lexer,AST,Parser,Type,Interp,Compiler,VM,Repl,Prelude,Errors}.hs`
- `js/halcyon.js` - the JavaScript mirror core (browser + node)
- `js/node.js` - node CLI wrapper for the mirror (differential testing)
- `index.html` - the browser playground
- `samples/*.hcy`, `test/cases/*.hcy` - programs and test suite
- `docs/` - language spec and internals documentation

## Notes

- Int is arbitrary precision (Haskell `Integer`); the JS mirror uses IEEE
  doubles, a documented divergence that only shows beyond 2^53.
- Float display uses a shared canonical 6-decimal formatter implemented
  identically in Haskell and JS, so differential tests are deterministic.
- The GHC WASM cross-compile path was investigated and rejected for the
  playground: it needs a separate wasm GHC plus a wasi toolchain; a
  hand-written JS mirror is deterministic, dependency-free, and testable.
