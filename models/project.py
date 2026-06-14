class Project:
    """belongs to one user, contains many tasks (one-to-many relationship).
    """
    
    VALID_STATUSES = ["active", "completed", "on_hold"]
    
    def __init__(self, title, owner_name, description=""):
        self.title = title
        self.owner_name = owner_name
        self.description = description
        self._tasks = []
        self._status = "active"
    
    def add_task(self, task_title):
        # Add task to this project
        if task_title not in self._tasks:
            self._tasks.append(task_title)
    
    def remove_task(self, task_title):
        # remove task
        if task_title in self._tasks:
            self._tasks.remove(task_title)
    
    def get_tasks(self):
        # list of task titles
        return self._tasks.copy()
    
    def get_task_count(self):
        # number of tasks
        return len(self._tasks)
    
    def get_status(self):
      #  project status
        return self._status
    
    def set_status(self, new_status):
      #  project status 
        if new_status in self.VALID_STATUSES:
            self._status = new_status
            return True
        return False
    
    def to_dict(self):
        # Convert project to dictionary for saving to JSON
        return {
            "title": self.title,
            "owner_name": self.owner_name,
            "description": self.description,
            "tasks": self._tasks,
            "status": self._status
        }
    
    @classmethod
    def from_dict(cls, data):
        # create a Project from a dictionary
        project = cls(
            data["title"],
            data["owner_name"],
            data.get("description", "")
        )
        project._tasks = data.get("tasks", [])
        project._status = data.get("status", "active")
        return project
    
    def __str__(self):
        return f"Project: {self.title} (Status: {self._status}, Tasks: {len(self._tasks)})"