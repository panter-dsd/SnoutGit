# -*- coding: utf-8 -*-
__author__ = 'panter.dsd@gmail.com'

import git


DEFAULT_ABBREV = 7


class Commit(object):
    def __init__(self, id):
        super(Commit, self).__init__()

        self._id = id
        self._name = str()
        self._author = str()
        self._timestamp = str()

    def _commit_info(self, format_id):
        command = "show -s --pretty=" + format_id + " " + self._id
        return git.Git().execute_command(command, False)

    def id(self):
        return self._id

    def abbreviated_id(self):
        return self._id[:DEFAULT_ABBREV]

    def full_name(self):
        if len(self._name) == 0:
            self._name = "\n".join(self._commit_info("%B")).rstrip()

        return self._name

    def name(self):
        name = self.full_name().splitlines()
        if len(name) == 0:
            return str()
        else:
            return name[0]

    def author(self):
        if len(self._author) == 0:
            self._author = self._commit_info("%ae")[0]
        return self._author

    def timestamp(self):
        if len(self._timestamp) == 0:
            self._timestamp = self._commit_info("%aD")[0]
        return self._timestamp

    def diff(self, lines_count=3):
        cmd_template = "show --pretty=fuller --unified={0} {1}"
        command = cmd_template.format(lines_count, self._id)

        return "\n".join(git.Git().execute_command(command, False))

    def changed_files(self):
        cmd_template = "show --pretty=format: --name-only {0}"
        command = cmd_template.format(self._id)

        return git.Git().execute_command(command, False)
