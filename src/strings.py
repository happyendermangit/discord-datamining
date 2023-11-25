import requests 
from bs4 import BeautifulSoup
from jsbeautifier import beautify as jsbeautify
import os 
from github import Github
import json

WEBHOOK = os.getenv('WEBHOOK')
GITHUB_TOKEN = os.getenv('ACCESS_TOKEN')
print(GITHUB_TOKEN) 

def scrapeStrings(code):
    strings = {}
    for l in code.splitlines():
        
        if ":" in l and "," in l and '"' in l and l.split(':')[0].strip().isupper() and "_" in l.split(':')[0]:
            v = l.split(':')[1].strip()[1:-1]
            strings[l.split(':')[0].strip()] = v[:-1]
    
    return strings

def compareStrings(before,after):
    diff = "# Strings:\n```diff\n"
    stuff = {
        "ADDED":"",
        "REMOVED":"",
        "UPDATED":""
    }
    for key,value in after.items():
        if key not in before.keys():
            stuff['ADDED'] += f'+ {key}: "{value}"\n'
        else:
            if value != before[key]:
                stuff['UPDATED'] += f'- {key}:"{before[key]}"\n+{key}: "{value}"\n'
    for key,value in before.items():
        if key not in after.keys():
            stuff['REMOVED'] += f'- {key}: "{value}"\n'
    
    for k,v in stuff.items():
        if v != "":
            diff += f"# {k.lower().capitalize()}:\n{v}\n\n"

    return diff + "```"


def commit_to_github(new_content):

    g = Github(GITHUB_TOKEN)
    
    repo = g.get_repo("happyendermangit/discord-datamining")
    
    contents = repo.get_contents("strings.json")
    
    if not isinstance(new_content, str):
        new_content = json.dumps(new_content,indent=4)
    
    c = repo.update_file(contents.path, "🚀strings updated!", new_content, contents.sha)
    print(c)
    return c.get('commit').sha


def add_comment_to_commit(commit_sha, comment):
    
    g = Github(GITHUB_TOKEN)
    repo = g.get_repo("happyendermangit/discord-datamining")
    commit = repo.get_commit(commit_sha)
    commit.create_comment(comment)

    


html = requests.get('https://canary.discord.com/login').text 

soup = BeautifulSoup(html,"html.parser")

scripts = soup.find_all('script')

srcs = [script.get('src') for script in scripts if script.get('src')]
r = requests.get('https://canary.discord.com/'+srcs[-2]) 
code = jsbeautify(r.text)
strings = scrapeStrings(code)
        

oldStrings = requests.get('https://raw.githubusercontent.com/happyendermangit/discord-datamining/main/strings.json')

if oldStrings.status_code != 404:
    print('found json')
    oldStrings = json.loads(oldStrings.text)
    if oldStrings != strings:
        print('not the same')
        diff = compareStrings(oldStrings,strings)
        sha = commit_to_github(strings)
        add_comment_to_commit(sha,diff)
else:
    commit_to_github(strings)
    
