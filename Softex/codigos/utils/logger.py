import logging
import os

if not os.path.exists("logs"):
    os.makedirs("logs")

logger = logging.getLogger("softex")
logger.setLevel(logging.INFO)

formato = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

handler_console = logging.StreamHandler()
handler_console.setFormatter(formato)
logger.addHandler(handler_console)

handler_arquivo = logging.FileHandler("logs/etl.log")
handler_arquivo.setFormatter(formato)
logger.addHandler(handler_arquivo)

def registrar_log(mensagem, nivel="info"):
    if nivel == "info":
        logger.info(mensagem)
    elif nivel == "error":
        logger.error(mensagem)
    elif nivel == "debug":
        logger.debug(mensagem)
    else:
        logger.info(mensagem)
