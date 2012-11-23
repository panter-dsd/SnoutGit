# -*- coding: utf-8 -*-
__author__ = 'panter.dsd@gmail.com'

import os
import subprocess

#noinspection PyUnresolvedReferences
class Commit(object):
    def __init__(self, path, id):
        super(Commit, self).__init__()
        self._path = path
        self._id = id
        self._name = str()
        self._author = str()
        self._abbreviated_id = str()

    #noinspection PyUnresolvedReferences
    def _commit_info(self, format_id):
        os.chdir(self._path)
        command = "git show -s --pretty=\"" + format_id + "\" " + self._id
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)

        #noinspection PyUnresolvedReferences
        return process.stdout.readline().decode().rstrip()

    def id(self):
        return self._id

    def abbreviated_id(self):
        if len(self._abbreviated_id) == 0:
            self._abbreviated_id = self._commit_info("%h")
        return self._abbreviated_id

    def name(self):
        if len(self._name) == 0:
            self._name = self._commit_info("%B").splitlines()[0]
        return self._name

    def author(self):
        if len(self._author) == 0:
            self._author = self._commit_info("%ae")
        return self._author

    def diff(self, lines_count = 3):
        os.chdir(self._path)
        command = "git show --pretty=fuller --unified={0} {1}".format(lines_count, self._id)
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)

        result = []
        for line in process.stdout.readlines():
            try:
                result.append(line.decode())
            except:
                result.append(line.decode("CP1251"))
        return "".join(result)

    def changed_files(self):
        os.chdir(self._path)
        command = "git show --pretty=\"format:\" --name-only {0}".format(self._id)
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)

        result = []
        for line in process.stdout.readlines():
            line = line.strip()
            if len(line) > 0:
                result.append(line.decode())
        return result
