RED = "\033[1;31m"
BLUE = "\033[1;34m"
GREEN = "\033[0;32m"
NUM_AGENCIA = "0001"

usuarios = []
contas_correntes = []
saldo = 0
limite_de_saques = 3
valor_limite = 500
count_saque = 0
extrato = ""


def criar_usuario(
    cpf, nome, data_nascimento, logradouro,
    numero, bairro, cidade, estado, usuarios
):
    endereço = f"{logradouro}, {numero} - {bairro} - {cidade}/{estado.upper()}"
    usuarios.append(
        {
            "cpf": cpf,
            "nome": nome,
            "data_nascimento": data_nascimento,
            "endereço": endereço,
            "contas": []
        }
    )
    print(f"{GREEN}Usuário cadastrado com sucesso!\033[m")
    return usuarios


def criar_conta_corrente(contas_correntes, usuarios, cpf):
    num_da_conta = len(contas_correntes) + 1
    cpf_existe = [user for user in usuarios if user["cpf"] == cpf]

    if cpf_existe:
        contas_correntes.append({
            "numero": num_da_conta,
            "agencia": NUM_AGENCIA,
            "cpf": cpf
        })

        [user["contas"].append(num_da_conta)
            for user in usuarios if user["cpf"] == cpf]

        print(f"{GREEN}Conta corrente criada com sucesso!\033[m")
    else:
        print(f"{RED}Usuário não existe!\033[m")


def depositar(saldo, extrato, /):
    valor = float(input("Valor do depósito: "))
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
    print(" EXTRATO ".center(40, "="))
    print(f"{extrato} \n{BLUE}Saldo: R${saldo:.2f}\033[m")


print(f" {BLUE}BANCO DEVSOLUTIONS \033[m".center(50))
menu = """
**************** MENU *******************
(u) Cadastrar Usuário
(c) Criar conta corrente
(d) Deposito
(s) Saque
(e) Extrato
(q) Sair

Escolha a opção: """

while True:
    opçao = input(menu).lower()

    if opçao == "d":  # DEPÓSITO
        saldo, extrato = depositar(saldo, extrato)

    elif opçao == "s":  # SAQUE
        saldo, extrato = sacar(
            saldo=saldo,
            extrato=extrato,
            limite_de_saques=limite_de_saques,
            valor_limite=valor_limite,
        )

    elif opçao == "e":  # EXTRATO
        exibir_extrato(saldo, extrato=extrato)

    elif opçao == "u":  # CRIAR USUÁRIO
        print(" CADASTRO DE USUÁRIO ".center(40, "#"))
        cpf = input("CPF apenas números: ")
        cpf_existe = [user for user in usuarios if user["cpf"] == cpf]

        if not cpf_existe:
            nome = input("Nome: ")
            data_nascimento = input("Data de nascimento DD/MM/AAAA: ")
            logradouro = input("Logradouro: ")
            numero = input("N°: ")
            bairro = input("Bairro: ")
            cidade = input("Cidade: ")
            estado = input("Estado sigla: ")
            usuarios = criar_usuario(
                cpf,
                nome,
                data_nascimento,
                logradouro,
                numero,
                bairro,
                cidade,
                estado,
                usuarios,
            )
        else:
            print(f"{RED}CPF já existe!\033[m")

    elif opçao == 'c':  # CRIAR CONTA CORRENTE
        cpf = input("CPF apenas números: ")
        criar_conta_corrente(contas_correntes, usuarios, cpf)

    elif opçao == "q":  # SAIR
        break

    else:
        print(f"{RED}Operação inválida!\033[m")

print("Fim das operações!")
