#!/usr/bin/env python3
"""
Project Management CLI Tool
A command-line tool to manage users, projects, and tasks.

Usage:
    python3 main.py add-user --name "Alex"
    python3 main.py add-project --user "Alex" --title "CLI Tool"
    python3 main.py add-task --project "CLI Tool" --title "Implement add-task"
"""

from cli import main

if __name__ == "__main__":
    main()