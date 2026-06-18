import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes, ConversationHandler

logging.basicConfig(level=logging.INFO)

BOT_TOKEN = "8851137625:AAHsN3NzRZ9mmV025TG8My8b1c9YZUBoFrM"
ADMIN_ID = 6237578156

ISM, TELEFON = range(2)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    tugmalar = [
        [InlineKeyboardButton("💰 Narxlar", callback_data="narx")],
        [InlineKeyboardButton("📞 Aloqa", callback_data="aloqa")],
        [InlineKeyboardButton("🛒 Buyurtma", callback_data="buyurtma")],
    ]
    await update.message.reply_text("Salom! Quyidagilardan birini tanlang:", reply_markup=InlineKeyboardMarkup(tugmalar))

async def narx(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.edit_message_text("💰 Narx: 100,000 so'mdan")

async def aloqa(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.edit_message_text("📞 Aloqa: @Abdumuminovsalohiddin")

async def buyurtma_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.edit_message_text("🛒 Ismingizni yozing:")
    return ISM

async def ism_olish(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["ism"] = update.message.text
    await update.message.reply_text("📱 Telefon raqamingizni yozing:")
    return TELEFON

async def telefon_olish(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        await context.bot.send_message(chat_id=ADMIN_ID, text=f"🛒 Yangi buyurtma!\n👤 Ism: {context.user_data['ism']}\n📞 Tel: {update.message.text}")
    except Exception as e:
        logging.error(e)
    await update.message.reply_text("✅ Buyurtmangiz qabul qilindi!")
    return ConversationHandler.END

conv = ConversationHandler(
    entry_points=[CallbackQueryHandler(buyurtma_start, pattern="^buyurtma$")],
    states={
        ISM: [MessageHandler(filters.TEXT & ~filters.COMMAND, ism_olish)],
        TELEFON: [MessageHandler(filters.TEXT & ~filters.COMMAND, telefon_olish)],
    },
    fallbacks=[CommandHandler("start", start)],
)

app = Application.builder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(narx, pattern="^narx$"))
app.add_handler(CallbackQueryHandler(aloqa, pattern="^aloqa$"))
app.add_handler(conv)
app.run_polling()
