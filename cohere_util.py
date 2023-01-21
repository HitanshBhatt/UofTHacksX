import os
import cohere
from dotenv import load_dotenv

load_dotenv()
COHERE_TOKEN = os.environ.get("cohere-token")
co = cohere.Client(COHERE_TOKEN)

RESOURCE_FILES = ['data/uoft.json']
ANNOY_NN_FILE = 'search.ann'


def embed(text, model='large', truncate='LEFT'):
    if not text:
        print("cohere_embed called with falsy value {}".format(text))
    if isinstance(text, str):
        return co.embed(texts=[text], model=model, truncate=truncate).embeddings[0]
    else:
        return co.embed(texts=text, model=model, truncate=truncate).embeddings
