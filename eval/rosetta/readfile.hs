import System.Environment (getArgs)

main :: IO ()
main = do
    args <- getArgs
    case args of
        (filename:_) -> do
            contents <- readFile filename
            putStr contents
        _ -> putStrLn "Usage: runhaskell Program.hs <filename>"
