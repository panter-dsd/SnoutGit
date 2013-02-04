# -*- coding: utf-8 -*-
__author__ = 'panter.dsd@gmail.com'

import subprocess
import re
import commit


class Stash():
    name = str()
    description = str()

    def __init__(self, name, description):
        self.name = name
        self.description = description


class MergeOptions():
    source_target = str()
    commit = True
    fast_forward = False
    squash = False

    def __init__(self, source_target):
        self.source_target = source_target


class Git(object):
    git_path = "git"
    log_view = None
    _last_output = []
    _last_error = []

    def __init__(self):
        pass

    def execute_command(self, command, show_log=True):
        self._last_output = []
        self._last_error = []

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

        for line in process.stdout:
            line = line.rstrip()
            if len(line) > 0:
                try:
                    self._last_output.append(line.decode())
                except UnicodeDecodeError:
                    self._last_output.append(line.decode("CP1251"))

        for line in process.stderr:
            line = line.rstrip()
            if len(line) > 0:
                self._last_error.append(line.decode())

        if show_log:
            if self.log_view:
                self.log_view.append_command(" ".join(command))
                self.log_view.append_output(
                    "\n".join(self._last_output)
                )
                self.log_view.append_error(
                    "\n".join(self._last_error)
                )
            else:
                print(command)
                print(self._last_output)
                print(self._last_error)

        del process
        return self._last_output

    def push(self):
        command = ["push", "--porcelain"]
        self.execute_command(command, True)

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

        branch_re = re.compile(r"^[\*, ]? (\S*)$")
        for line in self.execute_command(command, True):
            match = branch_re.match(line)
            if match:
                result.append(match.group(1))

        return result

    def remote_branches(self):
        command = ["branch", "-r"]

        result = []

        branch_re = re.compile(r"^  (\w*)/(\S*)$")
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

        stash_re = re.compile(r"(stash@{\d*}): (.*)")

        for line in self.execute_command(command, True):
            match = stash_re.match(line)
            assert match
            result.append(Stash(match.group(1),
                                match.group(2)))

        return result

    def save_stash(self):
        command = ["stash", "save"]
        self.execute_command(command, True)

    def pop_stash(self):
        command = ["stash", "pop"]
        self.execute_command(command, True)

    def drop_stash(self, stash_name):
        command = ["stash", "drop", stash_name]
        self.execute_command(command, True)

    def tags(self):
        command = ["tag"]
        return self.execute_command(command, True)

    def merge(self, merge_options):
        command = [
            "merge",
            ["--no-commit", "--commit"][merge_options.commit],
            ["--no-ff", "--ff"][merge_options.fast_forward],
            ["--no-squash", "--squash"][merge_options.squash],
            merge_options.source_target
        ]
        self.execute_command(command, True)

    def abort_merge(self):
        command = ["merge", "--abort"]
        self.execute_command(command, True)

    def rename_branch(self, old_name, new_name):
        command = ["branch", "-m", old_name, new_name]
        self.execute_command(command, True)

    def merged(self, branch):
        command = ["branch", "--merged", branch]

        branch_re = re.compile(r"^[\*, ]? (\S*)$")

        result = []

        for line in self.execute_command(command, True):
            match = branch_re.match(line)
            if match:
                result.append(match.group(1))

        return result

    def delete_branch(self, branch, force=False):
        command = ["branch",
                   force and "-D" or "-d",
                   branch]

        self.execute_command(command, True)

    def last_output(self):
        return self._last_output

    def last_error(self):
        return self._last_error