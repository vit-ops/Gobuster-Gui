# Gobuster GUI

This project is a Python-based graphical user interface designed to simplify the usage of Gobuster, a widely used command-line tool for enumerating directories, domains, and subdomains on web targets.

Gobuster does not provide a native graphical interface. This project was developed to improve usability, abstract complex command-line syntax, and streamline execution.

## Purpose

- Provide a clean and intuitive graphical interface for Gobuster
- Abstract command-line syntax through configurable options
- Simplify execution of Gobuster’s main modes
- Reduce common command-line errors

## Command Abstraction

The application implements predefined commands and parameter abstractions, allowing users to run Gobuster scans without requiring in-depth knowledge of its CLI syntax.  
This approach improves usability and increases operational efficiency.

## Gobuster Dependency

Gobuster is required for the application to function; however, it does not need to be installed in the system PATH.

The GUI allows users to manually specify the Gobuster binary path, enabling greater flexibility, use of portable versions, and execution in isolated environments.

## Gobuster Download

Gobuster can be downloaded directly from the official project repository:

https://github.com/OJ/gobuster

After downloading, simply provide the path to the Gobuster binary in the graphical interface. No global installation is required.

## Final Notes

This project does not replace Gobuster. Instead, it serves as a usability layer, making Gobuster easier and more efficient to use through a graphical interface.
