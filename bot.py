import logging
import asyncio
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
        [InlineKeyboardButton("🛒 Buyurtma berish", callback_data="buyurtma")],
    ]
    await update.message.reply_text("Salom! Nima kerak?", reply_markup=InlineKeyboardMarkup(tugmalar))

async def tugma(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if query.data == "narx":
        await query.edit_message_text("💰 Narxlar:\nOddiy bot: 500,000 so'm\nDo'kon boti: 1,000,000 so'm")
    elif query.data == "aloqa":
        await query.edit_message_text("📞 Aloqa: @Abdumuminovsalohiddin")
    elif query.data == "buyurtma":
        await query.edit_message_text("Ismingizni yozing:")
        return ISM

async def ism(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["ism"] = update.message.text
    await update.message.reply_text("Telefon raqamingizni yozing:")
    return TELEFON

async def telefon(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        await context.bot.send_message(chat_id=ADMIN_ID, text=f"🛒 Yangi buyurtma!\n👤 Ism: {context.user_data['ism']}\n📞 Telefon: {update.message.text}")
    except Exception as e:
        logging.error(e)
    await update.message.reply_text("✅ Buyurtmangiz qabul qilindi!")
    return ConversationHandler.END

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    conv = ConversationHandler(
        entry_points=[CallbackQueryHandler(tugma)],
        states={
            ISM: [MessageHandler(filters.TEXT & ~filters.COMMAND, ism)],
            TELEFON: [MessageHandler(filters.TEXT & ~filters.COMMAND, telefon)],
        },
        fallbacks=[CommandHandler("start", start)],
    )
    app.add_handler(CommandHandler("start", start))
    app.add_handler(conv)
    print("Bot ishga tushdi!")
    app.run_polling()

if __name__ == "__main__":
    main()
