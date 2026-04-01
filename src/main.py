import sys, os
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QIcon
from ui.main_ui import FlowCleanWindow


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    return os.path.join(base_path, relative_path)

def main():
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon(resource_path("assets/flowclean_icon.png")))

    window = FlowCleanWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()