from github import Github
import os


'''
f = open("Output.txt", "w")

PERSONAL_TOKEN = os.getenv('PERSONAL_TOKEN')

g = Github(PERSONAL_TOKEN)
repo = g.get_repo("OWASP-BLT/BLT")

pulls = repo.get_pulls(state='all')
for pr in pulls:
    print(pr.title, pr.body)
    f.write(f"Title: {pr.title}\n")
    f.write(f"Body: {pr.body}\n\n")
'''

class Seeker:
    def __init__(self):
        self.PERSONAL_TOKEN = os.getenv('PERSONAL_TOKEN')
        self.store_dict = {}
        self.store_list = []
        self.do_not_include = """<!-- START COPILOT CODING AGENT TIPS -->
---

💬 We'd love your input! Share your thoughts on Copilot coding agent in our [2 minute survey](https://gh.io/copilot-coding-agent-survey)."""

        self.f = open("Output.txt", "w")
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
                self.f.writelines(store_list)
        print(store_list)

#seeker_obj = Seeker()
#seeker_obj.forward("OWASP-BLT/Toasty")