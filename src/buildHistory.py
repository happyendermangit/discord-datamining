import requests
import os
from github import Github

def save_html(url, path):
    response = requests.get(url)
    build_id = response.headers.get('X-Build-Id')
    html_content = response.text

    os.mkdir(path + "/"+build_id)
    with open(path + "/"+build_id+"/" +f'index.html', 'a+', encoding="utf-8") as f:
        f.write(html_content)

    return build_id 

github_token = os.getenv('ACCESS_TOKEN')
repository_name = 'discord-datamining'


g = Github(github_token)
repo = g.get_user().get_repo(repository_name)

ptb_path = "./builds/ptb"
canary_path = "./builds/canary"
stable_path = "./builds/stable"



ptb = save_html('https://ptb.discord.com/app', ptb_path)


canary = save_html('https://canary.discord.com/app', canary_path)


stable = save_html('https://discord.com/app', stable_path)

ptb_commit_msg = f"✅ PTB builds updated ({ptb})"
canary_commit_msg = f"✅ Canary builds updated ({canary})"
stable_commit_msg = f"✅ Stable builds updated ({stable})"



branch_name = "main"  

os.system(f'git add ./builds/ptb || git commit -am "{ptb_commit_msg}"') 
os.system(f'git add ./builds/canary || git commit -am "{canary_commit_msg}"') 
os.system(f'git add ./builds/stable || git commit -am "{stable_commit_msg}"') 

