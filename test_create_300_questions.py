'''
질문 데이터 300개 생성
한번만 실행할것
'''
from database import SessionLocal
from models import Question
from datetime import datetime

db = SessionLocal()
for i in range(300):
    #q = Question(subject="테스트 데이터입니다:[%03d]" % i, content="내용없음", create_date=datetime.now())
    db.add(q)
    db.commit()