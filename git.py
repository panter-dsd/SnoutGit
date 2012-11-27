# -*- coding: utf-8 -*-
__author__ = 'panter.dsd@gmail.com'


import subprocess

class Git(object):
    git_path = "git"

    def __init__(self):
        pass

    def execute_command(self, command):
        try:
            process = subprocess.Popen([self.git_path, command],
                                       shell=False,
                                       stdout=subprocess.PIPE,
                                       stderr=subprocess.PIPE)
        except:
            print(self.git_path, command, "error")
            return []

        output = []
        for line in process.stdout:
            line = line.rstrip()
            if len(line) > 0:
                output.append(line.decode())

        error = []
        for line in process.stderr:
            line = line.rstrip()
            if len(line) > 0:
                error.append(line.decode())

        print(error)

        del process
        return output
