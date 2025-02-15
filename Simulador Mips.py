import tkinter as tk
from tkinter import messagebox, filedialog
import sys

# Definindo a classe Registradores
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

# Definindo a classe Memoria
class Memoria:
    def __init__(self):
        self.memoria = {}  # Armazena o conteúdo da memória
        self.endereco_atual = 0x1000  # Endereço inicial para armazenar strings e inteiros

    def store(self, endereco, valor, tipo="inteiro"):
        if tipo == "inteiro":
            self.memoria[endereco] = valor  # Armazenar inteiro
        elif tipo == "string":
            # Armazenar string como bytes (caracteres codificados)
            for i, char in enumerate(valor):
                self.memoria[endereco + i] = ord(char)
            self.memoria[endereco + len(valor)] = 0  # Byte nulo no final da string

    def load(self, endereco, tipo="inteiro"):
        if tipo == "inteiro":
            return self.memoria.get(endereco, 0)  # Retorna o valor inteiro
        elif tipo == "string":
            string = ""
            while (char := self.memoria.get(endereco, 0)) != 0:  # Até o byte nulo
                string += chr(char)
                endereco += 1
            return string

    def get_endereco(self, nome_string):
        # Verifica se a string já está armazenada na memória
        if nome_string in self.memoria:
            return self.memoria[nome_string]['endereco']
        
        # Se a string ainda não estiver na memória, armazena ela
        endereco_string = self.endereco_atual
        self.memoria[nome_string] = {'endereco': endereco_string, 'string': nome_string}
        
        # Armazena os caracteres da string na memória
        self.store(endereco_string, nome_string, tipo="string")

        # Atualiza o próximo endereço disponível para a próxima string
        self.endereco_atual += len(nome_string) + 1
        
        return endereco_string

# Definindo a classe MIPSSimulator
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
        # Removido: self.pc = 0  (não usaremos um contador de programa)
        self.instrucoes = []
        self.tabela_simbolos = {}
        self.memoria_virtual = 0x10010000

    def load_programa(self, programa):
        self.instrucoes = []
        data_section = False
        text_section = False

        for linha in programa:
            linha = linha.strip()
            # Remove o comentário que pode estar em qualquer posição da linha.
            if '#' in linha:
                linha = linha.split('#', 1)[0].strip()
            if not linha:
                continue

            if linha.upper() == ".DATA":
                data_section = True
                text_section = False
                continue
            elif linha.upper() == ".TEXT":
                data_section = False
                text_section = True
                continue

            if data_section:
                self.processar_data(linha)
            elif text_section:
                self.instrucoes.append(linha)

    def processar_data(self, linha):
        if linha:
            linha = linha.strip()

            # Ignorar comentários
            if '#' in linha:
                linha = linha.split('#', 1)[0].strip()

            if ":" in linha:
                nome, valor = linha.split(":", 1)
                nome = nome.strip()
                valor = valor.strip()

                if ".word" in valor:
                    # Processa os inteiros (ou vetor)
                    valores = valor.replace(".word", "").strip().split(',')
                    for val in valores:
                        try:
                            val_int = int(val.strip())
                            endereco = self.memoria_virtual
                            self.memoria.store(endereco, val_int)
                            if nome not in self.tabela_simbolos:
                                self.tabela_simbolos[nome] = endereco
                            self.memoria_virtual += 4
                        except ValueError:
                            print(f"Valor inválido para .word: {val}")
                elif ".asciiz" in valor:
                    valor = valor.split('"')[1]  # Remove as aspas
                    endereco = self.memoria_virtual
                    # Armazena cada caractere como um byte
                    for i, char in enumerate(valor):
                        self.memoria.store(endereco + i, ord(char))
                    self.memoria.store(endereco + len(valor), 0)  # Byte nulo
                    self.tabela_simbolos[nome] = endereco
                    self.memoria_virtual += len(valor) + 1

    def parse_number(self, value):
        try:
            if value.startswith('0x') or value.startswith('0X'):
                return int(value, 16)
            return int(value)
        except ValueError:
            if value in self.tabela_simbolos:
                return self.tabela_simbolos[value]
            else:
                raise ValueError(f"Valor inválido ou símbolo não encontrado: {value}")

    def ALU(self, opcode, op1, op2=None, shamt=None):
        if opcode == "ADD":
            return op1 + op2
        elif opcode == "SUB":
            return op1 - op2
        elif opcode == "MULT":
            return op1 * op1
        elif opcode == "AND":
            return op1 & op2
        elif opcode == "OR":
            return op1 | op2
        elif opcode == "SLL":
            return op1 << shamt
        elif opcode == "ADDI":
            return op1 + op2
        elif opcode == "LUI":
            return op2 << 16
        elif opcode == "SLT":
            return 1 if op1 < op2 else 0
        elif opcode == "SLTI":
            return 1 if op1 < op2 else 0
        else:
            raise ValueError(f"Operação aritmética desconhecida: {opcode}")

    def executar_instrucoes(self, instrucao, interface=None):
        instrucao = instrucao.strip()
        if not instrucao or instrucao.startswith("#"):
            return

        parts = instrucao.split()
        opcode = parts[0].upper()

        # Operações aritméticas realizadas pela ALU
        if opcode in ["ADD", "SUB", "AND", "OR", "SLT"]:
            rd, rs, rt = parts[1].strip(','), parts[2].strip(','), parts[3].strip(',')
            op1 = self.registradores[rs].valor
            op2 = self.registradores[rt].valor
            result = self.ALU(opcode, op1, op2)
            self.registradores[rd].valor = result

        elif opcode == "MULT":
            rd, rs = parts[1].strip(','), parts[2].strip(',')
            op1 = self.registradores[rs].valor
            result = self.ALU(opcode, op1)
            self.registradores[rd].valor = result

        elif opcode == "SLL":
            rd, rt, shamt = parts[1].strip(','), parts[2].strip(','), int(parts[3])
            op1 = self.registradores[rt].valor
            result = self.ALU(opcode, op1, shamt=shamt)
            self.registradores[rd].valor = result

        elif opcode in ["ADDI", "SLTI"]:
            rt, rs, imm = parts[1].strip(','), parts[2].strip(','), self.parse_number(parts[3])
            op1 = self.registradores[rs].valor
            result = self.ALU(opcode, op1, op2=imm)
            self.registradores[rt].valor = result

        elif opcode == "LUI":
            rt, imm = parts[1].strip(','), self.parse_number(parts[2])
            result = self.ALU(opcode, None, op2=imm)
            self.registradores[rt].valor = result

        elif opcode == "LW":
            rt, offset_base = parts[1].strip(','), parts[2].strip(',')
            offset, base = offset_base.split('(')
            base = base.strip(')')
            if base in self.tabela_simbolos:
                endereco = self.tabela_simbolos[base] + int(offset)
            else:
                endereco = self.registradores[base].valor + int(offset)
            self.registradores[rt].valor = self.memoria.load(endereco)

        elif opcode == "SW":
            rt, offset_base = parts[1].strip(','), parts[2].strip(',')
            offset, base = offset_base.split('(')
            base = base.strip(')')
            endereco = self.registradores[base].valor + int(offset)
            self.memoria.store(endereco, self.registradores[rt].valor)

        elif opcode == "IMPRIMIR":
            tipo_impressao = parts[1].strip(',')
            if tipo_impressao.upper() == "INTEIRO":
                reg = parts[2].strip(',')
                valor = self.registradores[reg].valor
                print(valor)
            elif tipo_impressao.upper() == "STRING":
                endereco_str = parts[2].strip(',')
                if endereco_str in self.tabela_simbolos:
                    endereco = self.tabela_simbolos[endereco_str]
                else:
                    endereco = self.parse_number(endereco_str)
                string_endereco = self.memoria.load(endereco, tipo="string")
                print(string_endereco)

        elif opcode == "SAIR":
            self.registradores["$v0"].valor = 10
        else:
            raise ValueError(f"Instrução desconhecida: {opcode}")

        if interface:
            interface.update_saida()
            interface.root.update()


    def run(self, passo_a_passo=False, callback_update=None):
        for instrucao in self.instrucoes:
            instrucao = instrucao.strip()
            if not instrucao or instrucao.startswith("#"):
                continue
            self.executar_instrucoes(instrucao)
            if passo_a_passo:
                if callback_update:
                    callback_update()
                try:
                    input(f"Executou: {instrucao}. Pressione Enter para continuar.")
                except KeyboardInterrupt:
                    print("Execução interrompida pelo usuário.")
                    break



class ConsoleRedirect:
    def __init__(self, widget):
        self.widget = widget
        self.widget.config(state="disabled")

    def write(self, string):
        self.widget.config(state="normal")
        self.widget.insert(tk.END, string)
        self.widget.see(tk.END)  # Rolagem automática
        self.widget.config(state="disabled")

    def flush(self):
        pass

# Interface gráfica
class InterfaceGrafica:
    def __init__(self, root):
        self.root = root
        self.simulador = MIPSSimulator()
        self.programa = []
        self.passo_atual = 0  # Índice da instrução atual no modo passo a passo
        self.create_widgets()

    def create_widgets(self):
        self.text_area = tk.Text(self.root, height=10, width=50)
        self.text_area.pack()

        self.load_button = tk.Button(self.root, text="Carregar Programa", command=self.carregar_arquivo)
        self.load_button.pack()

        self.run_button = tk.Button(self.root, text="Run", command=self.run_program)
        self.run_button.pack()

        # Botão para execução passo a passo
        self.step_button = tk.Button(self.root, text="Próximo Passo", command=self.executar_proximo_passo)
        self.step_button.pack()

        # Label para exibir o passo atual de forma intuitiva
        self.step_info = tk.Label(self.root, text="Nenhum passo executado", fg="blue")
        self.step_info.pack()

        self.registradores_painel = tk.Label(self.root, text="Registradores:")
        self.registradores_painel.pack()

        self.registradores_saida = tk.Text(self.root, height=10, width=50, state="disabled")
        self.registradores_saida.pack()

        self.memoria_label = tk.Label(self.root, text="Memória:")
        self.memoria_label.pack()

        self.memoria_output = tk.Text(self.root, height=10, width=50, state="disabled")
        self.memoria_output.pack()

        self.console_label = tk.Label(self.root, text="Console:")
        self.console_label.pack()

        self.console_output = tk.Text(self.root, height=10, width=50, state="disabled", bg="black", fg="green")
        self.console_output.pack()

        sys.stdout = ConsoleRedirect(self.console_output)

        self.reset_button = tk.Button(self.root, text="Reset", command=self.reset)
        self.reset_button.pack()

    def carregar_arquivo(self):
        rota_arquivo = filedialog.askopenfilename(filetypes=[("All Files", "*.*")])
        if rota_arquivo:
            with open(rota_arquivo, 'r') as file:
                programa = file.read()
            self.text_area.delete(1.0, tk.END)
            self.text_area.insert(tk.END, programa)
            messagebox.showinfo("Sucesso!", "Programa Carregado com Sucesso!")

    def update_saida(self):
        self.registradores_saida.config(state="normal")
        self.memoria_output.config(state="normal")

        self.registradores_saida.delete(1.0, tk.END)
        self.memoria_output.delete(1.0, tk.END)

        regs = "\n".join([f"{nome}: {reg.valor}" for nome, reg in self.simulador.registradores.items()])
        self.registradores_saida.insert(tk.END, regs)

        memoria_str = ""
        simbolos = sorted(self.simulador.tabela_simbolos.items(), key=lambda item: item[1])
        mem = self.simulador.memoria.memoria

        for i, (nome_variavel, endereco_inicial) in enumerate(simbolos):
            memoria_str += f"{nome_variavel}:\n"

            if i < len(simbolos) - 1:
                region_end = simbolos[i+1][1]
            else:
                region_end = endereco_inicial + 100

            keys_na_regiao = [addr for addr in mem.keys() if endereco_inicial <= addr < region_end]
            keys_na_regiao.sort()

            for addr in keys_na_regiao:
                valor = mem[addr]
                memoria_str += f"    {hex(addr)}: {valor}\n"
            memoria_str += "\n"

        self.memoria_output.insert(tk.END, memoria_str)

        self.registradores_saida.config(state="disabled")
        self.memoria_output.config(state="disabled")

    def run_program(self):
        self.simulador.load_programa(self.text_area.get("1.0", tk.END).splitlines())
        self.simulador.run()
        self.update_saida()
        self.passo_atual = 0  # Reinicia o passo a passo
        self.step_info.config(text="Programa executado completamente.")

    def executar_proximo_passo(self):
        # Se o programa ainda não foi carregado, carrega-o
        if not self.simulador.instrucoes:
            self.simulador.load_programa(self.text_area.get("1.0", tk.END).splitlines())
            self.passo_atual = 0

        # Verifica se ainda há instruções a executar
        if self.passo_atual < len(self.simulador.instrucoes):
            instrucao = self.simulador.instrucoes[self.passo_atual]
            # Atualiza o label informando qual o passo atual e a instrução executada
            self.step_info.config(text=f"Passo {self.passo_atual + 1}: {instrucao}")
            self.simulador.executar_instrucoes(instrucao)
            self.update_saida()
            self.passo_atual += 1
        else:
            messagebox.showinfo("Fim", "Não há mais instruções para executar.")
            self.step_info.config(text="Fim do programa.")

    def reset(self):
        self.simulador = MIPSSimulator()
        self.text_area.delete(1.0, tk.END)
        self.console_output.config(state="normal")
        self.console_output.delete(1.0, tk.END)
        self.console_output.config(state="disabled")
        self.passo_atual = 0
        self.step_info.config(text="Nenhum passo executado")

root = tk.Tk()
root.title("Simulador MIPS")
interface = InterfaceGrafica(root)
root.mainloop()