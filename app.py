RED = "\033[1;31m"
BLUE = "\033[1;34m"
GREEN = "\033[0;32m"

print(f" {BLUE}BANCO DEVSOLUTIONS \033[m".center(70, "~"))
menu = """
(d) Deposito
(s) Saque
(e) Extrato
(q) Sair

Escolha a opção: """

saldo = 0
limit_saque = 3
valor_limite_saque = 500
count_saque = 0
extrato = ""

while True:
    opçao = input(menu).lower()

    if opçao == "d":  # DEPÓSITO
        valor = float(input("Digite o valor: "))

        if valor <= 0:
            print(f"{RED}Valor inválido!\033[m")
        else:
            print(f"{GREEN}Depósito de R${valor:.2f} feito com sucesso!\033[m")
            extrato += f"{GREEN}+ R${valor:.2f}\033[m\n"
            saldo += valor

    elif opçao == "s":  # SAQUE
        if count_saque == 3:
            print(f"{RED}Limite de saque excedido!\033[m")
        else:
            valor = float(input("Valor do saque: "))
            if valor > saldo:
                print(f"{RED}Saldo insuficiente!\033[m")
            elif valor == 0:
                print(f"{RED}Valor inválido!\033[m")
            elif valor > valor_limite_saque:
                print(f"{RED}Valor acima do limite!\033[m")
            else:
                saldo -= valor
                print(
                    f"{GREEN}Saque de R${valor:.2f} feito com sucesso!\033[m")
                extrato += f"{RED}- R${valor:.2f}\033[m\n"
                count_saque += 1

    elif opçao == "e":  # EXTRATO
        print(f"Extrato:  \n{extrato} \nSaldo: R${saldo:.2f}")

    elif opçao == "q":  # SAIR
        break

    else:
        print(f"{RED}Operação inválida!\033[m")

print("Fim das operações!")
