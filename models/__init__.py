from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Importar modelos para torná-los disponíveis quando o módulo models for importado
from .user import User
from .planilha import Planilha
from .dados_planilha import DadosPlanilha