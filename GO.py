try:
    import os
    import sys
    import shlex
    import configparser
    import subprocess
    import re
    from PySide6.QtWidgets import (
        QApplication, QWidget, QVBoxLayout, QLineEdit, QTextEdit
    )
    from PySide6.QtCore import Qt
    from PySide6.QtGui import QFont
except ImportError as e:
    print("Missing dependency:", e)
    os.system("pip install PySide6")




class OutputArea(QTextEdit):
    def __init__(self):
        super().__init__()
        self.setReadOnly(True)
        self.setStyleSheet("""
            QTextEdit {
                background-color: #000000;
                color: #00FF00;
                font-family: Consolas, "Courier New", monospace;
                font-size: 10pt;
                border: none;
                padding: 4px;
            }
        """)
        self.setLineWrapMode(QTextEdit.NoWrap)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)

    def append(self, text: str):
        super().append(text)
        self.verticalScrollBar().setValue(self.verticalScrollBar().maximum())

    def clear(self):
        super().clear()



CONFIG_FILE = os.path.join(os.path.dirname(__file__), "configs_gobuster.cfg")

def QUIT(command):
    global gobuster_path, last_command, wordlist
    cfg = configparser.ConfigParser()
    if os.path.exists(CONFIG_FILE):
        cfg.read(CONFIG_FILE, encoding="utf-8")
    else:
        cfg["CONFIG"] = {"gobuster_path": "", "last_command": "", "wordlist": ""}

    if "CONFIG" not in cfg:
        cfg["CONFIG"] = {}

    cfg["CONFIG"]["last_command"] = command
    cfg["CONFIG"]["gobuster_path"] = gobuster_path
    cfg["CONFIG"]["wordlist"] = wordlist

    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        cfg.write(f)

    quit()

def DADOS():
    cfg = configparser.ConfigParser()
    if not os.path.exists(CONFIG_FILE):
        cfg["CONFIG"] = {"gobuster_path": "", "last_command": "", "wordlist": ""}
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            cfg.write(f)
    try:
        cfg.read(CONFIG_FILE, encoding="utf-8")
        if "CONFIG" not in cfg or \
           "gobuster_path" not in cfg["CONFIG"] or \
           "last_command" not in cfg["CONFIG"] or \
           "wordlist" not in cfg["CONFIG"]:
            cfg["CONFIG"] = {"gobuster_path": "", "last_command": "", "wordlist": ""}
            with open(CONFIG_FILE, "w", encoding="utf-8") as f:
                cfg.write(f)
        gobuster_path = cfg["CONFIG"].get("gobuster_path", "")
        last_command = cfg["CONFIG"].get("last_command", "")
        wordlist = cfg["CONFIG"].get("wordlist", "")
        return gobuster_path, last_command, wordlist
    except Exception:
        cfg["CONFIG"] = {"gobuster_path": "", "last_command": "", "wordlist": ""}
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            cfg.write(f)
        return "", "", ""

gobuster_path, last_command, wordlist = DADOS()

list_commands = []

def readArgs(text):
    args = text.split()
    for i, arg in enumerate(args):
        if arg.lower() in ("$go", "$gobuster"):
            args[i] = gobuster_path
        elif arg.lower() in ("$w", "$word"):
            args[i] = wordlist
        elif arg.lower() in ("$l", "$last"):
            args[i] = last_command
    return " ".join(args)

def commands(inputCommand):
    global gobuster_path, last_command, wordlist
    command = inputCommand.text()

    if not command:
        return
    
    command  = readArgs(command)
    
    if command.lower() == "exit":
        last = list_commands[len(list_commands) - 1]
        QUIT(last)
        return

    if command[:3] == "$$$":
        args = command[3:].split()
        match args[0].lower():
            case "move":
                if len(args) < 3:
                    return
                if args[1].lower() not in ("$", "null", "none"):
                    gobuster_path = args[1]

                if args[2].lower() not in ("$", "null", "none"):
                    wordlist = args[2]
                output.clear()
                output.append(f"gobuster path : {gobuster_path} & wordilist path : {wordlist}")
            case "list":
                output.clear()
                output.append(f"gobuster path : {gobuster_path} & wordilist path : {wordlist} & last_command(save) : {last_command}")    
        inputCommand.setText("")
        return           
        
    if(command.lower() == "clear"):
        output.clear()
        inputCommand.setText("")
        return
    
    result = subprocess.getoutput(command)
    output.append(result)

    list_commands.append(command)
    inputCommand.setText("")


app = QApplication([])

janela = QWidget()
janela.setWindowTitle("Gobuster GUI")
janela.resize(550, 350)


janela.setStyleSheet("""
    QWidget {
        background-color: #000000;
        color: #00FF00;
        font-family: Consolas, "Courier New", monospace;
    }
""")

output = OutputArea()

inputCommand = QLineEdit()
inputCommand.setFont(QFont("Consolas", 10))
inputCommand.setPlaceholderText("Digite seu comando:")
inputCommand.returnPressed.connect(lambda: commands(inputCommand))


inputCommand.setStyleSheet("""
    QLineEdit {
        background-color: #000000;
        color: #00FF00;
        font-family: Consolas, "Courier New", monospace;
        font-size: 10pt;
        border: none;      /* SEM BORDA */
        padding: 6px;
    }
    QLineEdit::placeholder {
        color: #00FF00;
    }
""")

layout = QVBoxLayout()
layout.addWidget(output)
layout.addWidget(inputCommand)
layout.setContentsMargins(0, 0, 0, 0)
layout.setSpacing(0)

janela.setLayout(layout)

janela.closeEvent = lambda event: QUIT(
    list_commands[len(list_commands) - 1] if len(list_commands) >= 1 else last_command
)

janela.show()
app.exec()
