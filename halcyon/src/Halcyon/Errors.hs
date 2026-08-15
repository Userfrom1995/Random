module Halcyon.Errors (Pos (..), HErr (..), formatError, originPos) where

-- | A position in the source: 1-based line and column, 0-based offset.
data Pos = Pos
  { posLine :: !Int
  , posCol  :: !Int
  , posOff  :: !Int
  }
  deriving (Eq, Show)

originPos :: Pos
originPos = Pos 1 1 0

-- | An error with its source position.
data HErr = HErr
  { errPos :: Pos
  , errMsg :: String
  }
  deriving (Eq, Show)

-- | Render an error as \"file:line:col: message\", grep-friendly.
formatError :: String -> HErr -> String
formatError file (HErr p m) =
  file ++ ":" ++ show (posLine p) ++ ":" ++ show (posCol p) ++ ": " ++ m