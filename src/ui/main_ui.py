import os, sys
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton,
    QFrame, QHBoxLayout, QTextEdit, QFileDialog, QMessageBox
)

from core.limpiador import clean_flow_zip



class FlowCleanWindow(QWidget):
    ##icono de la app
    
    def __init__(self):
        super().__init__()
        self.setWindowIcon(QIcon(self.resource_path("assets/flowclean_icon.png")))
        self.setWindowTitle("Flow Clean v1.0")
        self.setMinimumSize(950, 600)
        self.selected_zip_path = ""
        self.cleaned_zip_path = ""
        self.build_ui()
        self.bind_events()

    def build_ui(self):
        self.setStyleSheet("""
            QWidget {
                background-color: #0a0f14;
                color: #d7ffe8;
                font-family: "Cascadia Code", "Consolas", monospace;
                font-size: 14px;
            }

            QLabel#titleLabel {
                color: #7fffd4;
                font-size: 30px;
                font-weight: bold;
                padding: 8px;
            }

            QLabel#subTitleLabel {
                color: #8be9fd;
                font-size: 13px;
                padding-bottom: 8px;
            }

            QFrame#mainPanel {
                background-color: #101820;
                border: 2px solid #00f5d4;
                border-radius: 12px;
            }

            QLabel#sectionLabel {
                color: #39ff14;
                font-size: 16px;
                font-weight: bold;
                padding: 6px 0;
            }

            QTextEdit#terminalBox {
                background-color: #05070a;
                border: 1px solid #39ff14;
                border-radius: 8px;
                padding: 10px;
                color: #39ff14;
            }

            QPushButton {
                background-color: #111111;
                color: #00ffd5;
                border: 2px solid #00ffd5;
                border-radius: 10px;
                padding: 12px 18px;
                font-weight: bold;
            }

            QPushButton:hover {
                background-color: #00ffd5;
                color: #061014;
            }

            QPushButton:pressed {
                background-color: #00c9aa;
                color: #061014;
            }
        """)

        root = QVBoxLayout()
        root.setContentsMargins(24, 24, 24, 24)
        root.setSpacing(16)

        self.lbl_title = QLabel("FLOW CLEAN")
        self.lbl_title.setObjectName("titleLabel")
        self.lbl_title.setAlignment(Qt.AlignCenter)

        self.lbl_subtitle = QLabel("Limpiador de referencias de flujos | Power Automate")
        self.lbl_subtitle.setObjectName("subTitleLabel")
        self.lbl_subtitle.setAlignment(Qt.AlignCenter)

        self.main_panel = QFrame()
        self.main_panel.setObjectName("mainPanel")

        panel_layout = QVBoxLayout(self.main_panel)
        panel_layout.setContentsMargins(20, 20, 20, 20)
        panel_layout.setSpacing(14)

        self.lbl_section = QLabel(">> PANEL PRINCIPAL")
        self.lbl_section.setObjectName("sectionLabel")

        self.txt_terminal = QTextEdit()
        self.txt_terminal.setObjectName("terminalBox")
        self.txt_terminal.setReadOnly(True)
        self.txt_terminal.setPlainText(
            "[STATUS] Flow Clean inicializado...\n"
            "[INFO] Cargando poderes....\n"
            "[INFO] Listo!.\n"
            "[INFO] Esperando archivo ZIP legacy."
        )

        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(12)

        self.btn_load = QPushButton("CARGAR ZIP")
        self.btn_clean = QPushButton("LIMPIAR FLOW")
        self.btn_export = QPushButton("EXPORTAR")

        buttons_layout.addWidget(self.btn_load)
        buttons_layout.addWidget(self.btn_clean)
        buttons_layout.addWidget(self.btn_export)

        panel_layout.addWidget(self.lbl_section)
        panel_layout.addWidget(self.txt_terminal)
        panel_layout.addLayout(buttons_layout)

        root.addWidget(self.lbl_title)
        root.addWidget(self.lbl_subtitle)
        root.addWidget(self.main_panel)

        self.setLayout(root)

    def bind_events(self):
        self.btn_load.clicked.connect(self.load_zip)
        self.btn_clean.clicked.connect(self.clean_zip)
        self.btn_export.clicked.connect(self.show_export_path)

    def log(self, message: str):
        self.txt_terminal.append(message)

    def load_zip(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Seleccionar paquete ZIP de Power Automate",
            "",
            "Archivos ZIP (*.zip)"
        )

        if not file_path:
            self.log("[WARN] Selección cancelada por el usuario.")
            return

        if self.selected_zip_path:
            respuesta = QMessageBox.question(
                self,
                "Reemplazar ZIP",
                (
                    "Ya hay un archivo ZIP cargado.\n\n"
                    f"Actual:\n{self.selected_zip_path}\n\n"
                    f"Nuevo:\n{file_path}\n\n"
                    "¿Deseas reemplazar el ZIP actual?"
                ),
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No
            )

            if respuesta == QMessageBox.No:
                self.log("[INFO] Se mantuvo el ZIP actual. No fue reemplazado.")
                return

            self.log(f"[WARN] ZIP reemplazado: {self.selected_zip_path}")

        self.selected_zip_path = file_path
        self.cleaned_zip_path = ""
        self.log(f"[OK] ZIP cargado: {file_path}")

    def clean_zip(self):
        if not self.selected_zip_path:
            QMessageBox.warning(self, "Flow Clean", "Primero selecciona un archivo ZIP.")
            self.log("[ERROR] No hay ZIP seleccionado.")
            return

        try:
            self.log("[INFO] Iniciando limpieza del paquete...")
            result = clean_flow_zip(self.selected_zip_path)

            if result.get("success"):
                self.cleaned_zip_path = result["output_zip"]
                self.log("[OK] Limpieza completada.")
                self.log(f"[OK] Archivo generado: {self.cleaned_zip_path}")

                for change in result.get("changes", []):
                    self.log(f"[CHG] {change}")

                QMessageBox.information(
                    self,
                    "Flow Clean",
                    "Limpieza completada correctamente."
                )
            else:
                self.log("[ERROR] La limpieza no devolvió éxito.")
                QMessageBox.critical(
                    self,
                    "Flow Clean",
                    "Ocurrió un problema durante la limpieza."
                )

        except Exception as e:
            self.log(f"[ERROR] {str(e)}")
            QMessageBox.critical(
                self,
                "Flow Clean",
                f"Error durante la limpieza:\n{str(e)}"
            )

    def show_export_path(self):
        if not self.cleaned_zip_path:
            self.log("[WARN] Aún no existe archivo exportado.")
            QMessageBox.information(
                self,
                "Flow Clean",
                "Todavía no has generado un ZIP limpio."
            )
            return

        self.log(f"[INFO] ZIP limpio disponible en: {self.cleaned_zip_path}")
        QMessageBox.information(
            self,
            "Flow Clean",
            f"Archivo generado en:\n{self.cleaned_zip_path}"
            )
    def resource_path(self, relative_path):
        try:
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(
                os.path.join(os.path.dirname(__file__), "..", "..")
            )
        return os.path.join(base_path, relative_path)