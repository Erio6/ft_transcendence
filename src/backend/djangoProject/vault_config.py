import hvac
from dotenv import load_dotenv
import os

load_dotenv()

def get_db_credentials():
    client = hvac.Client(
        url='http://vault:8200',
        token=os.getenv('VAULT_TOKEN')
    )

    return client.secrets.kv.v2.read_secret_version(
        path='database/credentials'
    )['data']['data']
