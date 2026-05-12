import logging
import os
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, ContextTypes, CallbackQueryHandler

# Railway will look for this variable in the 'Variables' tab
# If running locally, you can replace os.environ.get with your string "8250192946:AAGR8..."
BOT_TOKEN = os.environ.get( "8250192946:AAGR8rWvqg4qW4bJxfbTS1aq74CcBmo6HNA")

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
    
    message_text = "🚀 **Instagram Anti-Ban Console**\n\nYour token is active. Use these tools to protect your ID from bot-detection."
    
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
            "1. Switch to **Mobile Data**.\n"
            "2. Turn **Airplane Mode ON** for 10 seconds.\n"
            "3. Turn it OFF to get a fresh IP address.\n\n"
            "This makes your actions look like they are coming from a new user."
        )
    
    elif query.data == 'clean_device':
        text = (
            "🧹 **Device Cleanup**\n\n"
            "• **Android:** Clear IG Cache & Force Stop.\n"
            "• **iOS:** Offload and Reinstall IG app.\n"
            "• **Browser:** Clear all cookies for Instagram.com."
        )
    
    elif query.data == 'link_identity':
        text = (
            "🔗 **Identity Trust**\n\n"
            "Link a Facebook profile or WhatsApp Business number in your IG 'Accounts Center' to boost your human trust score."
        )

    back_keyboard = [[InlineKeyboardButton("⬅️ Back to Menu", callback_data='back_to_menu')]]
    await query.edit_message_text(text=text, parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(back_keyboard))

def main():
    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(start, pattern='^back_to_menu$'))
    application.add_handler(CallbackQueryHandler(button_handler))
    
    print("Bot is live with your token...")
    application.run_polling()

if __name__ == "__main__":
    main()
