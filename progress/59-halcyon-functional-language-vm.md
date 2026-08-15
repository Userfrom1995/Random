# Progress - Halcyon

Status: in-progress

- **Issue:** #59
- **Branch:** opencode/59-halcyon-functional-language-vm
- **Status:** in-progress
- **Updated:** 2026-08-15T07:25:00Z

## Checklist
- [x] scaffold: branch, progress file, ideas entry, Makefile, src tree, CLI stub, .gitignore
- [x] core: AST + Lexer + Parser + Errors + pretty printer, `parse`/`ast` CLI, 25 parsing round-trip tests
- [x] type checker: Hindley-Milner inference with constraint classes + numeric promotion + type annotations, `check`/`types` CLI, 59 type tests
- [ ] tree-walking interpreter: values, evaluator, canonical formatting, `run` CLI, REPL, embedded prelude, tests
- [ ] bytecode VM: compiler + stack VM + disassembler, `vm`/`bytecode` CLI, REPL `--vm`, tests
- [ ] samples: `samples/*.hcy` demonstration programs + full selftest suite + differential tests
- [ ] web playground core: faithful JS mirror (`js/halcyon.js`: lexer/parser/typecheck/interp/compile/vm/format) + node CLI + js tests
- [ ] web playground UI: `index.html` + css + app + embedded samples
- [ ] iteration/improvement cycle: brainstorm and implement at least one major enhancement
- [ ] docs: README, `docs/` (index.md/html, language.md, internals.md), ideas entry final, landing page + root README update, final push, Status: complete

## Current step
Type checker done: pure Algorithm W with fresh-variable counters,
occurs-check unification with global Int/Float promotion (Int meets Float ->
Float, including in if-branches), and a small constraint-class system
(Num/Ord/Eq/App) for overloaded operators. Constraints travel through
inference, transfer through unification, ride into generalized schemes as
qualified types (`forall a. (Num a) => a -> a`), and default to Int when
free. Type annotations are checked against the inferred type. 59 type tests
green (including 15 negative tests and let-polymorphism tests), `-Wall`
clean. Next: the tree-walking interpreter.

## Next steps
Tree-walking interpreter: value domain, evaluator with closures and
recursive let, canonical formatting (shared 6-decimal float formatter),
`print`, builtins (head/tail/null/print/show), embedded prelude; wire
`halcyon run`, `halcyon eval`, and the REPL; interpreter tests.

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
  touches the Haskell call stack. Scaffolded the project and pushed, opened
  PR #60.
- 2026-08-15 (run 1): implemented the core front end. Errors module
  (1-based line/col positions, grep-friendly rendering); AST (every
  expression node carries its start position so every later phase can report
  line:col); Lexer (line + nested block comments, string escapes, int/float
  literals, longest-match operator table, `!=` accepted as a friendly alias
  for `/=`); Parser (precedence climbing: `||` < `&&` < comparison <
  right-assoc cons `:` < `++`/`+`/`-` < `*`/`/`/`%` < unary minus/not <
  juxtaposition application < atoms; `let`/`letrec` disambiguated from
  top-level definitions by the presence of `in`; keywords banned as atoms;
  surface type syntax for `::` annotations); Pretty (round-trips the AST,
  binding-aware parens, shared binding-spacing helper). Wired `halcyon
  parse` (token dump), `halcyon ast` (AST dump), and the self-test harness.
  Fixed bugs found by the suite: `expectOp` never matched the dedicated
  `TEquals` token, pretty printer glued name and params (`let squarex =`),
  `parseAtom` accepted keywords as variables, and the statement-level
  `let ... in` branch never consumed `in`. 25 round-trip tests green,
  zero `-Wall` warnings. Committed and pushed.- 2026-08-15 (run 1): implemented the Hindley-Milner type checker
  (`Halcyon/Type.hs`). Pure Algorithm W in a `TC` monad over (fresh counter,
  substitution, constraint set, error position). Global Int/Float promotion
  in unification rewrites the substitution so both operands and if-branches
  join to Float. Constraint classes: Num (Int, Float), Ord (Int, Float,
  String), Eq (Int, Float, Bool, String, and lists with element transfer),
  App (String and any list) for `++`. Constraints are re-emitted on fresh
  vars at instantiation, transferred through unification, and either checked
  against ground types or carried into generalized schemes as qualified
  types; free constrained vars default to Int. Operators: `+ - *` Num,
  `/` Num but always Float, `%` strict Int, comparisons shared-class Bool,
  `==`/`/=` Eq, `&&`/`||` Bool, `++` App. `letrec`/top-level recursion uses
  the standard fresh-var-then-unify typing. `::` annotations unified against
  the inferred type. Scheme rendering normalizes quantified variables to
  a,b,c in first-occurrence order so output is stable. Wired `halcyon check`
  and `halcyon types`. Fixed bugs found by the suite: `%` was forced to
  Float, unify discarded the promoted result (if-branches returned Int
  instead of Float), ELam bound params as MonoT instead of Scheme. 84 tests
  green (25 parser + 59 type), zero warnings. Committed and pushed.
