import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog

class Registradores:
    def __init__(self, nome):
        self.nome = nome
        self.valor = 0

    def set_value(self, value):
        self.valor = value
    
    def get_value(self):
        return self.valor

    def __repr__(self):
        return f"{self.nome}: {self.valor}"
    
class Memoria:
    def __init__(self):
        self.memoria = {}  # Inicializa um dicionário vazio para armazenar os valores de memória
    
    def load(self, endereco):
        endereco = int(endereco, 16) if isinstance(endereco, str) and endereco.startswith("0x") else int(endereco)
        return self.memoria.get(endereco, 0)  # Retorna o valor armazenado no endereço ou 0 se não existir
    
    def store(self, endereco, valor):
        endereco = int(endereco, 16) if isinstance(endereco, str) and endereco.startswith("0x") else int(endereco)
        valor = int(valor, 16) if isinstance(valor, str) and valor.startswith("0x") else int(valor)
        self.memoria[endereco] = valor  # Armazena o valor no endereço correspondente

    def __repr__(self):
        # String com todos os endereços e valores da memória (em hexadecimal)
        return "\n".join([f"Address 0x{addr:08X}: 0x{val:X}" for addr, val in self.memoria.items()])


class MIPSSimulator:
    def __init__(self):
        registrador_nomes = [
            "r0", "at", "v0", "v1", "a0", "a1", "a2", "a3",
            "t0", "t1", "t2", "t3", "t4", "t5", "t6", "t7",
            "s0", "s1", "s2", "s3", "s4", "s5", "s6", "s7",
            "t8", "t9", "k0", "k1", "gp", "sp", "fp", "ra", "zero"
        ]
        self.registradores = {f"${nome}": Registradores(f"${nome}") for nome in registrador_nomes}
        self.registradores["$zero"].set_value(0)
        self.memoria = Memoria()
        self.pc = 0  # Contador de programa (Program Counter)
        self.instrucoes = []

    def load_programa(self, programa):
        self.instrucoes = programa

    @staticmethod
    def parse_number(value):
        if value.startswith("0x") or value.startswith("0X"):
            return int(value, 16)  # Hexadecimal
        return int(value)

    def inverter_bytes(self, numero):
        # Converte o número para hexadecimal e depois inverte a string dos dígitos
        hex_val = hex(numero)[2:]  # Converte para hex e remove o '0x'
        hex_val = hex_val.zfill(8)  # Garante que tenha 8 caracteres
        return int(hex_val[::-1], 16)  # Inverte a string e converte de volta para inteiro

    def executar_instrucoes(self, instrucao):
        instrucao = instrucao.strip()
        if not instrucao or instrucao.startswith("#"):
            return

        parts = instrucao.split()
        opcode = parts[0].upper()

        # Processamento de instruções MIPS
        if opcode == "ADD":
            rd, rs, rt = parts[1].strip(','), parts[2].strip(','), parts[3].strip(',')
            self.registradores[rd].valor = self.registradores[rs].valor + self.registradores[rt].valor
        elif opcode == "SUB":
            rd, rs, rt = parts[1].strip(','), parts[2].strip(','), parts[3].strip(',')
            self.registradores[rd].valor = self.registradores[rs].valor - self.registradores[rt].valor
        elif opcode == "MULT":
            rd, rs = parts[1].strip(','), parts[2].strip(',')
            self.registradores[rd].valor = self.registradores[rs].valor * self.registradores[rs].valor
        elif opcode == "AND":
            rd, rs, rt = parts[1].strip(','), parts[2].strip(','), parts[3].strip(',')
            self.registradores[rd].valor = self.registradores[rs].valor & self.registradores[rt].valor
        elif opcode == "OR":
            rd, rs, rt = parts[1].strip(','), parts[2].strip(','), parts[3].strip(',')
            self.registradores[rd].valor = self.registradores[rs].valor | self.registradores[rt].valor
        elif opcode == "SLL":
            rd, rt, shamt = parts[1].strip(','), parts[2].strip(','), int(parts[3])
            self.registradores[rd].valor = self.registradores[rt].valor << shamt
        elif opcode == "ADDI":
            rt, rs, imm = parts[1].strip(','), parts[2].strip(','), self.parse_number(parts[3])
            self.registradores[rt].valor = self.registradores[rs].valor + imm
        elif opcode == "LUI":
            rt, imm = parts[1].strip(','), self.parse_number(parts[2])
            # Chama o método inverter_bytes ao calcular o valor do registrador
            self.registradores[rt].valor = self.inverter_bytes(imm << 16)  # Desloca e inverte
        elif opcode == "SLT":
            rd, rs, rt = parts[1].strip(','), parts[2].strip(','), parts[3].strip(',')
            self.registradores[rd].valor = 1 if self.registradores[rs].valor < self.registradores[rt].valor else 0
        elif opcode == "SLTI":
            rt, rs, imm = parts[1].strip(','), parts[2].strip(','), self.parse_number(parts[3])
            self.registradores[rt].valor = 1 if self.registradores[rs].valor < imm else 0
        elif opcode == "SW":
            rt, offset_base = parts[1].strip(','), parts[2].strip(',')
            offset, base = offset_base.split('(')
            base = base.strip(')')
            endereco = self.registradores[base].valor + int(offset)
            self.memoria.store(endereco, self.registradores[rt].valor)
        elif opcode == "LW":
            rt, offset_base = parts[1].strip(','), parts[2].strip(',')
            offset, base = offset_base.split('(')
            base = base.strip(')')
            endereco = self.registradores[base].valor + int(offset)
            # Chama inverter_bytes ao carregar o valor da memória
            self.registradores[rt].valor = self.inverter_bytes(self.memoria.load(endereco))
        elif opcode == "IMPRIMIR":
            tipo_impressao = parts[1].strip(',')
            
            if tipo_impressao.upper() == "INTEIRO":
                reg = parts[2].strip(',')
                print(self.registradores[reg].valor)
            elif tipo_impressao.upper() == "STRING":
                endereco = self.parse_number(parts[2])
                string = ""
                while (char := self.memoria.load(endereco)) != 0:
                    string += chr(char)
                    endereco += 1
                print(string)
        elif opcode == "SAIR":
            self.registradores["$v0"].valor = 10
        else:
            raise ValueError(f"Instrução desconhecida: {opcode}")

    def run(self, passo_a_passo=False):
        while self.pc < len(self.instrucoes):
            instrucao = self.instrucoes[self.pc].strip()

            if not instrucao or instrucao.startswith("#"):
                self.pc += 1
                continue

            self.executar_instrucoes(instrucao)
            self.pc += 1

            if passo_a_passo:
                input(f"Executou: {instrucao}. Pressione Enter para continuar.")


class InterfaceGrafica:

    def __init__(self, root):
        self.root = root
        self.simulador = MIPSSimulator()
        self.programa = []
        self.create_widgets()

    def create_widgets(self):
        self.text_area = tk.Text(self.root, height=10, width=50)
        self.text_area.pack()

        self.load_button = tk.Button(self.root, text="Carregar Programa", command=self.carregar_arquivo)
        self.load_button.pack()

        self.run_button = tk.Button(self.root, text="Run", command=self.run_program)
        self.run_button.pack()

        self.step_button = tk.Button(self.root, text="Passo a passo", command=self.run_passo_a_passo)
        self.step_button.pack()

        self.registradores_painel = tk.Label(self.root, text="Registradores:")
        self.registradores_painel.pack()

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
        regs = "\n".join([f"{nome}: {reg.valor}" for nome, reg in self.simulador.registradores.items()])
        mems = str(self.simulador.memoria)

        # Carrega pra printar (convertendo valores dos registradores para decimal)
        registradores_decimal = "\n".join([f"{nome}: {reg.get_value()}" for nome, reg in self.simulador.registradores.items()])
        
        self.registradores_saida.insert(tk.END, registradores_decimal)
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
        self.simulador.run(passo_a_passo=True)
        self.update_saida()


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Simulador MIPS")
    app = InterfaceGrafica(root)
    root.mainloop()
