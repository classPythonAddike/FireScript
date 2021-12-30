# FireScript

Welcome! FireScript is a statically typed, Lisp language which is very similar to Scheme. Please note, that it is still under active development.

## Running FireScript Programs

You can use the shell script in `bin/` to run your code. As of now, you _must_ be in the same directory as this README, so that all imports work as expected. We hope to change this as soon as we have an interpreter rolled out!

To compile your `.fs` programs into bytecode -
```sh
$ chmod +x bin/firescript # Make the shell script executable
$ bin/firescript build examples/helloworld.fs
```

And you should see the resulting `.fsc` file in the same directory.

## How Does FireScript Work?

We have very ambitious plans for FireScript - We want to make it possible to interpret, compile, and transpile FireScript programs easily.

As of now, the first step has been partially implemented - A parser to convert FireScript code into bytecode, and the interpreter is under works.

Here are some perks of interpreting/compiling/transpiling FireScript -
1. Interpreting - Even thought interpreting a program is not very fast, as compared to running a compiled executable, interpreters are still pretty popular - you can edit the source code while the program is running, and see the changes ocurr live. While this feature will not be available in FireScript, we will offer something else - live reload. Live Reload is a great feature to use during dev time, as you don't need to keep rerunning the script. Even if you won't use that feature, just plain interpreting your program should speed up your development, as compared to compiling and running everytime you make your changes.
2. Compiling - Speed is the main driving force behind compiling FireScript.
3. Transpiling - FireScript may not be compiled for many operating systems and architectures. Over here, transpiling will help. You will be able to transpile a FireScript program into a cross platform language (Probably C, C++ or Golang) and compile it for your system. As these languages are ver fast, you should get good performance with your scripts.
