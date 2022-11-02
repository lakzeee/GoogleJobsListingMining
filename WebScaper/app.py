from src.Driver import Driver
import src.constants as const

with Driver(teardown=True) as bot:
    bot.get_all()
    # bot.select_team()
    # bot.select_a_role()
    # bot.get_all_links()