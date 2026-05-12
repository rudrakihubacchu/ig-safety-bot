import logging
import os
import random
import asyncio
import httpx
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, ContextTypes, CallbackQueryHandler

# --- CONFIGURATION ---
BOT_TOKEN = os.getenv("BOT_TOKEN")

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# --- ANTI-BAN UTILS ---

def generate_safe_link(target_url):
    """
    Wraps links in a 'Referrer Shield'. 
    Uses Instagram's own internal redirector to mask the traffic source.
    """
    prefixes = [
        "https://l.instagram.com/?u=",
        "https://www.facebook.com/l.php?u=",
        "https://t.co/redirect?url="
    ]
    # Randomly select a redirector to break link fingerprinting patterns
    return f"{random.choice(prefixes)}{target_url}"

async def human_delay():
    """Simulates a human thinking/typing delay (1.5 to 4 seconds)."""
    await asyncio.sleep(random.uniform(1.5, 4.0))

# --- UI COMPONENTS ---
def main_menu_keyboard():
    # We use the safe link generator for the Identity button
    id_link = generate_safe_link("https://accountscenter.instagram.com/profiles")
    
    keyboard = [
        [
            InlineKeyboardButton("🔄 IP Refresh", callback_data='ip_refresh'),
            InlineKeyboardButton("🧹 Clean Device", callback_data='clean_device')
        ],
        [
            InlineKeyboardButton("🔗 Link Identity (Safe)", url=id_link),
            InlineKeyboardButton("🛡️ Audit Logins", callback_data='audit_logins')
        ],
        [
            InlineKeyboardButton("⚠️ Anti-Ban Tips", callback_data='anti_ban_rules'),
            InlineKeyboardButton("📊 Meta Suite", url="https://business.facebook.com/")
        ]
    ]
    return InlineKeyboardMarkup(keyboard)

# --- HANDLERS ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await human_delay() # Anti-bot: don't reply instantly
    text = "🚀 **Instagram Anti-Ban Console [v2.4]**\n\nProtective protocols active. Use the menu below to manage your digital footprint."
    
    if update.message:
        await update.message.reply_text(text, reply_markup=main_menu_keyboard(), parse_mode="Markdown")
    else:
        await update.callback_query.edit_message_text(text, reply_markup=main_menu_keyboard(), parse_mode="Markdown")

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await human_delay() # Randomize response time

    if query.data == 'ip_refresh':
        msg = (
            "🔄 **IP ROTATION PROTOCOL**\n\n"
            "• **Status:** Waiting for local toggle...\n"
            "• **Action:** Airplane Mode ON ✈️ -> Wait 10s -> Airplane Mode OFF.\n\n"
            "This forces your ISP to assign a new mobile IP, clearing 'Flagged IP' status."
        )
    elif query.data == 'anti_ban_rules':
        msg = (
            "🛡️ **STOP 'BOT REASON' BANS**\n\n"
            "1. **Action Limits:** Max 15-20 likes/follows per hour.\n"
            "2. **The 24h Rule:** If you get a 'Try Again Later', STOP all activity for 48 hours.\n"
            "3. **Vary Content:** Don't send the same DM to 10+ people. Change emojis & wording.\n"
            "4. **Aged Accounts:** Link a Facebook account that is at least 1 year old."
        )
    elif query.data == 'clean_device':
        msg = "🧹 **CACHE PURGE**\n\nGo to Settings > Apps > Instagram > Storage > **Clear Data**. \n\n*Warning: This logs you out but clears all tracking tokens.*"
    else: return

    back_btn = InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ Back", callback_data='back_to_menu')]])
    await query.edit_message_text(text=msg, parse_mode="Markdown", reply_markup=back_btn)

# --- APP STARTUP ---
def main():
    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(start, pattern='^back_to_menu$'))
    application.add_handler(CallbackQueryHandler(button_handler))
    application.run_polling()

if __name__ == "__main__":
    main()
