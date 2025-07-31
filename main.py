from typing import List
from fastapi import FastAPI
from pydantic import BaseModel
from starlette.requests import Request
from starlette.responses import JSONResponse, Response

app = FastAPI()

#Q1
@app.get("/ping")
def read_ping(request: Request):
   return "pong" 
#Q2
@app.get("/home")
def read_home(request: Request):
    with open("index.html", "r", encoding="utf-8") as file:
        html_content = file.read()
    return Response(content=html_content, status_code=200, media_type="text/html")

#Q3
@app.get("/{full_path:path}")
def catch_all(full_path: str):
    with open("not_found.html", "r", encoding="utf-8") as file:
        html_content = file.read()
    return Response(content=html_content, status_code=404, media_type="text/html")


#Q4
class Item(BaseModel):
        author: str | None = None
        title: str | None = None
        content: str | None = None
        creation_dateTime: str | None = None
        
posts_store: List[Item] = []

def serialized_stored_posts():               
    posts_converted = []
    for posts in posts_store:
        posts_converted.append(posts.model_dump())
    return posts_converted

        
@app.post("/posts")                                
def new_posts(event_payload: List[Item]):
    posts_store.extend(event_payload)
    return {"events": serialized_stored_posts()}

#Q5
@app.get("/posts")
def get_events():
    return {"events": serialized_stored_posts()}   


#Q6
@app.put("/posts")
def update_or_create_events(posts_payload: List[Item]):
    global posts_store 

    for new_posts in posts_payload:
        
        found = False
        for i, existing_posts in enumerate(posts_store):
            if new_posts.name == existing_posts.name:
                posts_store[i] = new_posts
                found = True
                break
        if not found:
            posts_store.append(new_posts)
    return {"events": serialized_stored_posts()}

    