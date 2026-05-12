import logging
import time
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, ContextTypes, CallbackQueryHandler

# Replace with your actual Bot Token from @BotFather
BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [
            InlineKeyboardButton("🔄 IP Refresh", callback_data='ip_refresh'),
            InlineKeyboardButton("🧹 Clean Device", callback_data='clean_device')
        ],
        [
            InlineKeyboardButton("🔗 Link Identity", callback_data='link_identity'),
            InlineKeyboardButton("🛡️ Security Check", url="https://accountscenter.instagram.com/password_and_security/")
        ],
        [
            InlineKeyboardButton("🔥 Explore Niche", url="https://www.instagram.com/explore/tags/technology/"),
            InlineKeyboardButton("📊 Meta Suite", url="https://business.facebook.com/")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    # Check if this is a callback or a new command
    message_text = "🚀 **Instagram Anti-Ban Console (2026)**\n\nUse the buttons below to rotate your identity and stay invisible to AI detection."
    
    if update.message:
        await update.message.reply_text(message_text, reply_markup=reply_markup, parse_mode="Markdown")
    else:
        await update.callback_query.edit_message_text(message_text, reply_markup=reply_markup, parse_mode="Markdown")

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == 'ip_refresh':
        text = (
            "🔄 **IP REFRESH PROTOCOL**\n\n"
            "Instagram flags 'Static' or 'Blacklisted' IPs. Follow this to get a fresh one:\n\n"
            "1. **Switch to Mobile Data:** Never use Wi-Fi for this.\n"
            "2. **The 10-Second Cycle:** Turn on **Airplane Mode** for exactly 10 seconds.\n"
            "3. **Reconnect:** Turn it off. Your carrier will assign a brand new IP address.\n\n"
            "📍 **Check Success:** Go to [WhatIsMyIP](https://www.whatismyip.com/) before and after to confirm the address changed."
        )
    
    elif query.data == 'clean_device':
        text = "🧹 **Device Clean:** Clear IG Cache and Force Stop the app to remove session fingerprints."
    
    elif query.data == 'link_identity':
        text = "🔗 **Identity:** Link a verified Facebook or WhatsApp to increase your human 'Trust Score'."

    back_keyboard = [[InlineKeyboardButton("⬅️ Back to Menu", callback_data='back_to_menu')]]
    await query.edit_message_text(text=text, parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(back_keyboard), disable_web_page_preview=True)

def main():
    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(start, pattern='^back_to_menu$'))
    application.add_handler(CallbackQueryHandler(button_handler))
    
    print("Bot is running with IP Refresh logic...")
    application.run_polling()

if __name__ == "__main__":
    main()
