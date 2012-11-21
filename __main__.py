import setuptools.command

__author__ = 'panter'

import os
import subprocess

PATH = "/media/work/other/phradar"

def get_commites_list():
    os.chdir(PATH)
    result = []
    command = "git log --pretty=format:%H"
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)

    for line in process.stdout.readlines():
        result.append(line.strip().decode("utf-8"))
    return result

def get_commit_info(commit_id):
    os.chdir(PATH)
    result = []
    command = "git show -s --pretty=\"%s\" " + commit_id
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)

    for line in process.stdout.readlines():
        try:
            result.append(line.strip().decode("utf-8"))
        except:
            print(line)
    return result


COMMITS = get_commites_list()
for commit in COMMITS:
    print(commit, get_commit_info(commit))
