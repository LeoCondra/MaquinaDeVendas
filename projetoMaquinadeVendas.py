import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

class MaquinaDeVendas:
    def __init__(self):
        self.estado = 's0' 
        self.saldo = 0.0
        self.preco_produto = 2.00
        self.troco = 0.0

    def inserir_moeda(self, moeda):
        transicoes = {
            's0': {'m25': ('s1', 0.25), 'm50': ('s2', 0.50), 'm100': ('s4', 1.00)},
            's1': {'m25': ('s2', 0.25), 'm50': ('s3', 0.50), 'm100': ('s5', 1.00)},
            's2': {'m25': ('s3', 0.25), 'm50': ('s4', 0.50), 'm100': ('s6', 1.00)},
            's3': {'m25': ('s4', 0.25), 'm50': ('s5', 0.50), 'm100': ('s7', 1.00)},
            's4': {'m25': ('s5', 0.25), 'm50': ('s6', 0.50), 'm100': ('s8', 1.00)},
            's5': {'m25': ('s6', 0.25), 'm50': ('s7', 0.50), 'm100': ('s8', 1.00)},
            's6': {'m25': ('s7', 0.25), 'm50': ('s8', 0.50), 'm100': ('s8', 1.00)},
            's7': {'m25': ('s8', 0.25), 'm50': ('s8', 0.50), 'm100': ('s8', 1.00)},
            's8': {}  
        }
        if moeda in transicoes[self.estado]:
            novo_estado, valor_moeda = transicoes[self.estado][moeda]
            self.estado = novo_estado
            self.saldo += valor_moeda

        return self.estado

    def solicitar_refrigerante(self):
        if self.estado == 's8':
            self.troco = self.saldo - self.preco_produto
            self.saldo = 0.0
            self.estado = 's0'
            return f"Refrigerante entregue! Troco: R${self.troco:.2f}"
        else:
            return "Saldo insuficiente! Insira mais moedas."

class Interface:
    def __init__(self, root, maquina, background_image):
        self.root = root
        self.root.title("Simulador de Máquina de Vendas")
        
        window_width = 500
        window_height = 600
        self.root.geometry(f"{window_width}x{window_height}")

        self.maquina = maquina

        background_image = background_image.resize((window_width, window_height))
        self.background_image = ImageTk.PhotoImage(background_image)

        self.bg_label = tk.Label(root, image=self.background_image)
        self.bg_label.place(relwidth=1, relheight=1)

        self.saldo_label = tk.Label(root, text="Saldo: R$0.00", font=("Helvetica", 16), bg="white")
        self.saldo_label.place(x=20, y=20)

        self.moeda_025_btn = tk.Button(root, text="Inserir R$0.25", command=lambda: self.inserir_moeda('m25'), font=("Helvetica", 12))
        self.moeda_025_btn.place(x=20, y=100)   

        self.moeda_050_btn = tk.Button(root, text="Inserir R$0.50", command=lambda: self.inserir_moeda('m50'), font=("Helvetica", 12))
        self.moeda_050_btn.place(x=20, y=150)

        self.moeda_100_btn = tk.Button(root, text="Inserir R$1.00", command=lambda: self.inserir_moeda('m100'), font=("Helvetica", 12))
        self.moeda_100_btn.place(x=20, y=200)

        self.refrigerante_btn = tk.Button(root, text="Solicitar Refrigerante", command=self.solicitar_refrigerante, font=("Helvetica", 12))
        self.refrigerante_btn.place(x=20, y=250)

    def inserir_moeda(self, moeda):
        resultado = self.maquina.inserir_moeda(moeda)
        self.saldo_label.config(text=f"Saldo: R${self.maquina.saldo:.2f}")
        if resultado != self.maquina.estado:
            messagebox.showinfo("Estado", f"Estado atual: {self.maquina.estado}")

    def solicitar_refrigerante(self):
        resultado = self.maquina.solicitar_refrigerante()
        self.saldo_label.config(text=f"Saldo: R${self.maquina.saldo:.2f}")
        messagebox.showinfo("Resultado", resultado)


if __name__ == "__main__":
    root = tk.Tk()
    background_image = Image.open("maquinaDeVendas.jpg")
    maquina = MaquinaDeVendas()
    app = Interface(root, maquina, background_image)
    root.mainloop()
