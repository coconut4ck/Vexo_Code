from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QLabel, QStatusBar, QAction, QMessageBox, QInputDialog, \
    QShortcut
from editor_widget import EditorWidget
from file_manager import FileManager


class EditorWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.editor_widget = None
        self.file_manager = None
        self.setup_window()
        self.setup_ui()
        self.setup_menu()
        self.setup_toolbar()
        self.setup_statusbar()
        self.apply_theme()

    def setup_window(self):
        self.setWindowTitle("Vexo Studio")
        self.setGeometry(100, 100, 1200, 700)

    def setup_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.editor_widget = EditorWidget()
        layout.addWidget(self.editor_widget)

        self.file_manager = FileManager(self.editor_widget)
        self.file_manager.file_opened.connect(self.on_file_opened)
        self.file_manager.file_saved.connect(self.on_file_saved)

    def setup_menu(self):
        menubar = self.menuBar()

        file_menu = menubar.addMenu("File")

        new_action = self.create_action("New", "Ctrl+N", self.new_file)
        file_menu.addAction(new_action)

        open_action = self.create_action("Open...", "Ctrl+O", self.open_file)
        file_menu.addAction(open_action)

        file_menu.addSeparator()

        save_action = self.create_action("Save", "Ctrl+S", self.save_file)
        file_menu.addAction(save_action)

        save_as_action = self.create_action("Save As...", "Ctrl+Shift+S", self.save_file_as)
        file_menu.addAction(save_as_action)

        file_menu.addSeparator()

        exit_action = self.create_action("Exit", "Alt+F4", self.close)
        file_menu.addAction(exit_action)

        edit_menu = menubar.addMenu("Edit")

        undo_action = self.create_action("Undo", "Ctrl+Z", self.undo)
        edit_menu.addAction(undo_action)

        redo_action = self.create_action("Redo", "Ctrl+Y", self.redo)
        edit_menu.addAction(redo_action)

        edit_menu.addSeparator()

        cut_action = self.create_action("Cut", "Ctrl+X", self.cut)
        edit_menu.addAction(cut_action)

        copy_action = self.create_action("Copy", "Ctrl+C", self.copy)
        edit_menu.addAction(copy_action)

        paste_action = self.create_action("Paste", "Ctrl+V", self.paste)
        edit_menu.addAction(paste_action)

        edit_menu.addSeparator()

        find_action = self.create_action("Find", "Ctrl+F", self.find_text)
        edit_menu.addAction(find_action)

        help_menu = menubar.addMenu("Help")
        about_action = self.create_action("About", None, self.show_about)
        help_menu.addAction(about_action)


    def setup_toolbar(self):
        toolbar = self.addToolBar("Tools")
        toolbar.setMovable(False)

        actions = [
            ("New", self.new_file),
            ("Open", self.open_file),
            ("Save", self.save_file),
            ("Cut", self.cut),
            ("Copy", self.copy),
            ("Paste", self.paste),
            ("Undo", self.undo),
            ("Redo", self.redo),
            ("Find", self.find_text),
        ]

        for name, func in actions:
            action = self.create_action(name, None, func)
            toolbar.addAction(action)

    def setup_statusbar(self):
        self.status_bar = self.statusBar()
        self.file_label = QLabel("New file")
        self.status_bar.addWidget(self.file_label)

        self.cursor_label = QLabel("Line: 1 | Col: 1")
        self.status_bar.addPermanentWidget(self.cursor_label)

        editor = self.editor_widget.get_editor()
        editor.cursorPositionChanged.connect(self.update_cursor)

    def create_action(self, name, shortcut, callback):
        action = QAction(name, self)
        if shortcut:
            action.setShortcut(shortcut)
        action.triggered.connect(callback)
        return action

    def update_cursor(self):
        editor = self.editor_widget.get_editor()
        cursor = editor.textCursor()
        line = cursor.blockNumber() + 1
        col = cursor.columnNumber() + 1
        self.cursor_label.setText(f"Line: {line} | Col: {col}")

    def on_file_opened(self, path):
        self.file_label.setText(self.file_manager.get_file_name())
        self.setWindowTitle(f"Vexo Studio - {self.file_manager.get_file_name()}")
        self.status_bar.showMessage(f"Opened: {path}", 3000)

    def on_file_saved(self, path):
        self.file_label.setText(self.file_manager.get_file_name())
        self.setWindowTitle(f"Vexo Studio - {self.file_manager.get_file_name()}")
        self.status_bar.showMessage(f"Saved: {path}", 2000)

    def new_file(self):
        self.file_manager.new_file()
        self.file_label.setText("New file")
        self.setWindowTitle("Vexo Studio - New File")

    def open_file(self):
        self.file_manager.open_file(self)

    def save_file(self):
        self.file_manager.save_file(self)

    def save_file_as(self):
        self.file_manager.save_file_as(self)

    def undo(self):
        self.editor_widget.get_editor().undo_action()

    def redo(self):
        self.editor_widget.get_editor().redo_action()

    def cut(self):
        self.editor_widget.get_editor().cut_action()

    def copy(self):
        self.editor_widget.get_editor().copy_action()

    def paste(self):
        self.editor_widget.get_editor().paste_action()

    def find_text(self):
        text, ok = QInputDialog.getText(self, "Find", "Search for:")
        if ok and text:
            editor = self.editor_widget.get_editor()
            if not editor.find_text(text):
                QMessageBox.information(self, "Find", f"Text '{text}' not found")

    def show_about(self):
        QMessageBox.about(self, "About Vexo Studio",
                          """
                          <div style="text-align: center;">
                              <h1 style="color: #569CD6;">Vexo Studio</h1>
                              <p style="color: #888;">version 1.0</p>
              
                              <hr style="width: 50%; margin: 15px auto;">
              
                              <p>Vexo Studio is a development environment<br>
                              for the <b>Vexo</b> programming language.</p>
              
                              <p>Provides convenient work with files<br>
                              and programming language.</p>
              
                              <hr style="width: 50%; margin: 15px auto;">
              
                              <p><i>Developed by the Aurix team in 2026</i></p>
              
                              <p><b style="color: #6A9955;">MIT License</b></p>
                          </div>
                          """)

    def apply_theme(self):
        self.setStyleSheet("""
            QMainWindow { background-color: #1e1e1e; }
            QMenuBar { background-color: #2d2d30; color: #cccccc; border-bottom: 1px solid #3e3e42; }
            QMenuBar::item:selected { background-color: #04395e; }
            QMenu { background-color: #2d2d30; color: #cccccc; border: 1px solid #3e3e42; }
            QMenu::item:selected { background-color: #04395e; }
            QToolBar { background-color: #2d2d30; border: none; spacing: 3px; padding: 2px; }
            QToolButton { background-color: transparent; color: #cccccc; border: none; padding: 5px; }
            QToolButton:hover { background-color: #3e3e42; border-radius: 3px; }
            QStatusBar { background-color: #2d2d30; color: #cccccc; border-top: 1px solid #3e3e42; }
            QDialog { background-color: #2d2d30; color: #cccccc; }
            QDialog QLabel { color: #cccccc; }
            QDialog QLineEdit { background-color: #1e1e1e; color: #cccccc; border: 1px solid #3e3e42; padding: 3px; }
            QDialogButtonBox QPushButton { background-color: #3e3e42; color: #cccccc; border: 1px solid #4e4e52; padding: 5px 15px; }
            QDialogButtonBox QPushButton:hover { background-color: #4e4e52; }
        """)