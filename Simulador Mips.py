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
        return f"{self.name} ({self.reg_type}): {self.value}"
    
class Memoria:
    def __init__(self):
        self.memoria = {}   # Inicializa um dicionário vazio para armazenar os valores de memória
    
    def load(self, endereco):
        return self.memoria.get(endereco, 0) # Recebe endereco, volta valor
    
    def store(self, endereco, valor):
        self.memoria[endereco] = valor # Recebe valor e armazena no endereco

    def __repr__(self):
        # String com todos os endereços e valores da memória
        return "\n".join([f"Address {addr}: {val}" for addr, val in self.memory.items()])

class MIPSSimulator:
    def __init__(self):
        self.registers = {f"$R{i}": Registradores(f"$R{i}", tipo_registradores.get(f"$r{i}")) for i in range(32)}
        self.memoria = Memoria()
        self.pc = 0 # Contador de Processos
        self.instrucoes = []    #Lista de instrucoes

    def load_programa(self, programa):
        self.instrucoes = programa
    
    def executar_instrucoes(self, instrucoes):
        #depois eu faco, to com preguica agora
        print("a")
    
    def run(self, passo_a_passo = False):
        for i, instrucao in enumerate(self.instrucoes):
            self.pc = i
            self.executar_instrucoes(instrucao)
            if passo_a_passo:
                input(f"Executou: {instrucao}. Pressione Enter para continuar")

class InterfaceGrafica:
    #Usar a biblioteca tkinter

    #vai precisar de algumns metodos pra ler o arquivo

    def __init__(self):
        pass


def main():
    # Inicializando o simulador MIPS
    simulator = MIPSSimulator()
    
# Chama a função main para testar
if __name__ == "__main__":
    main()        
