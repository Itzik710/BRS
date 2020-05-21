import sys
from cx_Freeze import setup, Executable

base = None

# Necessary for 32-bit systems
if sys.platform == "win32":
    base = "Win32GUI"

executables = [Executable("main.py", base=base, targetName="ReportCards.exe")]

# Any packages that need to be added for compilation.
# Some may work but if not include them here
packages = ["numpy"]

options = {
    'build_exe': {
        'packages': packages,
    },
}

setup(
    # EXE NAME HERE
    name="Report Cards",
    options=options,
    version="VERSION_NUMBER e.g. 0.1",
    description='report card generator',
    executables=executables
)