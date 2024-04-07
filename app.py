from abc import ABC, abstractmethod
from datetime import date

RED = "\033[1;31m"
BLUE = "\033[1;34m"
GREEN = "\033[0;32m"


class Cliente:
    def __init__(self, endereço, contas=[]) -> None:
        self._endereço = endereço
        self._contas = contas

    @property
    def endereço(self):
        return self._endereço

    @property
    def contas(self):
        return self._contas

    def adicionar_conta(conta):
        pass


class PessoaFisica(Cliente):
    def __init__(
            self, endereço, cpf, nome, data_nascimento, contas=[]) -> None:
        super().__init__(endereço, contas)
        self._cpf = cpf
        self._nome = nome
        self._data_nascimento = data_nascimento

    @property
    def cpf(self):
        return self._cpf

    @property
    def nome(self):
        return self._nome

    @property
    def data_nascimento(self):
        return self._data_nascimento


class Conta:
    def __init__(
            self, numero, cliente, agencia, historico=[], saldo=0) -> None:
        self._saldo = saldo
        self._numero = numero
        self._cliente = cliente
        self._agencia = agencia
        self._historico = historico

    @property
    def saldo(self):
        return self._saldo

    @property
    def numero(self):
        return self._numero

    @property
    def historico(self):
        return self._historico

    def depositar(self, valor):
        if valor <= 0:
            print(f"\n{RED}Valor inválido!\033[m")
        else:
            self._saldo += valor
            print(
                f"\n{GREEN}Depósito de R${valor:.2f} feito com sucesso!\033[m")

    def __str__(self) -> str:
        if not self._historico:
            return "\nHistórico de operações vazio!"
        result = ""
        for valor in self._historico:
            result += f"{valor['tipo']} - {valor['valor']} - {valor['data']}\n"
        return result


class ContaCorrente(Conta):
    def __init__(
            self, numero, cliente, agencia, historico=[], saldo=0) -> None:
        super().__init__(numero, cliente, agencia, historico, saldo)
        self._limite = 500
        self._limite_saques = 3
        self._agencia = agencia

    @property
    def limite_saques(self):
        return self._limite_saques

    def sacar(self, valor):
        if valor > self._limite:
            print(f"\n{RED}Valor acima do limite!\033[m")
        elif valor > self._saldo:
            print(f"\n{RED}Saldo insuficiente!\033[m")
        elif valor == 0:
            print(f"\n{RED}Valor inválido!\033[m")
        else:
            self._saldo -= valor
            print(f"\n{GREEN}Saque de R${valor:.2f} feito com sucesso!\033[m")


class Historico:
    def __init__(self) -> None:
        self._transaçoes = []

    @property
    def transaçoes(self):
        return self._transaçoes

    def adicionar_transaçao(self, transaçao):
        self._transaçoes.append(transaçao)


class Transaçao(ABC):
    @abstractmethod
    def registrar(self, conta):
        pass


class Deposito(Transaçao):
    def __init__(self, valor) -> None:
        self._valor = valor

    def registrar(self, conta):
        conta.historico.append(
            {
                "tipo": "depósito",
                "numero": conta.numero,
                "valor": self._valor,
                "data": date.today(),
            }
        )
        conta.depositar(self._valor)


class Saque(Transaçao):
    def __init__(self, valor) -> None:
        self._valor = valor

    def registrar(self, conta):
        conta.historico.append(
            {
                "tipo": "saque",
                "numero": conta.numero,
                "valor": self._valor,
                "data": date.today(),
            }
        )
        conta.sacar(self._valor)


def criar_usuario(usuarios):
    cpf = input("CPF (apenas números): ")
    cpf_existe = [user for user in usuarios if user.cpf == cpf]

    if not cpf_existe:
        nome = input("Nome: ")
        data_nascimento = input("Data de nascimento DD/MM/AAAA: ")
        logradouro = input("Logradouro: ")
        numero = input("N°: ")
        bairro = input("Bairro: ")
        cidade = input("Cidade: ")
        estado = input("Estado sigla: ").upper()
        endereço = f"""{logradouro}, {numero} -{bairro} - {cidade}/{estado}"""

        usuario = PessoaFisica(endereço, cpf, nome, data_nascimento)
        usuarios.append(usuario)
        print(f"\n{GREEN}Usuário cadastrado com sucesso!\033[m")
    else:
        print(f"\n{RED}Usuário já cadastrado!\033[m")


def criar_conta_corrente(contas, usuarios):
    numero = len(contas) + 1
    cpf = input("CPF apenas numeros: ")
    cliente_existe = [user for user in usuarios if user.cpf == cpf]

    if cliente_existe:
        cc = ContaCorrente(numero, cliente_existe[0], "0001")
        contas.append(cc)

        [user.contas.append(numero) for user in usuarios if user.cpf == cpf]
        print(f"\n{GREEN}Conta corrente criada com sucesso!\033[m")
    else:
        print(f"\n{RED}Usuário não existe!\033[m")


def depositar(contas):
    numero = int(input("Número da conta: "))
    conta_existe = [conta for conta in contas if conta.numero == numero]

    if not conta_existe:
        print(f"\n{RED}Conta não existe!\033[m")
    else:
        valor = float(input("Valor do depósito: "))
        deposito = Deposito(valor)
        deposito.registrar(conta_existe[0])


def sacar(contas):
    numero = int(input("Número da conta: "))
    conta_existe = [conta for conta in contas if conta.numero == numero]
    if not conta_existe:
        print(f"\n{RED}Conta não existe!\033[m")
    else:
        conta = conta_existe[0]
        limite_saques = len(
            [transaçao for transaçao in conta.historico
                if transaçao["tipo"] == "saque"])
        if conta.limite_saques == limite_saques:
            print(f"\n{RED}Limite de saque excedido!\033[m")
        else:
            valor = float(input("Valor do saque: "))
            saque = Saque(valor)
            saque.registrar(conta_existe[0])


def exibir_extrato(contas):
    numero = int(input("Número da conta: "))
    conta_existe = [conta for conta in contas if conta.numero == numero]
    if not conta_existe:
        print(f"\n{RED}Conta não existe!\033[m")
    else:
        print(conta_existe[0])


menu = """
**************** MENU *******************
(u) Cadastrar Usuário
(c) Criar conta corrente
(d) Deposito
(s) Saque
(e) Extrato
(q) Sair

Escolha a opção: """


def program():
    usuarios = []
    contas = []

    while True:
        opçao = input(menu).lower()

        if opçao == "u":
            print("\n" + "CADASTRO DE USUÁRIO".center(40, "_") + "\n")
            criar_usuario(usuarios)
        elif opçao == "c":
            print("\n" + "CRIAR CONTA CORRENTE".center(40, "_") + "\n")
            criar_conta_corrente(contas, usuarios)
        elif opçao == "d":
            print("\n" + "TRANSAÇÃO DE DEPOSITO".center(40, "_") + "\n")
            depositar(contas)
        elif opçao == "s":
            print("\n" + "TRANSAÇÃO DE SAQUE".center(40, "_") + "\n")
            sacar(contas)
        elif opçao == "e":
            print("\n" + "EXTRATO".center(40, "_") + "\n")
            exibir_extrato(contas)
        elif opçao == "q":
            break
        else:
            print(f"\n{RED}Operação inválida!\033[m")


program()
