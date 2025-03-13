# Módulos de funcionalidades para o sistema de planilhas web
"""
Este pacote contém utilitários e lógica de negócios para o sistema de planilhas,
separados do código principal da aplicação para melhor organização.
"""

# Importações para facilitar o acesso aos módulos
from .excel_parser import ExcelParser
from .auth import verificar_admin, verificar_permissao
from .formula_translator import traduzir_formula, aplicar_formulas
from .data_processor import processar_dados, exportar_dados