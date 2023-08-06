import os, sys, code

from PyQt5 import QtGui, QtWidgets
from PyQt5.QtCore import QRect
from PyQt5.QtWidgets import QApplication, QFileDialog
from orangewidget import gui
from oasys.widgets import gui as oasysgui, widget

from PyQt5.QtWidgets import QWidget, QGridLayout, QLabel, QDialog, QVBoxLayout, QDialogButtonBox

from PyQt5.QtGui import QTextCursor


class PythonConsole(QtWidgets.QPlainTextEdit, code.InteractiveConsole):
    def __init__(self, locals=None, parent=None):
        QtWidgets.QPlainTextEdit.__init__(self, parent)
        code.InteractiveConsole.__init__(self, locals)
        self.history, self.historyInd = [""], 0
        self.loop = self.interact()
        next(self.loop)
        self.setStyleSheet("background-color:black; color: white; font-family: Courier, monospace;")

    def setLocals(self, locals):
        self.locals = locals


    def flush(self):
        pass

    def interact(self, banner=None):
        try:
            sys.ps1
        except AttributeError:
            sys.ps1 = ">>> "
        try:
            sys.ps2
        except AttributeError:
            sys.ps2 = "... "
        cprt = ('Type "help", "copyright", "credits" or "license" '
                'for more information.')
        if banner is None:
            self.write("Python %s on %s\n%s\n(%s)\n" %
                       (sys.version, sys.platform, cprt,
                        self.__class__.__name__))
        else:
            self.write("%s\n" % str(banner))
        more = 0
        while 1:
            try:
                if more:
                    prompt = sys.ps2
                else:
                    prompt = sys.ps1
                self.new_prompt(prompt)
                yield
                try:
                    line = self.raw_input(prompt)
                except EOFError:
                    self.write("\n")
                    break
                else:
                    more = self.push(line)
            except KeyboardInterrupt:
                self.write("\nKeyboardInterrupt\n")
                self.resetbuffer()
                more = 0

    def raw_input(self, prompt):
        input = str(self.document().lastBlock().previous().text())
        return input[len(prompt):]

    def new_prompt(self, prompt):
        self.write(prompt)
        self.newPromptPos = self.textCursor().position()

    def write(self, data):
        cursor = QTextCursor(self.document())
        cursor.movePosition(QTextCursor.End, QTextCursor.MoveAnchor)
        cursor.insertText(data)
        self.setTextCursor(cursor)
        self.ensureCursorVisible()

    def writelines(self, lines):
        for line in lines:
            self.write(line)

    def push(self, line):
        if self.history[0] != line:
            self.history.insert(0, line)
        self.historyInd = 0

        saved = sys.stdout, sys.stderr
        try:
            sys.stdout, sys.stderr = self, self
            return code.InteractiveConsole.push(self, line)
        finally:
            sys.stdout, sys.stderr = saved

    def setLine(self, line):
        cursor = QTextCursor(self.document())
        cursor.movePosition(QTextCursor.End)
        cursor.setPosition(self.newPromptPos, QTextCursor.KeepAnchor)
        cursor.removeSelectedText()
        cursor.insertText(line)
        self.setTextCursor(cursor)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Return:
            self.write("\n")
            next(self.loop)
        elif event.key() == Qt.Key_Up:
            self.historyUp()
        elif event.key() == Qt.Key_Down:
            self.historyDown()
        elif event.key() == Qt.Key_Tab:
            self.complete()
        elif event.key() in [Qt.Key_Left, Qt.Key_Backspace]:
            if self.textCursor().position() > self.newPromptPos:
                QtWidgets.QPlainTextEdit.keyPressEvent(self, event)
        else:
            QtWidgets.QPlainTextEdit.keyPressEvent(self, event)

    def historyUp(self):
        self.setLine(self.history[self.historyInd])
        self.historyInd = min(self.historyInd + 1, len(self.history) - 1)

    def historyDown(self):
        self.setLine(self.history[self.historyInd])
        self.historyInd = max(self.historyInd - 1, 0)

    def complete(self):
        pass

    def _moveCursorToInputLine(self):
        """
        Move the cursor to the input line if not already there. If the cursor
        if already in the input line (at position greater or equal to
        `newPromptPos`) it is left unchanged, otherwise it is moved at the
        end.

        """
        cursor = self.textCursor()
        pos = cursor.position()
        if pos < self.newPromptPos:
            cursor.movePosition(QTextCursor.End)
            self.setTextCursor(cursor)

    def pasteCode(self, source):
        """
        Paste source code into the console.
        """
        self._moveCursorToInputLine()

        for line in interleave(source.splitlines(), itertools.repeat("\n")):
            if line != "\n":
                self.insertPlainText(line)
            else:
                self.write("\n")
                next(self.loop)

    def insertFromMimeData(self, source):
        """
        Reimplemented from QPlainTextEdit.insertFromMimeData.
        """
        if source.hasText():
            self.pasteCode(str(source.text()))
            return



class MyPythonScript(widget.OWWidget):

    # name = "SRW Python Script (SE)"
    # description = "SRW Python Script (SE)"
    # icon = "icons/python_script_se.png"
    # maintainer = "Luca Rebuffi"
    # maintainer_email = "lrebuffi(@at@)anl.gov"
    # priority = 1
    # category = "Data Display Tools"
    # keywords = ["data", "file", "load", "read"]
    #
    # inputs = [("SRWData", SRWData, "set_input")]

    WIDGET_WIDTH = 950
    WIDGET_HEIGHT = 650

    want_main_area=1
    want_control_area = 0

    input_srw_data=None

    def __init__(self, show_automatic_box=True):
        super().__init__()

        geom = QApplication.desktop().availableGeometry()
        self.setGeometry(QRect(round(geom.width()*0.05),
                               round(geom.height()*0.05),
                               round(min(geom.width()*0.98, self.WIDGET_WIDTH)),
                               round(min(geom.height()*0.95, self.WIDGET_HEIGHT))))

        # self.setMaximumHeight(self.WIDGET_HEIGHT)
        # self.setMaximumWidth(self.WIDGET_WIDTH)
        #
        # tabs_setting = oasysgui.tabWidget(self.mainArea)
        # tabs_setting.setFixedHeight(self.WIDGET_HEIGHT-60)
        # tabs_setting.setFixedWidth(self.WIDGET_WIDTH-60)
        #
        # tab_scr = oasysgui.createTabPage(tabs_setting, "Python Script")

        self.pythonScript = oasysgui.textArea(readOnly=False)
        self.pythonScript.setStyleSheet("background-color: white; font-family: Courier, monospace;")
        self.pythonScript.setMaximumHeight(self.WIDGET_HEIGHT - 300)

        script_box = oasysgui.widgetBox(self.mainArea, "", addSpace=False, orientation="vertical", height=self.WIDGET_HEIGHT - 80, width=self.WIDGET_WIDTH - 80)
        script_box.layout().addWidget(self.pythonScript)

        console_box = oasysgui.widgetBox(script_box, "", addSpace=True, orientation="vertical",
                                          height=150, width=self.WIDGET_WIDTH - 80)

        self.console = PythonConsole(self.__dict__, self)
        console_box.layout().addWidget(self.console)

        self.shadow_output = oasysgui.textArea()

        # out_box = oasysgui.widgetBox(tab_out, "System Output", addSpace=True, orientation="horizontal", height=self.WIDGET_HEIGHT - 80)
        # out_box.layout().addWidget(self.shadow_output)

        #############################

        button_box = oasysgui.widgetBox(self.mainArea, "", addSpace=True, orientation="horizontal")

        gui.button(button_box, self, "Run Script", callback=self.execute_script, height=40)
        gui.button(button_box, self, "Save Script to File", callback=self.save_script, height=40)

    def execute_script(self):
        self._script = str(self.pythonScript.toPlainText())
        self.console.write("\nRunning script:\n")
        self.console.push("exec(_script)")
        self.console.new_prompt(sys.ps1)

    def save_script(self):
        file_name = QFileDialog.getSaveFileName(self, "Save File to Disk", os.getcwd(), filter='*.py')[0]

        if not file_name is None:
            if not file_name.strip() == "":
                file = open(file_name, "w")
                file.write(str(self.pythonScript.toPlainText()))
                file.close()

                QtWidgets.QMessageBox.information(self, "QMessageBox.information()",
                                              "File " + file_name + " written to disk",
                                              QtWidgets.QMessageBox.Ok)


    def set_input(self,text):


        self.pythonScript.setText("")

        try:
            self.pythonScript.setText(text)
        except Exception as e:
            self.pythonScript.setText("Problem in writing python script:\n" + str(sys.exc_info()[0]) + ": " + str(sys.exc_info()[1]))

            if self.IS_DEVELOP: raise e




if __name__ == "__main__":

    # app = QApplication(sys.argv)
    # w = MyPythonScript()
    # w.show()
    # app.exec()
    # w.saveSettings()



    from PyQt5.QtWidgets import QApplication
    app = QApplication([])

    widget = QWidget()

    layout = QVBoxLayout()

    oo = MyPythonScript()

    oo.set_input("print('Hello world')\n")

    layout.addWidget(oo)

    widget.setLayout(layout)

    widget.show()

    app.exec_()
