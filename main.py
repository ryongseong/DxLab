from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from domain.user import user_router
from domain.question import question_router
from domain.exam import exam_router
from domain.gemini import gemini_router

app = FastAPI()

origins = [
    "http://localhost:5173",
    "http://localhost:8000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_router.router)
app.include_router(question_router.router)
app.include_router(exam_router.router)
app.include_router(gemini_router.router)