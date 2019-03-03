import sys
import logging
import logging.config
from app.controller.USManager import MainApplication
from PyQt5.QtWidgets import QApplication

logging.config.fileConfig('logging.conf')
logger = logging.getLogger('simpleExample')

if __name__ == '__main__':
    #logger.basicConfig(filename = 'myLog.log', level = logging.DEBUG, format = '%(asctime)s %(message)s')
    logger.info("In run.py")
    app = QApplication(sys.argv)
    ex = MainApplication()
    sys.exit(app.exec_())
