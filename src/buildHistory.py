import requests
import os
from github import Github


def save_html(url, path):
    response = requests.get(url)
    build_id = response.headers.get('X-Build-Id')
    html_content = response.text

    os.mkdir(path + build_id)

    with open(path + build_id + '/index.html', 'a+', encoding="utf-8") as f:
        f.write(html_content)

    return build_id 

github_token = os.getenv('ACCESS_TOKEN')
repository_name = 'discord-datamining'


g = Github(github_token)
repo = g.get_user().get_repo(repository_name)

ptb_path = "./builds/ptb/"
canary_path = "./builds/canary/"
stable_path = "./builds/stable/"



ptb = save_html('https://ptb.discord.com/app', ptb_path)


canary = save_html('https://canary.discord.com/app', canary_path)


stable = save_html('https://discord.com/app', stable_path)

ptb_commit_msg = f"✅ PTB builds updated ({ptb})"
canary_commit_msg = f"✅ Canary builds updated ({canary})"
stable_commit_msg = f"✅ Stable builds updated ({stable})"


branch_name = "main"  


ptb_commit = repo.get_branch(branch_name).commit
ptb_commit.create_comment(ptb_commit_msg)


canary_commit = repo.get_branch(branch_name).commit
canary_commit.create_comment(canary_commit_msg)


stable_commit = repo.get_branch(branch_name).commit
stable_commit.create_comment(stable_commit_msg)
