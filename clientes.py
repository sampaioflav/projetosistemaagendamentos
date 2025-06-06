import tkinter as tk   #atualizado
from tkinter import messagebox
from db import conectar
from validations import validar_nome, validar_telefone, validar_email, validar_cpf, formatar_telefone
from logs import registrar_log  

def validar_campos(nome, telefone, email, cpf, endereco):
    if not nome or not telefone or not email or not cpf or not endereco:
        messagebox.showerror("Erro", "Todos os campos devem ser preenchidos")
        return False
    if not validar_nome(nome):
        messagebox.showerror("Erro", "Nome inválido")
        return False
    if not validar_telefone(telefone):
        messagebox.showerror("Erro", "Telefone no formato inválido")
        return False
    if not validar_email(email):
        messagebox.showerror("Erro", "Email inválido")
        return False
    if not validar_cpf(cpf):
        messagebox.showerror("Erro", "CPF inválido")
        return False
    
    return True

def menu_clientes(root, frame_anterior=None):
    if frame_anterior:
        frame_anterior.destroy()

    frame = tk.Frame(root)
    frame.pack(fill="both", expand=True)

    conteudo = tk.Frame(frame)
    conteudo.pack(expand=True)

    tk.Label(conteudo, text="Cadastro de Clientes", font=("Arial", 16)).pack(pady=10)

    def criar_linha(label_text):
        linha = tk.Frame(conteudo)
        linha.pack(pady=5)
        tk.Label(linha, text=label_text, width=12, anchor="e").pack(side="left")
        entry = tk.Entry(linha, width=30)
        entry.pack(side="left")
        return entry

    entry_nome = criar_linha("Nome:")
    entry_telefone = criar_linha("Telefone:")
    entry_email = criar_linha("Email:")
    entry_cpf = criar_linha("CPF:")
    entry_endereco = criar_linha("Endereço:")

    cliente_em_edicao = None  

    def limpar_campos():
        entry_nome.delete(0, tk.END)
        entry_telefone.delete(0, tk.END)
        entry_email.delete(0, tk.END)
        entry_cpf.delete(0, tk.END)
        entry_endereco.delete(0, tk.END)

    def cadastrar():
        nome = entry_nome.get().strip()
        telefone = entry_telefone.get().strip()
        email = entry_email.get().strip()
        cpf = entry_cpf.get().strip()
        endereco = entry_endereco.get().strip()

        if not validar_campos(nome, telefone, email, cpf, endereco):
            return

        telefone_formatado = formatar_telefone(telefone)

        conn, cursor = conectar()
        cursor.execute(
            "INSERT INTO clientes (nome, telefone, email, cpf, endereco) VALUES (?, ?, ?, ?, ?)",
            (nome, telefone_formatado, email, cpf, endereco)
        )
        conn.commit()
        conn.close()
        listar()
        limpar_campos()
        registrar_log(f"Cadastro: Cliente '{nome}' cadastrado.")
        messagebox.showinfo("Sucesso", "Cliente cadastrado com sucesso!")

    def editar():
        nonlocal cliente_em_edicao
        selecionado = lista.curselection()
        if selecionado:
            index = selecionado[0]
            dados = lista.get(index).split(" - ")
            cliente_em_edicao = dados[0]  
            entry_nome.delete(0, tk.END)
            entry_telefone.delete(0, tk.END)
            entry_email.delete(0, tk.END)
            entry_cpf.delete(0, tk.END)
            entry_endereco.delete(0, tk.END)

            entry_nome.insert(0, dados[1])
            entry_telefone.insert(0, dados[2])
            entry_email.insert(0, dados[3])
            entry_cpf.insert(0, dados[4])
            entry_endereco.insert(0, dados[5])
        else:
            messagebox.showerror("Erro", "Selecione um cliente para editar")

    def salvar_alteracao():
        nonlocal cliente_em_edicao
        if not cliente_em_edicao:
            messagebox.showerror("Erro", "Nenhum cliente está sendo editado")
            return

        novo_nome = entry_nome.get().strip()
        novo_telefone = entry_telefone.get().strip()
        novo_email = entry_email.get().strip()
        novo_cpf = entry_cpf.get().strip()
        novo_endereco = entry_endereco.get().strip()

        if not validar_campos(novo_nome, novo_telefone, novo_email, novo_cpf, novo_endereco):
            return

        telefone_formatado = formatar_telefone(novo_telefone)

        conn, cursor = conectar()
        cursor.execute(
            "UPDATE clientes SET nome = ?, telefone = ?, email = ?, cpf = ?, endereco = ? WHERE id = ?",
            (novo_nome, telefone_formatado, novo_email, novo_cpf, novo_endereco, cliente_em_edicao)
        )
        conn.commit()
        conn.close()
        registrar_log(f"Edição: Cliente '{novo_nome}' (ID {cliente_em_edicao}) atualizado.")
        cliente_em_edicao = None
        listar()
        limpar_campos()
        messagebox.showinfo("Sucesso", "Cliente atualizado com sucesso!")

    def excluir():
        confirmar = messagebox.askyesno("Confirmação", "Tem certeza que deseja excluir este cliente?")
        if not confirmar:
            return

        selecionado = lista.curselection()
        if selecionado:
            index = selecionado[0]
            linha = lista.get(index)
            partes = linha.split(" - ")
            id_cliente = partes[0]
            nome_cliente = partes[1]

            conn, cursor = conectar()
            cursor.execute("DELETE FROM clientes WHERE id = ?", (id_cliente,))
            conn.commit()
            conn.close()
            listar()
            limpar_campos()
            registrar_log(f"Exclusão: Cliente '{nome_cliente}' (ID {id_cliente}) excluído.")
            messagebox.showinfo("Sucesso", "Cliente excluído com sucesso!")
        else:
            messagebox.showerror("Erro", "Selecione um cliente para excluir")

    def listar():
        lista.delete(0, tk.END)
        conn, cursor = conectar()
        cursor.execute("SELECT * FROM clientes")
        for row in cursor.fetchall():
            
            lista.insert(tk.END, f"{row[0]} - {row[1]} - {row[2]} - {row[3]} - {row[4]} - {row[5]}")
        conn.close()

    linha_botoes = tk.Frame(conteudo)
    linha_botoes.pack(pady=10)
    tk.Button(linha_botoes, text="Cadastrar", command=cadastrar, width=12).pack(side="left", padx=5)
    tk.Button(linha_botoes, text="Editar", command=editar, width=12).pack(side="left", padx=5)
    tk.Button(linha_botoes, text="Salvar Alteração", command=salvar_alteracao, width=15).pack(side="left", padx=5)
    tk.Button(linha_botoes, text="Excluir", command=excluir, width=12).pack(side="left", padx=5)

    lista = tk.Listbox(conteudo, width=90)
    lista.pack(pady=10)

    def voltar():
        from menu_principal import mostrar_menu
        frame.destroy()
        mostrar_menu(root)

    tk.Button(conteudo, text="Voltar ao Menu", command=voltar, width=30).pack(pady=10)

    listar()
