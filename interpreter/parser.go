package main

import (
	"io/ioutil"
	"log"
	"strings"
)

type Parser struct {
    bytecode []string
    instructions map[int]Instruction
    pointer int
    stack *Stack
}

func NewParser(filename string) *Parser {
    bytecode, err := ioutil.ReadFile(filename)

    if err != nil {
        log.Fatal(err)
    }

    return &Parser{
        append(strings.Split(strings.TrimSpace(string(bytecode)), "\n"), ""),
        map[int]Instruction{},
        0,
        &Stack{
            []*Object{},
            map[int]*Object{},
        },
    }
}

func (p *Parser) ParseBytecode() {
    for num, raw_inst := range p.bytecode {
        p.instructions[num] = ParseInstruction(strings.Split(raw_inst, " "), p)
    }
}
