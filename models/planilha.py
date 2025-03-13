from datetime import datetime, timezone
import json
from . import db

class Planilha(db.Model):
    """Modelo de planilha importada no sistema"""
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False, 
                    comment="Nome da planilha")
    descricao = db.Column(db.Text, nullable=True, 
                        comment="Descrição detalhada da planilha")
    estrutura = db.Column(db.Text, nullable=False, 
                        comment="Estrutura da planilha em formato JSON")
    formulas = db.Column(db.Text, nullable=True, 
                        comment="Fórmulas da planilha em formato JSON")
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc), 
                        comment="Data e hora de importação da planilha")
    updated_at = db.Column(db.DateTime, default=datetime.now(timezone.utc), 
                        onupdate=datetime.now(timezone.utc), 
                        comment="Data e hora da última atualização")
    
    # Note que não definimos o relacionamento com DadosPlanilha aqui
    # porque ele já está definido no modelo DadosPlanilha com backref
    
    def get_estrutura(self):
        """Retorna a estrutura da planilha como um dicionário Python"""
        if self.estrutura:
            return json.loads(self.estrutura)
        return {}
    
    def get_formulas(self):
        """Retorna as fórmulas da planilha como um dicionário Python"""
        if self.formulas:
            return json.loads(self.formulas)
        return {}
    
    def get_primeiro_sheet(self):
        """Retorna o nome da primeira planilha na estrutura"""
        estrutura = self.get_estrutura()
        if estrutura:
            return next(iter(estrutura))
        return None
    
    def get_colunas_primeiro_sheet(self):
        """Retorna as colunas da primeira planilha na estrutura"""
        estrutura = self.get_estrutura()
        if estrutura:
            primeiro_sheet = next(iter(estrutura))
            return estrutura[primeiro_sheet].get('columns', [])
        return []
    
    def __repr__(self):
        """Representação string do objeto para depuração"""
        return f'<Planilha {self.nome}>'