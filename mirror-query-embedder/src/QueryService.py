from fastapi import FastAPI, Request

from TextVectoriser import TextVectoriser

QUERY_KEY = 'query'
embedding_model = TextVectoriser("../models/sup-simcse-roberta-base")

def get_embedding(data_list):
    return embedding_model.compute_vector(data_list)



app = FastAPI()
@app.post("/embed_query")
async def embed_query(request: Request):
    raw_query = await request.json()
    query = raw_query[QUERY_KEY]
    
    print(type(get_embedding([query]).cpu().detach().numpy()))
    return {"embed_query":get_embedding([query]).tolist()}
    
