#!/usr/bin/env python
# -*- coding: utf-8 -*-

from os.path import isfile
from json import dump, load


class JsonManager:

    def create_json(self, filepath, dirdata, *args):

        from os import mkdir

        try:
            mkdir(dirdata)
        except OSError:
            pass

        data = {"username": "", "password": ""}

        if args:
            data = {"username": f"{args[0]}", "password": f"{args[1]}"}

        with open(filepath, 'w') as f:
            dump(data, f, indent=2, separators=(',', ': '))

    def read_json(self, filepath):
        if isfile(filepath):
            with open(filepath) as f:
                data = load(f)
            return data
        else:
            return False

    def update_json(self, filepath, data):
        with open(filepath, 'w') as f:
            dump(data, f, indent=2, separators=(',', ': '))
