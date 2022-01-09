from compiler.parser.expression_models.atoms import (
    IntExp,
    FloatExp,
    BoolExp,
    StrExp,
    VarExp,
)

from compiler.parser.expressions import Program
from compiler.parser.expression_models.control_structures import IfExp
from compiler.parser.expression_models.definitions import DefExp, AssignExp
from compiler.parser.expression_models.builtins import PrintExp, PutExp, GetExp
from compiler.parser.expression_models.arithmetic import AddExp, SubExp, MulExp, DivExp
from compiler.parser.expression_models.typecasting import (
    IntTypeCast,
    FloatTypeCast,
    StrTypeCast,
)

atom_types = {
    exp.atom_type(): exp for exp in [IntExp, FloatExp, BoolExp, StrExp, VarExp]
}

expression_types = {
    exp.keyword(): exp
    for exp in [
        Program,
        IfExp,
        DefExp,
        AssignExp,
        PutExp,
        PrintExp,
        GetExp,
        AddExp,
        SubExp,
        MulExp,
        DivExp,
        IntTypeCast,
        FloatTypeCast,
        StrTypeCast,
    ]
}
