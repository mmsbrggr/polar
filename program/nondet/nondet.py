from typing import List
from utils import indent_string


class Nondet:
    branch1: List
    branch2: List

    children = ["branch1", "branch2"]

    def __init__(self, branch1, branch2):
        self.branch1 = branch1
        self.branch2 = branch2

    def __str__(self):
        def branch_to_str(branch):
            return indent_string("\n".join([str(b) for b in branch]), 4)

        string = f"if *:\n{branch_to_str(self.branch1)}"
        if len(self.branch2) > 0:
            string += f"\nelse:\n{branch_to_str(self.branch2)}"

        return string

