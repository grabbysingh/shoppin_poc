import requests
from os import getenv

from app.core.config import *

url = "https://r.jina.ai/https://www.amazon.in/"
headers = {
	"Authorization": "Bearer " + str(JINA_API_KEY)
}

response_jina = requests.get(url, headers=headers)
