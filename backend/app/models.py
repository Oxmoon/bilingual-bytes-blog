import enum
from datetime import datetime, timezone

import funcy
from flask import current_app
from flask_login import AnonymousUserMixin, UserMixin, current_user
from itsdangerous import BadSignature, SignatureExpired
from itsdangerous import URLSafeTimedSerializer as Serializer
from sqlalchemy import false
from sqlalchemy.ext.hybrid import hybrid_property
from werkzeug.security import check_password_hash, generate_password_hash

from .extensions import db, login


# -----------------------------------------------------------------------------
# Column functions
# -----------------------------------------------------------------------------
def aware_utcnow():
    return datetime.now(timezone.utc)


get_callable = lambda enum: [e.value for e in enum]

# -----------------------------------------------------------------------------
# Models
# -----------------------------------------------------------------------------


class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    username = db.Column(db.String(150), unique=True)
    role_id = db.Column(db.Integer, db.ForeignKey("roles.id"))
    role = db.relationship("Role", back_populates="users")
    password_hash = db.Column(db.String(170))
    archived = db.Column(db.Boolean, default=False, server_default=false())
    confirmed = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return "<User %s>" % (self.username)

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if self.role is None:
            if self.email in current_app.config["ADMINS"]:
                self.role = Role.query.filter_by(name="Admin").first()
            if self.role is None:
                self = Role.query.filter_by(default=True).first()

    def can(self, perm):
        return self.role is not None and self.role.has_permission(perm)

    def is_administrator(self):
        return self.can(Permission.ADMIN)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_confirmation_token(self):
        s = Serializer(current_app.config["SECRET_KEY"])
        return s.dumps(self.email, salt="email-confirm")

    def confirm(self, token):
        s = Serializer(current_app.config["SECRET_KEY"], salt="email-confirm")
        try:
            data = s.loads(token, salt="email-confirm", max_age=3600)
        except SignatureExpired:
            return False
        if data != self.email:
            return False
        self.confirmed = True
        db.session.add(self)
        return True

    def generate_password_token(self):
        s = Serializer(current_app.config["SECRET_KEY"])
        return s.dumps(self.email, salt="email-password")

    def confirm_password(self, token):
        s = Serializer(current_app.config["SECRET_KEY"], salt="email-password")
        try:
            data = s.loads(token, salt="email-password", max_age=3600)
        except SignatureExpired:
            return False
        if data != self.email:
            return False
        return True

    def get_role(self):
        if self.role:
            return self.role.name
        else:
            return "None"

    @classmethod
    def query_active_users(cls):
        return cls.query.filter_by(archived=False)

    @login.user_loader
    def load_user(id):
        return User.query.get(int(id))


class AnonymousUser(AnonymousUserMixin):
    def can(self, perm):
        return False

    def is_administrator(self):
        return False


class Permission:
    ADMIN = 1


roles = {
    "User": [0],
    "Admin": [
        Permission.ADMIN,
    ],
}


def get_all_roles():
    return funcy.omit(roles, "Admin")


class Role(db.Model):
    __tablename__ = "roles"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    default = db.Column(db.Boolean, default=False, index=True)
    permissions = db.Column(db.Integer)
    users = db.relationship("User", back_populates="role", lazy="dynamic")

    def __init__(self, **kwargs):
        super(Role, self).__init__(**kwargs)
        if self.permissions is None:
            self.permissions = 0

    def add_permission(self, perm):
        if not self.has_permission(perm):
            self.permissions += perm

    def remove_permission(self, perm):
        if self.has_permission(perm):
            self.permissions -= perm

    def reset_permissions(self):
        self.permissions = 0

    # Bitwise check on permissions
    def has_permission(self, perm):
        return self.permissions & perm == perm

    @staticmethod
    def insert_roles():
        default_role = "Unauthorized"
        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
            role.reset_permissions()
            for perm in roles[r]:
                role.add_permission(perm)
            role.default = role.name == default_role
            db.session.add(role)
        db.session.commit()
