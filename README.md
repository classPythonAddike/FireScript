# FireScript

Welcome! FireScript is a statically typed, Lisp language which is very similar to Scheme. Please note, that it is still under active development.

#### Please note: We will not be accepting PR's to the interpreter until we have a working implementation. However, you can make PR's to the compiler, after discussing your changes in a Github issue.

## How Does FireScript Work?

FireScript is a statically typed language, which means that the type of variables cannot be changed during runtime. Types of variables are inferred at compile time, so you don't need to specify them.

> NOTE: As of now, the compiler to convert FireScript code into bytecode is partially implemented, and the interpreter is under works.

FireScript will be compiled and interpreted - just like Java.
When you write a FireScript program, you will have to compile it to bytecode with the firescript compiler. Then, you can interpreted the emittted `.fsc` file with the FireScript interpreter. While this how many interpreted languages, like Python, and Ruby work, not all of them emit cross platform bytecode like Java. This is how FireScript is similar to Java - the bytecode produced can be used by the FireScript interpreter on any platform, hence making it distributable.

## Compiling FireScript Programs

Currently, since dev on FireScript is still ongoing, you will need to install all the required modules, and build the compiler manually. This will change as soon as we have a stable interpreter, and compiler rolled out.

Make sure you're using Python 3.10 -

```sh
# Create a venv
$ python -m venv ./venv

# Activate the venv
$ source venv/bin/activate # Linux/MacOS
$ venv\Scripts\activate.bat # Windows

# Install python packages
(venv) $ pip install -r requirements.txt

# Compile the compiler with nuitka
# and interpreter, with go
# If you want faster compile times, make sure you have `ccache` installed as nuitka uses it to cache builds
(venv) $ make build

```

To compile your `.fs` programs into bytecode -
```sh
$ bin/firescript build examples/helloworld.fs
$ bin/fscrun run -f examples/helloworld.fsc
```
