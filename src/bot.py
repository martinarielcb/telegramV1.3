from telegram.ext import Updater, CommandHandler, ConversationHandler, MessageHandler, Filters, CallbackContext
from engine import get_chiste, get_ips, get_hashes, get_endpoints, isolate_endpoints, procesar_sender, procesar_domain, procesar_url, procesar_ip, procesar_sha1, procesar_sha256
import logging, os

# Variables para los estados en la conversación
TEXTO_ENDPOINTS = 0
INPUT_TEXT = 0

# Funciones
def start(update, context):
    logger.info('He recibido un comando start')
    update.message.reply_text(f'¡Bienvenido al Actualizador de Compromisos {update.message.from_user.name}!')

def chiste(update, context):
    logger.info('Consultando API Chiste')
    update.message.reply_text(get_chiste())


# Funcion para cargar SHA256 separado por coma

def cargar_sha256(update: Update, context: CallbackContext) -> None:
    # Obtén el texto después del comando /sha256
    hashes = update.message.text[len('/sha256 '):]
    
    # Divide los hashes por coma y limpia espacios
    lista_hashes = [hash.strip() for hash in hashes.split(',')]
    
    # Llama a la función que maneja la carga de los hashes
    response = procesar_sha256(lista_hashes)
    
    # Envía el resultado al chat
    update.message.reply_text(f'Resultado de la carga de hashes: {response}')

# Función que se ejecuta al recibir el comando /sha1
def cargar_sha1(update: Update, context: CallbackContext) -> None:
    # Obtén el texto después del comando /sha1
    hashes = update.message.text[len('/sha1 '):]
    
    # Divide los hashes por coma y limpia espacios
    lista_hashes = [hash.strip() for hash in hashes.split(',')]
    
    # Llama a la función que maneja la carga de los hashes
    response = procesar_sha1(lista_hashes)
    
    # Envía el resultado al chat
    update.message.reply_text(f'Resultado de la carga de hashes: {response}')

# Función que se ejecuta al recibir el comando /ip
def cargar_ip(update: Update, context: CallbackContext) -> None:
    # Obtén el texto después del comando /ip
    ips = update.message.text[len('/ip '):]
    
    # Divide las IPs por coma y limpia espacios
    lista_ips = [ip.strip() for ip in ips.split(',')]
    
    # Llama a la función que maneja la carga de las IPs
    response = procesar_ip(lista_ips)
    
    # Envía el resultado al chat
    update.message.reply_text(f'Resultado de la carga de IPs: {response}')

# Función que se ejecuta al recibir el comando /url
def cargar_url(update: Update, context: CallbackContext) -> None:
    # Obtén el texto después del comando /url
    urls = update.message.text[len('/url '):]
    
    # Divide las URLs por coma y limpia espacios
    lista_urls = [url.strip() for url in urls.split(',')]
    
    # Llama a la función que maneja la carga de las URLs
    response = procesar_url(lista_urls)
    
    # Envía el resultado al chat
    update.message.reply_text(f'Resultado de la carga de URLs: {response}')

# Función que se ejecuta al recibir el comando /domain
def cargar_domain(update: Update, context: CallbackContext) -> None:
    # Obtén el texto después del comando /domain
    domains = update.message.text[len('/domain '):]
    
    # Divide los dominios por coma y limpia espacios
    lista_domains = [domain.strip() for domain in domains.split(',')]
    
    # Llama a la función que maneja la carga de los dominios
    response = procesar_domain(lista_domains)
    
    # Envía el resultado al chat
    update.message.reply_text(f'Resultado de la carga de dominios: {response}')

# Función que se ejecuta al recibir el comando /sender
def cargar_sender(update: Update, context: CallbackContext) -> None:
    # Obtén el texto después del comando /sender
    senders = update.message.text[len('/sender '):]
    
    # Divide las direcciones de correo por coma y limpia espacios
    lista_senders = [sender.strip() for sender in senders.split(',')]
    
    # Llama a la función que maneja la carga de los senders
    response = procesar_sender(lista_senders)
    
    # Envía el resultado al chat
    update.message.reply_text(f'Resultado de la carga de remitentes: {response}')

# Funcion para Aislar Equipos separado por coma

def aislar(update: Update, context: CallbackContext) -> None:
    # Obtén el texto después del comando /aislar
    equipos = update.message.text[len('/aislar '):]
    
    # Divide los nombres de equipos por coma y limpia espacios
    lista_equipos = [equipo.strip() for equipo in equipos.split(',')]
    
    # Llama a la función para aislar los equipos
    resultado = isolate_endpoints(lista_equipos)
    
    # Envía el resultado al chat
    update.message.reply_text(f'Resultado del aislamiento: {resultado}')

# Funcion para iniciar el comando /endpoints y pedir nombres de equipos
def endpoint(update: Update, context: CallbackContext) -> int:
    logger.info('Dialogo ENDPOINT')
    update.message.reply_text('Es necesario que me pases el nombre del equipo que deseas aislar.')
    return TEXTO_ENDPOINTS

# Funcion que recibe el nombre del equipo y lo aisla
def isolate_endpoints_handler(update: Update, context: CallbackContext) -> int:
    logger.info('Se recibio el nombre del equipo para aislar')
    team_name = update.message.text
    lista_de_endpoints = [team_name]  # Asumiendo que el mensaje contiene el nombre del equipo directamente

    if lista_de_endpoints:
        response = isolate_endpoints(lista_de_endpoints)
        update.message.reply_text(f'Se solicito el aislamiento del equipo. Respuesta de la API: {response}')
    else:
        update.message.reply_text('No se especifico ningun equipo para aislar.')

    # Finaliza la conversacion y resetea el estado
    return ConversationHandler.END

# Funcion para cargar indicadores de compromiso mediante conversacion, soporta SHA256 e IP
    # Comienza la conversacion con /ioc y nos pide que escribamos los indicadores
def ioc(update, context):
    logger.info('Dialogo IOC')
    update.message.reply_text('Es necesario que me pases el mensaje para parsearlo.')
    return INPUT_TEXT

    # Parsea el texto y determina cual es SHA256 y cual es IP
def update_ioc(update, context):
    logger.info('Se recibió el texto a parsear')
    text = update.message.text
    direcciones_ip = get_ips(text)
    hashes = get_hashes(text)
    if direcciones_ip:
        logger.info(f'Las Direcciones IP: {direcciones_ip}')
        update.message.reply_text(f'Se recibió el IoC, procederemos a aplicar los siguientes cambios. Direcciones IPs: {direcciones_ip}')
    if hashes:
        logger.info(f'Los Hash: {hashes}')
        update.message.reply_text(f'Se recibió el IoC, procederemos a aplicar los siguientes cambios. Hashes: {hashes}')
    return ConversationHandler.END

# Funcion que cancela la conversacion
def cancel(update: Update, context: CallbackContext) -> int:
    update.message.reply_text('Comando cancelado.', reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END

# Main del Programa
if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
    logger = logging.getLogger('AutomaticBot')

    # Llave API para conectarse a Telegram
    updater = Updater(token=os.getenv("TOKEN_TELEGRAM"), use_context=True)
    dp = updater.dispatcher

    # Handlers de los comandos
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler('chiste', chiste))
    dp.add_handler(CommandHandler("aislar", aislar))
    dp.add_handler(CommandHandler("sha256", cargar_sha256))
    dp.add_handler(CommandHandler("sha1", cargar_sha1))
    dp.add_handler(CommandHandler("ip", cargar_ip))
    dp.add_handler(CommandHandler("url", cargar_url))
    dp.add_handler(CommandHandler("domain", cargar_domain))
    dp.add_handler(CommandHandler("sender", cargar_sender))
    dp.add_handler(ConversationHandler(
        entry_points=[
            CommandHandler('ioc', ioc),
            CommandHandler('endpoint', endpoint)
        ],
        states={
            INPUT_TEXT: [MessageHandler(Filters.text & ~Filters.command, update_ioc)],
            TEXTO_ENDPOINTS: [MessageHandler(Filters.text & ~Filters.command, isolate_endpoints_handler)]
        },
        fallbacks=[]
    ))

#lineas que arrancan el bot
    updater.start_polling()
    updater.idle()
