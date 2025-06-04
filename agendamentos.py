import tkinter as tk
from tkinter import messagebox
from db import conectar
from datetime import datetime

def menu_agendamentos(root, frame_anterior):
    if frame_anterior:
        frame_anterior.destroy()

    frame = tk.Frame(root)
    frame.pack(fill="both", expand=True)

    container = tk.Frame(frame)
    container.place(relx=0.5, rely=0.1, anchor="n")

    def criar_label_entry(texto, linha):
        tk.Label(container, text=texto).grid(row=linha, column=0, padx=10, pady=5, sticky="e")
        entrada = tk.Entry(container)
        entrada.grid(row=linha, column=1, padx=10, pady=5)
        return entrada

    entry_id_cliente = criar_label_entry("ID Cliente:", 0)
    entry_id_servico = criar_label_entry("ID Serviço:", 1)
    entry_data = criar_label_entry("Data (DD/MM/AAAA):", 2)
    entry_hora = criar_label_entry("Horário (HH:MM):", 3)
    entry_observacoes = criar_label_entry("Observações:", 4)

    def cadastrar():
        id_cliente = entry_id_cliente.get()
        id_servico = entry_id_servico.get()
        data = entry_data.get()
        hora = entry_hora.get()
        observacoes = entry_observacoes.get()

        if id_cliente and id_servico and data and hora:
            try:
                data_convertida = datetime.strptime(data, "%d/%m/%Y").strftime("%Y-%m-%d")
                conn, cursor = conectar()
                cursor.execute(
                    "INSERT INTO agendamentos (cliente_id, servico_id, data, hora, observacoes) VALUES (?, ?, ?, ?, ?)",
                    (id_cliente, id_servico, data_convertida, hora, observacoes)
                )
                conn.commit()
                conn.close()
                listar()
                entry_id_cliente.delete(0, tk.END)
                entry_id_servico.delete(0, tk.END)
                entry_data.delete(0, tk.END)
                entry_hora.delete(0, tk.END)
                entry_observacoes.delete(0, tk.END)
                messagebox.showinfo("Sucesso", "Agendamento cadastrado com sucesso!")
            except Exception as e:
                messagebox.showerror("Erro ao cadastrar", str(e))
        else:
            messagebox.showerror("Erro", "Todos os campos devem ser preenchidos")

    def editar():
        selecionado = lista.curselection()
        if selecionado:
            index = selecionado[0]
            id_agendamento = lista.get(index).split(" - ")[0]
            id_cliente = entry_id_cliente.get()
            id_servico = entry_id_servico.get()
            data = entry_data.get()
            hora = entry_hora.get()
            observacoes = entry_observacoes.get()
            if id_cliente and id_servico and data and hora:
                try:
                    data_convertida = datetime.strptime(data, "%d/%m/%Y").strftime("%Y-%m-%d")
                    conn, cursor = conectar()
                    cursor.execute("""
                        UPDATE agendamentos 
                        SET cliente_id = ?, servico_id = ?, data = ?, hora = ?, observacoes = ?
                        WHERE id = ?
                    """, (id_cliente, id_servico, data_convertida, hora, observacoes, id_agendamento))
                    conn.commit()
                    conn.close()
                    listar()
                    entry_id_cliente.delete(0, tk.END)
                    entry_id_servico.delete(0, tk.END)
                    entry_data.delete(0, tk.END)
                    entry_hora.delete(0, tk.END)
                    entry_observacoes.delete(0, tk.END)
                except Exception as e:
                    messagebox.showerror("Erro ao editar", str(e))
            else:
                messagebox.showerror("Erro", "Todos os campos devem ser preenchidos")
        else:
            messagebox.showerror("Erro", "Selecione um agendamento para editar")

    def excluir():
        selecionado = lista.curselection()
        if selecionado:
            index = selecionado[0]
            id_agendamento = lista.get(index).split(" - ")[0]
            try:
                conn, cursor = conectar()
                cursor.execute("DELETE FROM agendamentos WHERE id = ?", (id_agendamento,))
                conn.commit()
                conn.close()
                listar()
                entry_id_cliente.delete(0, tk.END)
                entry_id_servico.delete(0, tk.END)
                entry_data.delete(0, tk.END)
                entry_hora.delete(0, tk.END)
            except Exception as e:
                messagebox.showerror("Erro ao excluir", str(e))
        else:
            messagebox.showerror("Erro", "Selecione um agendamento para excluir")

    def listar():
        lista.delete(0, tk.END)
        try:
            conn, cursor = conectar()
            cursor.execute("""
                SELECT a.id, c.nome, s.servico, a.data, a.hora, a.observacoes
                FROM agendamentos a
                JOIN clientes c ON a.cliente_id = c.id
                JOIN servicos s ON a.servico_id = s.id
            """)
            resultados = cursor.fetchall()
            if not resultados:
                lista.insert(tk.END, "Nenhum agendamento encontrado.")
            else:
                for row in resultados:
                    data_formatada = datetime.strptime(row[3], "%Y-%m-%d").strftime("%d/%m/%Y")
                    lista.insert(tk.END, f"{row[0]} - Cliente: {row[1]}, Serviço: {row[2]}, Data: {data_formatada}, Horário: {row[4]}, Observações: {row[5]}")

            conn.close()
        except Exception as e:
            messagebox.showerror("Erro ao listar agendamentos", str(e))

    botoes_frame = tk.Frame(frame)
    botoes_frame.place(relx=0.5, rely=0.45, anchor="n")

    tk.Button(botoes_frame, text="Cadastrar", command=cadastrar, width=15).grid(row=0, column=0, padx=10, pady=5)
    tk.Button(botoes_frame, text="Editar", command=editar, width=15).grid(row=0, column=1, padx=10, pady=5)
    tk.Button(botoes_frame, text="Excluir", command=excluir, width=15).grid(row=0, column=2, padx=10, pady=5)

    lista = tk.Listbox(frame, width=100)
    lista.place(relx=0.5, rely=0.6, anchor="n")

    def voltar():
        from menu import mostrar_menu
        frame.destroy()
        mostrar_menu(root)

    tk.Button(frame, text="Voltar ao Menu", command=voltar).place(relx=0.5, rely=0.95, anchor="s")

    listar()