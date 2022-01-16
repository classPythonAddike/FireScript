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
            case "ADD":
                return ADD(p)
            case "PRINT":
                return PRINT(p)
            default:
                log.Fatalf("Unknow bytecode sequence - %v\n", inst[0])
        }
    }

    return EXIT([]int{}, p)
}


