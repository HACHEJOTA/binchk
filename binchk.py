import telebot
import requests

from colorama import init, Fore, Style

def main():
    # Inicializar colorama
    init(autoreset=True)
    
    # Solicitar el token al usuario
    print(Fore.YELLOW + Style.BRIGHT + "Por favor, introduce tu token de Telegram:")
    TOKEN = input(Fore.GREEN + Style.BRIGHT + "> ")

    bot = telebot.TeleBot(TOKEN)
    
    
# URL base de la API de lookup.binlist.net
API_URL = 'https://lookup.binlist.net/'

# Inicializar el bot
bot = telebot.TeleBot(TOKEN)

# Manejador de comando '/start'
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "¡Hola! Envía el comando /bin seguido del número de BIN para obtener información sobre él.")

# Manejador de comando '/bin'
@bot.message_handler(commands=['bin'])
def lookup_bin_command(message):
    try:
        bin_number = message.text.split(' ', 1)[1].strip()
        if bin_number.isdigit() and len(bin_number) >= 6:
            response = requests.get(API_URL + bin_number)
            if response.status_code == 200:
                data = response.json()
                country = data.get('country', {}).get('name', 'Desconocido')
                brand = data.get('brand', 'Desconocido')
                scheme = data.get('scheme', 'Desconocido')
                bank = data.get('bank', {}).get('name', 'Desconocido')
                flag = data.get('country', {}).get('emoji', '🌍')
                reply_text = f"𝙱𝙸𝙽: {bin_number}\n━━━━━━━━━━━━━\n𝙿𝙰𝙸𝚂: {country}\n𝙱𝙰𝙽𝙳𝙴𝚁𝙰: {flag}\n𝙼𝙰𝚁𝙲𝙰: {brand}\n𝚃𝙸𝙿𝙾: {scheme}\n𝙱𝙰𝙽𝙲𝙾: {bank}\n━━━━━━━━━━━━━"
                bot.reply_to(message, reply_text)
            else:
                bot.reply_to(message, "Error al obtener información del BIN. Inténtalo de nuevo más tarde.")
        else:
            bot.reply_to(message, "Por favor, introduce un número de BIN válido.")
    except IndexError:
        bot.reply_to(message, "Por favor, proporciona un número de BIN después del comando /bin.")

# Ejecutar el bot
bot.polling()
