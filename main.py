from datetime import datetime
import json

# --- Constantes ---
DATA_FILE = 'data_contas.json'
AGENCIA = "0001"
LIMITE_PADRAO = 500.00

# ==============================================================================
# 1. CLASSES DE ENTIDADES (MODELOS)
# ==============================================================================

class Transacao:
    def __init__(self, tipo: str, valor: float, data: str = None):
        self.tipo = tipo
        self.valor = valor
        self.data = data if data else datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    @classmethod
    def from_dict(cls, dados: dict):
        return cls(tipo=dados['tipo'], valor=dados['valor'], data=dados['data'])

    def to_dict(self):
        return {"tipo": self.tipo, "valor": self.valor, "data": self.data}

    def __str__(self):
        return f"{self.data} | {self.tipo.capitalize()}: R$ {self.valor:.2f}"

class Conta:
    def __init__(self, numero_conta: str, saldo: float = 0.00, limite: float = LIMITE_PADRAO, extrato: list = None):
        self.agencia = AGENCIA
        self.numero_conta = numero_conta
        self.saldo = saldo
        self.limite = limite
        self._extrato = extrato if extrato is not None else []

    @property
    def saldo_total(self):
        """Propriedade: Saldo real disponível (Saldo + Limite)."""
        return self.saldo + self.limite

    @property
    def historico(self):
        """Propriedade: Retorna lista de objetos Transacao reconstruídos."""
        return [Transacao.from_dict(t) for t in self._extrato]

    @classmethod
    def from_dict(cls, dados: dict):
        return cls(
            numero_conta=dados['numero_conta'],
            saldo=dados.get('saldo', 0.0),
            limite=dados.get('limite', LIMITE_PADRAO),
            extrato=dados.get('extrato', [])
        )

    def depositar(self, valor: float) -> bool:
        if valor <= 0:
            print("\n****** Erro: O valor deve ser positivo. ******")
            return False
        self.saldo += valor
        self._registrar_transacao("deposito", valor)
        return True

    def sacar(self, valor: float) -> bool:
        if valor <= 0: return False
        if self.saldo_total < valor:
             print("\n ****** Erro: Saldo insuficiente. ******")
             return False
        self.saldo -= valor
        self._registrar_transacao("saque", valor)
        return True

    def _registrar_transacao(self, tipo: str, valor: float):
        self._extrato.append(Transacao(tipo, valor).to_dict())

    def to_dict(self):
        return {
            "agencia": self.agencia,
            "numero_conta": self.numero_conta,
            "saldo": self.saldo,
            "limite": self.limite,
            "extrato": self._extrato
        }

class Cliente:
    def __init__(self, cpf: str, nome: str, endereco: str, contas: list = None):
        self.cpf = cpf
        self.nome = nome
        self.endereco = endereco
        self.contas = contas if contas is not None else []

    @property
    def cpf_formatado(self):
        c = self.cpf
        return f"{c[:3]}.{c[3:6]}.{c[6:9]}-{c[9:]}" if len(c) == 11 else c

    @classmethod
    def from_dict(cls, cpf: str, dados: dict):
        contas_obj = [Conta.from_dict(c) for c in dados.get('contas', [])]
        return cls(cpf=cpf, nome=dados['nome'], endereco=dados['endereco'], contas=contas_obj)

    def buscar_conta(self, numero: str):
        for conta in self.contas:
            if conta.numero_conta == numero:
                return conta
        return None

    def to_dict(self):
        return {
            "nome": self.nome,
            "endereco": self.endereco,
            "contas": [c.to_dict() for c in self.contas]
        }

# ==============================================================================
# 2. CLASSE DE SERVIÇO (SISTEMA)
# ==============================================================================

class SistemaBancario:
    def __init__(self, data_file: str):
        self.data_file = data_file
        self.clientes = self._carregar_dados()

    def _carregar_dados(self):
        try:
            with open(self.data_file, 'r') as f:
                dados_json = json.load(f)
                return {cpf: Cliente.from_dict(cpf, info) for cpf, info in dados_json.items()}
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    def salvar_dados(self):
        with open(self.data_file, 'w') as f:
            json.dump({cpf: cli.to_dict() for cpf, cli in self.clientes.items()}, f, indent=4)

    def criar_usuario(self, cpf, nome, endereco, limite):
        if cpf in self.clientes:
            print("\n****** Erro: CPF já cadastrado. ******")
            return
        nova_c = Conta(self._gerar_numero(), limite=limite)
        self.clientes[cpf] = Cliente(cpf, nome, endereco, contas=[nova_c])
        self.salvar_dados()
        print(f"\n=== Cliente {nome} cadastrado! Conta: {nova_c.numero_conta} ===")

    def criar_nova_conta(self, cpf, limite):
        """Adiciona uma nova conta a um cliente já existente."""
        cliente = self.clientes.get(cpf)
        if not cliente:
            print("\n****** Erro: Cliente não encontrado. Cadastre o usuário primeiro (nu). ******")
            return
        
        nova_c = Conta(self._gerar_numero(), limite=limite)
        cliente.contas.append(nova_c)
        self.salvar_dados()
        print(f"\n=== Nova conta {nova_c.numero_conta} adicionada para {cliente.nome}! ===")

    def _gerar_numero(self):
        maior = 100000
        for cli in self.clientes.values():
            for conta in cli.contas:
                maior = max(maior, int(conta.numero_conta))
        return str(maior + 1)

    def listar_contas(self):
        print(f"\n{'CONTA':<10} {'TITULAR':<20} {'CPF':<15} {'DISPONÍVEL':>15}")
        print("-" * 65)
        for cli in self.clientes.values():
            for c in cli.contas:
                print(f"{c.numero_conta:<10} {cli.nome[:20]:<20} {cli.cpf_formatado:<15} R$ {c.saldo_total:>12.2f}")

# ==============================================================================
# 3. INTERFACE E EXECUÇÃO
# ==============================================================================

def main():
    sistema = SistemaBancario(DATA_FILE)
    
    while True:
        print("""\n
    ================ MENU ================
    [d]  Depositar
    [s]  Sacar
    [e]  Extrato
    [nc] Nova conta
    [lc] Listar contas
    [nu] Novo usuário
    [q]  Sair
    ======================================
    
    Informe a sigla da operação desejada
    """)
        op = input("=> ").lower()

        if op == "q": break
        
        if op == "nu":
            cpf = input("CPF: ")
            nome = input("Nome: ")
            end = input("Endereço: ")
            limite = float(input("Limite inicial: "))
            sistema.criar_usuario(cpf, nome, end, limite)

        elif op == "nc":
            cpf = input("Informe o CPF do cliente: ")
            limite = float(input("Limite da nova conta: "))
            sistema.criar_nova_conta(cpf, limite)

        elif op in ["d", "s", "e"]:
            cpf = input("CPF: ")
            num = input("Nro Conta: ")
            cli = sistema.clientes.get(cpf)
            if not cli: 
                print("Cliente não encontrado.")
                continue
            
            conta = cli.buscar_conta(num)
            if not conta:
                print("Conta não encontrada.")
                continue

            if op == "d":
                valor = float(input("Valor Depósito: "))
                if conta.depositar(valor): sistema.salvar_dados()
            elif op == "s":
                valor = float(input("Valor Saque: "))
                if conta.sacar(valor): sistema.salvar_dados()
            elif op == "e":
                print(f"\n--- Extrato Conta {conta.numero_conta} ---")
                for t in conta.historico: print(t)
                print(f"Saldo: R$ {conta.saldo:.2f} | Disponível: R$ {conta.saldo_total:.2f}")

        elif op == "lc":
            sistema.listar_contas()

if __name__ == "__main__":
    main()