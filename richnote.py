import sys
from PySide6.QtWidgets import QMainWindow, QApplication, QFileDialog, QTextEdit, QInputDialog, QWidget, QVBoxLayout, QMessageBox, QLabel
from PySide6.QtCore import QTimer
from datetime import datetime
import os

app = QApplication(sys.argv)
file = QFileDialog()

class RichNote(QMainWindow):
    def __init__(self):
        super().__init__()
        self.file_path = None
        self.count = 1
        self.windows = []
        self.resize(1000, 700)
        self.setWindowTitle("Untitled")

        self.date = QLabel()
        now = datetime.now()
        self.date.setText(now.strftime("%d-%m-%Y")) # 25-01-2026   day-month-year

        self.clock_label = QLabel()
        # ✅ Correct — self makes window own the timer, stays alive
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)
        self.update_time()  # call once immediately so no blank at start
        # Without self the timer will be caught by python garbage collector. because if not it will be outside of window class.

        self.statusBar().addWidget(self.date)  # left side
        self.statusBar().addPermanentWidget(self.clock_label)  # right side — permanent means it stays right
        # self.menuBar()          # top    — menus
        # self.toolBar()          # below menu — icon buttons
        # self.centralWidget()    # middle — your main content
        # self.statusBar()        # bottom — info bar
        # These are window's own methods so no need of separate library importing.

        central = QWidget()
        layout = QVBoxLayout()

        self.textbox = QTextEdit()
        self.textbox.setPlaceholderText("Type here!")

        layout.addWidget(self.textbox)

        central.setLayout(layout)
        self.setCentralWidget(central)

        menubar = self.menuBar()

        filemenu = menubar.addMenu("File")

        Exit = filemenu.addAction("Exit", self.exit_app)
        Exit.setShortcut("Ctrl+E")

        save = filemenu.addAction("Save")
        save.setShortcut("Ctrl+S")
        save.triggered.connect(lambda: self.save_file(self.textbox.toPlainText()))

        New = filemenu.addAction("New File")
        New.setShortcut("Ctrl+N")
        New.triggered.connect(self.new_window)

        Open = filemenu.addAction("Open")
        Open.setShortcut("Ctrl+O")
        Open.triggered.connect(self.open_file)

        Edit = menubar.addMenu("Edit")

        Table = Edit.addAction("Table")
        Table.setShortcut("Ctrl+T")
        Table.triggered.connect(self.create_table)

        Image = Edit.addAction("Image")
        Image.setShortcut("Ctrl+I")
        Image.triggered.connect(self.insert_image)

        Hyperlink = Edit.addAction("Hyperlink")
        Hyperlink.setShortcut("Ctrl+H")
        Hyperlink.triggered.connect(self.create_link)

    def save_file(self, contents):
        if self.file_path is None:
            # QFileDialog.getSaveFileName(parent window, title or caption, default_filename, file_filter)
            filename, _ = file.getSaveFileName(self.window(),"Save File", "untitled", "Text Files (*.txt);;Python Files (*.py);;All Files (*)") # self.window() is the parent for the message box to appear, Save file is title of the message box.
            if not filename:
                return
            self.file_path = filename
            self.setWindowTitle(os.path.basename(filename)) # The base name takes the base string that user provided and keep it as window title.
        with open(self.file_path, "w") as textfile:
            textfile.write(contents)

    def create_table(self):
        row, condition1 = QInputDialog.getInt(self.window(),"Rows","Enter number of rows:") # The inputDialog returns number or input and true or false if entered.
        column, condition2 = QInputDialog.getInt(self,"Columns","Enter number of columns:")
        if condition1 and condition2:
            cursor = self.textbox.textCursor()
            # QTextCursor = typing position, like the blinking cursor: Hello |, and Qt needs this cursor position to insert something.
            # A Table or text or image to insert it we have to get current cursor position. This textCursor() is given to TextEdit() itself, so textEdit()'s cursor will be returned.
            cursor.insertTable(row, column)
            # Like in microsoft-word,  the TextBox() widget has its own or supports table, image, para etc by, inserttable(), insertimage() etc.

    def insert_image(self):
        path, _ = file.getOpenFileName(self.window(), "Open Image", "", "All Images (*.png *.jpg *.jpeg)")
        if path:
            # cursor = self.textbox.textCursor()
            # Why cursor is left because HTML uses internally the widget's cursor so no need of cursor.
            self.textbox.insertHtml(f'<img src="{path}" width = "300" height = "300">')

    def create_link(self):
        cursor = self.textbox.textCursor() # To get selected Text or blue highlighted text.
        selected = cursor.selectedText()
        link, condition = QInputDialog.getText(self.window(), "Insert Link", "Enter Url: ")
        if condition and link:
            if selected:
                cursor.insertHtml(f'<a href = "{link}" >{selected}</a>')
            else:
                self.textbox.insertHtml(f'<a href = "{link}" >{link}</a>')

    def exit_app(self):
        reply = QMessageBox.question(
            self.window(), "Exit", "Save before exiting?",
            QMessageBox.StandardButton.Yes |
            QMessageBox.StandardButton.No |
            QMessageBox.StandardButton.Cancel
        )
        if reply == QMessageBox.StandardButton.Yes:
            self.save_file(self.textbox.toPlainText())
            self.close()
        elif reply == QMessageBox.StandardButton.No:
            self.close()
        # Cancel — does nothing, window stays open

    def new_window(self):
        new = RichNote()
        self.windows.append(new) # We can create object instead of again inheritance
        new.show()

    def open_file(self):
        path, _ = file.getOpenFileName(self.window(), "Open File", "", "Text Files (*.txt)")
        if path:
            with open(path, mode = "r") as textfile:
                contents = textfile.read()
                # We open the file read it instead of directly writing and then put into our editor.
            self.textbox.setPlainText(contents) # setPlainText sets or puts contents of the file to textbox or TextEdit class().
            self.file_path = path
            self.setWindowTitle(os.path.basename(path))

    def update_time(self):
        now = datetime.now()
        self.clock_label.setText(now.strftime("%H:%M:%S"))  # 14:35:22
        # strftime stands for "string format time", It takes a datetime object and converts it into a readable string in whatever format you want.


window = RichNote()
window.show()

app.exec()