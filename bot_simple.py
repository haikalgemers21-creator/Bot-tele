import requests
import random
import subprocess
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, ContextTypes, filters

TOKEN = "8792762407:AAHHP3bTh-J5AM-I5daqMgAoQ-6yjkq5sGk"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = """🎮 Bot Game & Download

/dice - Tebak angka 1-6
/rock - Rock Paper Scissors
/download <URL> - Download TikTok/YouTube/Instagram
    
Contoh: /download https://www.tiktok.com/video/xxxxx"""
    await update.message.reply_text(text)

async def dice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    answer = random.randint(1, 6)
    context.user_data["dice"] = answer
    await update.message.reply_text("🎲 Angka sudah dipilih!\n\nKetik: /guess <angka>")

async def guess(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        user_guess = int(update.message.text.split()[1])
        answer = context.user_data.get("dice")
        if user_guess == answer:
            await update.message.reply_text(f"🎉 BENAR! Angkanya {answer}")
        else:
            await update.message.reply_text(f"❌ SALAH! Angkanya {answer}")
    except:
        await update.message.reply_text("Format: /guess <angka>")

async def rock(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🪨", callback_data="rock_r"),
         InlineKeyboardButton("📄", callback_data="rock_p"),
         InlineKeyboardButton("✂️", callback_data="rock_s")]
    ]
    await update.message.reply_text("Pilih:", reply_markup=InlineKeyboardMarkup(keyboard))

async def rock_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    choice = {"rock_r": "🪨", "rock_p": "📄", "rock_s": "✂️"}
    user = choice[query.data]
    bot = random.choice(["🪨", "📄", "✂️"])
    
    if user == bot:
        result = "🤝 Seri!"
    elif (user == "🪨" and bot == "✂️") or (user == "📄" and bot == "🪨") or (user == "✂️" and bot == "📄"):
        result = "🎉 Menang!"
    else:
        result = "😢 Kalah!"
    
    await query.edit_message_text(f"Kamu: {user} | Bot: {bot}\n\n{result}")

async def download(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        url = update.message.text.replace("/download ", "").strip()
        await update.message.reply_text("⏳ Downloading...")
        
        cmd = ["yt-dlp", "-f", "best", "-o", "/tmp/vid.%(ext)s", url]
        subprocess.run(cmd, timeout=30, capture_output=True)
        
        if os.path.exists("/tmp/vid.mp4"):
            with open("/tmp/vid.mp4", "rb") as f:
                await update.message.reply_document(f)
            os.remove("/tmp/vid.mp4")
        elif os.path.exists("/tmp/vid.webm"):
            with open("/tmp/vid.webm", "rb") as f:
                await update.message.reply_document(f)
            os.remove("/tmp/vid.webm")
        else:
            await update.message.reply_text("❌ Download gagal")
    except Exception as e:
        await update.message.reply_text(f"❌ Error: {str(e)[:50]}")

async def handle_msg(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if "/guess" in update.message.text:
        await guess(update, context)

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("dice", dice))
    app.add_handler(CommandHandler("rock", rock))
    app.add_handler(CommandHandler("download", download))
    app.add_handler(CallbackQueryHandler(rock_callback, pattern="^rock_"))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_msg))
    print("Bot running...")
    app.run_polling()

if __name__ == "__main__":
    main()
