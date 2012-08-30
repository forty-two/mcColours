#! /usr/bin/python

from PySide.QtCore import *
from PySide.QtGui import *

import re

 
class InputWindow(QMainWindow):
   
    def __init__(self, parent=None):
        super(InputWindow, self).__init__(parent)
        self.setWindowTitle('Minecraft Colour Preview')

        self.edit = QTextEdit(u"Write your text in here")
        self.output = QTextEdit('It comes back here in colour')
        self.output.setMinimumSize(250, 100)
        self.output.setReadOnly(True)
        self.edit.setMinimumSize(250, 100)
        self.output.setAlignment(Qt.AlignTop)

        layout = QHBoxLayout()
        layout.addWidget(self.edit)
        layout.addWidget(self.output)

        self.centreWidget = QWidget()
        self.centreWidget.setLayout(layout)
        self.setCentralWidget(self.centreWidget)

        self.edit.textChanged.connect(self.addWriting)
        self.textCreator = TextCreator()

    def addWriting(self):
        newLabelText = self.textCreator.changeText(self.edit.toPlainText())
        self.output.setHtml(newLabelText)


class TextCreator():
    def __init__(self):
        self.colours = {'0': "#000",
                        '1': "#00A",
                        '2': "#0A0",
                        '3': "#0AA",
                        '4': "#A00",
                        '5': "#A0A",
                        '6': "#FA0",
                        '7': "#AAA",
                        '8': "#555",
                        '9': "#55F",
                        'a': "#5F5",
                        'b': "#5FF",
                        'c': "#F55",
                        'd': "#F5F",
                        'e': "#FF5",
                        'f': "#FFF",
                        }

        self.markers = [u'&', u'\u00A7']
        self.regexes = [u"{}([0-9a-fA-F])(.*?)(?={}|$)".format(marker, u'|'.join(self.markers)) for marker in self.markers]

    def changeText(self, text):
        # Replace new lines with substitute so regex works properly
        text = text.replace(u'\n', u'\u001A')

        for x in self.regexes:
            text = re.sub(x, self.replaceMarkers, text, re.DOTALL)

        # Change whitespace characters so the HTML won't eat them
        text = text.replace(u'\u001A', u'<br>')
        text = text.replace(u' ', u'\u00a0')

        return "<html>"+text+"</html>"


    def replaceMarkers(self, match):
        colourCode = match.group(1)
        text = match.group(2)
        return u'<font color={}>{}</font>'.format(self.colours[colourCode.lower()], text)

 
if __name__ == '__main__':
    app = QApplication("Minecraft Colour Preview")
    form = InputWindow()
    form.show()
    app.exec_()