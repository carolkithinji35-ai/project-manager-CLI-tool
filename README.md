# Project Management CLI Tool

A command-line tool to manage users, projects, and tasks.

## Setup

```bash
# Clone the repository
git clone https://github.com/carolkithinji35-ai/project-manager-CLI-tool.git
cd project-manager-CLI-tool

# Create and activate virtual environment
python3 -m venv env
source env/bin/activate

# Install dependencies
pip install -r requirements.txt
## Usage

# Create a new user called Alex
python3 main.py add-user --name "Alex"

# Show all registered users
python3 main.py list-users

# Create a new project called CLI Tool and assign it to Alex
python3 main.py add-project --user "Alex" --title "CLI Tool"

# Show all projects
python3 main.py list-projects

# Show only Alex's projects

python3 main.py list-projects --user "Alex"

# Add a task to the CLI Tool project
python3 main.py add-task --project "CLI Tool" --title "Implement add-task"

# Show all tasks
python3 main.py list-tasks

# Show only tasks for CLI Tool project
python3 main.py list-tasks --project "CLI Tool"

# Mark the task as completed
python3 main.py complete-task --title "Implement add-task" --project "CLI Tool"

# Assign the task to Alex
python3 main.py assign-task --title "Implement add-task" --project "CLI Tool" --user "Alex"

# Display help menu with all available commands
python3 main.py --help

## Running Tests

# Run all 20 unit tests to verify everything works
python3 -m pytest tests/test_project.py -v
