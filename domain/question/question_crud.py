'''
하지만 파이보 프로젝트는 데이터를 처리하는 부분을 quesiton_crud.py 파일에 분리하여 작성
왜냐하면 서로 다른 라우터에서 데이터를 처리하는 부분이 동일하여 중복될수 있기 때문
'''
from datetime import datetime
from sqlalchemy import and_

from models import Question, User, Answer
from sqlalchemy.orm import Session
from domain.question.question_schema import QuestionCreate, QuestionUpdate

'''
질문 목록 수정 
skip 과 limit 매개변수를 추가
skip은 조회한 데이터의 시작위치 
limit는 시작위치부터 가져올 데이터의 건수

300개의 데이터중에서 21~30번째 데이터를 가져오려면 skip은 20, limit는 10을 전달하면 됨
'''
def get_question_list(db: Session, skip: int=0, limit: int=10, keyword:str =''):
    # 검색 기능 추가 - crud 수정
    question_list = db.query(Question)
    if keyword:
        search = '%%{}%%'.format(keyword)
        sub_query = db.query(Answer.question_id, Answer.content, User.username).outerjoin(User, Answer.user_id == User.id).subquery()
        question_list = question_list.outerjoin(User).outerjoin(sub_query, sub_query.c.question_id == Question.id).filter(Question.subject.ilike(search) |  #질문 제목
                                                                                                                          Question.content.ilike(search) |  #질문 내용
                                                                                                                          User.username.ilike(search) |     # 질문 글쓴이
                                                                                                                          sub_query.c.content.ilike(search) |   #답변 내용
                                                                                                                          sub_query.c.username.ilike(search))   #답변 글쓴이

    total = question_list.distinct().count()
    question_list = question_list.order_by(Question.create_date.desc()).offset(skip).limit(limit).distinct().all()

    return total, question_list

'''
CRUD
질문 1건을 조회하는 get_question 함수를 선언
question_id에 해당하는 질문을 조회하여 리턴하는 함수
'''
def get_question(db: Session, question_id: int):
    question = db.query(Question).get(question_id)
    return question

'''
질문 등록 CRUD

'''
def create_question(db: Session, question_create: QuestionCreate, user: User):
    db_question = Question(subject=question_create.subject, content=question_create.content, create_date=datetime.now(),
                           user=user)
    db.add(db_question)
    db.commit()


'''
질문 수정 CRUD
'''
def update_question(db:Session, db_question: Question, question_update: QuestionUpdate):
    db_question.subject = question_update.subject
    db_question.content = question_update.subject
    db_question.modify_date = datetime.now()
    db.add(db_question)
    db.commit()

'''
질문 삭제 CRUD
'''
def delete_question(db:Session, db_question: Question):
    db.delete(db_question)
    db.commit()

'''
질문 추천 CRUD
'''
def vote_question(db: Session, db_question: Question, db_user: User):
    db_question.voter.append(db_user)
    db.commit()