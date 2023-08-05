import pytest
from app import db
from app.models.user_model import UserModel


@pytest.mark.usefixtures('db')
class TestTable:
    def test_get_by_id(self):
        user = UserModel(name='test_name', score=100)
        db.add(user)
        db.commit()

        retrieved = UserModel.get_info_by_id(user.uid)
        assert retrieved == user
