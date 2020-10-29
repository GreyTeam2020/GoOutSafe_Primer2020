from monolith.database import db, User


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
    def modify_user(user: User, role_id: int = None):
        """
        This method take an user that is populate from te called (e.g: the flat form)
        and make the operation to store it as persistent (e.g database).
        We can assume that by default is not possible change the password
        :param user: the user felt from the form
        :param role_id: by default is none but it is possible setup to change also the role id
        :return: the user with the change if is changed
        """
        if role_id is not None:
            user.role_id = role_id
        db.session.add(user)
        db.session.commit()

        q = db.session.query(User).filter(User.email == user.email)
        user = q.first()
        return user

    @staticmethod
    def delete_user(user_id: int = None, email: str = ""):
        if user_id is not None:
            db.session.query(User).filter_by(id=user_id).delete()
        else:
            db.session.query(User).filter_by(email=email).delete()
        db.session.commit()
