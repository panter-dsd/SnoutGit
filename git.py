# -*- coding: utf-8 -*-
__author__ = 'panter.dsd@gmail.com'


import subprocess

class Git(object):
    git_path = "git"

    def __init__(self):
        pass

    def execute_command(self, command):
        if type(command) != type([]):
            command = command.split()
        try:
            process = subprocess.Popen([self.git_path] + command,
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

        print(command)
        print(output)
        print(error)

        del process
        return output

    def push(self):
        self.execute_command("push")

    def pull(self):
        self.execute_command("pull")

    def svn_rebase(self):
        self.execute_command("svn_rebase")

    def svn_dcommit(self):
        self.execute_command("svn dcommit")

    def commit(self, name, description):
        command = ["commit", "-m", "{0}".format(name + "\n" + description)]
        self.execute_command(command)

        return True
