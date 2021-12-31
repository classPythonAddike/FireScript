from parser.parser.expression_models.atoms import IntExp, FloatExp, BoolExp, StrExp, VarExp

from parser.parser.expressions import Program
from parser.parser.expression_models.arithmetic import AddExp, SubExp, MulExp, DivExp
from parser.parser.expression_models.builtins import PrintExp, PutExp, DefExp
from parser.parser.expression_models.typecasting import IntTypeCast, FloatTypeCast, StrTypeCast

atom_types = {
    exp.atom_type(): exp
    for exp in [IntExp, FloatExp, BoolExp, StrExp, VarExp]
}

expression_types = {
    exp.keyword(): exp
    for exp in [
        AddExp,
        SubExp,
        MulExp,
        DivExp,
        Program,
        PutExp,
        PrintExp,
        DefExp,
        IntTypeCast,
        FloatTypeCast,
        StrTypeCast
    ]
}
