import os
import datetime
import requests
path = os.getcwd()
host_path = r'C:\Windows\System32\drivers\etc\hosts'
log_path = os.path.join(path, 'AutoRunLog.log')

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
}

res = requests.get('https://gitee.com/if-the-wind/github-hosts/raw/main/hosts', headers=headers)

for line in res.text.split('\n'):
    if 'github' in line and line[0] != '#':
        url = line.split(' ')[-1]
        ip = line.split(' ')[0]
        with open(host_path, 'r') as f:
            c = f.readlines()
        switch = False
        for i, l in enumerate(c):
            if url == l.split(' ')[-1]: 
                c[i] = '\n' + ip +' ' + url
                print('inserted '+ line +' to '+ host_path)
                switch = True       
                break
        if i == len(c) - 1 and switch == False:
            c.append('\n' + ip +' ' + url)
            print('inserted '+ line +' to '+ host_path)
        with open(host_path, 'w') as f:
            f.writelines(c)
with open(log_path, 'a',encoding='utf-8') as f:
    f.write('AutoFix executed at '+ str(datetime.datetime.now())+'\n')