from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from typing import List
import os
import shutil
from backend.vec import rele_data, get_content
from backend.llm import get_response

app = FastAPI()

BASE_DIR = "uploads"

vector_retriever= None

counter=0

@app.post("/upload/")
async def upload_files(name: str, files: List[UploadFile] = File(...)):
    collection_dir = os.path.join(BASE_DIR, name)
    if not os.path.exists(collection_dir):
        os.makedirs(collection_dir)

    for file in files:
        file_path = os.path.join(collection_dir, file.filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

    return JSONResponse(status_code=200, content={"message": "Files uploaded successfully."})

@app.get("/collections/")
async def get_collections():
    if not os.path.exists(BASE_DIR):
        return []
    
    collections = []
    for folder_name in os.listdir(BASE_DIR):
        collections.append({"name": folder_name})

    return collections

@app.get("/collections/{name}/deploy")
async def deploy_collection(name: str):
    global vector_retriever
    
    vector_retriever= rele_data(f'{BASE_DIR}/{name}')
    collection_dir = os.path.join(BASE_DIR, name)
    if not os.path.exists(collection_dir):
        raise HTTPException(status_code=404, detail="Collection not found")

    files = [os.path.join(collection_dir, f) for f in os.listdir(collection_dir)]
    
    vector_db = {f: "Vector representation of {}".format(f) for f in files}
    return {"vector_db": vector_db, "message": f"Collection {name} deployed"}

@app.post("/query/")
async def process_query(request: dict):
    global counter
    collection = request.get("collection")
    query = request.get("query")
    
    
    content=get_content(vector_retriever,query)

    response= get_response(query,content,'NONE')
    
    return {"response": response}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)