import Mappings


# contains bug metadata
class Bug:

    # constructor
    def __init__(self):
        self.id = 0
        self.name = 'default_name'
        self.project = 'default_project'
        self.component = 'default_component'
        self.status = 'default_status'
        self.resolution = 'default_resolution'
        self.priority = 0
        self.severity = 'default_severity'
        self.assignee = 'default_assignee'
        self.fogStatus = 0  # fogbugz specific status index
        self.comments = []

    # map all metadata to new fogbugz values
    def fixbug(self):
        self.assignee = Mappings.users.get(self.assignee, self.assignee)
        self.project = Mappings.projects.get(self.project, self.project)

        # if the bug is 'resolved' we should handle this properly
        if self.status == 'RESOLVED':
            self.fogStatus = Mappings.resolutions.get(self.resolution, self.fogStatus)
        else:
            self.fogStatus = Mappings.statuses.get(self.status, self.fogStatus)

        # set bug priority
        if self.priority is not None:
            self.priority = Mappings.priorities.get(self.priority, self.priority)

    # utility method to print out bug details
    def printdetails(self):
        if self.project is not None:
            print('PROJECT: ' + self.project)

        print('BUG ID: ' + self.id)

        if self.name is not None:
            print('TITLE: ' + self.name)
        if self.component is not None:
            print('COMPONENT: ' + self.component)
        if self.status is not None:
            print('STATUS: ' + self.status)
        if self.resolution is not None:
            print('RESOLUTION: ' + self.resolution)
        if self.priority is not None:
            print('PRIORITY: ' + str(self.priority))
        if self.assignee is not None:
            print('ASSIGNEE: ' + self.assignee)
        if self.fogStatus is not None:
            print('FOGBUGZ STATUS: ' + str(self.fogStatus) + '\n')

        # print comments associated with the bug
        for comment in self.comments:
            if len(self.comments) > 0:
                if comment.who is not None and comment.when is not None:
                    print(comment.who + ' said on ' + comment.when + ':')
                if comment.text is not None:
                    print(comment.text + '\n\n')

        # separator for cleanliness at end of bug
        print('====================\n')


# contains comments, in the comment structure in the bug
class Comment:
    def __init__(self):
        self.who = 'default_name'
        self.when = 'default_time'
        self.text = 'default_text'


# structure to store all processed bugs
class BugList:
    def __init__(self):
        self.bugs = set()
        self.projects = set()
        self.users = set()
