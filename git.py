# -*- coding: utf-8 -*-
__author__ = 'panter.dsd@gmail.com'

import subprocess

class Git(object):
    git_path = "git"
    log_view = None

    def __init__(self):
        pass

    def execute_command(self, command, show_log=True):
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

        if show_log:
            if self.log_view:
                self.log_view.append_command(" ".join(command))
                self.log_view.append_output("\n".join(output))
                self.log_view.append_error("\n".join(error))
            else:
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
        self.execute_command("svn rebase")

    def svn_dcommit(self):
        self.execute_command("svn dcommit")

    def commit(self, name, description):
        command = ["commit", "-m", "{0}".format(name + "\n" + description)]
        self.execute_command(command)

        return True

    def get_status(self):
        command = ["status", "-u", "--porcelain"]
        return self.execute_command(command, False)


    def stage(self, file_name):
        command = ["add", "{0}".format(file_name)]
        self.execute_command(command)


    def unstage(self, file_name):
        command = ["reset", "{0}".format(file_name)]
        self.execute_command(command)
