from random import randrange
from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
import time


app = FastAPI()


class CreatePost(BaseModel):
    title: str
    content: str
    published: bool = True  # default value


class EditPost(BaseModel):
    name: Optional[str] = None
    designation: Optional[str] = None


while True:
    try:
        conn = psycopg2.connect(
            host="localhost",
            database="fastapi",
            user="postgres",
            password="Password@123",
            cursor_factory=RealDictCursor,
        )
        cursor = conn.cursor()
        print("Connection successful!")
        break
    except Exception as error:
        print("Connecting to DB failed!")
        print("Error: ", error)
        time.sleep(3)

sim_database = [
    {"id": 10, "name": "Michael Scott", "designation": "Manager"},
    {"id": 102, "name": "Dwight Schrute", "designation": "Assistant to the Manager"},
]


@app.get("/posts")
async def get_all_posts():
    cursor.execute("""Select * from post""")
    posts = cursor.fetchall()
    return {"data": posts, "count": len(posts)}


@app.get("/posts/{id}")  # path parameter
async def get_one_post(id: int):
    cursor.execute("""SELECT * FROM post WHERE id = %s """, (str(id)))
    # convert int to str because select statement is a string, and does not support int
    post = cursor.fetchone()
    return {"data": post}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
async def create_post(payload: CreatePost):
    # did not use formatted strings
    # they're vulnerable to sql injections
    cursor.execute(
        """ INSERT INTO POST (title, content, published) VALUES (%s, %s, %s) RETURNING id""",
        (payload.title, payload.content, payload.published),
    )
    created_post_id = cursor.fetchone()

    conn.commit()  # should commit to db after changes

    return {
        "success": True,
        "message": "Created post!",
        "created_post_id": created_post_id,
    }


@app.put("/posts/{id}")
async def update_post(id: int, payload: EditPost, response: Response):
    name, designation = payload.model_dump().values()
    print(name, designation)
    found_post = list(filter(lambda post: post["id"] == id, sim_database))

    if not bool(name is None or designation is None):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Either name or designation should be provided!",
        )

    if not found_post:
        raise HTTPException(
            status_code=404, detail=f"Post with id {id} does not exist!"
        )

    post = found_post[0]

    if name != None:
        post["name"] = name

    if designation != None:
        post["designation"] = designation

    return {"message": "Post edited successfully!", "id": id}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int):
    cursor.execute("""DELETE * FROM post WHERE id = %s RETURNING id""", str(id))
    deleted_post_id = cursor.fetchone()
    conn.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)
