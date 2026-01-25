# Intranet ACJOGOS-RJ

Sistema web desenvolvido em **Django** para a gestão de empresas, profissionais e projetos
do setor de jogos digitais do **Estado do Rio de Janeiro**, funcionando como uma **intranet
administrativa** e **vitrine pública de dados agregados**.

O projeto foi desenvolvido no contexto de um **curso de Back-end em Python**, com foco em
boas práticas de arquitetura, autenticação, regras de negócio e persistência de dados.

---

## 🎯 Objetivo do Projeto

Centralizar, organizar e gerenciar informações sobre o ecossistema de jogos digitais do
Estado do Rio de Janeiro, permitindo:

- Cadastro e gerenciamento de empresas e estúdios de jogos
- Associação de projetos às empresas
- Controle de acesso por tipo de usuário
- Visualização pública de dados agregados
- Estrutura preparada para expansão futura (relatórios, pesquisas e dashboards)

---

## 🧩 Funcionalidades Principais

- Autenticação de usuários com controle de permissões
- Perfis de usuário desacoplados do `User` padrão do Django
- Cadastro e edição de empresas
- Cadastro e gerenciamento de projetos vinculados às empresas
- Fluxo de navegação inteligente pós-login
- Área pública para visualização de informações
- Estrutura híbrida:
  - Django Templates
  - Consumo de dados via API

---

## 👥 Tipos de Usuário

- **Diretoria**  
  Acesso total ao sistema, com permissão para gerenciar usuários e dados.

- **Associado**  
  Empresas ou estúdios filiados, com permissão para editar apenas seus próprios dados e projetos.

- **Afiliado**  
  Profissionais independentes, com acesso restrito ao próprio perfil.

- **Público**  
  Visitantes externos, com acesso apenas a informações públicas e agregadas.

---

## 🛠️ Tecnologias Utilizadas

### Back-end
- Python
- Django (Django puro)
- SQLite (banco de dados relacional)

### Front-end
- Django Templates
- Integração com endpoints de API

### Dependências Principais
```txt
asgiref==3.11.0
Django==6.0
python-dotenv==1.2.1
sqlparse==0.5.4
tzdata==2025.3
```

## 🚀 Como Executar o Projeto Localmente

1. Clone o repositório
2. Crie e ative um ambiente virtual
3. Instale as dependências
4. Execute as migrações
5. Inicie o servidor

```bash
python manage.py migrate
python manage.py runserver
