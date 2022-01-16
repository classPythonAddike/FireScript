package main

type Stack struct {
    stack []*Object
    variables map[int64]*Object
}

func (s *Stack) Push(item Object) {
    s.stack = append(s.stack, &item)
}

func (s *Stack) Pop() *Object {
    obj := s.stack[len(s.stack) - 1]
    s.stack = s.stack[:len(s.stack) - 1]
    return obj
}

func (s *Stack) Store(id int64) {
    s.variables[id] = s.Pop()
}

func (s *Stack) Load(id int64) {
    s.Push(*s.variables[id])
}
