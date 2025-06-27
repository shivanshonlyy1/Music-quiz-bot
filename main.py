from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext
import random
import logging

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

# BOT TOKEN
TOKEN = '7744319812:AAFgV1kp2FCwNOQxrDuMfv_HLbBDDUoWwi0'

# 🎶 Quiz Data
quiz_data = [
    {
        "song": "Tum Hi Ho",
        "options": ["Aashiqui 2", "Dilwale", "Tamasha", "Yeh Jawaani Hai Deewani"],
        "answer": "Aashiqui 2"
    },
    {
        "song": "Tujh Mein Rab Dikhta Hai",
        "options": ["Rab Ne Bana Di Jodi", "Dilwale", "Kal Ho Na Ho", "Ae Dil Hai Mushkil"],
        "answer": "Rab Ne Bana Di Jodi"
    },
    {
        "song": "Channa Mereya",
        "options": ["Ae Dil Hai Mushkil", "Tamasha", "Barfi", "Rockstar"],
        "answer": "Ae Dil Hai Mushkil"
    },
    {
        "song": "Ajeeb Dastan Hai Yeh",
        "options": ["Dil Apna Aur Preet Parai", "Kati Patang", "Guide", "Aradhana"],
        "answer": "Dil Apna Aur Preet Parai"
    },
    {
        "song": "Lag Ja Gale",
        "options": ["Woh Kaun Thi", "Guide", "Padosan", "Teesri Manzil"],
        "answer": "Woh Kaun Thi"
    }
    # 👉 Add more here easily
]

# 🔥 Score Dictionaries
user_scores = {}
daily_scores = {}

# 🎯 Start Command
def start(update: Update, context: CallbackContext):
    update.message.reply_text(
        "🎶 Hey there!\n\nThis is a music quiz bot. 🎧\n\nTo get a random question type /guess\nType /help to see all available commands."
    )

# 🎵 Guess Command
def guess(update: Update, context: CallbackContext):
    question = random.choice(quiz_data)
    song = question['song']
    options = question['options']
    random.shuffle(options)

    keyboard = [
        [InlineKeyboardButton(opt, callback_data=f"{opt}|{question['answer']}")] for opt in options
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text(
        f"🎵 Song: *{song}*\n\n👉 Can you guess the movie name?",
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

# 🎯 Button Handling
def button(update: Update, context: CallbackContext):
    query = update.callback_query
    user = query.from_user
    query.answer()

    selected, correct = query.data.split('|')

    if user.id not in user_scores:
        user_scores[user.id] = 0
    if user.id not in daily_scores:
        daily_scores[user.id] = 0

    if selected == correct:
        user_scores[user.id] += 1
        daily_scores[user.id] += 1
        query.edit_message_text(
            text=f"✅ Correct {user.first_name}! 🎉\n+1 Point 🥳"
        )
    else:
        user_scores[user.id] -= 1
        daily_scores[user.id] -= 1
        query.edit_message_text(
            text=f"❌ Wrong {user.first_name}! 😢\n✅ Correct answer was *{correct}*\n-1 Point 🙈",
            parse_mode='Markdown'
        )

# 🏆 Leaderboard
def leaderboard(update: Update, context: CallbackContext):
    if not user_scores:
        update.message.reply_text("No scores yet! 😅")
        return
    leaderboard_text = "🏆 *Leaderboard (All Time)* 🏆\n\n"
    sorted_users = sorted(user_scores.items(), key=lambda x: x[1], reverse=True)

    for rank, (user_id, score) in enumerate(sorted_users, start=1):
        try:
            user = context.bot.get_chat(user_id)
            leaderboard_text += f"{rank}. {user.first_name} — {score} points\n"
        except:
            leaderboard_text += f"{rank}. Unknown — {score} points\n"

    update.message.reply_text(leaderboard_text, parse_mode='Markdown')

# 🌟 Top 10 Daily
def top10(update: Update, context: CallbackContext):
    if not daily_scores:
        update.message.reply_text("No scores today! 😅")
        return
    top10_text = "🌟 *Top 10 (Today)* 🌟\n\n"
    sorted_users = sorted(daily_scores.items(), key=lambda x: x[1], reverse=True)[:10]

    for rank, (user_id, score) in enumerate(sorted_users, start=1):
        try:
            user = context.bot.get_chat(user_id)
            top10_text += f"{rank}. {user.first_name} — {score} points\n"
        except:
            top10_text += f"{rank}. Unknown — {score} points\n"

    update.message.reply_text(top10_text, parse_mode='Markdown')

# 🏗️ Main Function
def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler('guess', guess))
    dp.add_handler(CommandHandler('leaderboard', leaderboard))
    dp.add_handler(CommandHandler('top10', top10))
    dp.add_handler(CallbackQueryHandler(button))

    updater.start_polling()
    print("🤖 Bot is running... ✅")
    updater.idle()

if __name__ == '__main__':
    main()