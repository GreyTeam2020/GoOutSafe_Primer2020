import os

import pytest
from monolith.database import db, User
from monolith.forms import UserForm
from monolith.services.user_service import UserService
from monolith.tests.utils import get_user_with_email


@pytest.mark.usefixtures("client")
class Test_UserServices:
    """"""

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

    def test_create_customer(self):
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
        user = UserService.create_user(user, form.password, 2)
        assert user is not None
        assert user.role_id is not 3
        assert user.role_id is 2

        db.session.query(User).filter_by(id=user.id).delete()
        db.session.commit()

    def test_modify_user_role_id(self):
        """
        With this code is tested the services to perform the user modification
        with service and have the result on db

        Test flow
        - Create user
        - Modify user
        - check user
        - delete user to clean the database
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
        user = UserService.create_user(user, form.password, 2)
        assert user is not None
        assert user.role_id is 2

        user_modified = UserService.modify_user(user, 3)
        assert user is not None
        assert user.role_id is not 2
        UserService.delete_user(user_modified.id)
        user_modified = get_user_with_email(user_modified.email)
        assert user_modified is None

    def test_modify_user_role_id(self):
        """
        With this code is tested the services to perform the user modification
        with service and have the result on db

        Test flow
        - Create user
        - Modify user
        - check user
        - delete user to clean the database
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
        user = UserService.create_user(user, form.password, 2)
        assert user is not None
        assert user.role_id is 2

        user.firstname = "Vincent"
        user_modified = UserService.modify_user(user)
        assert user is not None
        assert user_modified.firstname == "Vincent"
        assert user.role_id is 2
        UserService.delete_user(user_modified.id)
        user_modified = get_user_with_email(user_modified.email)
        assert user_modified is None

    def test_delete_user_with_email(self):
        """
        This test cases test if the user service are able to
        remove correctly the user inside the DB
        Test flow
        - Create a new user with the service
        - delete a new user with service with user pass
        - check on db if this user is gone
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
        user = UserService.create_user(user, form.password, 2)
        assert user is not None
        assert user.role_id is 2
        UserService.delete_user(email=user.email)
        user = db.session.query(User).filter_by(email=user.email).first()
        assert user is None

    def test_delete_user_with_id(self):
        """
        This test cases test if the user service are able to
        remove correctly the user inside the DB
        Test flow
        - Create a new user with the service
        - delete a new user with service with user id
        - check on db if this user is gone
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
        user = UserService.create_user(user, form.password, 2)
        assert user is not None
        assert user.role_id is 2
        UserService.delete_user(user_id=user.id)
        user = db.session.query(User).filter_by(id=user.id).first()
        assert user is None
