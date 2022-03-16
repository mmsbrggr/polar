from typing import Tuple, List
from symengine.lib.symengine_wrapper import Expr, logical_and, logical_not, zero, false

Branch = Tuple[Expr, Expr]
Expectation = List[Branch]


def simplify_expectation(expectation: Expectation) -> Expectation:
    exp_dict = {}
    for cond, expr in expectation:
        if cond in exp_dict:
            exp_dict[cond] += expr
        else:
            exp_dict[cond] = expr

    if false in exp_dict:
        del exp_dict[false]

    return [(c, e) for c, e in exp_dict.items() if e is not zero]


def expand_expectation_exhaustively(expectation: Expectation) -> Expectation:
    if len(expectation) == 0:
        return expectation
    if len(expectation) == 1:
        return [(expectation[0][0], expectation[0][1]), (logical_not(expectation[0][0]), zero)]
    first_cond, first_expr = expectation[0]
    rest = expectation[1:]
    rest_expanded = expand_expectation_exhaustively(rest)

    expectation_true = []
    for cond, expr in rest_expanded:
        expectation_true.append((logical_and(first_cond, cond), first_expr + expr))

    expectation_false = []
    for cond, expr in rest_expanded:
        expectation_false.append((logical_and(logical_not(first_cond), cond), expr))

    return expectation_true + expectation_false
