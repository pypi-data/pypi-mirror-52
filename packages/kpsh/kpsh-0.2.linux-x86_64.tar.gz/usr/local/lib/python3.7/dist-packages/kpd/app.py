# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2019 Michał Góral.

import os
import sys
import shlex
import argparse
from functools import lru_cache

from prompt_toolkit import PromptSession
from prompt_toolkit.formatted_text.html import HTML

from kpd.db import DelayedPyKeePass
from kpd.utils import eprint
from kpd.commands import (
    CommandError, autotype, show, echo, sleep, ls, help_, exit, unlock, lock,
    open_)
from kpd.completion import CommandCompleter
from kpd._version import version


class ArgumentParserError(Exception): pass


class ThrowingArgumentParser(argparse.ArgumentParser):
    def error(self, message):
        raise ArgumentParserError(message)


@lru_cache(maxsize=32)
def ps1(prompt, dbpath):
    if not dbpath:
        dbpath = ''
    home = os.path.expanduser('~')
    if dbpath.startswith(home):
        dbpath = dbpath.replace(home, '~')

    return HTML(prompt.format(dbpath))


def readprompt(kp, prompt, parsers):
    compl = CommandCompleter(kp, (p for p in parsers if p))
    session = PromptSession(completer=compl, complete_while_typing=False)

    def _fn():
        while True:
            try:
                yield session.prompt(ps1(prompt, kp.db))
            except EOFError:
                break
            except KeyboardInterrupt:
                continue
    return _fn


def readinput():
    while True:
        try:
            yield input()
        except EOFError:
            break


def run_shell(kp, prompt, cmd_parser, parsers):
    if sys.stdin.isatty():
        reader = readprompt(kp, prompt, parsers)
    else:
        reader = readinput

    for text in reader():
        cmd = shlex.split(text)
        if not cmd:
            continue

        try:
            cargs = cmd_parser.parse_args(cmd)
            if cargs.func(kp, cargs) is False:
                break
        except ArgumentParserError as e:
            eprint(str(e))
        except CommandError as e:
            eprint(str(e))


def prepare_command_parser():
    cp = ThrowingArgumentParser(prog='', add_help=False)
    sp = cp.add_subparsers(required=True)

    parsers = {}
    parsers[None] = cp

    # helper function which automatically creates help-friendly parsers
    def add_parser(command, *a, **kw):
        kw['add_help'] = False

        descr = kw.get('description')
        if descr:
            kw['description'] = '{}\n\n{}'.format(kw['help'], descr)
        else:
            kw['description'] = kw['help']

        parser = sp.add_parser(command, *a, **kw)
        parsers[command] = parser
        return parser

    ######### open
    open_sp = add_parser('open', help='Change currently opened database.')
    open_sp.add_argument('filepath', help='path to database file.')
    open_sp.set_defaults(func=open_)

    ######### unlock
    unlock_sp = add_parser('unlock', help='Unlock currently opened database.')
    unlock_sp.add_argument('--keyfile', default='',
                           help='key file used for unlocking database')
    unlock_sp.set_defaults(func=unlock)

    ######### lock
    lock_sp = add_parser('lock', help='Lock a database.')
    lock_sp.set_defaults(func=lock)

    ######### ls
    ls_sp = add_parser('ls', help='List contents of database.')
    ls_sp.add_argument('glob', nargs='?', default='*',
                       help='display only entries which match glob expression')
    ls_sp.set_defaults(func=ls)

    ######### show
    show_sp = add_parser('show', help='Show contents of entry.',
        description='Search is case-sensitive.')
    show_sp.add_argument('path', help='path which should be shown')
    show_sp.add_argument('fields', nargs='*',
        help='only display certain fields')
    show_sp.add_argument('-n', '--no-field-name', action='store_true',
        help='hide field name when printing entry fields.')
    show_sp.set_defaults(func=show)

    ######### autotype
    at_sp = add_parser('autotype', help='Auto-type sequence of entry fields.',
        description='This simulates keypresses to any currently open window. '
                    'It\'s particularily useful when kpsh is run from a script '
                    'or keypress in non-interactive mode (`-c` switch). If '
                    '`-s` is given, it will be used as auto-type sequence. '
                    'Otherwise sequence defined for selected entry will be '
                    'used or the default one if there is none (`-d`).')
    at_sp.add_argument('path', help='path of entry to auto-type')
    at_sp.add_argument('-s', '--sequence', help='override auto-type sequence')
    at_sp.add_argument('-d', '--default',
        default='{USERNAME}{TAB}{PASSWORD}{ENTER}',
        help='default auto-type sequence used when entry doesn\'t specify '
             'sequence itself.')
    at_sp.add_argument('-D', '--delay', type=int, default=40,
        help='delay beteen simulated keypresses')
    at_sp.add_argument('-f', '--force', action='store_true',
        help='force auto-type for entries for which auto-type was disabled')
    at_sp.set_defaults(func=autotype)

    ######### exit
    exit_sp = add_parser('exit', help='Exit shell.')
    exit_sp.set_defaults(func=exit)

    ######### echo
    echo_sp = add_parser('echo', help='Display a message.')
    echo_sp.add_argument('message', nargs='*', help='message to be displayed')
    echo_sp.set_defaults(func=echo)

    ######### sleep
    sleep_sp = add_parser('sleep', help='Sleep for a given number of seconds.',
        description='Seconds might be a floating number when fractions of '
                    'second are needed.')
    sleep_sp.add_argument('secs', type=float, help='seconds to sleep')
    sleep_sp.set_defaults(func=sleep)

    ######### help
    help_sp = add_parser('help', help='Show help for any message.')
    help_sp.add_argument('command', nargs='?')
    help_sp.set_defaults(func=lambda *a, parsers=parsers: help_(*a, parsers))

    return cp, parsers


def prepare_args():
    ap = argparse.ArgumentParser(description='KeePass database shell access.')
    ap.add_argument('db', nargs='?', help='path to KeePass database.')

    ap.add_argument('--password', default=None,
        help='Database password.')
    ap.add_argument('--pw-cmd', default=None,
        help='Password will be obtained from the output of this command.')
    ap.add_argument('--keyfile', default=None,
        help='Key file for unlocking database.')
    ap.add_argument('--pinentry',
        help='Command used to run pinentry.')
    ap.add_argument('-c', '--command', action='append',
        help='Command to execute. If command contains spaces, it must be '
             'enclosed in double quotes. kpsh will be started in '
             'non-interactive mode.')
    ap.add_argument('--prompt', default='<style fg="ansiblue">{}</style>> ',
        help='Text used by shell for prompt.')
    ap.add_argument('--version', action='version',
                    version='%(prog)s {}'.format(version))
    return ap.parse_args()

def main():
    args = prepare_args()

    kp = DelayedPyKeePass(args)

    cmd_parser, parsers = prepare_command_parser()
    if args.command:
        for command in args.command:
            command = shlex.split(command)
            cargs = cmd_parser.parse_args(command)
            cargs.func(kp, cargs)
    else:
        run_shell(kp, args.prompt, cmd_parser, parsers)
