from typing import Tuple, List
from symengine.lib.symengine_wrapper import Expr

Branch = Tuple[Expr, Expr]
Expectation = List[Branch]


def simplify_expectation(expectation: Expectation) -> Expectation:
    exp_dict = {}
    for cond, expr in expectation:
        if cond in exp_dict:
            exp_dict[cond] += expr
        else:
            exp_dict[cond] = expr

    return [(c, e) for c, e in exp_dict.items()]
