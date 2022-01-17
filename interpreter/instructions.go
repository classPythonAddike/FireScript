package main

import (
	"bufio"
	"fmt"
	"log"
	"os"
	"strconv"
)

var instructions map[int]string = map[int]string{
    0: "PUSH",
    1: "STORE",
    2: "LOAD",
    4: "CAST",
    5: "INT",
    6: "FLOAT",
    7: "STRING",
    8: "BOOL",
    9: "ADD",
    10: "SUB",
    11: "MUL",
    12: "DIV",
    13: "PRINT",
    14: "GET",
}

type Instruction func()

func PUSH_INT(values []int, parser *Parser) Instruction {
    val := NewInteger(values)
    return func() {
        parser.stack.Push(val)
    }
}

func PUSH_FLOAT(values []int, parser *Parser) Instruction {
    val := NewFloat(values)
    return func() {
        parser.stack.Push(val)
    }
}

func PUSH_STRING(values []int, parser *Parser) Instruction {
    val := NewString(values)
    return func() {
        parser.stack.Push(val)
    }
}

func PUSH_BOOL(values []int, parser *Parser) Instruction {
    val := NewBool(values)
    return func() {
        parser.stack.Push(val)
    }
}

func STORE(values []int, parser *Parser) Instruction {
    return func() {
        parser.stack.Store(values[0])
    }
}

func LOAD(values []int, parser *Parser) Instruction {
    return func() {
        parser.stack.Load(values[0])
    }
}

func CAST(values []int, parser *Parser) Instruction {
    return func() {
        switch instructions[values[0]] {
            case "INT":
                val, err := strconv.Atoi((*parser.stack.Pop()).String())
                if err != nil {
                    log.Fatal(err)
                }
                parser.stack.Push(&Integer{val})
            case "FLOAT":
                val, err := strconv.ParseFloat((*parser.stack.Pop()).String(), 64)
                if err != nil {
                    log.Fatal(err)
                }
                parser.stack.Push(&Float{val})
            case "BOOL":
                var value *Bool
                top := *parser.stack.Pop()

                switch top.ObjType() {
                    case "String":
                        value = &Bool{top.String() == ""}
                    case "Integer":
                        value = &Bool{top.String() != "0"}
                    case "Float":
                        value = &Bool{top.(*Float).value != 0.0}
                    case "Bool":
                        value = &Bool{top.String() == "true"}
                    default:
                        log.Fatalf("Unknown type encountered while casting - %v\n", top.ObjType())
                }
                parser.stack.Push(value)
            case "STRING":
                parser.stack.Push(&String{(*parser.stack.Pop()).String()})
            default:
                log.Fatalf("Unknown type (in bytecode) encountered while casting - %v\n", values[0])
        }
    }
}

func PRINT(parser *Parser) Instruction {
    return func() {
        fmt.Print(*(parser.stack.Pop()))
    }
}

func GET(parser *Parser) Instruction {
    return func() {
        scanner := bufio.NewScanner(os.Stdin)
        scanner.Scan()
        parser.stack.Push(&String{scanner.Text()})
    }
}

func EXIT(values []int, parser *Parser) Instruction {
    return func() {
        os.Exit(0)
    }
}
