# Gobuster GUI

Gobuster GUI is a Python-based graphical user interface designed to simplify the usage of **Gobuster**, a widely used command-line tool for enumerating directories, domains, DNS records, and virtual hosts on web targets.

Gobuster does not provide a native graphical interface. This project was developed to improve usability, abstract command-line syntax, and streamline execution through a clean and intuitive terminal-like GUI.

---

## Purpose

* Provide a clean and intuitive graphical interface for Gobuster
* Simulate a terminal experience with command execution
* Abstract repetitive command-line syntax through aliases
* Simplify execution of Gobuster’s main modes
* Reduce common command-line errors
* Persist configuration between sessions

---

## Command Abstraction

The application implements predefined **aliases** and **internal commands**, allowing users to execute Gobuster scans without requiring in-depth knowledge of its full CLI syntax.

This approach improves usability, reduces errors, and increases operational efficiency while preserving the power of the original tool.

---

## Available Aliases

Aliases are replaced automatically before command execution.

### `@go` or `@gobuster`

Uses the path currently configured for the Gobuster executable.

Example:

```
@go dir -u http://example.com -w @word
```

---

### `@w` or `@word`

Uses the path currently configured for the wordlist.

Example:

```
@go dir -u http://example.com -w @w
```

---

### `@l` or `@last`

Executes the last command saved by the application.

Example:

```
@l
```

---

## Internal Commands

These commands are handled internally by the application and are **not** sent to the operating system.

---

### `@ move <gobuster_path> <wordlist_path>`

Defines the paths for the Gobuster executable and the wordlist.

* Requires **two arguments**
* First argument: path to the Gobuster executable
* Second argument: path to the wordlist

To keep the currently saved value, use one of the following:

```
$
null
none
```

Example:

```
@ move /opt/gobuster/gobuster /usr/share/wordlists/common.txt
```

---

### `@ list`

Displays the current configuration:

* Gobuster executable path
* Wordlist path
* Last saved command

---

### `clear`

Clears the output screen.

---

### `exit`

Saves the current configuration and exits the application.

---

## Help Command

### `@h` or `@help`

Displays the built-in help text inside the application.

### Help Content

```
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
```

---

## Command Execution

Any command that is not internal is executed directly by the operating system using the current user’s permissions.

This means the interface behaves like a real terminal with alias support.

---

## Gobuster Dependency

Gobuster is required for this application to function; however, it does **not** need to be installed in the system PATH.

The GUI allows users to manually specify the Gobuster binary path, enabling:

* Greater flexibility
* Use of portable Gobuster versions
* Execution in isolated or restricted environments

---

## Gobuster Download

Gobuster can be downloaded from the official repository:

```
https://github.com/OJ/gobuster
```

After downloading, simply provide the path to the Gobuster binary using the `@ move` command. No global installation is required.

---

## Final Notes

This project does **not** replace Gobuster. Instead, it serves as a usability layer, making Gobuster easier, faster, and more efficient to use through a graphical, terminal-style interface.
