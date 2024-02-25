from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import FileResponse
from starlette.staticfiles import StaticFiles

from domain.answer import answer_router
from domain.question import question_router
from domain.user import user_router


app = FastAPI()

origins = [
    "http://127.0.0.1:5173",
    "http://localhost:5173",   # 또는 "http://localhost:5173"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

'''
생성한 question 라우터 등록
잘보면 question_router의 router 로 작성되어있다
다른책과 다른방식으로 표현함 - 표현 방식이 다른것뿐임

중요한건 그 라우터에 있는 APIRouter를 어떻게 불렸나가 중요
'''
app.include_router(question_router.router)
app.include_router(answer_router.router)
app.include_router(user_router.router)
app.mount("/assets", StaticFiles(directory="frontend/dist/assets"))

#npm run build 한것을 연결
@app.get("/")
def index():
    return FileResponse("frontend/dist/index.html")
