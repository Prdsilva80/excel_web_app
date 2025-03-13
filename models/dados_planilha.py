from datetime import datetime, timezone
import json
from . import db

class DadosPlanilha(db.Model):
    """
    Modelo para armazenar os dados inseridos pelos usuários nas planilhas.
    Cada instância representa um conjunto de dados inserido por um usuário 
    em uma determinada planilha.
    """
    id = db.Column(db.Integer, primary_key=True)
    planilha_id = db.Column(db.Integer, db.ForeignKey('planilha.id'), 
                        nullable=False, 
                        comment="ID da planilha relacionada")
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), 
                        nullable=False, 
                        comment="ID do usuário que inseriu os dados")
    dados = db.Column(db.Text, nullable=False, 
                    comment="Dados inseridos em formato JSON")
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc), 
                        comment="Data e hora de inserção dos dados")
    updated_at = db.Column(db.DateTime, default=datetime.now(timezone.utc), 
                        onupdate=datetime.now(timezone.utc), 
                        comment="Data e hora da última atualização")
    
    # Definindo os relacionamentos com outros modelos
    planilha = db.relationship('Planilha', backref=db.backref('dados', lazy=True), 
                            foreign_keys=[planilha_id])
    user = db.relationship('User', backref=db.backref('dados_planilhas', lazy=True), 
                        foreign_keys=[user_id])
    
    def get_dados(self):
        """Retorna os dados como um dicionário Python"""
        if self.dados:
            return json.loads(self.dados)
        return {}
    
    def set_dados(self, dados_dict):
        """Define os dados a partir de um dicionário Python"""
        self.dados = json.dumps(dados_dict)
    
    def aplicar_formulas(self):
        """
        Aplica as fórmulas da planilha aos dados.
        Método para ser implementado com a lógica de cálculo das fórmulas.
        """
        # Implementação futura
        pass
    
    def __repr__(self):
        """Representação string do objeto para depuração"""
        return f'<DadosPlanilha {self.id} - Planilha: {self.planilha_id} - Usuário: {self.user_id}>'