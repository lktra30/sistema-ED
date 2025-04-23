# Projeto Fila de Atendimento Médico

O objetivo desse sistema é facilitar o controle de uma fila de atendimento de um hospital ou posto médico, garantindo qualidade e organização durante o processo de atendimento. 

O projeto em geral conta com um sistema de lista duplamente encadeada e visa, não só permitir operações básicas de adição, remoção e edição, mas também informar sobre o consumo de memória de cada operação, buscando uma análise técnica mais detalhada.

## Classes

### 1. Pacientes:

Representa o paciente da fila.

Atributos: 
- Nome, 
- Idade, 
- Prioridade (1=Normal ou 2=Prioritario), 
- Próximo (referência ao próximo paciente da fila), 
- Anterior (referência ao paciente anterior da fila).

Métodos:
__init__(self, nome, idade, prioridade): Inicializa um novo paciente com novos dados.
calcular_memoria(self): Calcula o tamanho do objeto paciente. 

### 2. FilaAtendimento:

Simula a fila de pacientes, permitindo operações de adição, remoção, edição e exibição.

Atributos:
- inicio: Referência ao primeiro paciente da fila.
- fim: Referência ao último paciente  da fila.
- pacientes_prioritarios: Contador de pacientes prioritários.
- pacientes_normais: Contador de pacientes normais.
- alterna_normal: Controle para alternância de atendimento entre normais e prioritários.

Métodos:
- __init__(self): Inicializa a fila vazia e os contadores.
- memoria_total(self): Calcula a soma da memória ocupada por todos os pacientes na fila.
- _monitorar_memoria(self, operacao, mem_antes): Exibe no console a diferença de memória antes e depois de uma operação.
- adicionar_paciente(self, nome, idade, prioridade): Adiciona um novo paciente à fila, respeitando a prioridade.
- remover_paciente(self): Remove um paciente da fila, simulando um atendimento, alternando entre prioritário e normal conforme regras internas.
- alterar_paciente(self, nome_busca, novo_nome=None, nova_idade=None, nova_prioridade=None): Altera os dados de um paciente existente, podendo inclusive mudar sua prioridade.
- _remover_nodo(self, nodo): Remove um nó (paciente) específico da fila, ajustando os ponteiros.
- exibir_fila(self): Exibe no console a fila de pacientes, mostrando nome e tipo (N = normal, P = prioritário) na formatação ASCII

## Menu

Exibe um menu interativo no console, permitindo realizar operações no sistema (Utilize somente números):
- 1. Adicionar pacientes
- 2. Remover pacientes
- 3. Editar pacientes
- 4. Exibir Fila
- 5. Sair

A função utiliza a classe FilaAtendimento e seus métodos para manipular a fila conforme as escolhas do usuário.

## Funcionamento
- Inicialização: O programa começa criando uma instância de FilaAtendimento e adicionando 12 pacientes de exemplo para teste de funcionalidade
- Menu Interativo: O usuário pode escolher entre as opções do menu para manipular a fila.
- Adição de Pacientes: Pacientes são inseridos na fila conforme sua prioridade.
- Remoção de Pacientes: A remoção alterna entre pacientes prioritários e normais, simulando um atendimento, conforme a quantidade de cada tipo na fila.
- Alteração de Pacientes: Permite modificar nome, idade e prioridade de um paciente.
- Exibição da Fila: Mostra todos os pacientes, indicando se são normais ou prioritários.
- Monitoramento de Memória: Após cada operação de adição, remoção ou alteração, o sistema exibe o uso de memória antes e depois da operação.

## Observações
- Não há persistência dos dados: ao encerrar o programa, a fila é perdida.
