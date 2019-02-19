from datetime import date
#from git import Repo,remote
import getpass

class Delivery(object):
    def __init__(self, name:str, project:object, workers:list, time_limit:date=None, 
                repository:str=None, branch:str=None, repository_folder:str=None,
                description:str=None):
        self.name = name
        self.description = description
        self.project = project
        if(time_limit is None): time_limit = project.get_time_limit()
        self.time_limit = time_limit
        self._difficulty = {}
        self.workers = dict([(worker,0) for worker in workers])
        self._commit_message = None
        self._files = []
        if(repository is None): repository = project.get_repository()
        self.repository = repository
        self.branch = branch
        if(repository_folder is None): project.get_repository_folder()
        self.repository_folder = repository_folder
        #Debug
        self._commit_message = "Hola"
        self._files = ["Universe.py"]
        self.bloqued_by_leader = False
        self.review_by = None
        self.finished = False

    ### FUNCTIONS

    def push_github(self):
        if(self.repository is None or not self.review_by is None): return
        if(not len(self._files)): 
            print("\n")
            self._files = [input("Looks like "
                    "the file you're trying to push is not set. \nLocation: ")]
        while(self._commit_message is None or len(self._commit_message)>50):
            print("\n")
            self._commit_message = input("Looks like the commit message of"
                    "the file you're trying to push is not or valid. \nMessage: ")
            if(self._commit_message == ""): return   
        repository = remote.Remote(self.repository,self.name) #Name just to fill args
        repository.git.add(self._files)
        repository.git.push(self.repository_folder, self.branch)

        self._commit_message = None

    def apply_cycle(self):
        points = 20
        if(not self.finished): points *= -1
        points += self._difficulty
        for worker in self.workers:
            worker.change_points(self.project, points)

    ### SET

    def set_repository(self, repository):
        self.repository = repository

    def set_commit_message(self, commit_message:str):
        self._commit_message = commit_message

    def set_branch(self, branch):
        self.branch = branch

    def set_repository_folder(self, repository_folder:str):
        self.repository_folder = repository_folder

    def set_leader_block(self, block:bool):
        self.bloqued_by_leader = block

    def set_time_limit(self, time_limit:date):
        if(not self.bloqued_by_leader):
            self.time_limit = time_limit

    def set_review(self, leader):
        self.review_by = leader

    def set_finished(self, finished):
        self.finished = finished

    ### ADD

    def add_github_file_push(self, files):
        self._files.extend(files)

    ### GET

    def get_difficulty(self):
        if(not len(self._difficulty)): return 0
        return sum(self._difficulty.values())/len(self._difficulty)

    def get_time_limit(self):
        return self.time_limit
    
    def get_review(self):
        return self.review_by

    def get_finished(self):
        return self.finished

    """
    time_limit = property(get_time_limit, set_time_limit)
    review = property(get_review)
    finished = property(get_finished, set_finished)
    """
