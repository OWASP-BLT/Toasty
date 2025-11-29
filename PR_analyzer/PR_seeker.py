from github import Github
import os

f = open("Output.txt", "w")

PERSONAL_TOKEN = os.getenv('PERSONAL_TOKEN')

g = Github(PERSONAL_TOKEN)
repo = g.get_repo("OWASP-BLT/Toasty")

pulls = repo.get_pulls(state='all')
for pr in pulls:
    print(pr.title, pr.body)
    f.write(f"Title: {pr.title}\n")
    f.write(f"Body: {pr.body}\n\n")