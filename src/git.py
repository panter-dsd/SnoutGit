# -*- coding: utf-8 -*-
__author__ = 'panter.dsd@gmail.com'

import subprocess
import re
import tempfile
import fileinput

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


class PushOptions():
    branch = str()
    remote = str()
    force = False
    include_tags = True

    def __init__(self, branch, remote):
        self.branch = branch
        self.remote = remote


class PullOptions():
    remote = str()
    force = False
    no_tags = False
    prune = True

    def __init__(self, remote):
        self.remote = remote


class Remote(object):
    def __init__(self, git):
        super(Remote, self).__init__()

        self._git = git

    def remotes_list(self):
        command = ["remote"]
        return self._git.execute_command(command, True)

    def add_remote(self, name, url):
        command = ["remote", "add", name, url]
        self._git.execute_command(command, True)

    def remove_remote(self, name):
        command = ["remote", "rm", name]
        self._git.execute_command(command, True)

    def rename_remote(self, name, new_name):
        command = ["remote", "rename", name, new_name]
        self._git.execute_command(command, True)


class Git(object):
    git_path = "git"
    repo_path = str()
    log_view = None
    _last_output = []
    _last_error = []

    def __init__(self):
        pass

    def execute_command(self, command, show_log=True):
        self._last_output = []
        self._last_error = []

        if not isinstance(command, list):
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
            if line:
                try:
                    self._last_output.append(line.decode())
                except UnicodeDecodeError:
                    self._last_output.append(line.decode("CP1251"))

        for line in process.stderr:
            line = line.rstrip()
            if line:
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

    def push(self, push_options):
        command = ["push", "--porcelain"]
        if push_options.force:
            command.append("-f")
        if push_options.include_tags:
            command.append("--tags")
        if push_options.remote:
            command.append("-u")
            command.append(push_options.remote)

        command.append(push_options.branch)
        self.execute_command(command, True)

    def pull(self, pull_options):
        command = ["pull"]
        if pull_options.force:
            command.append("-f")
        if pull_options.no_tags:
            command.append("--no-tags")
        if pull_options.prune:
            command.append("--prune")

        command.append(pull_options.remote)
        self.execute_command(command, True)


    def svn_rebase(self):
        self.execute_command("svn rebase")

    def svn_dcommit(self):
        self.execute_command("svn dcommit")

    def commit(self, name, description=str()):
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
            result.append(commit.Commit(self, line))
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

    def apply_stash(self, stash_name):
        command = ["stash", "apply", stash_name]
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

    def _merged_or_no_merged(self, branch, merged=True):
        command = ["branch",
                   "--all",
                   merged and "--merged" or "--no-merged",
                   branch]

        branch_re = re.compile(r"^[\*, ]? (\S*)$")

        result = []

        for line in self.execute_command(command, True):
            match = branch_re.match(line)
            if match:
                result.append(match.group(1).replace("remotes/", str()))

        return result

    def merged(self, branch):
        return self._merged_or_no_merged(branch, True)

    def no_merged(self, branch):
        return self._merged_or_no_merged(branch, False)

    def delete_branch(self, branch, force=False):
        command = ["branch",
                   force and "-D" or "-d",
                   branch]

        self.execute_command(command, True)

    def last_output(self):
        return self._last_output

    def last_error(self):
        return self._last_error

    def remote_list(self):
        command = ["remote"]
        return self.execute_command(command, True)

    def create_tag(self, commit, name, message=None):
        command = ["tag"]

        message_file = None
        if message:
            message_file = tempfile.NamedTemporaryFile()
            message_file.write(message.encode("utf-8"))
            message_file.flush()
            command += ["-F", message_file.name]

        command.append(name)
        command.append(commit)

        self.execute_command(command, True)
        if message_file:
            message_file.close()

    def commit_message(self):
        result = str()

        try:
            with fileinput.input(self.repo_path + "/MERGE_MSG") as f:
                for line in f:
                    result += line
        except IOError:
            pass

        return result
