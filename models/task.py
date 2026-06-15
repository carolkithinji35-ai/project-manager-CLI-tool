from dateutil.parser import parse
from datetime import datetime
class Task:
    
    # Represents a task in a project.
    # Belongs to one project; can be assigned to one user.
  
    
    VALID_PRIORITIES = ["low", "medium", "high", "critical"]
    
    def __init__(self, title, project_title, description="", priority="medium"):
        self.title = title
        self.project_title = project_title
        self.description = description
        self.priority = priority if priority in self.VALID_PRIORITIES else "medium"
        self._status = "todo"
        self._assigned_to = ""
        self.created_at = datetime.now().isoformat()
    
    def complete(self):
        """mark task as complete"""
        self._status = "done"
    
    def start(self):
        """mark task as inprogress"""
        self._status = "in_progress"
    
    def assign_to(self, username):
        """Assign task to a user"""
        self._assigned_to = username
    
    def get_status(self):
        """Return task status"""
        return self._status
    
    def get_assigned_user(self):
        """Return assigned username"""
        return self._assigned_to
    
    def is_done(self):
        """Check if task is completed"""
        return self._status == "done"
    
    def to_dict(self):
        
        return {
            "title": self.title,
            "project_title": self.project_title,
            "description": self.description,
            "priority": self.priority,
            "status": self._status,
            "assigned_to": self._assigned_to,
            "created_at": self.created_at
        }
    
    @classmethod
    def from_dict(cls, data):
       
        task = cls(
            data["title"],
            data["project_title"],
            data.get("description", ""),
            data.get("priority", "medium")
        )
        task._status = data.get("status", "todo")
        task._assigned_to = data.get("assigned_to", "")
        task.created_at = data.get("created_at","")
        return task
    
    def __str__(self):
        return f"Task: {self.title} [{self._status}]"