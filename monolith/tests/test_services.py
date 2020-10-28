import pytest
from monolith.database import db, User
from monolith.forms import UserForm
from monolith.services.user_service import UserService


@pytest.mark.usefixtures("client")
class Test_UserServices:
    """

    """

    def test_create_user(self):
        """
        test create user
        :return:
        """
        form = UserForm()
        form.data["email"] = "alibaba@alibaba.com"
        form.data["password"] = "Alibaba"
        form.firstname = "Vincenzo"
        form.lastname = "Palazzo"
        form.password = "Alibaba"
        form.phone = "12345"
        form.dateofbirth = "12/12/2020"
        form.email.data = "alibaba@alibaba.com"
        user = User()
        form.populate_obj(user)
        user = UserService.create_user(user, form.password)
        assert user is not None
        assert user.role_id is 3

        db.session.query(User).filter_by(id=user.id).delete()
        db.session.commit()
