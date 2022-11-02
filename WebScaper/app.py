from src.Driver import Driver
import src.constants as const

with Driver(teardown=True) as bot:
    bot.load_a_page(const.BASE_URL)
    bot.get_all()
    # bot.select_team()
    # bot.select_a_role()
    # bot.get_all_links()