from random  import randint
from sqlalchemy.exc import IntegrityError
from faker import Faker
from . import db
from .models import Outbox, User
from datetime import datetime

def letters(count=50):
    u = User.query.filter_by(login='kostya').first()
    fake = Faker()
    i = 0
    while i < count:
        o = Outbox(subject=fake.text(max_nb_chars=20),
                user_id = u.id,
                reg_date = fake.date_time_between(start_date='-3y',
                    end_date='now', tzinfo=None),
                recipient=fake.name(),
                notes=fake.text(max_nb_chars=20))
        db.session.add(o)
        try:
            db.session.commit()
            i += 1
        except IntegrityError:
            db.session.rollback()
