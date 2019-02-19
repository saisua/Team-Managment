import Project, Delivery
from datetime import datetime, timedelta

class Worker(object):
    def __init__(self, name):
        print(f"Created worker {name}")
        self.name = name
        self.deliveries = {}
        self.projects = []
        self.projects_leader = []
        self.points = {}
        self.total_points = {}
        self.leader_punctuations = {}
        self.notifications = {}

    def change_points(self, project, points:int):
        print(f"{self.name} + {points} points in project '{project.get_name()}'")
        self.points[project] += points
        self.total_points[project] += points
        for project in self.projects:
            if(self in project.get_leaders()): continue
            for leader in project.get_leaders():
                leader.change_points(project, int(points/3))
            
    def recieve_notification(self, project:"Project", question:str, options:list, sender:"Worker"):
        print(f"{self.name} recieved notification by {sender} ({project.get_name()})")
        print(question)
        print(options)
        if(project not in self.notifications.keys()):
            self.notifications[project] = []
        self.notifications[project].append([question, options, sender])

    # ADD

    def add_leader_punctuation(self, project:"Project", cycle_num:int, punct:float):
        print(f"{self.name} got + {punct} Leader points")
        if(not project in self.projects_leader): return -1
        if(not project in self.leader_punctuations.keys()):
            self.leader_punctuations[project] = [[cycle_num, [punct]]]
            return
        if(self.leader_punctuations[project][-1][0] != cycle_num):
            self.leader_punctuations[project].append([cycle_num, [punct]])
            return
        self.leader_punctuations[project][-1][1].append(punct)

    def add_project(self, project:"Project", leader:bool=False):
        print(f"{self.name} joined '{project.get_name()}'")
        self.projects.append(project)
        self.points[project] = 0
        self.total_points[project] = 0
        if(leader): self.add_leader(project)

    def add_leader(self, project:"Project"):
        print(f"{self.name} is now a '{project.get_name()}' leader")
        self.projects_leader.append(project)

    def add_delivery(self, project:"Project", delivery:"Delivery"):
        print(f"{self.name} has a new delivery in '{project.get_name()}'")
        print(f"'{delivery.get_name()}' ({delivery.get_time_limit()})")
        if(project in self.projects):
            if(not project in self.deliveries.keys()):
                self.deliveries[project] = []
            self.deliveries[project].append(delivery)

    # REMOVE

    def remove_notification(self, project:"Project", notification:list):
        self.notifications[project].remove(notification)

    # CREATE

    def create_project(self,name:str, add_self:bool=True, time_limit:datetime=None, 
                description:str=None, parent:"Project"=None, 
                independent:bool=False, cycle:timedelta=None, repository:str=None):
        new_project = Project.Project(name=name, time_limit=time_limit,description=description,
                        parent=parent,independent=independent, cycle=cycle,
                        repository=repository)
        print(f"{self.name} has started a new project ({name})")
        if(add_self):
            self.add_project(new_project)
            new_project.add_person(self)

    # GET

    def get_projects(self):
        return self.projects
        
    def get_notifications(self):
        return self.notifications

    def get_name(self):
        return self.name

    #Buy

Ausias = Worker("Ausias")
Gomego = Worker("Gomego")
Other =  Worker("Other")
Ausias.create_project("Test", cycle=timedelta(0,0,0,1), description="Just a test")
Ausias.get_projects()[0].ask_add_person(sender=Ausias, person=Gomego, anonymous=False)
proj,info = list(Gomego.get_notifications().items())[0] #(q,opt,s)
info = info[0]
proj.answer_question(sender=Gomego, question=info[0], response=info[1][0])
Gomego.get_projects()[0].ask_add_person(sender=Gomego, person=Other, anonymous=True)
q,opt,s = Ausias.get_notifications()[Ausias.get_projects()[0]][0]
Ausias.get_projects()[0].answer_question(sender=Ausias, question=q, response=opt[0])
print("End")