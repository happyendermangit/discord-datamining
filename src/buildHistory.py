import requests
import os
import json 
from github import Github
from datetime import datetime

builds = requests.get("https://raw.githubusercontent.com/happyendermangit/discord-datamining/main/builds.json").json()



class Build:
    def __init__(self,hash,type,date,html) -> None:
        self.hash = hash 
        self.type = type 
        self.date = date 
        self.html = html

def save_html(url, path):
    response = requests.get(url)
    build_id = response.headers.get('X-Build-Id')
    html_content = response.text
    if os.path.isdir(path + "/"+build_id) == False:
        
        os.mkdir(path + "/"+build_id)
        current_datetime = datetime.now()
        date_now = current_datetime.strftime("%A, %B %Y,%w %H:%M:%S")

        b = Build(build_id,path.split('/')[2],date_now,html_content).__dict__
        builds.append(b)
        with open(path + "/"+build_id+"/" +f'index.html', 'a+', encoding="utf-8") as f:
            f.write(html_content)
        with open(path + "/"+build_id+"/" +"build.json", 'a+') as json_file:
            json.dump(b, json_file, indent=2)

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

with open("./builds.json", 'w') as json_file:
    json.dump(builds, json_file, indent=2)

branch_name = "main"  

