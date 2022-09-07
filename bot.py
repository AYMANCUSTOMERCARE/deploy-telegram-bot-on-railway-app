
import psycopg2

import asyncio
from datetime import datetime
from typing import Optional

import aiogram.utils.markdown as md
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ParseMode
from aiogram.utils import executor
from aiogram.types import InlineKeyboardMarkup,InlineKeyboardButton,KeyboardButton
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove, ReplyKeyboardMarkup    
from aiogram.dispatcher.filters import Text
import logging
from aiogram.types import ReplyKeyboardRemove
from aiogram.contrib.middlewares.logging import LoggingMiddleware



API_TOKEN = '5730303832:AAGE3lbjVqNaqJ0bUww-eRUzW_dNTkrJXrg'
DB_URI ="postgresql://postgres:SEvju9ySxpC7lfoeXwwU@containers-us-west-79.railway.app:7370/railway"

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
dp.middleware.setup(LoggingMiddleware())


db_connection = psycopg2.connect(DB_URI, sslmode="require")
db_object = db_connection.cursor()

async def gen_main_markup():
    markup = InlineKeyboardMarkup(resize_keyboard=True)
    #arkup = ReplyKeyboardMarkup(resize_keyboard=False,one_time_keyboard=False)
    
    markup.row_width = 1
    markup.add(InlineKeyboardButton("📖BUTTON1📖", callback_data="inst"),
               InlineKeyboardButton("💰BUTTON2💰", callback_data="bal"),
               InlineKeyboardButton("✍NOTE✍️", callback_data="add_comment"),
			   
               
               )
                                    
              
    return markup

    
@dp.message_handler(commands=['start'])
async def command_start(message: types.Message):
	user_id = message.from_user.id
	username = message.from_user.username
	if message.chat.type== "private":




				

		db_object.execute(f"SELECT id FROM users WHERE id = {user_id}")
	    
		result = db_object.fetchone()

	    

		if not result:
			db_object.execute("INSERT INTO users(id, username) VALUES (%s, %s)", (user_id, username))
			db_connection.commit()
			await bot.send_message(message.chat.id, f"السلام عليكم 🖐\n Welcome {username}\nYou have got 2 points for free",reply_markup=await gen_main_markup())
	  		
	  		
		else:
			await bot.send_message(message.chat.id, f"السلام عليكم 🖐\n Welcome {username}",reply_markup=await gen_main_markup())

  	

		   
		    

print("working..............")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=False)

  

    
     
	     		
