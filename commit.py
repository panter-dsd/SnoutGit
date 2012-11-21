__author__ = 'panter'

import os
import subprocess

class Commit(object):
    def __init__(self, path, id):
        super(Commit, self).__init__()
        self._path = path
        self._id = id
        self.name_ = str()
        self.author_ = str()

    def _commit_info(self, format_id):
        os.chdir(self._path)
        command = "git show -s --pretty=\"" + format_id + "\" " + self._id
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)

        return process.stdout.readline().strip().decode("utf-8")

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
