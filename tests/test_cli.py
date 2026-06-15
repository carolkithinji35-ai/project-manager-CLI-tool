from cli import ProjectManagerCLI
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class TestCLI:

    def test_add_user(self):
        cli = ProjectManagerCLI()
        cli.users = []
        cli._cmd_add_user(type('Args', (), {'name': 'TestUser', 'email': ''}))
        assert len(cli.users) == 1
        assert cli.users[0].name == "TestUser"

    def test_add_duplicate_user_fails(self):
        cli = ProjectManagerCLI()
        cli.users = []
        cli._cmd_add_user(type('Args', (), {'name': 'TestUser', 'email': ''}))
        cli._cmd_add_user(type('Args', (), {'name': 'TestUser', 'email': ''}))
        assert len(cli.users) == 1  # still 1, no duplicate

    def test_list_users_empty(self):
        cli = ProjectManagerCLI()
        cli.users = []
        cli._cmd_list_users(None)  # should not crash

    def test_find_user(self):
        cli = ProjectManagerCLI()
        cli.users = []
        cli._cmd_add_user(type('Args', (), {'name': 'Alice', 'email': ''}))
        user = cli._find_user("Alice")
        assert user is not None
        assert user.name == "Alice"

    def test_find_user_not_found(self):
        cli = ProjectManagerCLI()
        cli.users = []
        user = cli._find_user("Nobody")
        assert user is None

    def test_add_project(self):
        cli = ProjectManagerCLI()
        cli.users = []
        cli.projects = []
        cli._cmd_add_user(type('Args', (), {'name': 'Bob', 'email': ''}))
        cli._cmd_add_project(
            type('Args', (), {'title': 'TestProject', 'user': 'Bob', 'description': ''}))
        assert len(cli.projects) == 1
        assert cli.projects[0].title == "TestProject"

    def test_add_task(self):
        cli = ProjectManagerCLI()
        cli.users = []
        cli.projects = []
        cli.tasks = []
        cli._cmd_add_user(type('Args', (), {'name': 'Carol', 'email': ''}))
        cli._cmd_add_project(
            type('Args', (), {'title': 'TestProject', 'user': 'Carol', 'description': ''}))
        cli._cmd_add_task(type(
            'Args', (), {'title': 'TestTask', 'project': 'TestProject', 'priority': 'high'}))
        assert len(cli.tasks) == 1
        assert cli.tasks[0].title == "TestTask"

    def test_complete_task(self):
        cli = ProjectManagerCLI()
        cli.users = []
        cli.projects = []
        cli.tasks = []
        cli._cmd_add_user(type('Args', (), {'name': 'Dave', 'email': ''}))
        cli._cmd_add_project(
            type('Args', (), {'title': 'TestProject', 'user': 'Dave', 'description': ''}))
        cli._cmd_add_task(type('Args', (), {
                          'title': 'TestTask', 'project': 'TestProject', 'priority': 'medium'}))
        cli._cmd_complete_task(
            type('Args', (), {'title': 'TestTask', 'project': 'TestProject'}))
        assert cli.tasks[0].is_done() == True

    def test_assign_task(self):
        cli = ProjectManagerCLI()
        cli.users = []
        cli.projects = []
        cli.tasks = []
        cli._cmd_add_user(type('Args', (), {'name': 'Eve', 'email': ''}))
        cli._cmd_add_project(
            type('Args', (), {'title': 'TestProject', 'user': 'Eve', 'description': ''}))
        cli._cmd_add_task(type('Args', (), {
                          'title': 'TestTask', 'project': 'TestProject', 'priority': 'medium'}))
        cli._cmd_assign_task(
            type('Args', (), {'title': 'TestTask', 'project': 'TestProject', 'user': 'Eve'}))
        assert cli.tasks[0].get_assigned_user() == "Eve"
