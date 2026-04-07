import os
from PyQt5.QtWidgets import QFileDialog, QMessageBox
from PyQt5.QtCore import QObject, pyqtSignal


class FileManager(QObject):
    file_opened = pyqtSignal(str)
    file_saved = pyqtSignal(str)

    def __init__(self, editor_widget):
        super().__init__()
        self.editor = editor_widget.get_editor()
        self.current_file = None

    def new_file(self):
        self.editor.clear_all()
        self.current_file = None
        return True

    def open_file(self, parent_widget):
        path, _ = QFileDialog.getOpenFileName(
            parent_widget,
            "Open File",
            "",
            "Code files (*.vexo *.py *.txt);;All files (*.*)"
        )

        if path:
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    self.editor.set_text(f.read())
                    self.current_file = path
                    self.file_opened.emit(path)
                    return True
            except Exception as e:
                QMessageBox.critical(parent_widget, "Error", f"Failed to open file:\n{str(e)}")
                return False
        return False

    def save_file(self, parent_widget):
        if self.current_file:
            try:
                with open(self.current_file, 'w', encoding='utf-8') as f:
                    f.write(self.editor.get_text())
                self.file_saved.emit(self.current_file)
                return True
            except Exception as e:
                QMessageBox.critical(parent_widget, "Error", f"Failed to save file:\n{str(e)}")
                return False
        else:
            return self.save_file_as(parent_widget)

    def save_file_as(self, parent_widget):
        path, _ = QFileDialog.getSaveFileName(
            parent_widget,
            "Save File",
            "",
            "Code files (*.vexo);;Python files (*.py);;Text files (*.txt);;All files (*.*)"
        )

        if path:
            self.current_file = path
            return self.save_file(parent_widget)
        return False

    def get_current_file(self):
        return self.current_file

    def get_file_name(self):
        if self.current_file:
            return os.path.basename(self.current_file)
        return "New file"