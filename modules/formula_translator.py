"""
Módulo para tradução e processamento de fórmulas Excel
"""
import re
import math
import numpy as np
from datetime import datetime

# Mapeamento de funções Excel para Python
EXCEL_TO_PYTHON_FUNCS = {
    'SUM': 'sum',
    'AVERAGE': 'np.mean',
    'MAX': 'max',
    'MIN': 'min',
    'COUNT': 'len',
    'COUNTA': 'len',
    'ABS': 'abs',
    'ROUND': 'round',
    'ROUNDUP': 'math.ceil',
    'ROUNDDOWN': 'math.floor',
    'IF': 'lambda x, y, z: y if x else z',
    'AND': 'all',
    'OR': 'any',
    'NOT': 'not',
    'POWER': 'pow',
    'SQRT': 'math.sqrt',
    'LN': 'math.log',
    'LOG10': 'math.log10',
    'EXP': 'math.exp',
    'TODAY': 'datetime.now().date',
    'NOW': 'datetime.now',
    'CONCATENATE': 'lambda *args: "".join([str(arg) for arg in args])',
    'LEFT': 'lambda text, num_chars: str(text)[:num_chars]',
    'RIGHT': 'lambda text, num_chars: str(text)[-num_chars:] if num_chars > 0 else ""',
    'MID': 'lambda text, start_num, num_chars: str(text)[start_num-1:start_num-1+num_chars]',
    'LEN': 'len',
    'UPPER': 'str.upper',
    'LOWER': 'str.lower',
    'PROPER': 'str.title',
    'TRIM': 'str.strip',
}

def traduzir_formula(excel_formula):
    """
    Converte uma fórmula Excel em código Python executável
    
    Args:
        excel_formula (str): Fórmula no formato Excel
        
    Returns:
        str: Código Python equivalente
    """
    if not excel_formula:
        return None
    
    # Remove o sinal de igual inicial se existir
    if excel_formula.startswith('='):
        excel_formula = excel_formula[1:]
    
    # Substitui referências de células por acesso a dicionário
    # Exemplo: A1 se torna data['A1']
    cell_pattern = r'([A-Z]+[0-9]+)'
    python_formula = re.sub(cell_pattern, r"data['\1']", excel_formula)
    
    # Substitui funções Excel por equivalentes Python
    for excel_func, python_func in EXCEL_TO_PYTHON_FUNCS.items():
        pattern = r'\b' + excel_func + r'\b'
        python_formula = re.sub(pattern, python_func, python_formula)
    
    # Substitui outros operadores/formatos
    # Operador de concatenação & para +
    python_formula = python_formula.replace('&', '+')
    
    # Substitui comparações de texto (iguais em ambos)
    # python_formula = re.sub(r'=', r'==', python_formula)
    
    return python_formula

def _evaluate_formula(formula, data):
    """
    Avalia uma fórmula Python com os dados fornecidos
    
    Args:
        formula (str): Fórmula Python a ser avaliada
        data (dict): Dicionário com valores para as células
        
    Returns:
        any: Resultado da avaliação da fórmula
    """
    try:
        # Cria um ambiente de execução seguro com as funções necessárias
        safe_dict = {
            'data': data,
            'sum': sum,
            'np': np,
            'max': max,
            'min': min,
            'len': len,
            'abs': abs,
            'round': round,
            'math': math,
            'datetime': datetime,
            'all': all,
            'any': any,
            'pow': pow,
            'str': str,
            'int': int,
            'float': float,
            'lambda': lambda: None,  # Este será substituído pela expressão lambda
        }
        
        # Avalia a fórmula no ambiente seguro
        return eval(formula, {"__builtins__": {}}, safe_dict)
    except Exception as e:
        print(f"Erro ao avaliar fórmula '{formula}': {str(e)}")
        return None

def aplicar_formulas(formulas, dados):
    """
    Aplica as fórmulas aos dados fornecidos
    
    Args:
        formulas (dict): Dicionário de fórmulas onde a chave é a coordenada da célula e o valor é a fórmula Excel
        dados (dict): Dicionário com os dados de entrada, onde as chaves são as coordenadas das células
        
    Returns:
        dict: Dados com os resultados das fórmulas aplicadas
    """
    resultado = dados.copy()
    
    # Traduz e aplica cada fórmula
    for celula, formula_excel in formulas.items():
        formula_python = traduzir_formula(formula_excel)
        if formula_python:
            valor = _evaluate_formula(formula_python, resultado)
            resultado[celula] = valor
    
    return resultado

def construir_dependencias(formulas):
    """
    Constrói um grafo de dependências entre as células com fórmulas
    para determinar a ordem correta de cálculo
    
    Args:
        formulas (dict): Dicionário de fórmulas
        
    Returns:
        dict: Grafo de dependências
    """
    dependencias = {}
    
    for celula, formula in formulas.items():
        # Encontra todas as referências de células na fórmula
        referencias = set(re.findall(r'([A-Z]+[0-9]+)', formula))
        dependencias[celula] = referencias
    
    return dependencias

def ordenar_calculos(dependencias):
    """
    Ordena as células para cálculo com base nas dependências
    usando ordenação topológica
    
    Args:
        dependencias (dict): Grafo de dependências
        
    Returns:
        list: Lista ordenada de células para cálculo
    """
    visitados = set()
    ordem = []
    
    def visitar(celula):
        """Visita uma célula e suas dependências recursivamente"""
        if celula in visitados:
            return
        visitados.add(celula)
        
        # Visita todas as dependências primeiro
        for dependencia in dependencias.get(celula, []):
            if dependencia in dependencias:
                visitar(dependencia)
        
        ordem.append(celula)
    
    # Visita todas as células
    for celula in dependencias:
        visitar(celula)
    
    return ordem