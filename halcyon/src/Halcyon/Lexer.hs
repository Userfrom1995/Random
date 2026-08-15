module Halcyon.Lexer (Tok (..), TokKind (..), lexer) where

import Data.List (isPrefixOf)
import Halcyon.Errors

-- | The kind of a token.
data TokKind
  = TInt Integer
  | TFloat Double
  | TStr String
  | TIdent Name
  | TOp Name
  | TLparen
  | TRparen
  | TLbrack
  | TRbrack
  | TComma
  | TEquals
  | TDoubleColon
  | TBackslash
  | TArrow
  | TEOF
  deriving (Eq, Show)

data Tok = Tok
  { tokPos :: !Pos
  , tokK   :: !TokKind
  }
  deriving (Eq, Show)

type Name = String

-- | Lexing state: line (1-based), column (1-based), offset (0-based), and the
-- unconsumed input.
data LS = LS
  { lsLine :: !Int
  , lsCol  :: !Int
  , lsOff  :: !Int
  , lsRest :: String
  }

posOf :: LS -> Pos
posOf s = Pos (lsLine s) (lsCol s) (lsOff s)

errAt :: LS -> String -> Either HErr a
errAt s m = Left (HErr (posOf s) m)

-- | Consume one character, updating line/column/offset.
skip1 :: LS -> LS
skip1 s = case lsRest s of
  [] -> s
  c : rest
    | c == '\n' -> LS (lsLine s + 1) 1 (lsOff s + 1) rest
    | otherwise -> LS (lsLine s) (lsCol s + 1) (lsOff s + 1) rest

-- | Consume @n@ characters.
takeN :: LS -> Int -> LS
takeN s 0 = s
takeN s n = takeN (skip1 s) (n - 1)

isNameStart :: Char -> Bool
isNameStart c = c `elem` ['a' .. 'z'] || c `elem` ['A' .. 'Z'] || c == '_'

isNameChar :: Char -> Bool
isNameChar c = isNameStart c || c `elem` ['0' .. '9'] || c == '\''

isDigit :: Char -> Bool
isDigit c = c `elem` ['0' .. '9']

-- | Multi-character tokens, longest match first. The friendly alias \/= is
-- accepted as a spelling of \/= (not-equal).
opTable :: [(String, String)]
opTable =
  [ ("->", "->")
  , ("==", "==")
  , ("/=", "/=")
  , ("!=", "/=")
  , ("<=", "<=")
  , (">=", ">=")
  , ("&&", "&&")
  , ("||", "||")
  , ("++", "++")
  , ("::", "::")
  , ("+", "+")
  , ("-", "-")
  , ("*", "*")
  , ("/", "/")
  , ("%", "%")
  , ("<", "<")
  , (">", ">")
  , (":", ":")
  , ("=", "=")
  , ("\\", "\\")
  , ("(", "(")
  , (")", ")")
  , ("[", "[")
  , ("]", "]")
  , (",", ",")
  ]

matchOp :: String -> Maybe (TokKind, Int)
matchOp input = go opTable
  where
    go [] = Nothing
    go ((src, canon) : rest)
      | src `isPrefixOf` input = Just (tokFrom canon, length src)
      | otherwise = go rest
    tokFrom canon = case canon of
      "(" -> TLparen
      ")" -> TRparen
      "[" -> TLbrack
      "]" -> TRbrack
      "," -> TComma
      "=" -> TEquals
      "::" -> TDoubleColon
      "\\" -> TBackslash
      "->" -> TArrow
      _ -> TOp canon

-- | Skip a line comment (rest already past the '--').
skipLine :: LS -> LS
skipLine s = case lsRest s of
  [] -> s
  '\n' : _ -> s
  _ -> skipLine (skip1 s)

-- | Skip a nested block comment. @depth@ is the current nesting depth.
skipComment :: Int -> LS -> Either HErr LS
skipComment depth s = case lsRest s of
  [] -> if depth == 0 then Right s else errAt s "unterminated block comment"
  '{' : '-' : _ -> skipComment (depth + 1) (skip1 (skip1 s))
  '-' : '}' : _
    | depth > 0 -> skipComment (depth - 1) (skip1 (skip1 s))
    | otherwise -> errAt s "unexpected end of block comment"
  _ -> skipComment depth (skip1 s)

-- | Consume a string literal, returning the decoded value and the new state.
lexString :: LS -> Either HErr (String, LS)
lexString s = go [] (skip1 s)
  where
    go acc st = case lsRest st of
      [] -> errAt st "unterminated string literal"
      '"' : _ -> Right (reverse acc, skip1 st)
      '\\' : c : _ -> case c of
        'n' -> go ('\n' : acc) (skip1 (skip1 st))
        't' -> go ('\t' : acc) (skip1 (skip1 st))
        'r' -> go ('\r' : acc) (skip1 (skip1 st))
        '\\' -> go ('\\' : acc) (skip1 (skip1 st))
        '"' -> go ('"' : acc) (skip1 (skip1 st))
        '\'' -> go ('\'' : acc) (skip1 (skip1 st))
        _ -> errAt st ("unknown escape sequence '\\" ++ [c] ++ "'")
      c : _ -> go (c : acc) (skip1 st)

-- | Consume a number literal (integer or float).
lexNumber :: LS -> Either HErr (TokKind, LS)
lexNumber s =
  let (intPart, rest) = span isDigit (lsRest s)
  in case rest of
    '.' : frac
      | (d : _) <- frac, isDigit d ->
          let (fracPart, _) = span isDigit frac
              n = length intPart + 1 + length fracPart
          in Right (TFloat (read (intPart ++ "." ++ fracPart)), takeN s n)
    _ -> Right (TInt (read intPart), takeN s (length intPart))

-- | Consume a name and return its text and the new state.
lexName :: LS -> (String, LS)
lexName s =
  let (name, _) = span isNameChar (lsRest s)
  in (name, takeN s (length name))

-- | Tokenize a source string. Always ends with a TEOF token.
lexer :: String -> Either HErr [Tok]
lexer src = reverse <$> go (LS 1 1 0 src) []
  where
    go :: LS -> [Tok] -> Either HErr [Tok]
    go s acc = case lsRest s of
      [] -> Right (Tok (posOf s) TEOF : acc)
      c : _
        | c == '\n' || c == ' ' || c == '\t' || c == '\r' -> go (skip1 s) acc
        | take 2 (lsRest s) == "--" -> go (skipLine (skip1 (skip1 s))) acc
        | take 2 (lsRest s) == "{-" -> skipComment 1 (skip1 (skip1 s)) >>= \s' -> go s' acc
        | c == '"' -> do
            (str, s') <- lexString s
            go s' (Tok (posOf s) (TStr str) : acc)
        | isDigit c -> do
            (k, s') <- lexNumber s
            go s' (Tok (posOf s) k : acc)
        | isNameStart c ->
            let (name, s') = lexName s
            in go s' (Tok (posOf s) (TIdent name) : acc)
        | otherwise -> case matchOp (lsRest s) of
            Just (k, n) -> go (takeN s n) (Tok (posOf s) k : acc)
            Nothing -> errAt s ("unexpected character '" ++ [c] ++ "'")