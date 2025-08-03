from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

main = ReplyKeyboardMarkup(keyboard= [[KeyboardButton (text = 'Leave a message⚙️')]],
                                             resize_keyboard=True, 
                                             input_field_placeholder='Press to the button...',
                                             one_time_keyboard= True)

admin = ReplyKeyboardMarkup(keyboard= [[KeyboardButton (text = 'Answer to the message')]],
                                             resize_keyboard=True, 
                                             input_field_placeholder='Press the button...',
                                             one_time_keyboard= True)