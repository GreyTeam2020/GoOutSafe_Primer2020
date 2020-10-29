from monolith.database import db, User


class UserService:
    """"""

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
