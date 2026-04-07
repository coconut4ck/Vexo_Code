import re
from PyQt5.QtGui import QSyntaxHighlighter, QTextCharFormat, QColor, QFont
from PyQt5.QtCore import QRegularExpression


class SyntaxHighlighter(QSyntaxHighlighter):
    def __init__(self, parent):
        super().__init__(parent)
        self.rules = []
        self.setup_rules()

    def setup_rules(self):
        self.rules = []

        keywords = [
            'make', 'var', 
            'and', 'or', 'not',
            'true', 'false',
        ]
        self.add_rule(keywords, "#569CD6", bold=True)

        builtins = ['say', 'stick', 'ask', 'number', 'float', 'string', 'logic']
        self.add_rule(builtins, "#DCDCAA")

        self.add_pattern(r'"[^"\\]*(\\.[^"\\]*)*"', "#CE9178")
        self.add_pattern(r"'[^'\\]*(\\.[^'\\]*)*'", "#CE9178")

        self.add_pattern(r'\b[0-9]+\b', "#B5CEA8")
        self.add_pattern(r'\b[0-9]+\.[0-9]+\b', "#B5CEA8")

        self.add_pattern(r'//[^\n]*', "#6A9955", italic=True)

    def add_rule(self, words, color, bold=False, italic=False):
        fmt = QTextCharFormat()
        fmt.setForeground(QColor(color))
        if bold:
            fmt.setFontWeight(QFont.Bold)
        if italic:
            fmt.setFontItalic(True)

        for word in words:
            pattern = QRegularExpression(r'\b' + word + r'\b')
            self.rules.append((pattern, fmt))

    def add_pattern(self, pattern, color, bold=False, italic=False):
        fmt = QTextCharFormat()
        fmt.setForeground(QColor(color))
        if bold:
            fmt.setFontWeight(QFont.Bold)
        if italic:
            fmt.setFontItalic(True)

        self.rules.append((QRegularExpression(pattern), fmt))

    def highlightBlock(self, text):
        for pattern, fmt in self.rules:
            matches = pattern.globalMatch(text)
            while matches.hasNext():
                match = matches.next()
                self.setFormat(match.capturedStart(), match.capturedLength(), fmt)

    def update_color(self, element, color):
        for i, (pattern, fmt) in enumerate(self.rules):
            if hasattr(fmt, 'element') and fmt.element == element:
                fmt.setForeground(QColor(color))
                self.rehighlight()
                break
