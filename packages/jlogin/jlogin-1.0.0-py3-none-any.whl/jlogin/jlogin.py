#!/usr/bin/env python
# -*- coding: utf-8 -*-

from os.path import dirname, realpath, join
from jlogin.utils.jlib import JsonManager
from getpass import getpass
from crypt import crypt
from hmac import compare_digest as hashEquals
from textwrap import dedent


class JLogin(JsonManager):

    def test(self):
        return 'oi'

    def __init__(self):
        self.root = dirname(realpath(__file__))
        self.path_data = join(self.root, 'data/data.json')

    def sign_in(self):
        # data = JsonManager().read_json(self.path_data)
        print('### Sign In ###')
        username = input('Enter your username: ')
        password = getpass('Enter your password: ')
        password_verify = getpass('Repeat your password: ')

        while password != password_verify:
            print('Password do not match!')
            password_verify = getpass('Repeat your password: ')

        dirdata = join(self.root, 'data')
        JsonManager().create_json(self.path_data, dirdata, username, crypt(password_verify))
        print('Registration done!')

    def home(self, data):

        opc = '0'

        while opc != '2':
            print(dedent("""
            Menu:

            1 - Alterar Login.
            2 - Sair

            Escolha uma opção:
            """))

            opc = input('> ')

            if opc == '1':
                try:
                    self.update_login(data)
                except KeyboardInterrupt:
                    print('\nCancelado')
            elif opc == '2':
                break
            else:
                print('Option invalid!')

    def update_login(self, data):
        print('### Update Login ###')
        username = input('Enter new your username: ')
        password_old = getpass('Enter your old password: ')

        while not hashEquals(data['password'], crypt(password_old, data['password'])):
            print('Old password invalid!')
            password_old = getpass('Enter your old password: ')

        password_new = getpass('Enter your new password: ')
        password_new_repeat = getpass('Repeat new password: ')

        while password_new != password_new_repeat:
            print('New password do not match.')
            password_new_repeat = getpass('Repeat new password: ')

        data['username'] = username
        data['password'] = crypt(password_new_repeat)

        JsonManager().update_json(self.path_data, data)
        print('Update success!')

    def logging_in(self, data):
        print('### Logging In ###')
        username = input('Enter your username: ')

        while username != data['username']:
            print('Username invalid!')
            username = input('Enter your username: ')

        password = getpass('Enter your password: ')

        if not hashEquals(data['password'], crypt(password, data['password'])):
            print('Password invalid!')
        else:
            print('Login success!')
            self.home(data)

    def main(self):
        data = JsonManager().read_json(self.path_data)
        if data:
            try:
                self.logging_in(data)
            except KeyboardInterrupt:
                print('\nCancelado')
        else:
            try:
                self.sign_in()
            except KeyboardInterrupt:
                print('\nCancelado')

    def __str__(self):
        return self.main
