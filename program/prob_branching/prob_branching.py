from typing import List
from symengine.lib.symengine_wrapper import Expr, sympify
from utils import indent_string


class ProbBranching:
    branches: List
    probs: List[Expr]

    children = ["branches"]

    def __init__(self, branches, probs):
        self.branches = branches
        self.probs = [sympify(p) for p in probs]
        self.probs.append(1 - sum(self.probs))

    def __str__(self):
        def branch_to_str(branch):
            return indent_string("\n".join([str(b) for b in branch]), 4)

        string = f"if P({self.probs[0]}):\n{branch_to_str(self.branches[0])}"
        for i, branch in enumerate(self.branches[1:], start=1):
            string += f"\nelse if P({self.probs[i]}):\n{branch_to_str(branch)}"

        return string
