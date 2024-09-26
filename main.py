from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
from database import engine, Base
from router import UserRouter, CaseRouter


# @app.on_event("startup")
# async def startup():
#     async with engine.begin() as conn:
#         await conn.run_sync(Base.metadata.create_all)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "*"
    ],  # Allow all origins (you can restrict this to specific domains)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(UserRouter)
app.include_router(CaseRouter)


@app.get("/")
def read_root():
    return {"ping": "pong"}
