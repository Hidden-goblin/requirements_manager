# A simple setup script to create an executable using PyQt5. This also
# demonstrates the method for creating a Windows executable that does not have
# an associated console.
import sys
from cx_Freeze import setup, Executable

application_title = "Feature Manager" #what you want to application to be called

main_python_file = "run.py" #the name of the python file you use to run the program


base = None
if sys.platform == "win32":
    base = "Win32GUI"

includes = ["atexit", "re"]
includes_files = []

setup(
        name = application_title,
        version = "0.2",
        description = "Freeze Feature Manager",
        options = {"build_exe": {"includes": includes, "include_files": includes_files},
                   "bdist_msi": {"upgrade_code": "{d7a45f7d-f499-45a6-9cc9-bd90aca124cf}"}},
        executables = [Executable(main_python_file, base = base, shortcutName = 'Feature Manager', shortcutDir = "ProgramMenuFolder")],
        install_requires = [
                "PyQt5==5.9",
                "tinydb==3.6.0"
            ],
        python_requires = "~=3.5.3",
        packages=["app",
                  "app.controller",
                  "app.ui",
                  "app.static",
                  "app.data",
                  "app.exceptions"],
        author = "Eric Aïvayan",
        author_email = "e.aivayan@neopost.com"
    )
