(begin
    (put "Hello, World!")
    (print "As you can see, `put` prints to stdout and then prints a newline\n")
    (print "However, print doesn't add the newline for you\n")
    (put "You " "can " "even " "pass " "in " "many " "arguments!")
    (put "Along with arguments of different types - " 85 " and " true " and " 54.5)
    
    (print "FireScript is a statically typed, compiled _and_ interpreted, Lisp programming language. ")
    (print "The parser is written in Python, which compiles your `.fs` files into bytecode. ")
    (print "And the interpreter is written in Rust. ")
    (put "We also have plans to compile the bytecode into executables!")
)
