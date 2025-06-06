import tkinter as tk  #atualizado
from tkinter import messagebox
from db import conectar
from validations import validar_nome, validar_preco, validar_inteiro_positivo
from logs import registrar_log

def validar_campos(servico, preco, descricao, duracao, categoria):
    if not servico or not preco or not descricao or not duracao or not categoria:
        messagebox.showerror("Erro", "Todos os campos devem ser preenchidos")
        return False
    if not validar_nome(servico):
        messagebox.showerror("Erro", "Nome do serviço inválido")
        return False
    try:
        preco_float = float(preco)
        if preco_float < 0:
            raise ValueError
    except:
        messagebox.showerror("Erro", "Preço inválido")
        return False
    if not validar_inteiro_positivo(duracao):
        messagebox.showerror("Erro", "Duração deve ser um número inteiro positivo")
        return False
    return True

def menu_servicos(root, frame_anterior=None):
    if frame_anterior:
        frame_anterior.destroy()

    frame = tk.Frame(root)
    frame.pack(fill="both", expand=True)

    conteudo = tk.Frame(frame)
    conteudo.pack(expand=True)

    tk.Label(conteudo, text="Cadastro de Serviços", font=("Arial", 16)).pack(pady=10)

    def criar_linha(label_text):
        linha = tk.Frame(conteudo)
        linha.pack(pady=5)
        tk.Label(linha, text=label_text, width=12, anchor="e").pack(side="left")
        entry = tk.Entry(linha, width=30)
        entry.pack(side="left")
        return entry

    entry_servico = criar_linha("Serviço:")
    entry_preco = criar_linha("Preço:")
    entry_descricao = criar_linha("Descrição:")
    entry_duracao = criar_linha("Duração (min):")
    entry_categoria = criar_linha("Categoria:")

    servico_em_edicao = None

    def limpar_campos():
        entry_servico.delete(0, tk.END)
        entry_preco.delete(0, tk.END)
        entry_descricao.delete(0, tk.END)
        entry_duracao.delete(0, tk.END)
        entry_categoria.delete(0, tk.END)

    def cadastrar():
        servico = entry_servico.get().strip()
        preco = entry_preco.get().strip()
        descricao = entry_descricao.get().strip()
        duracao = entry_duracao.get().strip()
        categoria = entry_categoria.get().strip()

        if not validar_campos(servico, preco, descricao, duracao, categoria):
            return

        conn, cursor = conectar()
        cursor.execute(
            "INSERT INTO servicos (servico, preco, descricao, duracao, categoria) VALUES (?, ?, ?, ?, ?)",
            (servico, preco, descricao, int(duracao), categoria)
        )
        conn.commit()
        conn.close()
        listar()
        limpar_campos()
        registrar_log(f"Cadastro: Serviço '{servico}' cadastrado.")
        messagebox.showinfo("Sucesso", "Serviço cadastrado com sucesso!")

    def editar():
        nonlocal servico_em_edicao
        selecionado = lista.curselection()
        if selecionado:
            index = selecionado[0]
            dados = lista.get(index).split(" - ")
            servico_em_edicao = dados[0]
            entry_servico.delete(0, tk.END)
            entry_preco.delete(0, tk.END)
            entry_descricao.delete(0, tk.END)
            entry_duracao.delete(0, tk.END)
            entry_categoria.delete(0, tk.END)

            entry_servico.insert(0, dados[1])
            entry_preco.insert(0, dados[2])
            entry_descricao.insert(0, dados[3])
            entry_duracao.insert(0, dados[4])
            entry_categoria.insert(0, dados[5])
        else:
            messagebox.showerror("Erro", "Selecione um serviço para editar")

    def salvar_alteracao():
        nonlocal servico_em_edicao
        if not servico_em_edicao:
            messagebox.showerror("Erro", "Nenhum serviço está sendo editado")
            return

        servico = entry_servico.get().strip()
        preco = entry_preco.get().strip()
        descricao = entry_descricao.get().strip()
        duracao = entry_duracao.get().strip()
        categoria = entry_categoria.get().strip()

        if not validar_campos(servico, preco, descricao, duracao, categoria):
            return

        conn, cursor = conectar()
        cursor.execute(
            "UPDATE servicos SET servico = ?, preco = ?, descricao = ?, duracao = ?, categoria = ? WHERE id = ?",
            (servico, preco, descricao, int(duracao), categoria, servico_em_edicao)
        )
        conn.commit()
        conn.close()
        registrar_log(f"Edição: Serviço '{servico}' (ID {servico_em_edicao}) atualizado.")
        servico_em_edicao = None
        listar()
        limpar_campos()
        messagebox.showinfo("Sucesso", "Serviço atualizado com sucesso!")

    def excluir():
        confirmar = messagebox.askyesno("Confirmação", "Tem certeza que deseja excluir este serviço?")
        if not confirmar:
            return

        selecionado = lista.curselection()
        if selecionado:
            index = selecionado[0]
            linha = lista.get(index)
            partes = linha.split(" - ")
            id_servico = partes[0]
            nome_servico = partes[1]

            conn, cursor = conectar()
            cursor.execute("DELETE FROM servicos WHERE id = ?", (id_servico,))
            conn.commit()
            conn.close()
            listar()
            limpar_campos()
            registrar_log(f"Exclusão: Serviço '{nome_servico}' (ID {id_servico}) excluído.")
            messagebox.showinfo("Sucesso", "Serviço excluído com sucesso!")
        else:
            messagebox.showerror("Erro", "Selecione um serviço para excluir")

    def listar():
        lista.delete(0, tk.END)
        conn, cursor = conectar()
        cursor.execute("SELECT * FROM servicos")
        for row in cursor.fetchall():
            # id, servico, preco, descricao, duracao, categoria
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
