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
    elif isinstance(text, str):
        return co.embed(texts=[text], model=model, truncate=truncate).embeddings[0]
    else:
        return co.embed(texts=text, model=model, truncate=truncate).embeddings

def classify(text, model='large', preset=None):
    if not text:
        print("cohere_classify called with falsy value {}".format(text))
    elif isinstance(text, str):
        return co.classify([text], model, preset=preset).classifications[0]
    else:
        return co.classify(text, model, preset=preset).classifications
    
def generate(text, preset=None):
    if not text:
        print("cohere_classify called with falsy value {}".format(text))
    else:
        return co.generate(text, preset=preset, max_tokens=50, temperature=0.1, num_generations=1, k=20, end_sequences=['.']).generations[0].text