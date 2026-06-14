import argparse

from models import User, Project, Task
from utils import FileHandler

try:
    from rich.console import Console
    from rich.table import Table
    console = Console()
    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False


class ProjectManagerCLI:
    
    def __init__(self):
        self.file_handler = FileHandler()
        self.users = self.file_handler.load("users.json", User)
        self.projects = self.file_handler.load("projects.json", Project)
        self.tasks = self.file_handler.load("tasks.json", Task)
        self.parser = self._create_parser()
    
    def save_all(self):
        self.file_handler.save("users.json", self.users)
        self.file_handler.save("projects.json", self.projects)
        self.file_handler.save("tasks.json", self.tasks)
    
    def _find_user(self, name):
        for user in self.users:
            if user.name.lower() == name.lower():
                return user
        return None
    
    def _find_project(self, title):
        for project in self.projects:
            if project.title.lower() == title.lower():
                return project
        return None
    
    def _find_task(self, title, project_title):
        for task in self.tasks:
            if (task.title.lower() == title.lower() and 
                task.project_title.lower() == project_title.lower()):
                return task
        return None
    
    def _create_parser(self):
        parser = argparse.ArgumentParser(
            description="Project Management CLI Tool"
        )
        
        subparsers = parser.add_subparsers(dest="command", help="Commands")
        
        # add-user
        add_user = subparsers.add_parser("add-user", help="Add a new user")
        add_user.add_argument("--name", required=True, help="User's name")
        add_user.add_argument("--email", help="User's email (optional)")
        
        # list-users
        subparsers.add_parser("list-users", help="Show all users")
        
        # add-project
        add_project = subparsers.add_parser("add-project", help="Add a new project")
        add_project.add_argument("--title", required=True, help="Project title")
        add_project.add_argument("--user", required=True, help="Owner's username")
        add_project.add_argument("--description", help="Project description (optional)")
        
        # list-projects
        list_projects = subparsers.add_parser("list-projects", help="Show projects")
        list_projects.add_argument("--user", help="Show only this user's projects")
        
        # add-task
        add_task = subparsers.add_parser("add-task", help="Add a new task")
        add_task.add_argument("--title", required=True, help="Task title")
        add_task.add_argument("--project", required=True, help="Project to add task to")
        add_task.add_argument("--priority", choices=["low", "medium", "high", "critical"],
                             default="medium", help="Task priority")
        
        # list-tasks
        list_tasks = subparsers.add_parser("list-tasks", help="Show tasks")
        list_tasks.add_argument("--project", help="Show only tasks for this project")
        
        # complete-task
        complete_task = subparsers.add_parser("complete-task", help="Mark a task as done")
        complete_task.add_argument("--title", required=True, help="Task title")
        complete_task.add_argument("--project", required=True, help="Project name")
        
        # assign-task
        assign_task = subparsers.add_parser("assign-task", help="Assign a task to a user")
        assign_task.add_argument("--title", required=True, help="Task title")
        assign_task.add_argument("--project", required=True, help="Project name")
        assign_task.add_argument("--user", required=True, help="Username to assign")
        
        return parser
    
    def _cmd_add_user(self, args):
        if self._find_user(args.name):
            print(f"Error: User '{args.name}' already exists!")
            return
        user = User(args.name, args.email or "")
        self.users.append(user)
        self.save_all()
        print(f"Created user: {user.name}")
    
    def _cmd_list_users(self, args):
        if not self.users:
            print("No users found.")
            return
        if RICH_AVAILABLE:
            table = Table(title="Users")
            table.add_column("Name", style="cyan")
            table.add_column("Email", style="green")
            table.add_column("Projects", style="yellow")
            for user in self.users:
                table.add_row(user.name, user.email or "-", str(user.get_project_count()))
            console.print(table)
        else:
            print("\n--- Users ---")
            for user in self.users:
                print(f"  {user.name} | {user.email or '-'} | Projects: {user.get_project_count()}")
    
    def _cmd_add_project(self, args):
        user = self._find_user(args.user)
        if not user:
            print(f"Error: User '{args.user}' not found!")
            return
        if self._find_project(args.title):
            print(f"Error: Project '{args.title}' already exists!")
            return
        project = Project(args.title, args.user, args.description or "")
        self.projects.append(project)
        user.add_project(args.title)
        self.save_all()
        print(f"Created project: {project.title} (owner: {args.user})")
    
    def _cmd_list_projects(self, args):
        if args.user:
            user = self._find_user(args.user)
            if not user:
                print(f"Error: User '{args.user}' not found!")
                return
            user_projects = [p for p in self.projects if p.owner_name.lower() == user.name.lower()]
            if not user_projects:
                print(f"No projects found for {args.user}")
                return
            if RICH_AVAILABLE:
                table = Table(title=f"Projects for {args.user}")
                table.add_column("Title", style="cyan")
                table.add_column("Status", style="green")
                table.add_column("Tasks", style="yellow")
                for project in user_projects:
                    table.add_row(project.title, project.get_status(), str(project.get_task_count()))
                console.print(table)
            else:
                print(f"\n--- Projects for {args.user} ---")
                for project in user_projects:
                    print(f"  {project.title} | Status: {project.get_status()} | Tasks: {project.get_task_count()}")
        else:
            if not self.projects:
                print("No projects found.")
                return
            if RICH_AVAILABLE:
                table = Table(title="All Projects")
                table.add_column("Title", style="cyan")
                table.add_column("Owner", style="green")
                table.add_column("Status", style="yellow")
                table.add_column("Tasks", style="magenta")
                for project in self.projects:
                    table.add_row(project.title, project.owner_name, project.get_status(), str(project.get_task_count()))
                console.print(table)
            else:
                print("\n--- All Projects ---")
                for project in self.projects:
                    print(f"  {project.title} | Owner: {project.owner_name} | Status: {project.get_status()} | Tasks: {project.get_task_count()}")
    
    def _cmd_add_task(self, args):
        project = self._find_project(args.project)
        if not project:
            print(f"Error: Project '{args.project}' not found!")
            return
        task = Task(args.title, args.project, priority=args.priority)
        self.tasks.append(task)
        project.add_task(args.title)
        self.save_all()
        print(f"Created task: {task.title} (project: {args.project})")
    
    def _cmd_list_tasks(self, args):
        if args.project:
            project = self._find_project(args.project)
            if not project:
                print(f"Error: Project '{args.project}' not found!")
                return
            project_tasks = [t for t in self.tasks if t.project_title.lower() == project.title.lower()]
            if not project_tasks:
                print(f"No tasks found for '{args.project}'")
                return
            if RICH_AVAILABLE:
                table = Table(title=f"Tasks for {args.project}")
                table.add_column("Title", style="cyan")
                table.add_column("Status", style="green")
                table.add_column("Priority", style="yellow")
                table.add_column("Assigned", style="magenta")
                for task in project_tasks:
                    table.add_row(task.title, task.get_status(), task.priority, task.get_assigned_user() or "-")
                console.print(table)
            else:
                print(f"\n--- Tasks for {args.project} ---")
                for task in project_tasks:
                    print(f"  {task.title} | {task.get_status()} | Priority: {task.priority} | Assigned: {task.get_assigned_user() or 'unassigned'}")
        else:
            if not self.tasks:
                print("No tasks found.")
                return
            if RICH_AVAILABLE:
                table = Table(title="All Tasks")
                table.add_column("Title", style="cyan")
                table.add_column("Project", style="green")
                table.add_column("Status", style="yellow")
                for task in self.tasks:
                    table.add_row(task.title, task.project_title, task.get_status())
                console.print(table)
            else:
                print("\n--- All Tasks ---")
                for task in self.tasks:
                    print(f"  {task.title} | Project: {task.project_title} | Status: {task.get_status()}")
    
    def _cmd_complete_task(self, args):
        task = self._find_task(args.title, args.project)
        if not task:
            print(f"Error: Task '{args.title}' not found in '{args.project}'!")
            return
        task.complete()
        self.save_all()
        print(f"Task '{args.title}' marked as done!")
    
    def _cmd_assign_task(self, args):
        user = self._find_user(args.user)
        if not user:
            print(f"Error: User '{args.user}' not found!")
            return
        task = self._find_task(args.title, args.project)
        if not task:
            print(f"Error: Task '{args.title}' not found in '{args.project}'!")
            return
        task.assign_to(args.user)
        self.save_all()
        print(f"Task '{args.title}' assigned to {args.user}")
    
    def run(self):
        args = self.parser.parse_args()
        
        commands = {
            "add-user": self._cmd_add_user,
            "list-users": self._cmd_list_users,
            "add-project": self._cmd_add_project,
            "list-projects": self._cmd_list_projects,
            "add-task": self._cmd_add_task,
            "list-tasks": self._cmd_list_tasks,
            "complete-task": self._cmd_complete_task,
            "assign-task": self._cmd_assign_task,
        }
        
        if not args.command:
            self.parser.print_help()
            return
        
        handler = commands.get(args.command)
        if handler:
            handler(args)


def main():
    app = ProjectManagerCLI()
    app.run()


if __name__ == "__main__":
    main()