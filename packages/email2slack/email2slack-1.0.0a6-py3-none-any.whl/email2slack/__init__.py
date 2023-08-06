#!/usr/bin/env python
from __future__ import unicode_literals

import argparse
import sys

from .parser import EmailParser
from .slack import Slack


def get_arg_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-d', '--debug', action='store_true',
        help='dry run, does not post to slack.'
    )
    parser.add_argument(
        '-f', '--config',
        help='email2slack config file'
    )
    parser.add_argument(
        '-s', '--slack', help='override default Slack incoming hook endpoint'
    )
    parser.add_argument(
        '-t', '--team', help='override default Slack steam'
    )
    parser.add_argument(
        '-c', '--channel',
        help='override default Slack channel'
    )
    return parser


def main():
    args = get_arg_parser().parse_args()
    try:
        fp = sys.stdin.buffer
    except AttributeError:
        fp = sys.stdin
    mail = EmailParser.parse(fp)
    Slack(args).notify(mail)


if __name__ == '__main__':
    main()

__all__ = ['EmailParser', 'Slack', 'main']
