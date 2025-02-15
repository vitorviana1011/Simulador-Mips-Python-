    .data
msg1: .asciiz "Vetor armazenado: "  # String para ser impressa
vetor: .word 10, 20, 30, 40, 50     # Vetor com 5 números
newline: .asciiz "\n"               # Nova linha após cada número

    .text
    # Inicia a execução
    IMPRIMIR STRING msg1            # Imprime a string "Vetor armazenado: "
    
    # Carrega e imprime os elementos do vetor
    LW $t0, 0(vetor)     # Carrega o primeiro valor do vetor em $t0
    IMPRIMIR INTEIRO $t0  # Imprime o valor de $t0
    
    LW $t0, 4(vetor)     # Carrega o segundo valor do vetor em $t0
    IMPRIMIR INTEIRO $t0  # Imprime o valor de $t0
    
    LW $t0, 8(vetor)     # Carrega o terceiro valor do vetor em $t0
    IMPRIMIR INTEIRO $t0  # Imprime o valor de $t0
    
    LW $t0, 12(vetor)    # Carrega o quarto valor do vetor em $t0
    IMPRIMIR INTEIRO $t0  # Imprime o valor de $t0
    
    LW $t0, 16(vetor)    # Carrega o quinto valor do vetor em $t0
    IMPRIMIR INTEIRO $t0  # Imprime o valor de $t0

