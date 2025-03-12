import os
from datetime import timedelta

class Config:
    """Configuração base da aplicação"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'chave-secreta-desenvolvimento'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///planilhas.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # Limite de upload: 16MB
    UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')
    ALLOWED_EXTENSIONS = {'xls', 'xlsx'}
    SESSION_TYPE = 'filesystem'
    PERMANENT_SESSION_LIFETIME = timedelta(hours=2)  # Sessão expira em 2 horas

class DevelopmentConfig(Config):
    """Configuração para desenvolvimento"""
    DEBUG = True
    # Permite ver detalhes de SQL
    SQLALCHEMY_ECHO = True

class ProductionConfig(Config):
    """Configuração para produção"""
    DEBUG = False
    # Em produção, a chave secreta deve ser definida como variável de ambiente
    SECRET_KEY = os.environ.get('SECRET_KEY')
    # Em produção, usar banco de dados PostgreSQL ou similar
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'postgresql://user:password@localhost/excel_web_app'
    # SSL/TLS para produção
    SESSION_COOKIE_SECURE = True
    REMEMBER_COOKIE_SECURE = True

class TestingConfig(Config):
    """Configuração para testes"""
    TESTING = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False

# Configuração padrão
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}

def get_config():
    """Retorna a configuração baseada no ambiente"""
    env = os.environ.get('FLASK_ENV', 'default')
    return config.get(env, config['default'])