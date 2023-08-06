import argparse
import sys
import os
from typing import Tuple

from .core import modules_loader, traverser, parser

CURRENT_FILE_DIR = os.path.dirname(__file__)


def create_parser() -> argparse.ArgumentParser:
    argparser = argparse.ArgumentParser()
    argparser.add_argument('-c', '--checks',
                           help='enable checks in the following format: style* legacy*',
                           default=['*'],
                           nargs='+',
                           type=str)
    argparser.add_argument('-v', '--verbose',
                           help='enable verbose logging for large projects',
                           action='store_true')
    argparser.add_argument('--custom-checks',
                           metavar='PATH',
                           help='directory with user-defined checks',
                           default=None,
                           type=str)

    me_group_action = argparser.add_mutually_exclusive_group(required=True)
    me_group_action.add_argument('-p', '--path',
                                 help='path to start check from',
                                 type=str)
    me_group_action.add_argument('--list-checks',
                                 help='list all available checks',
                                 action='store_true')

    me_group_including_excluding = argparser.add_mutually_exclusive_group()
    me_group_including_excluding.add_argument('--exclude',
                                              help='filter out files by mask',
                                              default=None,
                                              nargs='+',
                                              type=str)
    me_group_including_excluding.add_argument('--include',
                                              help='include only files by mask',
                                              default=['*'],
                                              nargs='+',
                                              type=str)
    return argparser


def parse_args(argparser, args) -> Tuple[list, list, list, bool, list, bool, str]:
    args = argparser.parse_args(args)

    include_filters = args.include
    exclude_filters = args.exclude

    if exclude_filters:
        include_filters = None

    modules_list = [os.path.join(CURRENT_FILE_DIR, 'modules')]
    if args.custom_checks:
        modules_list.append(args.custom_checks)

    do_list_checks = bool(args.list_checks)

    return include_filters, exclude_filters, modules_list, do_list_checks, args.checks, args.verbose, args.path


def main(args):
    argparser = create_parser()
    includes, excludes, modules, do_list_checks, checks, is_verbose, path = parse_args(
        argparser, args[1:])

    if do_list_checks:
        loader = modules_loader.ModulesLoader(modules)
        for module in loader.loaded_modules:
            print(module.__name__)
        return

    loader = modules_loader.ModulesLoader(modules, checks)
    file_parser = parser.CMakeParser(os.path.join(
        CURRENT_FILE_DIR, 'static', 'simple_grammar.ebnf'))
    project_traverser = traverser.Traverser(file_parser,
                                            checkers=loader.loaded_checkers,
                                            include_filters=includes,
                                            exclude_filters=excludes,
                                            verbose=is_verbose)

    project_traverser.traverse(path)

def entrypoint():
    main(sys.argv)
