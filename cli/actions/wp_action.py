from argparse import Namespace

from symengine.lib.symengine_wrapper import true

from program.transformer import DistTransformer
from wp import LoopFreeWpTransformer
from .action import Action
from cli.common import parse_program
from sympy import sympify


class WpAction(Action):

    cli_args: Namespace

    def __init__(self, cli_args: Namespace):
        self.cli_args = cli_args

    def __call__(self, *args, **kwargs):
        benchmark = args[0]
        program = parse_program(benchmark, self.cli_args.transform_categoricals)
        program = DistTransformer().execute(program)
        wp_transformer = LoopFreeWpTransformer()
        wp = wp_transformer.transform(program.loop_body, [(true, sympify("x"))])
        print(wp)
        print(program)
