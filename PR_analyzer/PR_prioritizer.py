import os
from github import Github
from sarvamai import SarvamAI
from PR_seeker import Seeker
from priority_generator import Generator


seeker = Seeker()
generator = Generator()
client = SarvamAI(api_subscription_key=os.getenv("SARVAM_API_KEY"))

# Priority segregation.
high = ["Bug Fix", "Performance Improvement", "Security Fix"]
mid = ["Feature Addition", "Refactoring", "Testing"]
low = ["Documentation Update", "Others"]

gh_link = input("Enter repo link: ").strip()
# Converting repo links to a 'owner/repo' format, without requiring the maintainer to format it themselves, thus reducing the cognitive load needed (to an extent).
new_gh_link = gh_link
if new_gh_link.startswith("https://github.com/"):
    new_gh_link = new_gh_link.replace("https://github.com/", "")
'''
elif new_gh_link.startswith("http://github.com/"):
    new_gh_link = new_gh_link.replace("http://github.com/", "")
'''
new_gh_link = new_gh_link.rstrip('/')

if new_gh_link.endswith('.git'):
    new_gh_link = new_gh_link[:-4]

print(new_gh_link)

response = ''
store_lst = seeker.forward(new_gh_link)
for i in range(len(store_lst)):
    title = store_lst[i]['Title']
    body = store_lst[i]['Body']

    response = generator.forward(title, body).strip()
    
    if response in high:
        print(response, ": high")
    elif response in mid:
        print(response, ": medium")
    elif response in low:
        print(response, ": low")