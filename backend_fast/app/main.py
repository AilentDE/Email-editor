from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .dependencies import get_query_token, get_token_header, csrf_check
from .internal import admin
from .routers import items, users, back, files, email

app = FastAPI(dependencies=[Depends(csrf_check)])

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# app.include_router(users.router)
# app.include_router(items.router)
# app.include_router(
#     admin.router,
#     prefix="/admin",
#     tags=["admin"],
#     dependencies=[Depends(get_token_header)],
#     responses={418: {"description": "I'm a teapot"}},
# )
# app.include_router(back.router)
app.include_router(files.router)
app.include_router(email.router)

@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications!"}