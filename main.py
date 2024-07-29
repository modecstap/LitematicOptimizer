from app import AiohttpApplication
from logger import Logger

if __name__ == '__main__':
    Logger.setup_logging()

    AiohttpApplication().run()
