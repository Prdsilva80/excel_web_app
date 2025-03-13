"""
Módulo de autenticação e autorização
Fornece funções auxiliares para controle de acesso e permissões
"""
from functools import wraps
from flask import flash, redirect, url_for
from flask_login import current_user

def verificar_admin(f):
    """
    Decorador para verificar se o usuário é administrador.
    Uso:
        @verificar_admin
        def minha_rota_admin():
            # código aqui
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            flash('Acesso restrito a administradores.', 'danger')
            return redirect(url_for('dashboard'))
        return f(*args, **kwargs)
    return decorated_function

def verificar_permissao(planilha_id=None, dado_id=None):
    """
    Verifica se o usuário atual tem permissão para acessar uma planilha ou dado específico.
    
    Args:
        planilha_id: ID da planilha a verificar
        dado_id: ID do dado da planilha a verificar
        
    Returns:
        bool: True se tem permissão, False caso contrário
    """
    from models import Planilha, DadosPlanilha
    
    # Administrador tem acesso a tudo
    if current_user.is_admin:
        return True
        
    # Verificar acesso a um dado específico
    if dado_id:
        dado = DadosPlanilha.query.get(dado_id)
        if not dado:
            return False
        return dado.user_id == current_user.id
    
    # Verificar acesso a uma planilha
    if planilha_id:
        # Qualquer usuário pode ver qualquer planilha
        planilha = Planilha.query.get(planilha_id)
        return planilha is not None
        
    return False

def criar_token_acesso(user_id, expiracao=3600):
    """
    Cria um token de acesso temporário para um usuário.
    Útil para compartilhamento de links ou reset de senha.
    
    Args:
        user_id: ID do usuário
        expiracao: Tempo de validade em segundos (padrão: 1 hora)
        
    Returns:
        str: Token de acesso
    """
    import jwt
    import datetime
    from flask import current_app
    
    payload = {
        'user_id': user_id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=expiracao)
    }
    
    token = jwt.encode(
        payload,
        current_app.config['SECRET_KEY'],
        algorithm='HS256'
    )
    
    return token

def verificar_token(token):
    """
    Verifica a validade de um token de acesso.
    
    Args:
        token: Token a verificar
        
    Returns:
        dict|None: Payload do token se válido, None caso contrário
    """
    import jwt
    from flask import current_app
    
    try:
        payload = jwt.decode(
            token,
            current_app.config['SECRET_KEY'],
            algorithms=['HS256']
        )
        return payload
    except:
        return None