from argparse import Namespace
from .action import Action
from expansions import GramCharlierExpansion
from symengine.lib.symengine_wrapper import sympify
from sympy import Symbol
from sympy.plotting import plot as symplot
from cli.common import prepare_program, get_all_cumulants


class GramCharlierAction(Action):
    cli_args: Namespace

    def __init__(self, cli_args: Namespace):
        self.cli_args = cli_args

    def __call__(self, *args, **kwargs):
        benchmark = args[0]
        monom = sympify(self.cli_args.gram_charlier)
        program = prepare_program(benchmark, self.cli_args)
        cumulants = get_all_cumulants(program, monom, self.cli_args.gram_charlier_order, self.cli_args)
        expansion = GramCharlierExpansion(cumulants)
        density = expansion()
        print(density)
        if self.cli_args.at_n >= 0:
            mu = float(cumulants[1])
            sigma = float(cumulants[2]) ** (1 / 2)
            symplot(density, (Symbol("x"), mu - 5 * sigma, mu + 5 * sigma))