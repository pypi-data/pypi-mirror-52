"""
Module that contains the command line app.

Why does this file exist, and why not put this in __main__?

  You might be tempted to import things from __main__ later, but that will cause
  problems: the code will get executed twice:

  - When you run `python -mmake_help` python will execute
    ``__main__.py`` as a script. That means there won't be any
    ``make_help.__main__`` in ``sys.modules``.
  - When you import __main__ it will get executed again (as a module) because
    there's no ``make_help.__main__`` in ``sys.modules``.

  Also see (1) from http://click.pocoo.org/5/setuptools/#setuptools-integration
"""
from pathlib import Path
from typing import Optional
import click
import click_pathlib
import click_log
import argparse
import subprocess
import itertools
import re
from enum import Enum
import logging


logger = logging.getLogger(__name__)
click_log.basic_config(logger)


class LogMessages(str, Enum):
    FILE_NOT_SPECIFIED = 'No makefile specified, proceeding with implicit makefile lookup behaviour.'
    FILE_SPECIFIED_FILE_NOT_FOUND = (
        'The specified makefile does not exist. '
        'Falling back to implicit makefile lookup behaviour.'
    )
    FILE_SPECIFIED_FILE_FOUND = 'Using specified makefile.'
    UNKNOWN = (
        "Dont know how you got here, "
        "but I'm falling back to implicit makefile lookup behaviour and trying to proceed anyway."
    )


# https://github.com/Snaipe/python-rst2ansi/ - Simple pre-styled block ReST -> Formatted Terminal Text ?
# https://github.com/emdb-empiar/styled - styled output?
# https://pypi.org/project/blessings/


# Raw command line basic formatting codes.
# http://www.lihaoyi.com/post/BuildyourownCommandLinewithANSIescapecodes.html#writing-a-command-line


def green_text(text):
    return f'\u001b[32;1m{text}\u001b[0m'


@click.command()
@click.argument('makefile', type=click_pathlib.Path(exists=True))
# @click_log.simple_verbosity_option(logger)
def main(makefile: Optional[Path]):
    # ----------------------------------------
    if makefile is None:
        # logger.info(LogMessages.FILE_NOT_SPECIFIED.value)
        subprocess_invocation = ['make', '-pRrq', ':']
        current_working_directory = Path.cwd()
    elif not makefile.exists():
        # logger.warning(LogMessages.FILE_SPECIFIED_FILE_NOT_FOUND.value)
        subprocess_invocation = ['make', '-pRrq', ':']
        current_working_directory = Path.cwd()
    elif makefile.exists():
        # logger.info(LogMessages.FILE_SPECIFIED_FILE_FOUND.value)
        subprocess_invocation = ['make', '-pRrq', '-f', makefile.name, ':']
        current_working_directory = makefile.parent
    else:
        # logger.error(LogMessages.UNKNOWN.value)
        subprocess_invocation = ['make', '-pRrq', ':']
        current_working_directory = Path.cwd()
    # ----------------------------------------
    target_details = {}
    match_list = []
    # ----------------------------------------
    # click.echo(repr(makefile))
    # ----------------------------------------
    cmd_result = subprocess.run(
        subprocess_invocation,
        capture_output=True,
        cwd=current_working_directory,
    )
    result = cmd_result.stdout.decode('utf8')
    # ----------------------------------------
    split = result.split('\n\n')
    # ----------------------------------------
    lines = list(itertools.takewhile(lambda s: not s.startswith('# Finished Make data base'),
                                     itertools.dropwhile(lambda s: not s.startswith('# File'), split)))
    # ----------------------------------------
    target_lines = [line for line in lines if not (line.startswith('#') or line.startswith('.'))]
    # ----------------------------------------
    target_list = [line.splitlines()[0].split(':')[0] for line in lines if
                   not (line.startswith('#') or line.startswith('.'))]
    # ----------------------------------------

    # noinspection PyTypeChecker
    with open(makefile) as target_makefile:
        for line_number, line_text in enumerate(target_makefile):
            for target in target_list:
                if line_text.startswith(target):
                    if target not in target_details:
                        target_details[target] = {}
                    target_details[target]['line_number'] = line_number
        for target in target_list:
            target_makefile.seek(0)
            match = re.search(
                fr"# -{{5,}}\n# +(?P<type>(?:>>>help>>>)\n)(?P<help>(?:# +.+\n)+)(?:.+\n)?(?:{target}:)",
                target_makefile.read(),
                flags=re.MULTILINE
            )
            # print(target, match)
            if match is not None:
                match_text = match.group('help').replace('# ', '').replace('\n', '')
                match_list.append(match_text)
                target_details[target]['help_text'] = match_text
            else:
                target_details[target]['help_text'] = None
    # ----------------------------------------
    # click.echo()
    # click.echo(target_details)
    # click.echo()
    # click.echo(match_list)
    # click.echo()
    # ----------------------------------------

    parser = argparse.ArgumentParser(prog='make', add_help=False)

    # parser.add_argument('a', help='a help')

    subparsers = parser.add_subparsers(
        title='Makefile Targets',
        help='These are the available makefile targets.',
        metavar=''
    )

    for target in target_list:
        help_text = target_details[target]['help_text']
        if help_text is None:
            help_text = "No help has been provided for this makefile target."
        parser.add_argument_group(green_text(target), help_text)

    print('-'*80)
    print()
    parser.print_help()
    print()

    # # create the parser for the "a" command
    # parser_a = subparsers.add_parser('b', help='B help')
    # parser_a.add_argument('bar', type=int, help='bar help')
    # # create the parser for the "b" command
    # parser_b = subparsers.add_parser('c', help='c help')
    # parser_b.add_argument('--baz', choices='XYZ', help='baz help')

    # # for key, val in target_details.items():
    # #     subparser = parser.add_subparsers(
    # #         title=key, dest=key, help=target_details[key]['help_text'], metavar=''
    # #     )
    #
    # parser.print_help()
    #
    # print('-' * 20)
    # #
    # # create the top-level parser
    # parser = argparse.ArgumentParser(prog='PROG')
    # parser.add_argument('--foo', action='store_true', help='foo help')
    # subparsers = parser.add_subparsers(help='sub-command help')
    # # create the parser for the "a" command
    # parser_a = subparsers.add_parser('a', help='a help')
    # parser_a.add_argument('bar', type=int, help='bar help')
    # # create the parser for the "b" command
    # parser_b = subparsers.add_parser('b', help='b help')
    # parser_b.add_argument('--baz', choices='XYZ', help='baz help')
    # # parse some argument lists
    # parser.print_help()
