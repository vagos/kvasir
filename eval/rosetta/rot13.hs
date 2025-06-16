import Data.Char (chr, ord, isLower, isUpper)

rot13 :: Char -> Char
rot13 c
  | isLower c = chr $ ((ord c - ord 'a' + 13) `mod` 26) + ord 'a'
  | isUpper c = chr $ ((ord c - ord 'A' + 13) `mod` 26) + ord 'A'
  | otherwise = c
