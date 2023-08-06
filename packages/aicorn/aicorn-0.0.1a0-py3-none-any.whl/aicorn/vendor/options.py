#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# @DATE     : 2019-09-22 10:29
# @AUTHOR   : 程巍巍 <aicorn@aicorn.cn>
#
#
#            DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE
#                    Version 2, December 2004
#
# Copyright (C) 2004 Sam Hocevar <sam@hocevar.net>
#
# Everyone is permitted to copy and distribute verbatim or modified
# copies of this license document, and changing it is allowed as long
# as the name is changed.
#
#            DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE
#   TERMS AND CONDITIONS FOR COPYING, DISTRIBUTION AND MODIFICATION
#
#  0. You just DO WHAT THE FUCK YOU WANT TO.

from argparse import ArgumentParser
from functools import partial, update_wrapper
from inspect import isawaitable
import asyncio


class Callable:
    def __init__(self, func):
        update_wrapper(self, func)
        self.options = []
        self.parser = None
        self.subparsers = None

        async def impl(*args, **kwargs):
            result = func(*args, **kwargs)
            if isawaitable(result):
                await result

        self.func = impl

    def __call__(self):
        options = self.parser.parse_args()
        func = options.func
        asyncio.run(func(options))

    def add_option(self, *args, **kwargs):
        self.options.append((args, kwargs))
        if self.parser is not None:
            self.parser.add_argument(*args, **kwargs)

    def subcommand(self, func=None, **kwargs):
        """kwargs with save keyword argument for subparsers.add_parser
        """
        if func is None:
            return partial(self.subcommand, **kwargs)

        if 'prog' not in kwargs:
            kwargs['prog'] = func.__name__

        if not isinstance(func, (Callable,)):
            func = Callable(func)

        if self.subparsers is None:
            self.subparsers = self.parser.add_subparsers(title='commands')

        func.parser = self.subparsers.add_parser(kwargs['prog'], **kwargs)
        func.parser.set_defaults(func=partial(func.func, func.parser))
        for args, kwargs in func.options:
            func.parser.add_argument(*args, **kwargs)

        return func


def command(func=None, **kwargs):
    """kwargs with same keyword arguments for ArgumentParser
    usage:
        @command
        def main(cmder, options: Namespace):
            pass
        @command(prog='matata')
        def main(cmder, options: Namespace):
            pass
    """
    if func is None:
        return partial(command, **kwargs)

    if 'prog' not in kwargs:
        kwargs['prog'] = func.__name__

    if not isinstance(func, (Callable,)):
        func = Callable(func)

    func.parser = ArgumentParser(**kwargs)
    func.parser.set_defaults(func=partial(func.func, func.parser))
    for args, kwargs in func.options:
        func.parser.add_argument(*args, **kwargs)

    return func


def option(*args, **kwargs):
    """same arguments for ArgumentParser
    """
    def wrapper(func):
        if not isinstance(func, (Callable,)):
            func = Callable(func)
        func.add_option(*args, **kwargs)
        return func

    return wrapper
