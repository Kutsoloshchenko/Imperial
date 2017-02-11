#encoding=utf-8

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class Kick_dict(Base):
    __tablename__ = 'kick'
    user_id = Column(Integer, primary_key=True)
    user_domain = Column(String(25))
    voters = Column(String(100))
    votes = Column(Integer)

    def __repr__(self):
        return ('kick_db entry (user_id=%s, user_domain=%s, voters=%s, votes=%s)' % (
        self.user_id, self.user_domain, self.voters, self.votes))

class Auto_kick(Base):
    __tablename__ = 'auto_kick'
    user_id = Column(Integer, primary_key=True)

    def __repr__(self):
        return ('auto_kick db entry (user_id=%s)' % self.user_id)

class Kind_mail(Base):
    __tablename__ = 'kind_mail'
    sender_id = Column(Integer, primary_key=True)
    reciver_id = Column(String(100))

    def __repr__(self):
        return ('kind_mail db entry (sender_id=%s, recivers_ids = %s)' % (self.sender_id, self.reciver_id))

class DB:
    def __init__(self):
        self.engine = create_engine('mysql://root:abcd12345!!!@localhost/imperial', encoding = 'latin1')
        Session=sessionmaker(bind=self.engine)
        self.session = Session()

    def find_first_to_kick(self, parametr):
        return self.session.query(Kick_dict).filter_by(user_domain=parametr).first()

    def in_auto_kick(self,user_id):
        return self.session.query(Auto_kick).filter_by(user_id=user_id).first()

    def create_entry(self, kick_id, domain_name, kicker_id):
        User = Kick_dict(user_id=kick_id, user_domain=domain_name, voters=str(kicker_id), votes=1)
        self.session.add(User)
        self.session.commit()

    def remove(self, db_entry):
        self.session.delete(db_entry)
        self.session.commit()

    def add_to_auto_kick(self, user_id):
        user = Auto_kick(user_id=user_id)
        self.session.add(user)
        self.session.commit()

    def add_kicker_and_vote(self, db_entry, kicker_id):
        db_entry.votes += 1
        db_entry.voters = db_entry.voters + ' ' + str(kicker_id)
        self.session.add(db_entry)
        self.session.commit()

    def get_all_kind_mail(self):
        return self.session.query(Kind_mail).all()

    def find_kind_mail(self, sender_uid):
        return self.session.query(Kind_mail).filter_by(sender_id=sender_uid).first()

    def kind_mail_append(self, db_entry, reciver_domain_name):
        db_entry.reciver_id += ' ' + reciver_domain_name
        self.session.add(db_entry)
        self.session.commit()

    def kind_mail_create(self, sender_uid, reciver_domain_name):
        User = Kind_mail(sender_id=sender_uid, reciver_id=reciver_domain_name)
        self.session.add(User)
        self.session.commit()

    def remove_from_kind_mail(self, sender_id, message_domain):
        db_entry = self.find_kind_mail(sender_id)
        db_entry.reciver_id = db_entry.reciver_id.replace(message_domain,'')
        db_entry.reciver_id = db_entry.reciver_id.lstrip()
        if len(db_entry.reciver_id) == 0:
            self.remove(db_entry)
        else:
            self.session.add(db_entry)
            self.session.commit()
