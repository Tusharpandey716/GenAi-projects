from fastapi import FastAPI
from pydantic import BaseModel
from transformers import pipeline
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Enable CORS for frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (set to frontend URL in production)
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, OPTIONS)
    allow_headers=["*"],  # Allow all headers
)

# Load the BioGPT model once (better performance)
print("Loading BioGPT model... This may take a few minutes.")
bio_gpt = pipeline("text-generation", model="microsoft/biogpt")
print("BioGPT model loaded successfully!")

# Request Model
class QueryRequest(BaseModel):
    question: str

@app.post("/query/")
async def query_disease(request: QueryRequest):
    response = bio_gpt(request.question, max_length=200, do_sample=True)
    generated_text = response[0]['generated_text'].strip()
    return {"response": generated_text}
