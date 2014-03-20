import sys

from cx_Freeze import setup, Executable

PROJECT_NAME = "SnoutGit"
BASE = None

if sys.platform == "win32":
    BASE = "Win32GUI"

MODULES = [
    "src.main_window"
]

PYQT4_MODULES = [
    "sip",
    "PyQt4.QtCore",
    "PyQt4.uic",
    "PyQt4.QtGui",
]

build_exe = {
    "includes": ["atexit", "re"] + PYQT4_MODULES + MODULES,
    #"icon": "../../share/images/main.ico",
}

setup(
    name=PROJECT_NAME,
    version="0.0.0.0",
    packages=['src'],
    url='https://github.com/panter-dsd/SnoutGit',
    license='GPLv3',
    author='PanteR',
    author_email='panter.dsd@gmail.com',
    description='Git gui client.',

    options={
        "build_exe": build_exe
    },

    executables=[
        Executable("src/__main__.py", base=BASE, targetName=PROJECT_NAME + ".exe")
    ]
)
