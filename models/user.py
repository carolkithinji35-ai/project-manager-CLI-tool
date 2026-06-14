class User:

  def __init__(self,name,email=""):
    self.name = name
    self.email = email
    self._projects = []

  def add_project(self, project_title):
        """Add a project to this user's list"""
        if project_title not in self._projects:
            self._projects.append(project_title)
    
  def remove_project(self, project_title):
        """Remove a project from this user's list"""
        if project_title in self._projects:
            self._projects.remove(project_title)
    
  def get_projects(self):
        """return list of project titles"""
        return self._projects.copy()
    
  def get_project_count(self):
        """return number of projects"""
        return len(self._projects)
    
  def to_dict(self):
        """convert user to dictionary for saving to JSON"""
        return {
            "name": self.name,
            "email": self.email,
            "projects": self._projects
        }
    
  @classmethod
  def from_dict(cls, data):
        """Create a User from a dictionary"""
        user = cls(data["name"], data.get("email", ""))
        user._projects = data.get("projects", [])
        return user
    
  def __str__(self):
        return f"User: {self.name} (Projects: {len(self._projects)})"
