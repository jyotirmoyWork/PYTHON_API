from fastapi import FastAPI
# SQL ALCHEMY
from fastapi.middleware.cors import CORSMiddleware
from .routes import post, user, auth, votes
# import utils



# SQL ALCHEMY
# models.Base.metadata.create_all(bind=engine)
app = FastAPI()


origins = ["*"]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# BASE ROUTE
@app.get("/")
def root():
    return {"message": "Hello World from sql-alchemy"}

# POSTS ROUTE
app.include_router(post.router)

# USER ROUTES
app.include_router(user.router)

# LOGIN ROUTES
app.include_router(auth.router)

# VOTES ROUTES
app.include_router(votes.router)




