# Sistema de Migração de Planilhas Excel para Aplicação Web

Um sistema completo para migrar planilhas Excel personalizadas para um ambiente web seguro, com controle de acesso, processamento de fórmulas e geração de relatórios.

## 📋 Visão Geral

Este sistema permite importar planilhas Excel, transformá-las em formulários web interativos e disponibilizá-las para usuários autorizados, enquanto mantém a funcionalidade das fórmulas originais. Os dados inseridos ficam armazenados em um banco de dados central, permitindo consultas, histórico e relatórios personalizados.

### Principais Funcionalidades

- **Importação de Planilhas Excel**: Suporte para arquivos .xlsx e .xls com extração automática de estrutura e fórmulas
- **Autenticação e Autorização**: Sistema de login seguro com diferentes níveis de acesso (admin e usuário comum)
- **Formulários Dinâmicos**: Criação automática de formulários web baseados na estrutura da planilha original
- **Processamento de Fórmulas**: Execução dos cálculos originais das planilhas Excel no ambiente web
- **Armazenamento Centralizado**: Banco de dados SQL para armazenar todos os dados inseridos pelos usuários
- **Histórico e Relatórios**: Visualização do histórico de dados inseridos e geração de relatórios
- **Interface Responsiva**: Design adaptável para diferentes dispositivos e tamanhos de tela

## 🛠️ Tecnologias Utilizadas

- **Backend**: Python 3.x, Flask
- **ORM**: SQLAlchemy
- **Banco de Dados**: SQLite (desenvolvimento), PostgreSQL (produção)
- **Autenticação**: Flask-Login
- **Processamento de Excel**: Pandas, Openpyxl
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap 5
- **Templates**: Jinja2

## 🚀 Instalação e Execução

### Pré-requisitos

- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)
- Ambiente virtual (recomendado)

### Passos para Instalação

1. Clone o repositório:
   ```bash
   git clone https://github.com/seu-usuario/excel-web-app.git
   cd excel-web-app
   ```

2. Crie e ative um ambiente virtual:
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # Linux/Mac
   source venv/bin/activate
   ```

3. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure as variáveis de ambiente (opcional):
   ```bash
   # Windows
   set FLASK_ENV=development
   
   # Linux/Mac
   export FLASK_ENV=development
   ```

5. Execute a aplicação:
   ```bash
   python app.py
   ```

6. Acesse a aplicação no navegador:
   ```
   http://localhost:5000
   ```

7. Faça login com o usuário administrador padrão:
   ```
   Email: admin@example.com
   Senha: admin123
   ```

### Configuração para Produção

Para ambientes de produção, edite o arquivo `config.py` ajustando as seguintes configurações:

- Altere `SECRET_KEY` para uma string aleatória e segura
- Configure `SQLALCHEMY_DATABASE_URI` para apontar para seu banco de dados de produção
- Defina `SESSION_COOKIE_SECURE` e `REMEMBER_COOKIE_SECURE` como `True` se estiver usando HTTPS

## 📁 Estrutura do Projeto

```
excel_web_app/
│
├── app.py                      # Arquivo principal da aplicação Flask
├── config.py                   # Configurações da aplicação
├── requirements.txt            # Dependências do projeto
│
├── static/                     # Arquivos estáticos
│   ├── css/
│   │   ├── main.css            # Estilos principais
│   │   ├── admin.css           # Estilos da área administrativa
│   │   └── forms.css           # Estilos específicos para formulários
│   ├── js/
│   │   └── main.js             # JavaScript principal
│   └── img/
│
├── templates/                  # Templates HTML do Flask
│   ├── base.html               # Template base
│   ├── login.html              # Página de login
│   ├── dashboard.html          # Dashboard principal
│   ├── planilha.html           # Visualização/edição de planilha
│   ├── relatorios.html         # Lista de relatórios
│   ├── ver_relatorio.html      # Visualizar um relatório específico
│   │
│   └── admin/                  # Templates da área administrativa
│       ├── dashboard.html      # Dashboard admin
│       ├── usuarios.html       # Gerenciar usuários
│       ├── novo_usuario.html   # Criar novo usuário
│       ├── editar_usuario.html # Editar usuário
│       ├── planilhas.html      # Gerenciar planilhas
│       └── importar_planilha.html # Importar planilha
│
├── uploads/                    # Pasta para upload temporário de arquivos
│
├── models/                     # Modelos de banco de dados
│   ├── __init__.py
│   ├── user.py                 # Modelo de usuário
│   ├── planilha.py             # Modelo de planilha
│   └── dados_planilha.py       # Modelo de dados de planilha
│
└── modules/                    # Módulos Python da aplicação
    ├── __init__.py
    ├── auth.py                 # Autenticação e gerenciamento de usuários
    ├── excel_parser.py         # Parser de planilhas Excel
    ├── formula_translator.py   # Tradutor de fórmulas Excel para Python
    └── data_processor.py       # Processamento de dados
```

## 🔒 Segurança

- Senhas armazenadas com hash seguro usando `werkzeug.security`
- Proteção contra CSRF em formulários
- Validação de entrada em todos os formulários
- Controle de acesso baseado em autenticação e autorização
- Sessões criptografadas
- Proteção contra download não autorizado de planilhas originais

## 📝 Fluxo de Uso

### Administrador

1. Faz login no sistema com credenciais de administrador
2. Acessa o painel administrativo
3. Importa planilhas Excel através do formulário de importação
4. Gerencia usuários (criar, editar, excluir)
5. Monitora o uso do sistema através do dashboard administrativo

### Usuário Comum

1. Recebe credenciais de acesso do administrador
2. Faz login no sistema
3. Visualiza as planilhas disponíveis no dashboard
4. Seleciona uma planilha para preencher
5. Insere os dados no formulário web
6. Salva os dados (cálculos são processados automaticamente)
7. Acessa o histórico e relatórios dos seus dados inseridos

## 🔄 Processamento de Fórmulas

O sistema converte fórmulas Excel em código Python executável, mantendo a funcionalidade original:

1. **Extração**: As fórmulas são extraídas da planilha Excel durante a importação
2. **Tradução**: Convertidas para equivalentes em Python usando o módulo `formula_translator.py`
3. **Aplicação**: Quando o usuário insere dados, as fórmulas são aplicadas para calcular automaticamente os resultados
4. **Armazenamento**: Tanto os dados inseridos quanto os resultados calculados são armazenados no banco de dados

## 🚧 Limitações Atuais

- Suporte limitado para funções Excel complexas ou personalizadas
- Não há suporte para macros VBA
- Formatação visual limitada comparada ao Excel original
- Suporte limitado para fórmulas entre planilhas diferentes do mesmo arquivo

## 🔍 Testes

Execute os testes unitários com:

```bash
python -m unittest discover tests
```

## 📈 Roadmap Futuro

- [ ] Exportação de dados para Excel/CSV
- [ ] Suporte para gráficos e visualizações
- [ ] Personalização de temas e cores
- [ ] API REST para integração com outros sistemas
- [ ] Notificações por email
- [ ] Comentários e colaboração em tempo real
- [ ] Suporte para upload em lote de múltiplas planilhas
- [ ] Auditoria e logs de atividades detalhados

## 👥 Contribuição

Contribuições são bem-vindas! Por favor, siga estas etapas:

1. Faça fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/nova-funcionalidade`)
3. Implemente suas alterações
4. Execute os testes para garantir que nada foi quebrado
5. Faça commit das suas alterações (`git commit -m 'feat: Adiciona nova funcionalidade'`)
6. Faça push para a branch (`git push origin feature/nova-funcionalidade`)
7. Abra um Pull Request

## 📄 Licença

Este projeto está licenciado sob a licença MIT - veja o arquivo [LICENSE](LICENSE) para mais detalhes.

---

Desenvolvido com ❤️ por Paulo Roberto