import logging
from aiogram import Bot, Dispatcher
import os
from dotenv import load_dotenv
from aiogram.fsm.storage.memory import MemoryStorage

load_dotenv()
storage = MemoryStorage()
API_TOKEN = os.getenv('TOKEN')

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Initialize bot with os and dispatcher
Bot = Bot(token=API_TOKEN, parse_mode="HTML")
dp = Dispatcher(storage=MemoryStorage())