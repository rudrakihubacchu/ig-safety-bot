import logging
import os
import sys
import httpx  # You'll need to run: pip install httpx
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, ContextTypes, CallbackQueryHandler

# --- CONFIGURATION ---
BOT_TOKEN = os.getenv("BOT_TOKEN")

if not BOT_TOKEN:
    print("❌ ERROR: BOT_TOKEN variable is missing!")
    sys.exit(1)

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# --- UTILS ---
async def get_public_ip():
    """Fetches the current public IP of the requester."""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get("https://api.ipify.org?format=json")
            return response.json().get("ip")
    except Exception:
        return "Unable to fetch IP"

# --- UI COMPONENTS ---
def main_menu_keyboard():
    keyboard = [
        [
            InlineKeyboardButton("🔄 IP Refresh & Check", callback_data='ip_refresh'),
            InlineKeyboardButton("🧹 Clean Device", callback_data='clean_device')
        ],
        [
            # Masked Link: Using a redirector or Meta's own internal routing
            InlineKeyboardButton("🔗 Secure Link Identity", url="https://l.instagram.com/?u=https://accountscenter.instagram.com/"),
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
    text = "🚀 **Instagram Anti-Ban Console**\n\nUse these tools to rotate your digital footprint and stay safe."
    if update.message:
        await update.message.reply_text(text, reply_markup=main_menu_keyboard(), parse_mode="Markdown")
    else:
        await update.callback_query.edit_message_text(text, reply_markup=main_menu_keyboard(), parse_mode="Markdown")

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == 'ip_refresh':
        # Logic: We provide the instruction + a real-time check
        current_ip = await get_public_ip()
        msg = (
            "🔄 **IP REFRESH PROTOCOL**\n\n"
            f"📍 **Current Detection:** `{current_ip}`\n\n"
            "1. Switch to **Mobile Data**.\n"
            "2. **Airplane Mode ON** (10 seconds).\n"
            "3. **Airplane Mode OFF**.\n\n"
            "**Note:** To see the change, click 'IP Refresh' again after toggling."
        )
    elif query.data == 'clean_device':
        msg = (
            "🧹 **DEVICE CLEANUP**\n\n"
            "• **Android:** Settings > Apps > Instagram > Clear Cache.\n"
            "• **iOS:** Settings > General > iPhone Storage > Instagram > Offload App."
        )
    else:
        return

    back_btn = InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ Back to Menu", callback_data='back_to_menu')]])
    await query.edit_message_text(text=msg, parse_mode="Markdown", reply_markup=back_btn)

def main():
    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(start, pattern='^back_to_menu$'))
    application.add_handler(CallbackQueryHandler(button_handler))
    print("✅ Bot is running...")
    application.run_polling()

if __name__ == "__main__":
    main()
