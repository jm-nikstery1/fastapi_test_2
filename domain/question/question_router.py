from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from domain.question import question_schema, question_crud
from database import get_db
#from models import Question
from domain.user.user_router import get_current_user
from models import User

from starlette import status

router = APIRouter(
    prefix="/api/question"
)


'''
db: Session 문장의 의미는 db 객체가 Session 타입임을 의미
- 대부분 동기 형식

question_list 함수에 페이지 번호와 한 페이지에 보여줄 게시물 갯수인 page, size 매개변수 추가 
page*size의 값을 skip에 대입할수 있다 - (size가 10인경우)즉 page가 0인 경우에는 skip은 0이 되고 page가 1인경우 skip은 10이 됨
'''
@router.get("/list", response_model=question_schema.QuestionList)
def question_list(db: Session = Depends(get_db), page: int=0, size: int=10, keyword: str=''):
    #_question_list = db.query(Question).order_by(Question.create_date.desc()).all()  - question_crud를 사용 안할때
    #_question_list = question_crud.get_question_list(db)    # question_crud를 사용할때
    total, _question_list = question_crud.get_question_list(db, skip=page*size, limit=size, keyword=keyword)  # page * size의 question리스트

    return {
        'total': total,
        'question_list': _question_list
    }


'''
CRUD 
get_question 함수를 위한 라우터
'''
@router.get("/detail/{question_id}", response_model=question_schema.Question)
def question_detail(question_id: int, db: Session = Depends(get_db)):
    question = question_crud.get_question(db, question_id=question_id)
    return question

'''
질문 등록 라우터
'''
@router.post("/create", status_code=status.HTTP_204_NO_CONTENT)
def question_create(_question_create: question_schema.QuestionCreate, db:Session=Depends(get_db),
                    current_user: User = Depends(get_current_user)):
    question_crud.create_question(db=db, question_create=_question_create,
                                  user=current_user)

'''
질문 수정 라우터
'''
@router.put("/update", status_code=status.HTTP_204_NO_CONTENT)
def question_update(_question_update: question_schema.QuestionUpdate, db:Session = Depends(get_db), current_user:User = Depends(get_current_user)):
    db_question = question_crud.get_qeustion(db, question_id = _question_update.question_id)

    if not db_question:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="데이터를 찾을수 없습니다.")

    if current_user.id != db_question.user.id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="수정 권한이 없습니다")

    question_crud.update_question(db=db, db_question=db_question, question_update=_question_update)


'''
질문 삭제 라우터
'''
@router.delete("/delete", status_code=status.HTTP_204_NO_CONTENT)
def question_delete(_question_delete: question_schema.QuestionDelete, db: Session=Depends(get_db), current_user:User = Depends(get_current_user)):
    db_question = question_crud.get_question(db, question_id=_question_delete.question_id)
    if not db_question:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="데이터를 찾을수 없습니다")

    if current_user.id != db_question.id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="삭제 권한이 없습니다")

    question_crud.delete_question(db=db, db_question=db_question)


'''
질문 추천 라우터
'''
@router.post("/vote", status_code=status.HTTP_204_NO_CONTENT)
def question_vote(_question_vote: question_schema.QuestionVote,
                  db:Session = Depends(get_db),
                  current_user: User = Depends(get_current_user)):
    db_question = question_crud.get_question(db, question_id=_question_vote.question_id)
    if not db_question:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="데이터를 찾을수 없습니다")

    question_crud.vote_question(db, db_question=db_question, db_user=current_user)





'''
router 객체 생성시 사용한 prefix 속성은 요청 URL에 항상 포함되어야 하는 값이다. 
이 말이 좀 애매할 수 있는데 question_list 함수에 적용된 @router.get("/list")를 연계하여 생각하면 이해가 쉽다.
즉, /api/question/list 라는 URL 요청이 발생하면 /api/question 이라는 prefix가 등록된 question_router.py 파일의 /list로 등록된 함수 question_list가 실행되는 것이다.

question_list 함수는 db 세션을 생성하고 해당 세션을 이용하여 질문 목록을 조회하여 리턴하는 함수이다.
그리고 사용한 세션은 db.close()를 수행하여 사용한 세션을 반환했다.

db.close() 함수는 사용한 세션을 컨넥션 풀에 반환하는 함수이다. (세션을 종료하는 것으로 착각하지 말자.)

========================
_question_list = db.query(Question).order_by(Question.create_date.desc()).all()

즉, Question 모델의 모든 항목이 출력으로 리턴되는 것이다. 
하지만 외부로 공개되면 안되는 출력항목이 있을수도 있고 또 출력값이 정확한지 검증하고 싶을 수도 있을 것이다. 즉, 위와 같은 형태로는 이러한 조건을 충족할수 없다.
출력 부분에 대한 추가적인 코딩이 필요하다. 이러한 상황에 사용할 수 있는 라이브러리가 바로 Pydantic이다.
'''