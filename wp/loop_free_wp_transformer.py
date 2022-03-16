from singledispatchmethod import singledispatchmethod
from symengine.lib.symengine_wrapper import logical_and, true, logical_not

from program.assignment import DistAssignment, PolyAssignment
from program.ifstatem import IfStatem
from program.nondet import Nondet
from program.prob_branching import ProbBranching
from .common import Expectation, simplify_expectation


class LoopFreeWpTransformer:

    @singledispatchmethod
    def transform(self, element, expectation: Expectation):
        return expectation

    @transform.register
    def _(self, elements: list, expectation: Expectation):
        for el in reversed(elements):
            expectation = self.transform(el, expectation)
        return expectation

    @transform.register
    def _(self, dist_assignment: DistAssignment, expectation: Expectation):
        raise NotImplementedError("wp transformer for dist assignments not implemented.")

    @transform.register
    def _(self, poly_assignment: PolyAssignment, expectation: Expectation):
        result = []
        for poly, prob in zip(poly_assignment.polynomials, poly_assignment.probabilities):
            for condition, expr in expectation:
                c = condition.subs({poly_assignment.variable: poly})
                e = prob * expr.subs({poly_assignment.variable: poly})
                result.append((c, e))
        return simplify_expectation(result)

    @transform.register
    def _(self, prob_branching: ProbBranching, expectation: Expectation):
        expects = [self.transform(b, expectation) for b in prob_branching.branches]
        result = []
        for expect, prob in zip(expects, prob_branching.probs):
            for branch_cond, branch_expr in expect:
                result.append((branch_cond, prob * branch_expr))
        return simplify_expectation(result)

    @transform.register
    def _(self, if_statem: IfStatem, expectation: Expectation):
        expects = [self.transform(b, expectation) for b in if_statem.branches]
        if_conds = [c.to_symengine_expr() for c in if_statem.conditions]

        result = []
        not_previous_cases = true
        for if_cond, expect in zip(if_conds, expects):
            for branch_cond, branch_expr in expect:
                case_cond = logical_and(not_previous_cases, if_cond)
                result.append((logical_and(case_cond, branch_cond), branch_expr))
            not_previous_cases = logical_and(not_previous_cases, logical_not(if_cond))

        else_expect = expectation if not if_statem.else_branch else self.transform(if_statem.else_branch, expectation)
        for branch_cond, branch_expr in else_expect:
            result.append((logical_and(not_previous_cases, branch_cond), branch_expr))

        return simplify_expectation(result)

    @transform.register
    def _(self, nondet: Nondet, expectation: Expectation):
        raise NotImplementedError("TODO.")
        #expect1 = self.transform(nondet.branch1, expectation)
        #expect2 = self.transform(nondet.branch2, expectation)
        #result = []
        #return expectation
