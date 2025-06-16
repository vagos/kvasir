module Main where

data NestedList a
  = Elem a
  | List [NestedList a]
  deriving (Show, Eq)

flatmap :: (a -> b) -> NestedList a -> [b]
flatmap f (Elem x) = [f x]
flatmap f (List x) = concatMap (flatmap f) x

main :: IO ()
main = do
    let result1 = flatmap (+1) (Elem 5)
    let result2 = flatmap (+1) (List [Elem 1, List [Elem 2, Elem 3], Elem 4])
    print result1  -- Output: [6]
    print result2  -- Output: [2,3,4]
