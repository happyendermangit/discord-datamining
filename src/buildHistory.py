import requests,os 

ptb_path = "./ptb/"
canary_path = "./canary/"
stable_path = "./stable/"


ptb = requests.get('https://ptb.discord.com/app')

canary = requests.get('https://canary.discord.com/app')

stable = requests.get('https://discord.com/app')

ptb = {"hash":ptb.headers['X-Build-Id'],"html":ptb.text}

canary = {"hash":canary.headers['X-Build-Id'],"html":canary.text}

stable = {"hash":stable.headers['X-Build-Id'],"html":stable.text}

os.mkdir(ptb_path + ptb.get('hash'))

with open(ptb_path + ptb.get('hash')+'/index.html','a+',encoding="utf-8") as f:
    f.write(ptb.get('html'))


os.mkdir(canary_path + canary.get('hash'))

with open(canary_path + canary.get('hash')+'/index.html','a+',encoding="utf-8") as f:
    f.write(canary.get('html'))


os.mkdir(stable_path + stable.get('hash'))

with open(stable_path + stable.get('hash')+'/index.html','a+',encoding="utf-8") as f:
    f.write(stable.get('html'))


