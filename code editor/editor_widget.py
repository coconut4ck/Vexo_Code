from PyQt5.QtWidgets import QPlainTextEdit, QWidget, QHBoxLayout, QTextEdit
from PyQt5.QtCore import QRect, QTimer, Qt, QSize
from PyQt5.QtGui import QFont, QColor, QPainter, QTextFormat, QTextCursor
from syntax_highlighter import SyntaxHighlighter


class LineNumberArea(QWidget):
    def __init__(self, editor):
        super().__init__(editor)
        self.editor = editor

    def sizeHint(self):
        return QSize(self.editor.line_width(), 0)

    def paintEvent(self, event):
        self.editor.paint_line_area(event)


class CodeEditor(QPlainTextEdit):
    def __init__(self):
        super().__init__()
        self.line_area = None
        self.minimap = None
        self.setup_editor()

    def setup_editor(self):
        font = QFont("Consolas", 11)
        font.setFixedPitch(True)
        self.setFont(font)

        self.line_area = LineNumberArea(self)
        self.highlighter = SyntaxHighlighter(self.document())

        self.blockCountChanged.connect(self.update_line_width)
        self.updateRequest.connect(self.update_line_area)
        self.cursorPositionChanged.connect(self.highlight_line)

        self.update_line_width()
        self.highlight_line()
        self.setTabStopDistance(4 * self.fontMetrics().width(' '))
        self.setLineWrapMode(QPlainTextEdit.NoWrap)

        self.setStyleSheet("""
            QPlainTextEdit {
                background-color: #1e1e1e;
                color: #d4d4d4;
                border: none;
                selection-background-color: #264f78;
            }
        """)

    def setup_minimap(self, minimap_widget):
        self.minimap = minimap_widget
        self.textChanged.connect(self.update_minimap)

    def update_minimap(self):
        if not self.minimap:
            return

        text = self.toPlainText()
        lines = text.split('\n')

        if lines:
            max_len = max([len(l) for l in lines] + [0])
            if max_len > 150:
                size = 1
            elif max_len > 100:
                size = 2
            elif max_len > 60:
                size = 3
            else:
                size = 4

            if len(lines) > 500:
                size = max(1, size - 2)
            elif len(lines) > 200:
                size = max(1, size - 1)
        else:
            size = 4

        self.minimap.setFont(QFont("Consolas", size))
        self.minimap.setPlainText(text)

    def line_width(self):
        digits = len(str(max(1, self.blockCount())))
        return 8 + self.fontMetrics().width('9') * digits

    def update_line_width(self):
        self.setViewportMargins(self.line_width(), 0, 0, 0)

    def update_line_area(self, rect, dy):
        if dy:
            self.line_area.scroll(0, dy)
        else:
            self.line_area.update(0, rect.y(), self.line_area.width(), rect.height())
        if rect.contains(self.viewport().rect()):
            self.update_line_width()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        cr = self.contentsRect()
        self.line_area.setGeometry(QRect(cr.left(), cr.top(), self.line_width(), cr.height()))

    def highlight_line(self):
        selections = []
        if not self.isReadOnly():
            sel = QTextEdit.ExtraSelection()
            sel.format.setBackground(QColor(40, 40, 40))
            sel.format.setProperty(QTextFormat.FullWidthSelection, True)
            sel.cursor = self.textCursor()
            sel.cursor.clearSelection()
            selections.append(sel)
        self.setExtraSelections(selections)

    def paint_line_area(self, event):
        painter = QPainter(self.line_area)
        painter.fillRect(event.rect(), QColor(37, 37, 38))

        block = self.firstVisibleBlock()
        num = block.blockNumber()
        top = self.blockBoundingGeometry(block).translated(self.contentOffset()).top()
        bottom = top + self.blockBoundingRect(block).height()

        while block.isValid() and top <= event.rect().bottom():
            if block.isVisible() and bottom >= event.rect().top():
                line_num = str(num + 1)
                painter.setPen(QColor(136, 136, 136))
                painter.drawText(0, int(top), self.line_area.width() - 3,
                                 self.fontMetrics().height(), Qt.AlignRight, line_num)
            block = block.next()
            top = bottom
            bottom = top + self.blockBoundingRect(block).height()
            num += 1

    def clear_all(self):
        self.clear()

    def undo_action(self):
        if self.document().isUndoAvailable():
            self.document().undo()

    def redo_action(self):
        if self.document().isRedoAvailable():
            self.document().redo()

    def cut_action(self):
        if self.textCursor().hasSelection():
            self.cut()

    def copy_action(self):
        if self.textCursor().hasSelection():
            self.copy()

    def paste_action(self):
        self.paste()

    def get_text(self):
        return self.toPlainText()

    def set_text(self, text):
        self.setPlainText(text)

    def find_text(self, text):
        return self.find(text)


class EditorWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.editor = None
        self.minimap = None
        self.setup_ui()

    def setup_ui(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(1)

        self.editor = CodeEditor()
        layout.addWidget(self.editor, 4)

        self.minimap = QTextEdit()
        self.minimap.setReadOnly(True)
        self.minimap.setMaximumWidth(150)
        self.minimap.setStyleSheet("""
            QTextEdit {
                background-color: #1e1e1e;
                color: #666666;
                border-left: 1px solid #3e3e42;
                font-family: 'Consolas', monospace;
            }
        """)

        self.editor.setup_minimap(self.minimap)
        layout.addWidget(self.minimap)

    def get_editor(self):
        return self.editor

    def update_minimap(self):
        if self.editor:
            self.editor.update_minimap()