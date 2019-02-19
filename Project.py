from datetime import datetime, timedelta
from collections import OrderedDict

class Project(object):
    def __init__(self, name:str, time_limit:datetime=None, description:str=None, parent=None, 
                independent:bool=False, cycle:timedelta=None, repository:str=None):
        if(parent is None and cycle is None):
            raise ValueError("The project is set as independent, yet"
                            "at least one setting is missing")
        
        self.name = name
        self.description = description
        self.sub_projects = []
        self.deliveries = []
        self.chat = OrderedDict
        self.people = []
        self.leaders = []
        self.parent = parent
        self.proposals = {}
        self.repository = repository
        self.cycle_num = 0

        if(parent is None): independent = True
        self.independent = independent

        if(time_limit is None):
            if(not parent is None): 
                time_limit = parent.get_time_limit()
            else:
                time_limit = datetime.now()+cycle
        self.time_limit = time_limit

        if(cycle is None): cycle = parent.get_cycle()
        self.cycle = cycle

    def ask_people(self, sender:object, question:str, options:list, people:list=None,
                    anonymous:bool=True, percentage_min:dict={}, do_if:dict={}):
        if(len(self.people) == 1 and sender in self.people): 
            for do, args in do_if.items():
                do(**args)
        if(people is None): people = []
        if(not len(people)): people = self.people
        for person in people:
            self.ask_person(person=person, sender=sender, 
                    question=question, options=options, 
                    anonymous=anonymous, percentage_min=percentage_min, 
                    do_if=do_if)

    def ask_person(self, person:object, question:str, sender:object=None, options:list=None, 
                    anonymous:bool=True, percentage_min:dict={}, do_if:dict={}):
        for option in percentage_min.keys():
            percentage_min[option] = abs(percentage_min[option]%101)
            if(percentage_min[option] > 1): 
                percentage_min[option] =  percentage_min[option]/100
        if(not options is None): options.extend(["Whatever","None"])
        if(not question in self.proposals.keys()):
            self.proposals[question] = {"sender":sender, "question":question, 
                                        "options":dict([(option,[]) for option in options]), 
                                        "anonymous":anonymous, "sent_to":[person],
                                        "percentage_min":percentage_min, "do_if":do_if}
        else: self.proposals[question]["sent_to"].extend(person)
        if(anonymous): sender = None
        if(person is sender or person in self.leaders): return
        person.recieve_notification(project=self, question=question, options=options, sender=sender) #from, title, options, sender
        
    def answer_question(self, sender:object, question:str, response:str):
        if(not sender in self.proposals[question]["options"][response]):
            self.proposals[question]["options"][response].append(sender)
            if(len(self.proposals[question]["options"])-len(self.proposals[question]["options"]["Whatever"]) >= len(self.proposals[question]["sent_to"])
                                                * self.proposals[question]["percentage_min"]):
                #for 
                #    for do,args in self.proposals[question]["do_if"].items():
                #        do(**args)
                print()
            return True
        return False

    def send_message_chat(self, sender:object, message:str):
        self.chat.__setitem__(datetime.now(),[sender, message])

    def apply_cycle(self):
        for delivery in self.deliveries:
            delivery.apply_cycle()

    ### ASK PRE-MADE MODULES

    def ask_set_parent(self, sender:object, parent:object, anonymous:bool=True):
        self.ask_people(sender=sender, question=f"Should we move to project {parent.get_name()}?",
                        options=["Yes","No"], anonymous=anonymous,
                        do_if={self.set_parent:{"parent":parent}})

    def ask_add_person(self, sender:object, person:object, anonymous:bool=True):
        self.ask_people(sender=sender, question=f"Should we add {person.get_name()} to our project?",
                        options=["Yes","No"], anonymous=anonymous, percentage_min={"Yes":50},
                        do_if={self.ask_person:{"person":person, "sender":self,
                        "question":f"Would you like to join our project '{self.name}'?",
                        "options":["Yes","No"], "anonymous":False, "percentage_min":{"Yes":100},
                        "do_if":{self.add_person:{"person":person}}}})

    def ask_remove_delivery(self, sender:object, delivery:object, anonymous:bool=True):
        self.ask_people(sender=sender, question=f"Can I remove my delivery {delivery.get_name()}?",
                        options=["Yes","No"], anonymous=anonymous, people=self.leaders,
                        percentage_min={"Yes":50},
                        do_if={self.remove_delivery:{"delivery":delivery}})

    def make_proposal(self, sender:object, proposal):
        self.ask_people(sender=sender, question=proposal,
                        options=["Yes","No"], anonymous=False, percentage_min={"Yes":50},
                        do_if={sender.change_points:{"points":3,"project":self}})

    ### SET

    def set_parent(self, parent):
        self.parent = parent

    def set_time_limit(self, time_limit):
        self.time_limit = time_limit

    def set_repository(self, repository):
        self.repository = repository

    def set_name(self, name):
        self.name = name

    ### ADD

    def add_delivery(self, delivery):
        self.deliveries.extend(delivery)

    def add_sub_project(self, sub_project):
        self.sub_projects.extend(sub_project)

    def add_person(self, person):
        self.people.append(person)
        for proposal in self.proposals.values():
            if(not person in proposal["sent_to"]):
                self.ask_person(person=person, question=proposal["question"])

    ### REMOVE

    def remove_delivery(self, delivery):
        self.deliveries.remove(delivery)

    ### GET

    def get_name(self):
        return self.name

    def get_parent(self):
        return self.parent

    def get_cycle(self):
        return self.cycle

    def get_time_limit(self):
        return self.time_limit

    def get_chat(self):
        return self.chat

    def get_leaders(self):
        return self.leaders

    # Properties
    """
    time_limit = property(get_time_limit,set_time_limit)
    cycle = property(get_cycle)
    parent = property(get_parent, set_parent)
    leaders = property(get_leaders)
    name = property(get_name,set_name)
    """

    
