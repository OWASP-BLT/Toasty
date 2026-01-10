from github import Github
import os

class Seeker:
    def __init__(self):
        self.PERSONAL_TOKEN = os.getenv('PERSONAL_TOKEN')
        self.store_dict = {}
        self.store_list = []
        self.do_not_include = """<!-- START COPILOT CODING AGENT TIPS -->
---

💬 We'd love your input! Share your thoughts on Copilot coding agent in our [2 minute survey](https://gh.io/copilot-coding-agent-survey)."""

        #self.f = open("Output.txt", "w")
    def forward(self, repository:str):
        g = Github(self.PERSONAL_TOKEN)
        repo = g.get_repo(repository)
        pulls = repo.get_pulls(state='all')
        store_list = []
        for pr in pulls:
            if pr != self.do_not_include:
                store_dict = {}
                store_dict['Title'] = pr.title
                store_dict['Body'] = pr.body
                store_list.append(store_dict)
                #self.f.writelines(store_list)
        return store_list

'''
seeker_obj = Seeker()
lst_store = []
lst_store = seeker_obj.forward("OWASP-BLT/Toasty")
#print("Title: ", lst_store[3]['Title'], "\n\n")
#print("Body: ", lst_store[3]['Body'])

print(lst_store[3]['Title'], "\n\n")
print(lst_store[3]['Body'])
'''