# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2019 Michał Góral.

import sys
import os
import subprocess
import time
import fnmatch

from kpd.utils import eprint

class CommandError(Exception):
    pass

def tokenize(seq):
    tokens = []

    i = 0
    while i < len(seq):
        start = seq.find('{', i)

        if start != -1:
            if i < start:
                tokens.append(seq[i:start])

            end = seq.find('}', start)
            nend = end + 1

            if end == -1:
                end = len(seq) - 1
            elif end == start + 1 and len(seq) > nend and seq[nend] == '}':  # {}}
                end = nend

            tokens.append(seq[start:end + 1])
            i = end + 1
        else:
            tokens.append(seq[i:])
            i = len(seq)

    return tokens


def xdotool(*args):
    cmd = ['/usr/bin/xdotool']
    cmd.extend(args)
    subprocess.run(cmd)


def autotype(kp, args):
    from kpd.autotype.xdotoolkeys import XDOTOOL_KEYS
    from kpd.autotype.placeholders import replace_placeholder
    from kpd.autotype.commands import run_command

    delay = str(args.delay)
    entry = _get(args.path, kp)

    if not entry.autotype_enabled and not args.force:
        eprint('Autotype disabled for {}. '
               'Use -f to force autotype.'.format(args.path))
        return

    sequence = args.sequence if args.sequence else entry.autotype_sequence
    if not sequence:
        sequence = args.default

    for token in tokenize(sequence):
        if token.startswith('{') and token.endswith('}'):
            if run_command(token):
                continue

            placeholder = replace_placeholder(entry, token)
            if placeholder is not None:
                xdotool('type', '--delay', delay, placeholder)
                continue

            specialkey = XDOTOOL_KEYS.get(token)
            if specialkey is not None:
                xdotool('key', '--clearmodifiers', '--delay', delay, specialkey)
                continue

            eprint('Unsupported keyword: {}'.format(token))
        else:
            xdotool('type', '--delay', delay, token)


def show(kp, args):
    entry = _get(args.path, kp)
    attrs = ['path', 'username', 'password', 'url', 'autotype_sequence',
              'notes']

    for attr in attrs:
        if args.fields and attr not in args.fields:
            continue
        val = getattr(entry, attr)
        if val is None:
            continue

        if args.no_field_name:
            print(val)
        else:
            print('{}: {}'.format(attr, val))


def echo(kp, args):
    print(*args.message)


def sleep(kp, args):
    time.sleep(args.secs)


def ls(kp, args):
    for path in fnmatch.filter(kp.iter_paths(), args.glob):
        print(path)


def help_(kp, args, parsers):
    parser = parsers.get(args.command)
    if parser is None:
        eprint('no such command: {}'.format(args.command))
        parser = parsers.get(None)

    parser.print_help()


def exit(*args):
    return False


def open_(kp, args):
    fp = os.path.expanduser(args.filepath)
    kp.change_db(fp)


def unlock(kp, args):
    if not kp.locked:
        return

    kf = os.path.expanduser(args.keyfile) if args.keyfile else None
    kp.change_credentials(keyfile=kf)
    kp.unlock()


def lock(kp, args):
    kp.lock()


def _get(path, kp):
    entry = kp.entries.get(path)
    if not entry:
        raise CommandError('entry not found: {}'.format(path))
    return entry
