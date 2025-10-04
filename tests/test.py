from telethon import TelegramClient

client = TelegramClient("session_name", 23817947, "85ad07bcf806bfd23e0c4c8463282829")
client.start(phone="+79508319396")  # здесь input сработает один раз локально
client.disconnect()