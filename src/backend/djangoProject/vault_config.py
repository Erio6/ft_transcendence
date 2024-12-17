import hvac
from dotenv import load_dotenv
import os

load_dotenv()

def get_db_credentials():
    client = hvac.Client(
        url='http://127.0.0.1:8200',
        token=os.getenv('VAULT_TOKEN')
    )

    return client.secrets.kv.v2.read_secret_version(
        path='database/credentials'
    )['data']['data']
