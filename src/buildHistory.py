import requests
import os
from github import Github

def commit_changes(repo, branch_name, commit_message, folder_path):
    branch = repo.get_branch(branch_name)
    head_commit = branch.commit
    tree = head_commit.commit.tree

    
    blobs = []
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if os.path.isfile(file_path):
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                blobs.append(repo.create_git_blob(content, 'utf-8'))

    
    new_tree = repo.create_git_tree(blobs, tree)

    
    new_commit = repo.create_git_commit(commit_message, new_tree, [head_commit], None)

    
    branch.edit(commit=new_commit.sha)

def save_html(url, path):
    response = requests.get(url)
    build_id = response.headers.get('X-Build-Id')
    html_content = response.text

    os.mkdir(path + "/"+build_id)
    with open(path + build_id+"/" +f'index.html', 'a+', encoding="utf-8") as f:
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


commit_changes("discord-datamining","main",ptb_commit_msg,"./builds/ptb")
commit_changes("discord-datamining","main",canary_commit_msg,"./builds/canary")
commit_changes("discord-datamining","main",stable_commit_msg,"./builds/stable")

