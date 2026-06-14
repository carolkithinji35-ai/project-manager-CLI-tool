# import pytest
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.user import User
from models.project import Project
from models.task import Task
from utils.file_handler import FileHandler




class TestUser:
    
    def test_create_user(self):
        user = User("Alice")
        assert user.name == "Alice"
        assert user.email == ""
        assert user.get_project_count() == 0
    
    def test_create_user_with_email(self):
        user = User("Bob", "bob@example.com")
        assert user.name == "Bob"
        assert user.email == "bob@example.com"
    
    def test_add_project(self):
        user = User("Charlie")
        user.add_project("Project A")
        user.add_project("Project B")
        assert user.get_project_count() == 2
    
    def test_add_duplicate_project(self):
        user = User("Diana")
        user.add_project("Project X")
        user.add_project("Project X")
        assert user.get_project_count() == 1
    
    def test_remove_project(self):
        user = User("Eve")
        user.add_project("Project Y")
        user.remove_project("Project Y")
        assert user.get_project_count() == 0
    
    def test_to_dict_and_from_dict(self):
        user = User("Grace", "grace@example.com")
        user.add_project("Project 1")
        data = user.to_dict()
        new_user = User.from_dict(data)
        assert new_user.name == "Grace"
        assert new_user.get_project_count() == 1




class TestProject:
    
    def test_create_project(self):
        project = Project("My Project", "Alice")
        assert project.title == "My Project"
        assert project.owner_name == "Alice"
        assert project.get_status() == "active"
    
    def test_add_task(self):
        project = Project("Dev Project", "Bob")
        project.add_task("Task 1")
        project.add_task("Task 2")
        assert project.get_task_count() == 2
    
    def test_set_status_valid(self):
        project = Project("Test", "Charlie")
        result = project.set_status("completed")
        assert result == True
        assert project.get_status() == "completed"
    
    def test_set_status_invalid(self):
        project = Project("Test", "Diana")
        result = project.set_status("invalid")
        assert result == False
        assert project.get_status() == "active"
    
    def test_to_dict_and_from_dict(self):
        project = Project("Dict Test", "Frank", "Description")
        project.add_task("Task X")
        project.set_status("on_hold")
        data = project.to_dict()
        new_project = Project.from_dict(data)
        assert new_project.title == "Dict Test"
        assert new_project.get_task_count() == 1
        assert new_project.get_status() == "on_hold"




class TestTask:
    
    def test_create_task(self):
        task = Task("My Task", "My Project")
        assert task.title == "My Task"
        assert task.project_title == "My Project"
        assert task.get_status() == "todo"
        assert task.priority == "medium"
    
    def test_create_task_with_priority(self):
        task = Task("Urgent", "Project X", priority="high")
        assert task.priority == "high"
    
    def test_complete_task(self):
        task = Task("To Do", "Project Z")
        task.complete()
        assert task.get_status() == "done"
        assert task.is_done() == True
    
    def test_assign_task(self):
        task = Task("Assign Me", "Project B")
        task.assign_to("Alice")
        assert task.get_assigned_user() == "Alice"
    
    def test_to_dict_and_from_dict(self):
        task = Task("Dict Task", "Project C", "Desc", "high")
        task.assign_to("Bob")
        task.complete()
        data = task.to_dict()
        new_task = Task.from_dict(data)
        assert new_task.title == "Dict Task"
        assert new_task.get_status() == "done"
        assert new_task.get_assigned_user() == "Bob"




class TestRelationships:
    
    def test_user_has_many_projects(self):
        user = User("Alice")
        project1 = Project("Project 1", "Alice")
        project2 = Project("Project 2", "Alice")
        user.add_project(project1.title)
        user.add_project(project2.title)
        assert user.get_project_count() == 2
    
    def test_project_has_many_tasks(self):
        project = Project("Big Project", "Bob")
        task1 = Task("Task A", "Big Project")
        task2 = Task("Task B", "Big Project")
        project.add_task(task1.title)
        project.add_task(task2.title)
        assert project.get_task_count() == 2
    
    def test_task_belongs_to_project(self):
        task = Task("My Task", "Specific Project")
        assert task.project_title == "Specific Project"




class TestFileHandler:
    
    def test_save_and_load(self, tmp_path):
        handler = FileHandler(str(tmp_path))
        users = [User("Alice"), User("Bob")]
        handler.save("test_users.json", users)
        loaded = handler.load("test_users.json", User)
        assert len(loaded) == 2
        assert loaded[0].name == "Alice"