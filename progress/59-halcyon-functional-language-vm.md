# Progress - Halcyon

Status: in-progress

- **Issue:** #59
- **Branch:** opencode/59-halcyon-functional-language-vm
- **Status:** in-progress
- **Updated:** 2026-08-15T07:25:00Z

## Checklist
- [x] scaffold: branch, progress file, ideas entry, Makefile, src tree, CLI stub, .gitignore
- [ ] core: AST + Lexer + Parser + Errors + pretty printer, `parse` CLI, parsing tests
- [ ] type checker: Hindley-Milner inference with constraint classes + numeric promotion + type annotations, `check` CLI, tests
- [ ] tree-walking interpreter: values, evaluator, canonical formatting, `run` CLI, REPL, embedded prelude, tests
- [ ] bytecode VM: compiler + stack VM + disassembler, `vm`/`bytecode` CLI, REPL `--vm`, tests
- [ ] samples: `samples/*.hcy` demonstration programs + full selftest suite + differential tests
- [ ] web playground core: faithful JS mirror (`js/halcyon.js`: lexer/parser/typecheck/interp/compile/vm/format) + node CLI + js tests
- [ ] web playground UI: `index.html` + css + app + embedded samples
- [ ] iteration/improvement cycle: brainstorm and implement at least one major enhancement
- [ ] docs: README, `docs/` (index.md/html, language.md, internals.md), ideas entry final, landing page + root README update, final push, Status: complete

## Current step
Scaffold. Creating the project tree, Makefile, CLI stub, progress file, and
ideas entry; pushing and opening the PR for issue #59.

## Next steps
Core front end: AST, Lexer, Parser, positional errors, pretty printer; wire
`halcyon parse` and self-test parsing cases.

## Agent log
- 2026-08-15 (run 1): oriented (builder.md, AGENTS.md, FACTORY.md, README,
  index.html landing, previous projects glyphforge/gambit/aftershock for
  conventions). Verified GHC 9.14.1 + cabal + stack + node + python available;
  network reachable. No branch/PR existed for issue #59 - started fresh on
  opencode/59-halcyon-functional-language-vm. Decided the architecture:
  a pure-GHC (bundled-libs only) Haskell core (lexer/parser/HM
  typechecker/tree-walking interpreter/bytecode VM/REPL) plus a faithful,
  deterministic JavaScript mirror of the whole core for the statically
  hostable web playground (GHC wasm cross-compilation rejected: fragile,
  needs a separate wasm GHC + wasi toolchain). Numeric promotion (Int+Float
  -> Float), constraint-class overload resolution (Num/Ord/Eq/App) in the
  type checker, and an explicit-frame heap-stack VM so deep recursion never
  touches the Haskell call stack. Scaffolded the project and pushed.