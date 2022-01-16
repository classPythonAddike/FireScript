package main

import (
	"os"
)

func main() {
    parser := NewParser(os.Args[1])
    parser.ParseBytecode()

    for {
        parser.instructions[parser.pointer]()
        parser.pointer += 1
    }
}
