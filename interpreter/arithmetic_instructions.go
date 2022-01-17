package main

func ADD(parser *Parser) Instruction {
    return func() {
        lval := *parser.stack.Pop()
        rval := *parser.stack.Pop()

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

func SUB(parser *Parser) Instruction {
    return func() {
        lval := *parser.stack.Pop()
        rval := *parser.stack.Pop()

        if lval.ObjType() == "Integer" {
            lv, rv := CheckIntegers(lval, rval)
            parser.stack.Push(
                &Integer{lv.value - rv.value},
            )
        } else if lval.ObjType() == "Float" {
            lv, rv := CheckFloats(lval, rval)
            parser.stack.Push(
                &Float{lv.value - rv.value},
            )
        }
    }
}


func MUL(parser *Parser) Instruction {
    return func() {
        lval := *parser.stack.Pop()
        rval := *parser.stack.Pop()

        if lval.ObjType() == "Integer" {
            lv, rv := CheckIntegers(lval, rval)
            parser.stack.Push(
                &Integer{lv.value * rv.value},
            )
        } else if lval.ObjType() == "Float" {
            lv, rv := CheckFloats(lval, rval)
            parser.stack.Push(
                &Float{lv.value * rv.value},
            )
        } else if lval.ObjType() == "Bool" {
            lv, rv := CheckBools(lval, rval)
            parser.stack.Push(
                &Bool{lv.value && rv.value},
            )
        }
    }
}

func DIV(parser *Parser) Instruction {
    return func() {
        lval := *parser.stack.Pop()
        rval := *parser.stack.Pop()

        if lval.ObjType() == "Integer" {
            lv, rv := CheckIntegers(lval, rval)
            parser.stack.Push(
                &Integer{lv.value / rv.value},
            )
        } else if lval.ObjType() == "Float" {
            lv, rv := CheckFloats(lval, rval)
            parser.stack.Push(
                &Float{lv.value / rv.value},
            )
        }
    }
}
