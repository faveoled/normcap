"""
 OCR-powered screen-capture tool to capture information instead of images.
"""
import locale

# Workaround for older tesseract version 4.0.0 on e.g. Debian Buster
locale.setlocale(locale.LC_ALL, "C")

import sys

from PySide2 import QtCore, QtWidgets

from normcap import __version__, utils
from normcap.args import create_argparser
from normcap.logger import logger
from normcap.window_main import WindowMain


def main():
    """Main entry point."""
    sys.excepthook = utils.except_hook

    arg_parser = create_argparser()
    args = vars(arg_parser.parse_args())

    if args["verbose"]:
        logger.setLevel("INFO")

    if args["very_verbose"]:
        logger.setLevel("DEBUG")

    if args["language"]:
        args["language"] = tuple(args["language"].split("+"))

    logger.info(f"Starting Normcap v{__version__}")
    logger.debug(f"CLI command: {' '.join(sys.argv)}")

    lib_paths = QtCore.QCoreApplication.libraryPaths()
    logger.debug(f"QT LibraryPaths: {lib_paths}")

    # Start Qt Application
    with utils.temporary_environ(XCURSOR_SIZE=24):
        QtCore.qInstallMessageHandler(utils.qt_message_handler)

        QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
        app = QtWidgets.QApplication(sys.argv)
        app.setQuitOnLastWindowClosed(False)

        # Screen info needs to be gathered _after_ app is instanciated
        system_info = utils.get_system_info()
        logger.debug(f"Detected system info:{system_info}")

        window = WindowMain(system_info, args)
        window.show()

        sys.exit(app.exec_())
