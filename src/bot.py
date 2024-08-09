from telegram.ext import Updater, CommandHandler, ConversationHandler, MessageHandler, Filters
from engine import get_chiste, get_ips, get_hashes, get_endpoints, isolate_endpoints
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

def ioc(update, context):
    logger.info('Dialogo IOC')
    update.message.reply_text('Es necesario que me pases el mensaje para parsearlo.')
    return INPUT_TEXT

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

def cargar_ioc(update, context):
    logger.info('Comando /cargarioc recibido')
    
    # Verificar si se proporcionaron argumentos
    if context.args:
        # Unir todos los argumentos en un solo string y dividir por comas
        ioc_data = ' '.join(context.args)
        ioc_list = ioc_data.split(',')
        
        # Eliminar espacios en blanco alrededor de cada IP
        ioc_list = [ioc.strip() for ioc in ioc_list]
        
        # Variables para almacenar resultados
        direcciones_ip = []
        hashes = []
        
        # Procesar cada IoC en la lista
        for ioc in ioc_list:
            ips = get_ips(ioc)
            hs = get_hashes(ioc)
            if ips:
                direcciones_ip.extend(ips)
            if hs:
                hashes.extend(hs)
        
        # Responder al usuario con los resultados
        if direcciones_ip:
            logger.info(f'Direcciones IP procesadas: {direcciones_ip}')
            update.message.reply_text(f'Se recibieron las siguientes IPs: {direcciones_ip}')
        
        if hashes:
            logger.info(f'Hashes procesados: {hashes}')
            update.message.reply_text(f'Se recibieron los siguientes hashes: {hashes}')
        
        if not direcciones_ip and not hashes:
            update.message.reply_text('No se encontraron direcciones IP ni hashes en los datos proporcionados.')
    else:
        update.message.reply_text('Por favor, proporciona uno o más datos de IoC después del comando, por ejemplo: /cargarioc 192.168.2.3, 10.0.0.1')

def endpoint(update, context):
    logger.info('Dialogo ENDPOINT')
    update.message.reply_text('Es necesario que me pases el nombre del equipo que deseas aislar.')
    return TEXTO_ENDPOINTS

def isolate_endpoints_handler(update, context):
    logger.info('Se recibió el nombre del equipo para aislar')
    team_name = update.message.text
    lista_de_endpoints = [team_name]  # Aquí asumimos que el mensaje contiene el nombre del equipo directamente
    if lista_de_endpoints:
        response = isolate_endpoints(lista_de_endpoints)
        update.message.reply_text(f'Se solicitó el aislamiento del equipo. Respuesta de la API: {response}')
    else:
        update.message.reply_text('No se especificó ningún equipo para aislar.')
    return ConversationHandler.END

# Main del Programa
if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
    logger = logging.getLogger('AutomaticBot')

    # Llave API para conectarse a Telegram
    updater = Updater(token=os.getenv("TOKEN_TELEGRAM"), use_context=True)
    dp = updater.dispatcher

    # Handlers
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler('chiste', chiste))
    dp.add_handler(CommandHandler('cargarioc', cargar_ioc))
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

    updater.start_polling()
    updater.idle()
