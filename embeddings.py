from sentence_transformers import SentenceTransformer

model = None   # global

def get_embedding(text):
    global model

    try:
        if model is None:
            model = SentenceTransformer('all-MiniLM-L6-v2')  # load once

        return model.encode(text)

    except Exception as e:
        print("Embedding Error:", e)
        return [0]*384