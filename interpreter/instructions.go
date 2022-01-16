package main

import (
	"fmt"
	"os"
)

var instructions map[int]string = map[int]string{
    0: "PUSH",
    1: "STORE",
    2: "LOAD",
    5: "INT",
    6: "FLOAT",
    7: "STRING",
    8: "BOOL",
    9: "ADD",
    13: "PRINT",
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

func ADD(parser *Parser) Instruction {
    return func() {
        rval := *parser.stack.Pop()
        lval := *parser.stack.Pop()

        if lval.ObjType() == "Integer" {
            lv, rv := CheckIntegers(lval, rval)
            parser.stack.Push(
                &Integer{lv.value + rv.value},
            )
        } else if lval.ObjType() == "Float" {
            lv, rv := CheckFloats(lval, rval)
            parser.stack.Push(
                &Float{lv.value + rv.value},
            )
        } else if lval.ObjType() == "String" {
            lv, rv := CheckStrings(lval, rval)
            parser.stack.Push(
                &String{lv.value + rv.value},
            )
        } else if lval.ObjType() == "Bool" {
            lv, rv := CheckBools(lval, rval)
            parser.stack.Push(
                &Bool{lv.value || rv.value},
            )
        }
    }
}

func PRINT(parser *Parser) Instruction {
    return func() {
        fmt.Print(*(parser.stack.Pop()))
    }
}

func EXIT(values []int, parser *Parser) Instruction {
    return func() {
        os.Exit(0)
    }
}
