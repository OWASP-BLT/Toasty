from sarvamai import SarvamAI
from PR_seeker import Seeker
#from dotenv import load_dotenv
import os

#load_dotenv()
client = SarvamAI(api_subscription_key=os.getenv("SARVAM_API_KEY"))

class Generator:
    def __init__(self):
        self.client = client
        self.categories = ["Bug Fix", "Feature Addition", "Documentation Update", 
                          "Performance Improvement", "Refactoring", "Testing", "Others"]
    
    def forward(self, pr_title: str, pr_body: str):
        pr_content = f"Title: {pr_title}\nBody: {pr_body}"
        
        response = self.client.chat.completions(
            messages=[
                {'role': 'system', 'content': f'You are a Pull Request (PR) analyzer. You classify them into the following categories: {", ".join(self.categories)}. Classify the PR into exactly ONE of these categories: {", ".join(self.categories)}. Output ONLY the category label, with no explanation or additional text.'},
                {"role": "user", "content": pr_content}
            ],
            temperature=0.5,
            top_p=1,
            max_tokens=1000,
        )
        
        return response.choices[0].message.content


generator = Generator()
seeker = Seeker()
response = ''
store_lst = seeker.forward('OWASP-BLT/Toasty')
for i in range(len(store_lst)):
    title = store_lst[i]['Title']
    body = store_lst[i]['Body']

    response = generator.forward(title, body)
    print(response)