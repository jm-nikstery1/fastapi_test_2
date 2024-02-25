'''
답변 등록 API

답변 schema
중요한 정보 - 입력 항목을 처리하는 스키마는 왜 필요할까
결론 - get 방식의 입력 항목은 Pydantic 스키마로 읽을 수 없고 각각의 입력 항목을 라우터 함수의 매개변수로 읽어야 한다.

답변 등록 API는 post 방식이고 content라는 입력 항목이 있다.
답변 등록 라우터에서 content의 값을 읽기 위해서는 반드시 content 항목을 포함하는 Pydantic 스키마를 통해 읽어야 한다.
스키마를 사용하지 않고 라우터 함수의 매개변수에 content: str을 추가하여 그 값을 읽을 수는 없다.
왜냐하면 get이 아닌 다른 방식(post, put, delete)의 입력 값은 Pydantic 스키마로만 읽을수 있기 때문이다.

'''
'''
답변 표시하기
'''
import datetime

from pydantic import BaseModel, validator
from domain.user.user_schema import User

'''
답변 content schema 하나 
단 content 속성은 디폴트 값이 없고 필수로 넣어야함

@validator 빈값은 허용되지 않게 해줌
'''
class AnswerCreate(BaseModel):
    content: str

    @validator('content')
    def not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError("빈 값은 허용되지 않습니다")
        return v

'''
답변 표시하기 스키마
여기서 class Config 빼먹으니 에러나왔음
프론트엔드 문제인줄 알았는데 
백엔드 쪽 문제였음 
와 이거 책보고 하니까 파악한게 쉬운거지 
pydantic 사용할때 버젼마다 조심해야하네 

중요 - user: User | None - 이부분 python 3.9에서는 에러 발생함 - python3.9에서는 맞지 않는 문법
python 3.10에서는 사용 가능한 문법
'''
class Answer(BaseModel):
    id: int
    content: str
    create_date: datetime.datetime
    user: User | None
    question_id: int
    modify_date: datetime.datetime | None = None
    voter: list[User] = []

    class Config:
        orm_mode = True


'''
답변 수정 스키마
'''
class AnswerUpdate(AnswerCreate):
    answer_id: int


'''
답변 삭제 스키마
'''
class AnswerDelete(BaseModel):
    answer_id: int


'''
답변 추천 스키마
'''
class AnswerVote(BaseModel):
    answer_id: int