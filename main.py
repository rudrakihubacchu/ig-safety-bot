import logging
import os
import sys
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, ContextTypes, CallbackQueryHandler

# --- CONFIGURATION ---
# This pulls the token from Railway's 'Variables' tab
BOT_TOKEN = os.getenv("BOT_TOKEN")

if not BOT_TOKEN:
    print("❌ ERROR: BOT_TOKEN variable is missing in Railway/Environment!")
    sys.exit(1)

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# --- UI COMPONENTS ---
def main_menu_keyboard():
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
    return InlineKeyboardMarkup(keyboard)

# --- HANDLERS ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Sends the main dashboard."""
    text = "🚀 **Instagram Anti-Ban Console**\n\nUse these tools to rotate your digital footprint and stay safe from AI detection."
    if update.message:
        await update.message.reply_text(text, reply_markup=main_menu_keyboard(), parse_mode="Markdown")
    else:
        await update.callback_query.edit_message_text(text, reply_markup=main_menu_keyboard(), parse_mode="Markdown")

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handles all button logic."""
    query = update.callback_query
    await query.answer()

    if query.data == 'ip_refresh':
        msg = (
            "🔄 **IP REFRESH PROTOCOL**\n\n"
            "1. Switch to **Mobile Data** (Off Wi-Fi).\n"
            "2. **Airplane Mode ON** for 10 seconds.\n"
            "3. **Airplane Mode OFF**.\n\n"
            "Your IP has been rotated. Instagram now sees a fresh connection."
        )
    elif query.data == 'clean_device':
        msg = (
            "🧹 **DEVICE CLEANUP**\n\n"
            "• **Android:** Settings > Apps > Instagram > Clear Cache.\n"
            "• **iOS:** Settings > General > iPhone Storage > Instagram > Offload App.\n"
            "• **Desktop:** Clear cookies for `instagram.com`."
        )
    elif query.data == 'link_identity':
        msg = (
            "🔗 **IDENTITY TRUST**\n\n"
            "Connect an aged Facebook or WhatsApp Business account in your 'Accounts Center'. "
            "This significantly lowers the chance of a 'Bot Reason' suspension."
        )
    else:
        return

    back_btn = InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ Back to Menu", callback_data='back_to_menu')]])
    await query.edit_message_text(text=msg, parse_mode="Markdown", reply_markup=back_btn)

# --- APP STARTUP ---
def main():
    application = Application.builder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(start, pattern='^back_to_menu$'))
    application.add_handler(CallbackQueryHandler(button_handler))

    print("✅ Bot is running...")
    application.run_polling()

if __name__ == "__main__":
    main()
            
