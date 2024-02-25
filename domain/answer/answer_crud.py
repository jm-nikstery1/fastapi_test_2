'''
답변 데이터를 데이터베이스에 저장하기 위한
CRUD

'''
from datetime import datetime

from sqlalchemy.orm import Session

from domain.answer.answer_schema import AnswerCreate, AnswerUpdate
from models import Question, Answer, User

'''
db 에 저장하는 create_answer 함수
'''
def create_answer(db: Session, question: Question, answer_create: AnswerCreate,user: User):
    db_answer = Answer(question=question,
                       content=answer_create.content,
                       create_date=datetime.now(),
                       user=user,)  # User모델 추가로 전달받기
    db.add(db_answer)
    db.commit()


'''
답변 수정 CRUD
'''
def update_answer(db:Session, db_answer: Answer, answer_update: AnswerUpdate):
    db_answer.content = answer_update.content
    db_answer.modify_date = datetime.now()
    db.add(db_answer)
    db.commit()


'''
답변 삭제 CRUD
'''
def delete_answer(db: Session, db_answer: Answer):
    db.delete(db_answer)
    db.commit()


'''
답변 추천 CRUD
'''
def vote_answer(db: Session, db_answer: Answer, db_user: User):
    db_answer.voter.append(db_user)
    db.commit()