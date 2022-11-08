from src.Driver import Driver

with Driver(teardown=True) as bot:
    bot.get_all()