
# Sistema de Agendamento para uma Clínica de Estética - Studio Sublime (nome fictício)

Este é um sistema desktop de agendamentos desenvolvido em **Python** com interface gráfica usando **Tkinter** e banco de dados **SQLite**. O sistema foi projetado para facilitar o gerenciamento de **clientes**, **serviços** e **agendamentos** em uma clínica de estética.

## Objetivo Acadêmico e Portfólio

Este projeto foi desenvolvido com fins **acadêmicos** e para compor o **portfólio profissional** dos autores. O foco está no aprendizado prático de desenvolvimento de aplicações com interface gráfica, persistência de dados e organização modular de código em Python.

## Funcionalidades

- Tela de **Login e Cadastro de Usuário**
- Tela principal com menu de navegação
- Cadastro, edição e exclusão de **Clientes**
- Cadastro, edição e exclusão de **Serviços**
- Cadastro, edição, exclusão e listagem de **Agendamentos**
- **Validações** de entrada (ex: campos obrigatórios, datas/hora válidas)
- Registro de **logs de ações** (cadastro, edição e exclusão)
- Tela de **relatórios** acessível apenas pelo administrador (`administrator@email.com` / senha `0000`)
- Interface simples, funcional e centralizada

## Estrutura do Projeto

```
projeto_sistemaagendamentos/
├── main.py               # Arquivo principal para iniciar a aplicação
├── db.py                 # Conexão e criação do banco de dados SQLite
├──login.py               # Tela de login e cadastro de usuários
├── menu_principal.py     # Tela principal do sistema após login
├── clientes.py           # Tela de gerenciamento de clientes
├── servicos.py           # Tela de gerenciamento de serviços
├── agendamentos.py       # Tela de gerenciamento de agendamentos
├── relatorios.py         # Tela de exibição de logs para o administrador
├── logs.py               # Funções de geração e salvamento de logs
├── validations.py        # Funções auxiliares de validação (e-mail, CPF, senha etc.)
└── README.md             # Documentação do projeto
```

##  Tecnologias Utilizadas

- **Python 3.11.3**
- **Tkinter** (interface gráfica)
- **SQLite3** (banco de dados local)

## Login Administrador

Para acessar os **relatórios do sistema**, utilize as credenciais de administrador:

- **Usuário**: `administrator@email.com`
- **Senha**: `0000`

##  Como Executar o Projeto

1. Clone este repositório:
   ```bash
   git clone https://github.com/sampaioflav/projetosistemaagendamentos.git
   cd projeto_agendamento
   ```

2. Execute o script principal:
   ```bash
   python main.py
   ```

> **Nota:** O sistema criará o banco de dados automaticamente na primeira execução, se ele não existir.

##  Requisitos

- Python 3.10 ou superior
- Bibliotecas padrão (Tkinter, SQLite, datetime)


## Autores

Desenvolvido por **Flavia Sampaio**   
Projeto acadêmico e de portfólio com foco em desenvolvimento Python com interface gráfica.  

