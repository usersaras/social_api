from random import randrange
from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel

app = FastAPI()

class CreatePost(BaseModel):
    name: str
    designation: str
    # published: bool = True # default value
    # rating: Optional[int] = None # optional value

class EditPost(BaseModel):
    name: Optional[str] = None
    designation: Optional[str] = None

sim_database = [{"id": 10,"name": "Michael Scott", "designation": "Manager"}, {"id": 102,"name": "Dwight Schrute", "designation": "Assistant to the Manager"}]

@app.get("/posts")
async def get_all_posts():
    return {'data': sim_database, "count": len(sim_database)}


@app.get("/posts/{id}") # path parameter
async def get_one_post(id: int):
    filter_post = filter(lambda post: post['id'] == id, sim_database)
    post = (list(filter_post))

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found!")
    
    return {'data': list(post)[0]}

@app.post("/posts",  status_code=status.HTTP_201_CREATED)
async def create_post(payload: CreatePost):
    post = payload.model_dump() # is of type pydantic model
    post['id'] = randrange(1, 1000)
    sim_database.append(post)
    return { 
        'message': 'Created post!',
        'id': post['id']
    }

@app.put("/posts/{id}")
async def update_post(id: int, payload: EditPost, response: Response):
    name, designation = payload.model_dump().values()
    print(name, designation)
    found_post = list(filter(lambda post: post['id'] == id, sim_database))

    if not bool(name is None or designation is None):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Either name or designation should be provided!')

    if not found_post:
        raise HTTPException(status_code=404, detail=f"Post with id {id} does not exist!")
    
    post = found_post[0]

    if name != None:
        post['name'] = name

    if designation != None:
        post['designation'] = designation

    return {
        'message': 'Post edited successfully!',
        'id': id
    }

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id:int):
    global sim_database

    filter_post = filter(lambda post: post['id'] == id, sim_database)
    post = (list(filter_post))

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found!")
    
    new_list = [item for item in sim_database if item['id'] != id]
    sim_database = new_list
    return Response(status_code=status.HTTP_204_NO_CONTENT)
