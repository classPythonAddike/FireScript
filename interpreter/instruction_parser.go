package main

import (
    "log"
    "strconv"
)

func ParseInstruction(raw_inst []string, p *Parser) Instruction {

    if raw_inst[0] != "" {
    
        inst := []int{}
        for _, raw := range raw_inst {
            int_inst, err := strconv.Atoi(raw)
            if err != nil {
                log.Fatal(err)
            }
            inst = append(inst, int_inst)
        }

        switch instructions[inst[0]] {
            case "PUSH":
                switch instructions[inst[1]] {
                    case "INT":
                        return PUSH_INT(inst[2:], p)
                    case "FLOAT":
                        return PUSH_FLOAT(inst[2:], p)
                    case "STRING":
                        return PUSH_STRING(inst[2:], p)
                    case "BOOL":
                        return PUSH_BOOL(inst[2:], p)
                }
            case "STORE":
                return STORE(inst[1:], p)
            case "LOAD":
                return LOAD(inst[1:], p)
            case "CAST":
                return CAST(inst[1:], p)
            case "ADD":
                return ADD(p)
            case "SUB":
                return SUB(p)
            case "MUL":
                return MUL(p)
            case "DIV":
                return DIV(p)
            case "PRINT":
                return PRINT(p)
            case "GET":
                return GET(p)
            default:
                log.Fatalf("Unknown bytecode sequence - %v\n", inst)
        }
    }

    return EXIT([]int{}, p)
}


