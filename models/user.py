from datetime import datetime, timezone
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from . import db


class User(UserMixin, db.Model):
    """Modelo de usuário do sistema"""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False,
                        comment="Nome de usuário para identificação")
    email = db.Column(db.String(120), unique=True, nullable=False,
                    comment="Email do usuário, usado para login")
    password_hash = db.Column(db.String(256), nullable=False,
                            comment="Hash da senha do usuário")
    is_admin = db.Column(db.Boolean, default=False,
                        comment="Flag que indica se o usuário é administrador")
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc),
                        comment="Data e hora de criação do usuário")

    # Note que não definimos o relacionamento com DadosPlanilha aqui
    # porque ele já está definido no modelo DadosPlanilha com backref

    def set_password(self, password):
        """Define a senha criptografada do usuário"""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Verifica se a senha fornecida corresponde à senha armazenada"""
        return check_password_hash(self.password_hash, password)

    def is_administrator(self):
        """Retorna True se o usuário é administrador, False caso contrário"""
        return self.is_admin

    def __repr__(self):
        """Representação string do objeto para depuração"""
        return f'<User {self.username}>'
