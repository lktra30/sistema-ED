import sys

# Criamos a classe Paciente com os atributos nome, idade e prioridade
class Paciente:
    def __init__(self, nome, idade, prioridade):
        self.nome = nome
        self.idade = idade
        self.prioridade = prioridade
        self.proximo = None
        self.anterior = None

    # Calculamos o tamanho da memória ocupada pelo paciente
    def calcular_memoria(self):
        total = sys.getsizeof(self.nome) + sys.getsizeof(self.idade) + sys.getsizeof(self.prioridade)
        total += sys.getsizeof(self) + sys.getsizeof(self.proximo) + sys.getsizeof(self.anterior)
        return total

# Criamos a classe FilaAtendimento com os atributos inicio, fim, pacientes_prioritarios, pacientes_normais e alterna_normal
class FilaAtendimento:
    def __init__(self):
        # Inicializamos e apontamos os nós para o próximo e anterior
        self.inicio = None
        self.fim = None
        self.pacientes_prioritarios = 2
        self.pacientes_normais = 1
        self.alterna_normal = False

    # Calculamos o tamanho total da memória ocupada pela fila
    def memoria_total(self):
        total = 0
        atual = self.inicio
        while atual:
            total += atual.calcular_memoria()
            atual = atual.proximo
        return total

    # Monitoramos a memória antes e depois de cada operação
    def _monitorar_memoria(self, operacao, mem_antes):
        mem_depois = self.memoria_total()
        print(f"\n[{operacao}] Memória antes: {mem_antes} bytes | Depois: {mem_depois} bytes")
        print(f"[{operacao}] Diferença: {mem_depois - mem_antes} bytes")

    # Função adiciona um paciente à fila
    def adicionar_paciente(self, nome, idade, prioridade):
        mem_antes = self.memoria_total()

        # Criamos um novo paciente com os dados fornecidos, apontando para o próximo
        novo = Paciente(nome, idade, prioridade)
        if self.inicio is None:
            self.inicio = self.fim = novo
        elif prioridade == 2:
            atual = self.inicio
            while atual and atual.prioridade == 2:
                atual = atual.proximo
            if atual is None:
                self.fim.proximo = novo
                novo.anterior = self.fim
                self.fim = novo
            elif atual.anterior is None:
                novo.proximo = self.inicio
                self.inicio.anterior = novo
                self.inicio = novo
            else:
                anterior = atual.anterior
                anterior.proximo = novo
                novo.anterior = anterior
                novo.proximo = atual
                atual.anterior = novo
        else:
            self.fim.proximo = novo
            novo.anterior = self.fim
            self.fim = novo

        if prioridade == 2:
            self.pacientes_prioritarios += 1
        else:
            self.pacientes_normais += 1

        self._monitorar_memoria("ADICIONAR", mem_antes)

    # Remove um paciente da fila e refaz a fila de acordo com as regras
    def remover_paciente(self):
        if self.inicio is None:
            print("Fila vazia.")
            return
            
        mem_antes = self.memoria_total()

        atual = self.inicio

        # Verificamos se há pacientes prioritários e normais suficientes para alternar
        if self.pacientes_prioritarios >= 1 and self.pacientes_normais >= 7:
            if self.alterna_normal:
                while atual and atual.prioridade != 1:
                    atual = atual.proximo
                self.alterna_normal = False
            else:
                while atual and atual.prioridade != 2:
                    atual = atual.proximo
                self.alterna_normal = True
        else:
            atual = self.inicio

        if atual is None:
            print("Nenhum paciente atende aos critérios.")
            return

        print(f"Removendo: {atual.nome} (Prioridade: {atual.prioridade})")

        if atual == self.inicio:
            self.inicio = atual.proximo
            if self.inicio:
                self.inicio.anterior = None
        elif atual == self.fim:
            self.fim = atual.anterior
            if self.fim:
                self.fim.proximo = None
        else:
            anterior = atual.anterior
            proximo = atual.proximo
            anterior.proximo = proximo
            proximo.anterior = anterior

        if atual.prioridade == 2:
            self.pacientes_prioritarios -= 1
        else:
            self.pacientes_normais -= 1

        if self.inicio:
            print(f"Próximo paciente: {self.inicio.nome}")
        else:
            print("Fila agora está vazia.")

        self._monitorar_memoria("REMOVER", mem_antes)

    # Função para alterar os dados de um paciente
    def alterar_paciente(self, nome_busca, novo_nome=None, nova_idade=None, nova_prioridade=None):
        atual = self.inicio
        mem_antes = self.memoria_total()

        while atual:
            if atual.nome == nome_busca:
                print(f"Alterando dados de {atual.nome}")
                if novo_nome:
                    atual.nome = novo_nome
                if nova_idade:
                    atual.idade = nova_idade
                if nova_prioridade and nova_prioridade != atual.prioridade:
                    self._remover_nodo(atual)
                    self.adicionar_paciente(novo_nome or atual.nome, nova_idade or atual.idade, nova_prioridade)
                    return
                self._monitorar_memoria("ALTERAR", mem_antes)
                return
            atual = atual.proximo

        print("Paciente não encontrado.")

    # Função para remover nó do paciente editado da fila.
    def _remover_nodo(self, nodo):
        if nodo == self.inicio:
            self.inicio = nodo.proximo
            if self.inicio:
                self.inicio.anterior = None
        elif nodo == self.fim:
            self.fim = nodo.anterior
            if self.fim:
                self.fim.proximo = None
        else:
            nodo.anterior.proximo = nodo.proximo
            nodo.proximo.anterior = nodo.anterior

        if nodo.prioridade == 2:
            self.pacientes_prioritarios -= 1
        else:
            self.pacientes_normais -= 1

    # Função para exibir a fila
    def exibir_fila(self):
        # Cria uma lista com os pacientes na ordem da fila
        pacientes = []
        atual = self.inicio
        while atual:
            pacientes.append(atual)
            atual = atual.proximo

        # Mostra a ordem de atendimento simulando as regras
        print("Fila Atual (ordem de atendimento):")
        pacientes_prioritarios = sum(1 for p in pacientes if p.prioridade == 2)
        pacientes_normais = sum(1 for p in pacientes if p.prioridade == 1)
        alterna_normal = False

        while pacientes:
            if pacientes_prioritarios >= 1 and pacientes_normais >= 7:
                if alterna_normal:
                    # Procura o primeiro paciente normal
                    for i, p in enumerate(pacientes):
                        if p.prioridade == 1:
                            paciente = pacientes.pop(i)
                            print(f"[ {paciente.nome} (N) ] -->", end=" ")
                            pacientes_normais -= 1
                            alterna_normal = False
                            break
                else:
                    # Procura o primeiro paciente prioritário
                    for i, p in enumerate(pacientes):
                        if p.prioridade == 2:
                            paciente = pacientes.pop(i)
                            print(f"[ {paciente.nome} (P) ] -->", end=" ")
                            pacientes_prioritarios -= 1
                            alterna_normal = True
                            break
            else:
                # Remove o primeiro da fila de contagem 
                paciente = pacientes.pop(0)
                tipo = "P" if paciente.prioridade == 2 else "N"
                print(f"[ {paciente.nome} ({tipo}) ] -->", end=" ")
                if paciente.prioridade == 2:
                    pacientes_prioritarios -= 1
                else:
                    pacientes_normais -= 1
        print("FIM")

# Função para usar o menu
def menu():
    fila = FilaAtendimento()

    # Adicionamos pacientes à fila
    fila.adicionar_paciente("Cleiton", 55, 2)
    fila.adicionar_paciente("Joelma", 99, 2)
    fila.adicionar_paciente("Enzo", 12, 1)
    fila.adicionar_paciente("Otavio", 32, 1)
    fila.adicionar_paciente("Leandro", 2, 2)
    fila.adicionar_paciente("Lucas", 49, 1)
    fila.adicionar_paciente("Camila", 39, 1)
    fila.adicionar_paciente("Rafael", 27, 2)
    fila.adicionar_paciente("Isabela", 19, 1)
    fila.adicionar_paciente("Thiago", 34, 1)
    fila.adicionar_paciente("Mariana", 70, 2)
    fila.adicionar_paciente("Gustavo", 12, 1)
    
    
    while True:
        print("\n--- MENU ---")
        print("1. Adicionar paciente")
        print("2. Remover paciente")
        print("3. Alterar paciente")
        print("4. Exibir fila")
        print("5. Sair")
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            nome = input("Nome: ")
            idade = int(input("Idade: "))
            prioridade = int(input("Prioridade (1-Normal, 2-Prioritário): "))
            fila.adicionar_paciente(nome, idade, prioridade)
        elif opcao == "2":
            fila.remover_paciente()
        elif opcao == "3":
            nome = input("Nome do paciente a alterar: ")
            novo_nome = input("Novo nome (ou Enter para manter): ")
            nova_idade = input("Nova idade (ou Enter para manter): ")
            nova_prioridade = input("Nova prioridade (1-Normal, 2-Prioritário, ou Enter para manter): ")
            fila.alterar_paciente(
                nome,
                novo_nome if novo_nome else None,
                int(nova_idade) if nova_idade else None,
                int(nova_prioridade) if nova_prioridade else None
            )
        elif opcao == "4":
            fila.exibir_fila()
        elif opcao == "5":
            print("Saindo...")
            break
        else:
            print("Opção inválida!")


if __name__ == "__main__":
    menu()

