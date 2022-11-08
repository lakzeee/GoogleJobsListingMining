from src.Driver import Driver
import src.constants as const

with Driver(teardown=True) as bot:
    bot.get_all()