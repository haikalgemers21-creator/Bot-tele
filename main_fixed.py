import random
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes, filters, MessageHandler

TOKEN = "8792762407:AAHHP3bTh-J5AM-I5daqMgAoQ-6yjkq5sGk"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = "🎮 Bot Game\n\n/dice - Tebak angka 1-6\n/rock - Rock Paper Scissors"
    await update.message.reply_text(text)

async def dice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    answer = random.randint(1, 6)
    context.user_data["dice"] = answer
    await update.message.reply_text("🎲 Angka sudah dipilih!\nKetik: /guess 1 (sampai 6)")

async def guess(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        user_guess = int(update.message.text.split()[1])
        answer = context.user_data.get("dice", 0)
        if user_guess == answer:
            await update.message.reply_text(f"🎉 BENAR! Angkanya {answer}")
        else:
            await update.message.reply_text(f"❌ SALAH! Angkanya {answer}")
    except:
        await update.message.reply_text("Format: /guess <angka>")

async def rock(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🪨 Batu", callback_data="r_rock"),
         InlineKeyboardButton("📄 Kertas", callback_data="r_paper"),
         InlineKeyboardButton("✂️ Gunting", callback_data="r_scissors")]
    ]
    await update.message.reply_text("Pilih:", reply_markup=InlineKeyboardMarkup(keyboard))

async def rock_choice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    choice_map = {
        "r_rock": "🪨",
        "r_paper": "📄",
        "r_scissors": "✂️"
    }
    
    user_emoji = choice_map[query.data]
    bot_emoji = random.choice(["🪨", "📄", "✂️"])
    
    if user_emoji == bot_emoji:
        result = "🤝 Seri!"
    elif (user_emoji == "🪨" and bot_emoji == "✂️") or \
         (user_emoji == "📄" and bot_emoji == "🪨") or \
         (user_emoji == "✂️" and bot_emoji == "📄"):
        result = "🎉 Menang!"
    else:
        result = "😢 Kalah!"
    
    await query.edit_message_text(f"Kamu: {user_emoji} | Bot: {bot_emoji}\n\n{result}")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if "/guess" in update.message.text:
        await guess(update, context)

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("dice", dice))
    app.add_handler(CommandHandler("rock", rock))
    app.add_handler(CallbackQueryHandler(rock_choice, pattern="^r_"))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("Bot running...")
    app.run_polling()

if __name__ == "__main__":
    main()
