from flask_login import current_user

from monolith.database import db, User, Positive
from monolith.forms import UserForm


class UserService:
    """
    This service is a wrapper of all operation with user
    - create a new user
    - deleter a user if exist
    """

    @staticmethod
    def create_user(new_user: User, password, role_id: int = 3):
        """

        :return:
        """
        ## By default I assume CUSTOMER
        new_user.role_id = role_id
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()

        q = db.session.query(User).filter(User.email == new_user.email)
        user = q.first()
        return user

    @staticmethod
    def modify_user(form: UserForm, role_id: int = None):
        """
        This method take an user that is populate from te called (e.g: the flat form)
        and make the operation to store it as persistent (e.g database).
        We can assume that by default is not possible change the password
        :param form: the user form with new data
        :param role_id: by default is none but it is possible setup to change also the role id
        :return: the user with the change if is changed
        """

        if role_id is None:
            role_id = current_user.role_id
        db.session.query(User).filter(User.email == current_user.email).update(
            {
                "email": form.email.data,
                "firstname": form.firstname.data,
                "lastname": form.lastname.data,
                "dateofbirth": form.dateofbirth.data,
                "role_id": role_id,
            }
        )
        db.session.commit()

        user = db.session.query(User).filter_by(email=form.email.data).first()
        return user

    @staticmethod
    def delete_user(user_id: int = None, email: str = ""):
        if user_id is not None:
            db.session.query(User).filter_by(id=user_id).delete()
        else:
            db.session.query(User).filter_by(email=email).delete()
        db.session.commit()

    @staticmethod
    def is_positive(user_id: int):
        """
        Given a userid i return if the user is currently positive
        :param user_id: user id of the user checked
        return: boolean if the user is positive
        """
        check =db.session.query(Positive).filter_by(user_id=user_id).filter_by(marked=True).first()
        if check is None:
            return False
        return True