import os, subprocess, configparser, sys
try:
    from PySide6.QtWidgets import (
        QApplication, QWidget, QVBoxLayout,
        QLineEdit, QTextEdit
    )
    from PySide6.QtCore import Qt
    from PySide6.QtGui import QFont
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "PySide6"])
    from PySide6.QtWidgets import (
        QApplication, QWidget, QVBoxLayout,
        QLineEdit, QTextEdit
    )
    from PySide6.QtCore import Qt
    from PySide6.QtGui import QFont

class OutputArea(QTextEdit):
    def __init__(self):
        super().__init__()
        self.setReadOnly(True)
        self.setLineWrapMode(QTextEdit.NoWrap)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
    def append(self, text: str):
        super().append(text)
        self.verticalScrollBar().setValue(self.verticalScrollBar().maximum())


CONFIG_FILE = os.path.join(os.path.dirname(__file__), "configs_gobuster.cfg")
HELP_TEXT = """
Gobuster GUI - Help
==================

USO GERAL
---------
Digite comandos como em um terminal normal.
A aplicação executa comandos do sistema e substitui aliases automaticamente.


ALIASES
-------
@go, @gobuster
    Usa o caminho configurado para o executável do Gobuster.

@w, @word
    Usa o caminho configurado para a wordlist configurada.

@l, @last
    Executa o último comando salvo pela aplicação.


COMANDOS DE CONTROLE
-------------------
clear
    Limpa a tela do terminal.

exit
    Fecha o programa.


CONFIGURAÇÃO
------------
@ move <gobuster_path> <wordlist_path>
    Define o caminho do Gobuster e da wordlist.
    Use $, null ou none para manter os valores atuais.

@ list
    Exibe todas as configurações atuais:
        - Caminho do Gobuster
        - Caminho da wordlist
        - Último comando salvo


EXECUÇÃO DE COMANDOS
-------------------
Qualquer comando que não seja interno será executado no sistema.


GOBUSTER - EXEMPLOS PRÁTICOS
----------------------------
Scan de diretórios:
        @go dir -u http://example.com -w @word

Scan com extensões:
        @go dir -u http://example.com -w @word -x php,txt,html

Scan DNS:
        @go dns -d example.com -w @word

Scan VHOST:
        @go vhost -u example.com -w @word

Executar último comando:
        @l


OBSERVAÇÕES
-----------
- Gobuster é obrigatório para o funcionamento
- Não precisa estar no PATH do sistema
- Suporta versões portáteis
- A aplicação é apenas uma interface de usabilidade
"""

def QUIT(command):
    global gobuster_path, last_command, wordlist
    cfg = configparser.ConfigParser()
    cfg["CONFIG"] = {
        "gobuster_path": gobuster_path,
        "last_command": command,
        "wordlist": wordlist
    }
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        cfg.write(f)
    quit()

def DADOS():
    cfg = configparser.ConfigParser()
    if not os.path.exists(CONFIG_FILE):
        cfg["CONFIG"] = {
            "gobuster_path": "",
            "last_command": "",
            "wordlist": ""
        }
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            cfg.write(f)

    cfg.read(CONFIG_FILE, encoding="utf-8")
    c = cfg["CONFIG"]
    return (
        c.get("gobuster_path", ""),
        c.get("last_command", ""),
        c.get("wordlist", "")
    )

gobuster_path, last_command, wordlist = DADOS()
list_commands = []


def readArgs(text):
    args = text.split()
    for i, arg in enumerate(args):
        if arg.lower() in ("@go", "@gobuster"):
            args[i] = gobuster_path
        elif arg.lower() in ("@w", "@word"):
            args[i] = wordlist
        elif arg.lower() in ("@l", "@last"):
            args[i] = last_command
    return " ".join(args)

def commands(inputCommand):
    global gobuster_path, last_command, wordlist

    command = inputCommand.text().strip()
    if not command:
        return
    if(command.lower() in ("@h", "@help")):
        output.clear()
        output.append(HELP_TEXT)
        inputCommand.clear()
        return

    command = readArgs(command)

    if command.lower() == "exit":
        QUIT(list_commands[-1] if list_commands else last_command)

    if command[1:] == "@":
        args = command[1:].split()
        if args[0].lower() == "move" and len(args) >= 3:
            if args[1] not in ("$", "null", "none"):
                gobuster_path = args[1]
            if args[2] not in ("$", "null", "none"):
                wordlist = args[2]
            output.clear()
            output.append(f"gobuster: {gobuster_path}\nwordlist: {wordlist}")

        elif args[0].lower() == "list":
            output.clear()
            output.append(
                f"gobuster: {gobuster_path}\n"
                f"wordlist: {wordlist}\n"
                f"last: {last_command}"
            )

        inputCommand.clear()
        return

    if command.lower() == "clear":
        output.clear()
        inputCommand.clear()
        return

    result = subprocess.getoutput(command)
    output.append(result)
    list_commands.append(command)
    inputCommand.clear()

style = """
QWidget {
    background-color: #1e1e1e;
    color: #00FF00;
    font-family: Consolas, "Courier New", monospace;
}

QTextEdit {
    background-color: #1e1e1e;
    color: #00FF00;
    border: none;
    padding: 12px;
    font-size: 12pt;
}

QLineEdit {
    background-color: #1e1e1e;
    color: #00FF00;
    border: none;
    border-top: 1px solid #333;
    padding: 10px;
    font-size: 12pt;
}

QLineEdit::placeholder {
    color: #555;
}
"""

app = QApplication([])
app.setStyleSheet(style)

main = QWidget()
main.setWindowTitle("Gobuster GUI")
main.resize(900, 600)

layout = QVBoxLayout(main)
layout.setSpacing(0)
layout.setContentsMargins(0, 0, 0, 0)

output = OutputArea()

inputCommand = QLineEdit()
inputCommand.setPlaceholderText("Type a command...")
inputCommand.returnPressed.connect(lambda: commands(inputCommand))

layout.addWidget(output)
layout.addWidget(inputCommand)

main.closeEvent = lambda: QUIT(
    list_commands[-1] if list_commands else last_command
)

main.show()
app.exec()
