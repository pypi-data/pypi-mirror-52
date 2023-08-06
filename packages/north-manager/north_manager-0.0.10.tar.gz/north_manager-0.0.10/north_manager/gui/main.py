import sys
import os
import logging
from os import path
from PyQt5.uic import loadUi
from PyQt5.QtCore import QUrl, Qt, QSize, QTimer
from PyQt5.QtQuick import QQuickView
from PyQt5.QtWidgets import QApplication, QDialog
from north_manager.gui.models import get_state

logger = logging.getLogger(__name__)

os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
BASE_PATH = path.dirname(path.realpath(__file__))


def start():
    app = QApplication(sys.argv + ['--style', 'fusion'])
    app.setAttribute(Qt.AA_EnableHighDpiScaling)

    state = get_state()

    main_window = QQuickView()
    main_window.setTitle('North Robotics Firmware Utility')
    main_window.setMinimumSize(QSize(300, 175))
    main_window.setMaximumSize(QSize(200, 175))
    main_window.setFlags(Qt.Dialog)

    context = main_window.rootContext()
    context.setContextProperty('app', state)

    main_window.setSource(QUrl.fromLocalFile(path.join(BASE_PATH, 'mainWindow.qml')))

    if len(main_window.errors()) > 0:
        for err in main_window.errors():
            logger.error(err.toString())

        sys.exit(1)

    main_window.show()

    init_timer = QTimer(main_window)
    init_timer.setSingleShot(True)
    init_timer.timeout.connect(state.onReady)
    init_timer.start(0)

    sys.exit(app.exec_())


if __name__ == '__main__':
    start()
