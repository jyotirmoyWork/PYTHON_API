from fastapi import FastAPI, HTTPException, Response, status

import psycopg2
from psycopg2.extras import RealDictCursor
import time

from pydantic import BaseModel


app = FastAPI()

class Posts(BaseModel):
    TITLE: str
    CONTENT: str
    PUBLISHED: bool = True


# ========================DATABASE WITH DIRECT SQL WITHOUT SQL-ALCHEMY=======================================

# DATABASE CONNECTION TO DIRECT SQL
while True:
    try:
        conn = psycopg2.connect(host ='localhost', database='Python_fst_api', user='postgres', password='admin', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Successfully connected !!!")
        break
    except Exception as error:
        print("Connecting to data base failed")
        print("error:", error)
        time.sleep(2)


@app.get("/")
def root():
    return {"message": "Hello World"}


# GET ALL POSTS
@app.get("/posts")
def get_posts():
    cursor.execute(""" SELECT * FROM "POSTS" """)
    posts = cursor.fetchall()
    return {"data":posts}



# CREATE A SINGLE POST
@app.post("/posts", status_code = status.HTTP_201_CREATED)
def create_posts(post: Posts):
    cursor.execute(""" INSERT INTO "POSTS" ("TITLE", "CONTENT", "PUBLISHED") VALUES (%s, %s, %s) RETURNING * """, (post.TITLE, post.CONTENT, post.PUBLISHED))
    # posts = cursor.
    new_post = cursor.fetchone()
    conn.commit()
    return {"DATA":new_post}


# GET SINGLE POST BY ID
@app.get("/posts/{id}")
def get_post_one(id:int, response: Response):
    cursor.execute(""" SELECT * FROM "POSTS" WHERE "ID" = %s """, (str(id),))
    post = cursor.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="post with id " + str(id) + " not found")
    return {"post":post}


# DELETE A SINGLE POST
@app.delete("/posts/{id}",status_code = status.HTTP_201_CREATED )
def delete_post(id: int):
    cursor.execute(""" DELETE FROM "POSTS" WHERE "ID" = %s RETURNING * """, (str(id),))
    post = cursor.fetchone()
    conn.commit()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


# UPDATE  A SINGLE POST
@app.put("/posts/{id}")
def update_post(id: int, post: Posts):
    cursor.execute(""" UPDATE "POSTS" SET "TITLE" = %s, "CONTENT" = %s, "PUBLISHED" = %s WHERE "ID" = %s RETURNING * """, (post.TITLE, post.CONTENT, post.PUBLISHED, str(id)))
    updated_post = cursor.fetchone()
    conn.commit()
    if not updated_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    else:
        return {"Updated post": updated_post}

# ======================================END==============================


