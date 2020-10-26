from random  import randint
from sqlalchemy.exc import IntegrityError
from faker import Faker
from . import db
from .models import Outbox, User
from datetime import datetime

def letters(count=50):
    now = datetime.now()
    dt_str = now.strftime('%Y-%m-%d %H:%M:%S')
    u = User.query.filter_by(login='kostya').first()
    fake = Faker()
    i = 0
    while i < count:
        o = Outbox(subject=fake.text(),
                user_id = u.id,
                reg_date = dt_str,
                recipient=fake.name(),
                notes=fake.text())
        db.session.add(o)
        try:
            db.session.commit()
            i += 1
        except IntegrityError:
            db.session.rollback()
