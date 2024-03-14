import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from controller import Controller
from models import Base, User


class TestModel:
    @pytest.fixture()
    def set_up_db(self):
        engine = create_engine('sqlite:///:memory:', echo=True)
        Base.metadata.create_all(engine)
        with Session(engine) as sess:
            yield sess

    def test_user(self, set_up_db):
        record = User(email='person@example.com')
        assert record.email == 'person@example.com'

    def test_db(self, set_up_db):
        session = set_up_db
        user_1 = User(email='john@gmail.com')
        user_2 = User(email='jane@outlook.com')
        session.add_all((user_1, user_2))
        session.commit()
        assert session.query(User).count() == 2
        assert session.query(User).first().email == 'john@gmail.com'


class TestController:
    @pytest.fixture()
    def set_up_controller(self):
        controller = Controller(':memory:')
        Base.metadata.create_all(controller.engine)
        return controller

    def test_save(self, set_up_controller):
        controller = set_up_controller
        temp_email = 'person@example.com'
        save_message = controller.save(temp_email)
        assert save_message == f'The email {temp_email} was saved!'

    def test_save_wrong_email(self, set_up_controller):
        controller = set_up_controller
        with pytest.raises(ValueError) as error:
            controller.save('invalid_email')
            assert str(error.value) == 'Invalid email address'

    def test_save_duplicate_email(self, set_up_controller):
        controller = set_up_controller
        temp_email = 'person@example.com'
        controller.save(temp_email)
        with pytest.raises(ValueError) as error:
            controller.save(temp_email)
            assert str(error.value) == 'Email already registered'
