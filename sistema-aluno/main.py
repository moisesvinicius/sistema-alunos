import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime

class Aluno:
    def __init__(self, nome, data_matricula):
        self.nome = nome
        self.data_matricula = data_matricula

class SistemaAlunos:
    def __init__(self, master):
        self.master = master
        self.master.title("Sistema de Alunos")
        self.master.geometry("600x400")
        self.master.configure(bg="#e9ecef")

        self.alunos = []
        self.selected_aluno_index = None

        # Criação da interface
        self.create_widgets()

    def create_widgets(self):
        # Frame para lista de alunos
        self.frame_lista = tk.Frame(self.master, bg="#e9ecef")
        self.frame_lista.pack(pady=10)

        self.tree = ttk.Treeview(self.frame_lista, columns=("Nome", "Data"), show='headings', style="Treeview")
        self.tree.heading("Nome", text="Nome")
        self.tree.heading("Data", text="Data")
        self.tree.pack(side=tk.LEFT)

        self.scrollbar = ttk.Scrollbar(self.frame_lista, orient="vertical", command=self.tree.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.configure(yscrollcommand=self.scrollbar.set)

        # Estilo para Treeview
        style = ttk.Style()
        style.configure("Treeview", background="#ffffff", foreground="#333333", rowheight=25, fieldbackground="#ffffff")
        style.map("Treeview", background=[("selected", "#007bff")])

        # Botões
        self.btn_frame = tk.Frame(self.master, bg="#e9ecef")
        self.btn_frame.pack(pady=20)

        self.btn_add = tk.Button(self.btn_frame, text="Adicionar Aluno", command=self.add_aluno, bg="#28a745", fg="white", padx=10)
        self.btn_add.pack(side=tk.LEFT, padx=5)

        self.btn_edit = tk.Button(self.btn_frame, text="Editar Aluno", command=self.edit_aluno, bg="#17a2b8", fg="white", padx=10)
        self.btn_edit.pack(side=tk.LEFT, padx=5)

        self.btn_delete = tk.Button(self.btn_frame, text="Deletar Aluno", command=self.delete_aluno, bg="#dc3545", fg="white", padx=10)
        self.btn_delete.pack(side=tk.LEFT, padx=5)

        self.tree.bind("<<TreeviewSelect>>", self.on_select)

    def load_data(self):
        # Limpa a Treeview antes de carregar os dados
        for item in self.tree.get_children():
            self.tree.delete(item)
        for aluno in self.alunos:
            self.tree.insert("", tk.END, values=(aluno.nome, aluno.data_matricula.strftime("%d/%m/%Y")))

    def add_aluno(self):
        self.open_form("Adicionar Aluno", None)

    def edit_aluno(self):
        if self.selected_aluno_index is not None:
            self.open_form("Editar Aluno", self.alunos[self.selected_aluno_index])
        else:
            messagebox.showwarning("Selecione um aluno", "Por favor, selecione um aluno para editar.")

    def delete_aluno(self):
        if self.selected_aluno_index is not None:
            confirm = messagebox.askyesno("Confirmar Deletar", "Você tem certeza que deseja deletar este aluno?")
            if confirm:
                del self.alunos[self.selected_aluno_index]
                self.selected_aluno_index = None
                self.load_data()
        else:
            messagebox.showwarning("Selecione um aluno", "Por favor, selecione um aluno para deletar.")

    def on_select(self, event):
        selected_item = self.tree.selection()
        if selected_item:
            item = self.tree.item(selected_item)
            nome = item['values'][0]
            data_matricula = datetime.strptime(item['values'][1], "%d/%m/%Y")
            self.selected_aluno_index = self.tree.index(selected_item[0])  # Armazena o índice do aluno selecionado

    def open_form(self, title, aluno):
        form_window = tk.Toplevel(self.master)
        form_window.title(title)
        form_window.configure(bg="#f8f9fa")

        tk.Label(form_window, text="Nome:", bg="#f8f9fa").grid(row=0, column=0, padx=10, pady=10)
        nome_entry = tk.Entry(form_window)
        nome_entry.grid(row=0, column=1, padx=10, pady=10)

        if aluno:
            nome_entry.insert(0, aluno.nome)

        def save():
            nome = nome_entry.get().strip()
            if nome:
                if aluno:
                    aluno.nome = nome  # Atualiza o nome do aluno
                else:
                    new_aluno = Aluno(nome, datetime.now())
                    self.alunos.append(new_aluno)
                self.load_data()
                form_window.destroy()
            else:
                messagebox.showwarning("Campo Vazio", "Por favor, insira um nome.")

        tk.Button(form_window, text="Salvar", command=save, bg="#007bff", fg="white").grid(row=1, column=0, columnspan=2, pady=10)

if __name__ == "__main__":
    root = tk.Tk()
    app = SistemaAlunos(root)
    root.mainloop()
