import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog

tipo_registradores = {
    "$R0": "r0",
    "$R1": "at",
    "$R2": "v0",
    "$R3": "v1",
    "$R4": "a0",
    "$R5": "a1",
    "$R6": "a2",
    "$R7": "a3",
    "$R8": "t0",
    "$R9": "t1",
    "$R10": "t2",
    "$R11": "t3",
    "$R12": "t4",
    "$R13": "t5",
    "$R14": "t6",
    "$R15": "t7",
    "$R16": "s0",
    "$R17": "s1",
    "$R18": "s2",
    "$R19": "s3",
    "$R20": "s4",
    "$R21": "s5",
    "$R22": "s6",
    "$R23": "s7",
    "$R24": "t8",
    "$R25": "t9",
    "$R26": "k0",
    "$R27": "k1",
    "$R28": "gp",
    "$R29": "sp",
    "$R30": "fp",
    "$R31": "ra",
}


class Registradores:
    def __init__(self, nome, tipo):
        self.nome = nome
        self.valor = 0
        self.tipo = tipo

    def set_value(self, value):
        self.value = value
    
    def get_value(self):
        return self.value

    def __repr__(self):
        return f"{self.nome} ({self.tipo}): {self.valor}"
    
class Memoria:
    def __init__(self):
        self.memoria = {}   # Inicializa um dicionário vazio para armazenar os valores de memória
    
    def load(self, endereco):
        return self.memoria.get(endereco, 0) # Recebe endereco, volta valor
    
    def store(self, endereco, valor):
        self.memoria[endereco] = valor # Recebe valor e armazena no endereco

    def __repr__(self):
        # String com todos os endereços e valores da memória
        return "\n".join([f"Address {addr}: {val}" for addr, val in self.memoria.items()])

class MIPSSimulator:
    def __init__(self):
        self.registradores = {f"$R{i}": Registradores(f"$R{i}", tipo_registradores.get(f"$r{i}")) for i in range(32)}
        self.memoria = Memoria()
        self.pc = 0 # Contador de Processos
        self.instrucoes = []    #Lista de instrucoes

    def load_programa(self, programa):
        self.instrucoes = programa
    
    def executar_instrucoes(self, instrucoes):
        # Organiza e verifca as instrucoes
        instrucoes = instrucoes.strip()
        if not instrucoes:
            return
        
        parts = instrucoes.split()  # Separa as instrucoes
        opcode = parts[0].upper()

        # Processar instrucoes
        if opcode == "ADD":
            rd, rs, rt = parts[1], parts[2], parts[3]
            self.registradores[rd].value = self.registradores[rs].value + self.registradores[rt].value
        elif opcode == "SUB":
            rd, rs, rt = parts[1], parts[2], parts[3]
            self.registradores[rd].value = self.registradores[rs].value - self.registradores[rt].value
        elif opcode == "MULT":
            rd, rs = parts[1], parts[2]
            self.registradores[rd].value = self.registradores[rs].value * self.registradores[rs].value
        elif opcode == "LW":
            rt, offset_base = parts[1], parts[2]
            offset, base = offset_base.split('(')
            base = base[:-1]
            endereco = self.registradores[base].valor + int(offset) # Calcula o endereço de memória: registrador base + deslocamento
            self.registradores[rt].valor = self.memoria.load(endereco)  # Carrega o valor da memória no endereço calculado
        elif opcode == 'SW':
            rt, offset_base = parts[1], parts[2]
            offset, base = offset_base.split('(')
            base = base[:-1]
            endereco = self.registradores[base].valor + int(offset)
        else:  
            raise ValueError(f"Instrução desconhecida: {opcode}")
        
    

    def run(self, passo_a_passo = False):
        for i, instrucao in enumerate(self.instrucoes):
            self.pc = i
            self.executar_instrucoes(instrucao)
            if passo_a_passo:
                input(f"Executou: {instrucao}. Pressione Enter para continuar")

class InterfaceGrafica:

    def __init__(self, root):
        self.root = root
        self.simulador = MIPSSimulator()
        self.programa = []
        self.create_widgets()

    def create_widgets(self):
        self.text_area = tk.Text(self.root, height = 10, width = 50)
        self.text_area.pack()

        self.load_button = tk.Button(self.root, text = "Carregar Programa", command=self.carregar_arquivo)
        self.load_button.pack()

        self.run_button = tk.Button(self.root, text= "Run", command=self.run_program)
        self.run_button.pack()

        self.step_button = tk.Button(self.root, text= "Passo a passo", command=self.run_passo_a_passo)
        self.step_button.pack()

        self.registradores_painel = tk.Label(self.root, text="Registradores:")
        self.registradores_painel.pack

        self.registradores_saida = tk.Text(self.root, height=10, width=50, state="disabled")
        self.registradores_saida.pack()

        self.memoria_label = tk.Label(self.root, text="Memória:")
        self.memoria_label.pack()

        self.memoria_output = tk.Text(self.root, height=10, width=50, state="disabled")
        self.memoria_output.pack()

    def carregar_arquivo(self):
        rota_arquivo = filedialog.askopenfilename(filetypes=[("All Files", "*.*")])
        if rota_arquivo:
            with open(rota_arquivo, 'r') as file:
                programa = file.read()
            self.text_area.delete(1.0, tk.END)
            self.text_area.insert(tk.END, programa)
            messagebox.showinfo("Sucesso!", "Programa Carregado com Sucesso!")

    def update_saida(self):
        # Destrava
        self.registradores_saida.config(state="normal")
        self.memoria_output.config(state="normal")

        # Apaga
        self.registradores_saida.delete(1.0, tk.END)
        self.memoria_output.delete(1.0, tk.END)

        # Carrega do simulador
        regs = "\n".join([str(reg) for reg in self.simulator.registradores.valor()])
        mems = str(self.simulator.memoria)

        # Carrega pra printar
        self.registradores_saida.insert(tk.END, regs)
        self.memoria_output.insert(tk.END, mems)

        # Trava
        self.registradores_saida.config(state="disabled")
        self.memoria_output.config(state="disabled")

    def run_program(self):
        programa = self.text_area.get(1.0, tk.END).strip().split("\n")
        self.simulador.load_programa(programa)
        self.simulador.run()
        self.update_saida()

    def run_passo_a_passo(self):
        programa = self.text_area.get(1.0, tk.END).strip().split("\n")
        self.simulador.load_programa(programa)
        self.simulador.run(passo_a_passo= True)
        self.update_saida()


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Simulador MIPS")
    app = InterfaceGrafica(root)
    root.mainloop()     