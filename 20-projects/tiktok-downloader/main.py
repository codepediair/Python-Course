import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler
import requests
import re
import os
from dotenv import load_dotenv

# initializing .env file
load_dotenv()

# List of required channel usernames (without '@')
REQUIRED_CHANNELS = ['Scary_Horror', 'prsianmovies', 'dark_theori']

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Telegram Bot Token
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# TikTok API URL
API_URL = os.getenv("API_URL")
headers = {
    "accept": "application/json"
}

# Tiktok URL pattern
TIKTOK_URL_PATTERN = r'(https?://.*tiktok\.com/.*)'

async def is_user_member(user_id: int, bot: ContextTypes.DEFAULT_TYPE.bot) -> bool:
    """Check if the user is a member of all required channels."""
    for channel in REQUIRED_CHANNELS:
        try:
            member = await bot.get_chat_member(chat_id=f"@{channel}", user_id=user_id)
            if member.status not in ['member', 'administrator', 'creator']:
                return False
        except Exception as e:
            logging.error(f"Error checking membership for channel @{channel}: {e}")
            return False
    return True

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a message when the command /start is issued."""
    user_id = update.message.chat.id
    if not await is_user_member(user_id, context.bot):
        # Create inline keyboard with channel links and a "Check Membership" button
        keyboard = [
            [InlineKeyboardButton(f"عضویت در @{channel}", url=f"https://t.me/{channel}") for channel in REQUIRED_CHANNELS],
            [InlineKeyboardButton("بررسی عضویت", callback_data="check_membership")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await update.message.reply_text(
            "برای استفاده از ربات، ابتدا باید در کانال‌های زیر عضو شوید:",
            reply_markup=reply_markup
        )
        return
    await update.message.reply_text('سلام به دانلودر تیک تاک پرشین خوش آمدید!\n\nهر فایلی از تیک تاک که میخواید اینجا قابل دانلود است.\n\nلینک ویدیو رو برام بفرستید تا براتون دانلود کنم.\n\nمثلا: vm.tiktok.com')

async def check_membership_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle the 'Check Membership' button click."""
    query = update.callback_query
    user_id = query.from_user.id

    # Check membership again
    if await is_user_member(user_id, context.bot):
        await query.answer("عضویت شما تایید شد!", show_alert=True)
        await query.edit_message_text("شما اکنون می‌توانید از ربات استفاده کنید.")
    else:
        await query.answer("هنوز در کانال‌ها عضو نشده‌اید!", show_alert=True)

# async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     await update.message.reply_text('Just send me a TikTok URL (e.g., vm.tiktok.com/xxx or tiktok.com/@user/xxx)')

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message.text
    user = update.effective_user

    if re.match(TIKTOK_URL_PATTERN, message):
        loading_msg = await update.message.reply_text("در حال پردازش ⌛")
        try:
            params = {"url": message}
            response = requests.get(API_URL, params=params, headers=headers)
            video_url = response.json().get('video').get('noWatermark')

            if video_url:
                await loading_msg.edit_text("در حال دانلود ویدیو ⌛")
                video_content = requests.get(video_url).content
                # Send video to user
                await update.message.reply_video(video=video_content, caption="ویدئوی تیک تاک شما آماده است!")
            else:
                await loading_msg.edit_text("متاسفانه ویدیو پیدا نشد")
        except Exception as e:
            loading_msg.edit_text("متاسفانه مشکلی رخ داده است")
        
    else:
        await update.message.reply_text('لطفا یک لینک صحیح تیک تاک ارسال کنید.\n\nمثلا: vm.tiktok.com/xxx یا tiktok.com/@user/xxx')

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(check_membership_callback, pattern="check_membership"))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    app.run_polling()

if __name__ == '__main__':
    main()