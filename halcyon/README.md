# Halcyon

A small functional programming language and virtual machine written from
scratch in **Haskell** - the factory's first Haskell project and its first
compiler/language project. A complete, readable pipeline: a hand-written
lexer and parser, a real Hindley-Milner type checker (with `let`
polymorphism, constraint classes for overloaded operators, numeric
promotion, and type annotations), a tree-walking interpreter, a real
bytecode compiler and stack VM, a REPL, and a statically-hostable web
playground that runs Halcyon programs in the browser.

_(Skeleton - the full README lands with the finished build.)_

## Build

```sh
make        # builds ./halcyon with the system GHC (bundled libraries only)
make test   # builds and runs the full self-test suite
```

## Try it

```sh
./halcyon eval 'map (\x -> x * x) [1, 2, 3, 4]'
./halcyon repl
```