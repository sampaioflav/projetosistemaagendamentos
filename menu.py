import tkinter as tk
import clientes
import servicos
import agendamentos
from logs import registrar_log  

def mostrar_menu(root, email=None, frame=None):
    if frame:
        frame.destroy()

    registrar_log(f"Acesso ao menu principal: {email}")

    frame = tk.Frame(root)
    frame.pack(fill="both", expand=True)

    container = tk.Frame(frame)
    container.pack(expand=True)

    tk.Label(container, text="Menu Principal", font=("Arial", 16)).pack(pady=(0, 20))

    tk.Button(container, text="Clientes", width=20,
              command=lambda: clientes.menu_clientes(root, frame)).pack(pady=5)

    tk.Button(container, text="Serviços", width=20,
              command=lambda: servicos.menu_servicos(root, frame)).pack(pady=5)

    tk.Button(container, text="Agendamentos", width=20,
              command=lambda: agendamentos.menu_agendamentos(root, frame)).pack(pady=5)

    if email == "administrator@email.com":
        tk.Button(container, text="Relatórios do Sistema", width=20,
                  command=lambda: mostrar_logs(root)).pack(pady=5)  # corrigido

    tk.Button(container, text="Sair", width=20, command=root.quit).pack(pady=20)

def mostrar_logs(root):  # corrigido
    from logs import mostrar_tela_logs
    mostrar_tela_logs(root)
