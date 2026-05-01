from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

TOKEN = "8750506693:AAHnFP662n3fLbp-6SIBC726SqED9JyFITI"
ADMIN_ID = 5754662713
CHANNEL_USERNAME = "@blinchykiVisual"


def is_english(text):
    allowed = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_-. "
    return 2 <= len(text) <= 30 and all(c in allowed for c in text)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("📢 Subscribe", url="https://t.me/blinchykiVisual")],
        [InlineKeyboardButton("✅ Check subscription", callback_data="check")]
    ]

    await update.message.reply_text(
        "To get a watermark, subscribe first:\n"
        "https://t.me/blinchykiVisual\n\n"
        "Then press Check subscription.",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id

    if query.data == "check":
        try:
            member = await context.bot.get_chat_member(CHANNEL_USERNAME, user_id)
            status = member.status

            await query.message.reply_text(f"DEBUG STATUS: {status}")

            if status not in ["member", "administrator", "creator"]:
                await query.message.reply_text(
                    "❌ You are NOT subscribed.\n"
                    "Subscribe and press Check subscription again."
                )
                return

            context.user_data["waiting_for_nick"] = True

            await query.message.reply_text(
                "✅ Subscription confirmed!\n\n"
                "Send your nickname in English only.\n"
                "Example: blinchyki"
            )

        except Exception as e:
            await query.message.reply_text(
                "❌ Subscription check error:\n"
                f"{e}"
            )
            print("CHECK ERROR:", e)


async def get_nick(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.user_data.get("waiting_for_nick"):
        await update.message.reply_text("Press /start first.")
        return

    nick = update.message.text.strip()
    user = update.message.from_user

    if not is_english(nick):
        await update.message.reply_text(
            "❌ English only.\n"
            "Allowed: A-Z, numbers, space, _ - ."
        )
        return

    username = f"@{user.username}" if user.username else "no username"

    await update.message.reply_text("Order accepted ✅")

    await context.bot.send_message(
        chat_id=ADMIN_ID,
        text=(
            "🔥 New watermark order\n\n"
            f"Nick: {nick}\n"
            f"User: {username}\n"
            f"User ID: {user.id}"
        )
    )

    context.user_data["waiting_for_nick"] = False


app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, get_nick))

print("Bot started...")
app.run_polling()