# A simple setup script to create an executable using PyQt5. This also
# demonstrates the method for creating a Windows executable that does not have
# an associated console.
import sys
from setuptools import setup

application_title = "Feature Manager"  #what you want to application to be called
main_python_file = "run.py"  #the name of the python file you use to run the program


base = None
if sys.platform == "win32":
    base = "Win32GUI"

includes = ["atexit", "re"]
includes_files = []

setup(
    name = application_title,
    version = "0.2",
    description = "Freeze Feature Manager",
    classifiers = [  # Optional
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        #'Topic :: Software Development :: Build Tools',

        # Pick your license as you wish
        #'License :: OSI Approved :: MIT License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 3.5',
        ],
    install_requires = [
        "pyqt5~=5.9",
        "tinydb==3.6.0",
        "python-docx==0.8.6",
        "lxml~=4.2.5",
        "openpyxl==2.4.8",
        "XlsxWriter==1.0.0",
        "jdcal==1.3", 'requests', 'markdown'
        ],
    packages = ["app",
                "app.controller",
                "app.ui",
                "app.static",
                "app.data",
                "app.exceptions"],
    author = "Eric Aïvayan",
    author_email = "e.aivayan@neopost.com"
    )
