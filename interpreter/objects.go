package main

import (
	"fmt"
	"log"
	"strconv"
)

type Object interface {
    String() string
    ObjType() string
}


type Integer struct {
    value int
}
func NewInteger(val []int) *Integer {
    return &Integer{val[0]}
}
func (i Integer) String() string {
    return fmt.Sprint(i.value)
}
func (i *Integer) ObjType() string {
    return "Integer"
}


type Float struct {
    value float64
}
func NewFloat(val []int) *Float {
    float_val, err := strconv.ParseFloat(fmt.Sprintf("%v.%v", val[0], val[1]), 64)

    if err != nil {
        log.Fatal(err)
    }

    return &Float{float_val}
}
func (f Float) String() string {
    return fmt.Sprintf("%g", f.value)
}
func (f *Float) ObjType() string {
    return "Float"
}


type String struct {
    value string
}
func NewString (val []int) *String {
    s := String{}
    for _, item := range val {
        s.value += string(item)
    }
    return &s
}
func (s String) String() string {
    return s.value
}
func (s *String) ObjType() string {
    return "String"
}


type Bool struct {
    value bool
}
func NewBool(val []int) *Bool { 
    return &Bool{val[0] == 1}
}
func (b Bool) String() string {
    return fmt.Sprint(b.value)
}
func (b *Bool) ObjType() string {
    return "Bool"
}
