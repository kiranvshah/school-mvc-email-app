import sqlalchemy.exc
from sqlalchemy import create_engine, engine
from sqlalchemy.orm import Session
from models import User


class Controller:
    def __init__(self, db_name='emails.sqlite'):
        self.engine = create_engine(f'sqlite:///{db_name}', echo=True)

    def save(self, email, password):
        """
        Save the email
        :param email:
        :return:
        """

        # validate email
        try:
            dummy_user = User()
            dummy_user.validate_email('email', email)
        except ValueError as error:
            raise ValueError(error)

        # validate password
        try:
            User.validate_password(password)
        except ValueError as error:
            raise ValueError(error)

        try:
            # save the model
            with Session(self.engine) as session:
                email_record = User(email=email)
                email_record.set_password(password, email)
                session.add(email_record)
                session.commit()
            return f'The email {email} was saved!'
        except sqlalchemy.exc.IntegrityError as error:
            if 'UNIQUE constraint failed' in error.args[0]:
                raise ValueError('Email already registered')
            raise ValueError(error)

    def login_exists(self, email, password):
        password_hash = User.hash_password(password, email)
        with Session(self.engine) as session:
            return session.query(User).filter(User.email == email, User.password_hash == password_hash).count() >= 1
