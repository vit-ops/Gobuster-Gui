# Gobuster GUI

Gobuster GUI is a Python-based graphical user interface designed to simplify the usage of **Gobuster**, a widely used command-line tool for enumerating directories, domains, and subdomains on web targets.

Gobuster does not provide a native graphical interface. This project was developed to improve usability, abstract complex command-line syntax, and streamline execution through a clean and intuitive interface.

---

## Purpose

* Provide a clean and intuitive graphical interface for Gobuster
* Abstract command-line syntax through configurable options
* Simplify execution of Gobuster’s main modes
* Reduce common command-line errors

---

## Command Abstraction

The application implements predefined commands and parameter abstractions, allowing users to execute Gobuster scans without requiring in-depth knowledge of its CLI syntax.

This approach improves usability, reduces errors, and increases operational efficiency.

---

## Available Commands

### `$go` or `$gobuster`

Uses the path currently configured for the Gobuster executable.

Example:

```
$go dir -u example.com -w $word
```

---

### `$w` or `$word`

Uses the path currently configured for the wordlist.

---

### `$l` or `$last`

Executes the last command saved by the system.

---

### `$$$ move`

Sets the paths for the Gobuster executable and the wordlist.

* Requires **at least two arguments** after `$$$ move`
* First argument: path to the Gobuster executable
* Second argument: path to the wordlist

To keep the currently saved path, use one of the following values:

```
$, null, none
```

This rule applies to both arguments.

Example:

```
$$$ move C:\Tools\gobuster null
```

> **Note:** Do not include `.exe` in the Gobuster path.

---

### `$$$ list`

Displays the currently configured paths:

* Gobuster executable
* Wordlist
* Last saved command

---

### `exit`

Exits the application.

---

### `clear`

Clears the screen.

---

## Gobuster Dependency

Gobuster is required for this application to function; however, it does **not** need to be installed in the system PATH.

The GUI allows users to manually specify the Gobuster binary path, enabling:

* Greater flexibility
* Use of portable Gobuster versions
* Execution in isolated or restricted environments

---

## Gobuster Download

Gobuster can be downloaded directly from the official project repository:

```
https://github.com/OJ/gobuster
```

After downloading, simply provide the path to the Gobuster binary in the graphical interface. No global installation is required.

---

## Final Notes

This project does **not** replace Gobuster. Instead, it serves as a usability layer, making Gobuster easier, faster, and more efficient to use through a graphical interface.
