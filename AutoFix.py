import os
import datetime
import requests
import logging

logging.basicConfig(filename='AutoRunLog.log', level=logging.INFO)
path = os.getcwd()
host_path = r'C:\Windows\System32\drivers\etc\hosts'

logging.info('Start to run at'+ str(datetime.datetime.now()))

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
}

try:
    res = requests.get('https://gitee.com/if-the-wind/github-hosts/raw/main/hosts', headers=headers)
    for line in res.text.split('\n'):
        if 'github' in line and line[0] != '#':
            url = line.split(' ')[-1].strip()
            ip = line.split(' ')[0].strip()
            with open(host_path, 'r') as f:
                c = f.readlines()
            if not any(url in l for l in c):
                c.append('\n' + ip +' ' + url)
                print('inserted2 '+ line +' to '+ host_path)
                with open(host_path, 'w') as f:
                    f.writelines(c)
                logging.info('inserted '+ line +' to '+ host_path)
            else:
                for i, l in enumerate(c):
                    if url == l.split(' ')[-1].strip() and line[0] != '#': 
                        c[i] = '\n' + ip +' ' + url
                        print('refreshed '+ line +' to '+ host_path)
                        break   
                    else:
                        continue
                with open(host_path, 'w') as f:
                    f.writelines(c)
            logging.info('inserted '+ line +' to '+ host_path)
except Exception as e:
    logging.error(e)

logging.info('End at'+ str(datetime.datetime.now()))