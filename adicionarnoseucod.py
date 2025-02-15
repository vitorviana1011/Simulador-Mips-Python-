class InterfaceGrafica:
    def __init__(self, master):
        self.master = master
        self.master.title("Simulador MIPS")
        self.master.geometry("800x600")
        self.simulador = MIPSSimulator()

        # Caixa de entrada de código
        self.text_input = tk.Text(self.master, height=6, font=("Arial", 12))
        self.text_input.pack(pady=10, padx=20, fill="x")

        # Botão de execução
        self.execute_button = tk.Button(self.master, text="Executar", font=("Arial", 12), command=self.executar)
        self.execute_button.pack(pady=10)

        # Área de saída
        self.text_output = tk.Text(self.master, height=10, font=("Arial", 12))
        self.text_output.pack(pady=10, padx=20, fill="x")

        # Mostrar os registradores
        self.text_registers = tk.Text(self.master, height=8, font=("Arial", 12))
        self.text_registers.pack(pady=10, padx=20, fill="x")

    def atualizar_registradores(self):
        resultado_registradores = "\n".join([f"{reg}: {reg_info.valor}" for reg, reg_info in self.simulador.registradores.items()])
        self.text_registers.delete(1.0, tk.END)
        self.text_registers.insert(tk.END, resultado_registradores)

    def executar(self):
        codigo = self.text_input.get("1.0", tk.END).strip().splitlines()
        if not codigo:
            messagebox.showerror("Erro", "Por favor, insira o código!")
            return

        resultado = self.simulador.executar_programa(codigo)
        resultado_texto = "\n".join(resultado)

        self.text_output.delete(1.0, tk.END)
        self.text_output.insert(tk.END, resultado_texto)
        self.atualizar_registradores()
