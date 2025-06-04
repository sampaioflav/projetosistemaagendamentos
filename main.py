import tkinter as tk
from tkinter import messagebox
from db import criar_tabelas, cadastrar_usuario, validar_login, registrar_log
from logs import registrar_log
from menu import mostrar_menu

criar_tabelas()

def tela_login():
    limpar_tela()

    tk.Label(root, text="Email").pack(pady=5)
    email_entry = tk.Entry(root)
    email_entry.pack()

    tk.Label(root, text="Senha").pack(pady=5)
    senha_entry = tk.Entry(root, show="*")
    senha_entry.pack()

    def entrar():
        email = email_entry.get()
        senha = senha_entry.get()

        if "@" not in email:
            messagebox.showerror("Erro", "Formato de Email inválido")
            return

        if validar_login(email, senha):
            registrar_log(f"Login realizado com sucesso: {email}")
            limpar_tela()
            mostrar_menu(root, email)
        else:
            registrar_log(f"Tentativa de login inválida: {email}")
            messagebox.showerror("Erro", "Email ou senha inválidos.")

    def ir_para_cadastro():
        tela_cadastro()

    frame_botoes = tk.Frame(root)
    frame_botoes.pack(pady=10)
    tk.Button(frame_botoes, text="Fazer Cadastro", command=ir_para_cadastro).grid(row=0, column=0, padx=10)
    tk.Button(frame_botoes, text="Entrar", command=entrar).grid(row=0, column=1, padx=10)

def tela_cadastro():
    limpar_tela()

    tk.Label(root, text="Nome").pack()
    nome_entry = tk.Entry(root)
    nome_entry.pack()

    tk.Label(root, text="CPF").pack()
    cpf_entry = tk.Entry(root)
    cpf_entry.pack()

    def validar_cpf(tecla):
        return tecla.isdigit() and len(cpf_entry.get()) < 11

    cpf_entry.config(validate="key", validatecommand=(root.register(validar_cpf), '%S'))

    tk.Label(root, text="Email").pack()
    email_entry = tk.Entry(root)
    email_entry.pack()

    tk.Label(root, text="Senha").pack()
    senha_entry = tk.Entry(root, show="*")
    senha_entry.pack()

    tk.Label(root, text="Confirmar Senha").pack()
    confirmar_entry = tk.Entry(root, show="*")
    confirmar_entry.pack()

    def cadastrar():
        nome = nome_entry.get()
        cpf = cpf_entry.get()
        email = email_entry.get()
        senha = senha_entry.get()
        confirmar = confirmar_entry.get()

        if not email or "@" not in email:
            messagebox.showerror("Erro", "Formato de Email inválido")
            return

        if not cpf.isdigit() or len(cpf) != 11:
            messagebox.showerror("Erro", "CPF inválido. Deve conter 11 números.")
            return

        if senha != confirmar:
            messagebox.showerror("Erro", "As senhas não coincidem.")
            return

        sucesso = cadastrar_usuario(nome, cpf, email, senha)
        if sucesso:
            registrar_log(f"Novo usuário cadastrado: {email}")
            messagebox.showinfo("Sucesso", "Cadastro realizado com sucesso.")
            tela_login()
        else:
            messagebox.showerror("Erro", "Email já cadastrado.")

    tk.Button(root, text="Cadastrar", command=cadastrar).pack(pady=10)

def limpar_tela():
    for widget in root.winfo_children():
        widget.destroy()

root = tk.Tk()
root.title("Studio Sublime - Sistema de Agendamentos")
root.geometry("400x400")
tela_login()
root.mainloop()
