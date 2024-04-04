RED = "\033[1;31m"
BLUE = "\033[1;34m"
GREEN = "\033[0;32m"


saldo = 0
limite_de_saques = 3
valor_limite = 500
count_saque = 0
extrato = ""


def depositar(saldo, valor, extrato, /):
    if valor <= 0:
        print(f"{RED}Valor inválido!\033[m")
    else:
        print(f"{GREEN}Depósito de R${valor:.2f} feito com sucesso!\033[m")
        extrato += f"{GREEN}+ R${valor:.2f}\033[m\n"
        saldo += valor

    return saldo, extrato


def sacar(*, saldo, extrato, valor_limite, limite_de_saques):
    global count_saque
    if count_saque == limite_de_saques:
        print(f"{RED}Limite de saque excedido!\033[m")
    else:
        valor = float(input("Valor do saque: "))
        if valor > saldo:
            print(f"{RED}Saldo insuficiente!\033[m")
        elif valor == 0:
            print(f"{RED}Valor inválido!\033[m")
        elif valor > valor_limite:
            print(f"{RED}Valor acima do limite!\033[m")
        else:
            saldo -= valor
            print(f"{GREEN}Saque de R${valor:.2f} feito com sucesso!\033[m")
            extrato += f"{RED}- R${valor:.2f}\033[m\n"
            count_saque += 1

    return saldo, extrato


def exibir_extrato(saldo, /, *, extrato):
    print(f"Extrato:  \n{extrato} \nSaldo: R${saldo:.2f}")


print(f" {BLUE}BANCO DEVSOLUTIONS \033[m".center(50))
menu = """
**************** MENU *******************
(d) Deposito
(s) Saque
(e) Extrato
(q) Sair

Escolha a opção: """

while True:
    opçao = input(menu).lower()

    if opçao == "d":  # DEPÓSITO
        valor = float(input("Digite o valor: "))
        saldo, extrato = depositar(saldo, valor, extrato)

    elif opçao == "s":  # SAQUE
        saldo, extrato = sacar(
            saldo=saldo,
            extrato=extrato,
            limite_de_saques=limite_de_saques,
            valor_limite=valor_limite,
        )

    elif opçao == "e":  # EXTRATO
        exibir_extrato(saldo, extrato=extrato)

    elif opçao == "q":  # SAIR
        break

    else:
        print(f"{RED}Operação inválida!\033[m")

print("Fim das operações!")
