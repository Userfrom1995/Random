module Halcyon.AST (module Halcyon.AST) where

import Halcyon.Errors (Pos)

type Name = String

-- | Surface syntax for type annotations.
data Type
  = TyInt
  | TyFloat
  | TyBool
  | TyString
  | TyList Type
  | TyFun Type Type
  | TyVar Name
  deriving (Eq, Show)

-- | Every expression carries the position where it starts, so all later
-- phases (type checker, interpreter, compiler) can report line:col errors.
data Expr = Expr
  { exprPos :: !Pos
  , exprK   :: !ExprK
  }
  deriving (Eq, Show)

data ExprK
  = EInt Integer
  | EFloat Double
  | EBool Bool
  | EString String
  | EVar Name
  | EApp Expr Expr
  | ELam [Name] Expr
  | EIf Expr Expr Expr
  | ELet Name (Maybe Type) [Name] Expr Expr
  | ELetRec Name (Maybe Type) [Name] Expr Expr
  | EList [Expr]
  | ECons Expr Expr
  | EOp Name Expr Expr
  | EUnary Name Expr
  deriving (Eq, Show)

-- | A top-level statement.
data Stmt
  = SDef Name (Maybe Type) [Name] Expr
  | SPrint Expr
  | SExpr Expr
  deriving (Eq, Show)

at :: Pos -> ExprK -> Expr
at p k = Expr p k
