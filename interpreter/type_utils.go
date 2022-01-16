package main

import "log"

func MismatchingTypesErr(t1, t2 string) {
    log.Fatalf("Error: Got two mismatching types - %v, %v\n", t1, t2)
}

func CheckIntegers(lval, rval Object) (*Integer, *Integer) {
    l, r := lval.ObjType(), rval.ObjType()
    if l != r {
        MismatchingTypesErr(l, r)
    }

    return lval.(*Integer), rval.(*Integer)
}


func CheckFloats(lval, rval Object) (*Float, *Float) {
    l, r := lval.ObjType(), rval.ObjType()
    if l != r {
        MismatchingTypesErr(l, r)
    }

    return lval.(*Float), rval.(*Float)
}


func CheckBools(lval, rval Object) (*Bool, *Bool) {
    l, r := lval.ObjType(), rval.ObjType()
    if l != r {
        MismatchingTypesErr(l, r)
    }

    return lval.(*Bool), rval.(*Bool)
}

func CheckStrings(lval, rval Object) (*String, *String) {
    l, r := lval.ObjType(), rval.ObjType()
    if l != r {
        MismatchingTypesErr(l, r)
    }

    return lval.(*String), rval.(*String)
}
