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
        self.name_ = str()
        self.author_ = str()

    #noinspection PyUnresolvedReferences
    def _commit_info(self, format_id):
        os.chdir(self._path)
        command = "git show -s --pretty=\"" + format_id + "\" " + self._id
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)

        #noinspection PyUnresolvedReferences
        return process.stdout.readline().decode().strip()

    def id(self):
        return self._id

    def name(self):
        if len(self.name_) == 0:
            self.name_ = self._commit_info("%s")
        return self.name_

    def author(self):
        if len(self.author_) == 0:
            self.author_ = self._commit_info("%ae")
        return self.author_
