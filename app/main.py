from typing import List, Dict
from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
 
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

model = SentenceTransformer('paraphrase-mpnet-base-v2')

def get_similarities(headline: str, sentences: list):
    sentences.insert(0, headline)
    embeddings = model.encode(sentences)
    
    return cosine_similarity([embeddings[0]], embeddings[0:])[0]
    
class SentimentRequest(BaseModel):
    headline: str
    sentences: List[str]
 
class SentimentResponse(BaseModel): 
    # similarities: List[float]
    similarities: Dict[str, Dict[str, float]]

@app.get("/")
async def root():
    return {"message": "Sentence similarity"}
    
@app.post("/predict", response_model=SentimentResponse)
def predict(request: SentimentRequest):
    similarities = get_similarities(request.headline, request.sentences).tolist()

    response = {}
    dist_dict = {}
    for i, s in enumerate(request.sentences):
        dist_dict[s] = similarities[i]
    dist_dict.pop(request.headline, None)
    response[request.headline] = dist_dict
    
    return SentimentResponse(
        similarities=response
    )