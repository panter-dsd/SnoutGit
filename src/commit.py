# -*- coding: utf-8 -*-
__author__ = 'panter.dsd@gmail.com'

DEFAULT_ABBREV = 7


class RefNames():
    _locals = []
    _remotes = []
    _tags = []

    def __init__(self):
        self._locals = []
        self._remotes = []
        self._tags = []

    def locals(self):
        return self._locals

    def remotes(self):
        return self._remotes

    def tags(self):
        return self._tags

    def add_ref(self, ref):
        locals_start = "refs/heads/"
        remotes_start = "refs/remotes/"
        tags_start = "refs/tags/"

        if ref.startswith(locals_start):
            self._locals.append(ref.replace(locals_start, str()))
        elif ref.startswith(remotes_start):
            self._remotes.append(ref.replace(remotes_start, str()))
        elif ref.startswith(tags_start):
            self._tags.append(ref.replace(tags_start, str()))


class Commit(object):
    _git = None
    _id = None
    _name = str()
    _author = str()
    _timestamp = str()

    def __init__(self, git, id):
        super(Commit, self).__init__()

        self._git = git
        self._id = id

    def _commit_info(self, format_id):
        command = ["show",
                   "-s",
                   "--decorate=full",
                   "--pretty=" + format_id, self._id]
        return self._git.execute_command(command, False)

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
        return len(name) == 0 and str() or name[0]

    def author(self):
        if len(self._author) == 0:
            self._author = self._commit_info("%ae")[0]
        return self._author

    def timestamp(self):
        if len(self._timestamp) == 0:
            self._timestamp = self._commit_info("%at")[0]
        return self._timestamp

    def diff(self, lines_count=3):
        command = ["show",
                   "--pretty=fuller",
                   "--unified={0}".format(lines_count),
                   self._id]

        return "\n".join(self._git.execute_command(command, False))

    def changed_files(self):
        command = ["show",
                   "--pretty=format:",
                   "--name-only",
                   self._id]

        return self._git.execute_command(command, False)

    def ref_names(self):
        text = self._commit_info("%d")

        result = RefNames()

        if len(text) > 0:
            for name in text[0][2:-1].split(", "):
                result.add_ref(name)

        return result
