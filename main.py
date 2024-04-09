import telegram_bot.bot 
import logging
from colorama import init, Fore, Back, Style
import os
from neirwork.proxy_controller import AvalibleProxies

init()

if __name__ == '__main__':
    os.system('cls||clear')
    print(Fore.BLUE + """
████████╗ ██████╗ ██╗  ██╗██╗     ██████╗ 
╚══██╔══╝██╔════╝ ██║  ██║██║     ██╔══██╗
   ██║   ██║  ███╗███████║██║     ██████╔╝
   ██║   ██║   ██║██╔══██║██║     ██╔═══╝ 
   ██║   ╚██████╔╝██║  ██║███████╗██║     
   ╚═╝    ╚═════╝ ╚═╝  ╚═╝╚══════╝╚═╝     
Телеграм бот для помощи с выбором курсов | GPB_GPT_Hack
""")
    print(Fore.GREEN + 'starting telegram bot...', Style.RESET_ALL)
    telegram_bot.bot.main()