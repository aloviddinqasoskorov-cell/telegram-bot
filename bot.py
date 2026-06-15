from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes, ConversationHandler

BOT_TOKEN = "8851137625:AAHsN3NzRZ9mmV025TG8My8b1c9YZUBoFrM"
ADMIN_ID = 6237578156  # Sizning Telegram ID ingiz

ISM, TELEFON = range(2)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    tugmalar = [
        [InlineKeyboardButton("💰 Narxlar", callback_data="narx")],
        [InlineKeyboardButton("📞 Aloqa", callback_data="aloqa")],
        [InlineKeyboardButton("🛒 Buyurtma berish", callback_data="buyurtma")],
    ]
    markup = InlineKeyboardMarkup(tugmalar)
    await update.message.reply_text("Salom! Nima kerak?", reply_markup=markup)

async def tugma_bosildi(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "narx":
        await query.edit_message_text("💰 Narxlar:\n\nOddiy bot: 500,000 so'm\nDo'kon boti: 1,000,000 so'm")
    elif query.data == "aloqa":
        await query.edit_message_text("📞 Aloqa: @Abdumuminovsalohiddin")
    elif query.data == "buyurtma":
        await query.edit_message_text("Ismingizni yozing:")
        return ISM

async def ism_olish(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["ism"] = update.message.text
    await update.message.reply_text("Telefon raqamingizni yozing:")
    return TELEFON

async def telefon_olish(update: Update, context: ContextTypes.DEFAULT_TYPE):
    ism = context.user_data["ism"]
    telefon = update.message.text
    await update.message.reply_text("✅ Buyurtmangiz qabul qilindi! Tez orada bog'lanamiz.")
    await context.bot.send_message(
        chat_id=ADMIN_ID,
        text=f"🛒 Yangi buyurtma!\n\n👤 Ism: {Salohiddin}\n📞 Telefon: {970602530}"
    )
    return ConversationHandler.END

app = Application.builder().token(BOT_TOKEN).build()

conv_handler = ConversationHandler(
    entry_points=[CallbackQueryHandler(tugma_bosildi)],
    states={
        ISM: [MessageHandler(filters.TEXT & ~filters.COMMAND, ism_olish)],
        TELEFON: [MessageHandler(filters.TEXT & ~filters.COMMAND, telefon_olish)],
    },
    fallbacks=[CommandHandler("start", start)],
)

app.add_handler(CommandHandler("start", start))
app.add_handler(conv_handler)
print("Bot ishga tushdi!")
app.run_polling()