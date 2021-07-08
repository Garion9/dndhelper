from PyQt5.QtGui import QTextCursor

# auxiliary function to properly display formatted text inside of QTextEdit fields
def wrap_text_for_display(text):
    return "<pre style=\"font-family: Arial, Helvetica, sans-serif; margin: 0;\">" + text + "<pre>"

# auxiliary function to properly display formatted text inside of QTextEdit fields (remove redundant newlines at the end)
def trim_display(textfield):
    cursor = textfield.textCursor()
    cursor.movePosition(QTextCursor.End)
    cursor.deletePreviousChar()
