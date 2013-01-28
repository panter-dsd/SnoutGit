# -*- coding: utf-8 -*-
__author__ = 'panter.dsd@gmail.com'

import subprocess
import re
import commit

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
        except subprocess.CalledProcessError as error:
            print(self.git_path, command, error)
            return []

        output = []
        for line in process.stdout:
            line = line.rstrip()
            if len(line) > 0:
                try:
                    output.append(line.decode())
                except UnicodeDecodeError:
                    output.append(line.decode("CP1251"))

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


    def stage_files(self, files):
        command = ["add"] + files
        self.execute_command(command)

    def unstage_files(self, files):
        command = ["reset"] + files
        self.execute_command(command)

    def current_branch(self):
        command = ["branch"]
        for branch in self.execute_command(command, True):
            if branch.startswith('* '):
                return branch[2:]
        return "Unknow"

    def local_branches(self):
        command = ["branch"]

        result = []

        branch_re = re.compile(r"^[\*, ]? ([\w,/]*)$")
        for line in self.execute_command(command, True):
            match = branch_re.match(line)
            if match:
                result.append(match.group(1))

        return result

    def remote_branches(self):
        command = ["branch", "-r"]

        result = []

        branch_re = re.compile(r"^  (\w*)/([\w,/]*)$")
        for line in self.execute_command(command, True):
            match = branch_re.match(line)
            if match:
                result.append(match.group(1) + "/" + match.group(2))

        return result

    def tag_info(self, tag):
        command = ["show", "-s", "--pretty=%b", tag]
        result = self.execute_command(command, False)
        for line in result:
            if len(line.strip()) == 0:
                result.remove(line)
        return result

    def commites(self):
        result = []
        for line in self.execute_command(["log", "--pretty=%H"], False):
            result.append(commit.Commit(line))
        return result

    def revert_files(self, files):
        command = ["checkout", "--"] + files
        self.execute_command(command, True)

    def checkout(self, branch_name):
        command = ["checkout", branch_name]
        self.execute_command(command, True)

    def create_branch(self, branch_name, parent_branch):
        command = ["branch", branch_name, parent_branch]
        self.execute_command(command, True)

    def stashes(self):
        command = ["stash", "list"]
        result = []
        for line in self.execute_command(command, True):
            result.append(line)

        return result

    def save_stash(self):
        command = ["stash", "save"]
        self.execute_command(command, True)

    def pop_stash(self):
        command = ["stash", "pop"]
        self.execute_command(command, True)