package main

type Stack struct {
    stack []*Object
    variables map[int]*Object
}

func (s *Stack) Push(item Object) {
    s.stack = append(s.stack, &item)
}

func (s *Stack) Pop() *Object {
    obj := s.stack[len(s.stack) - 1]
    s.stack = s.stack[:len(s.stack) - 1]
    return obj
}

func (s *Stack) Store(id int) {
    s.variables[id] = s.Pop()
}

func (s *Stack) Load(id int) {
    s.Push(*s.variables[id])
}
