import threading
import random
import time
import os

class Encomenda:
    def __init__(self, id, origem, destino):
        self.id = id
        self.origem = origem
        self.destino = destino
        self.chegada_origem = None
        self.carregada_em = None
        self.descarregada_em = None
        self.veiculo_id = None

class PontoRedistribuicao(threading.Thread):
    def __init__(self, id):
        super().__init__()
        self.id = id
        self.fila = []
        self.lock = threading.Lock()
        self.sem = threading.Semaphore(0)  # Para controlar entregas

    def adicionar_encomenda(self, encomenda):
        with self.lock: # Garante exclusividade para adicionar encomenda
            self.fila.append(encomenda)
            self.sem.release()

    def retirar_encomenda(self):
        while encomendas_ativas.is_set() or self.fila: # Enquanto encomendas_ativas ou há encomendas na fila do ponto atual
            self.sem.acquire()
            with self.lock: # Garante exclusividade para retirar encomenda
                self.sem.release()
                if self.fila:
                    return self.fila.pop(0)
                else:
                    return None

    def run(self):
        while encomendas_ativas.is_set():
            time.sleep(0.1)  # Simula atividade do ponto
        print(f"Ponto {self.id} encerrado.")

class Veiculo(threading.Thread):
    def __init__(self, id, pontos, capacidade):
        super().__init__()
        self.id = id
        self.pontos = pontos
        self.capacidade = capacidade
        self.carga = []
        self.ponto_atual: PontoRedistribuicao = random.choice(self.pontos)  # Ponto inicial aleatório
        #print(f"[DEBUG] Veiculo {self.id} iniciado no ponto {self.ponto_atual.id}")

    def run(self):
        while encomendas_ativas.is_set() or any(p.fila for p in self.pontos): # Enquanto encomendas_ativas ou pontos com fila de encomendas
            # Descarrega encomendas no ponto atual
            for encomenda in self.carga[:]:
                if encomenda.destino == self.ponto_atual.id:
                    with self.ponto_atual.lock:  # Exclusividade para descarregar
                        #print(f"[DEBUG] Veiculo {self.id} descarregando encomenda {encomenda.id} no ponto {self.ponto_atual.id}")
                        time.sleep(random.uniform(0.5, 1.5)) # Tempo de descarga
                        encomenda.descarregada_em = time.time()
                        salvar_rastro(encomenda)
                        self.carga.remove(encomenda)
                        #print(f"[DEBUG] Encomenda {encomenda.id} descarregada no ponto {self.ponto_atual.id}")

            # Tenta carregar encomendas no ponto atual
            while len(self.carga) < self.capacidade: # Enquanto o veículo ainda tenha capacidade de carga
                encomenda = self.ponto_atual.retirar_encomenda()
                if encomenda: # Se houver encomenda para carregar
                    encomenda.carregada_em = time.time()
                    encomenda.veiculo_id = self.id
                    self.carga.append(encomenda)
                    #print(f"[DEBUG] Veiculo {self.id} carregou encomenda {encomenda.id} no ponto {self.ponto_atual.id}")
                else:
                    break

            # Aguarda se estiver sem carga e o ponto não tiver encomendas
            if not self.carga and not self.ponto_atual.fila:
                #print(f"[DEBUG] Veiculo {self.id} aguardando no ponto {self.ponto_atual.id}")
                time.sleep(1)  # Espera breve antes de seguir para o próximo ponto

            # Simula viagem para o próximo ponto
            proximo_ponto_id = (self.ponto_atual.id + 1) % len(self.pontos) # Fila circular
            proximo_ponto = self.pontos[proximo_ponto_id]
            #print(f"[DEBUG] Veiculo {self.id} viajando do ponto {self.ponto_atual.id} para o ponto {proximo_ponto.id}")
            time.sleep(random.uniform(1, 3))
            self.ponto_atual = proximo_ponto
            #print(f"[DEBUG] Veiculo {self.id} chegou ao ponto {self.ponto_atual.id}")

# Função para salvar o rastro de uma encomenda em um arquivo txt
def salvar_rastro(encomenda):
    filename = f"encomenda_{encomenda.id}.txt"
    with open(filename, "w") as f:
        f.write(f"Encomenda: {encomenda.id}\n")
        f.write(f"Origem: {encomenda.origem}\n")
        f.write(f"Destino: {encomenda.destino}\n")
        f.write(f"Criada em: {time.ctime(encomenda.chegada_origem)}\n")
        f.write(f"Carregada no veículo {encomenda.veiculo_id}: {time.ctime(encomenda.carregada_em)}\n")
        f.write(f"Descarregada no destino: {time.ctime(encomenda.descarregada_em)}\n")

def encomenda_thread(encomenda, pontos):
    encomenda.chegada_origem = time.time()
    pontos[encomenda.origem].adicionar_encomenda(encomenda)

def limpar_console():
    os.system('cls' if os.name == 'nt' else 'clear')

# Função para monitorar o sistema em tempo real
def monitoramento_real(pontos, veiculos, encomendas):
    while encomendas_ativas.is_set():
        limpar_console()
        print("Monitoramento em tempo real")
        print("=" * 50)
        
        print("Pontos de Redistribuição:")
        for ponto in pontos:
            with ponto.lock:
                fila = [e.id for e in ponto.fila]
            print(f"Ponto {ponto.id}: Estoque: {len(fila)}")

        print("\nVeículos:")
        for veiculo in veiculos:
            proximo_ponto_id = (veiculo.ponto_atual.id + 1) % len(pontos)
            localizacao = f"{veiculo.ponto_atual.id} -> {proximo_ponto_id}"

            carga_formatada = [f"{e.id} -> P{e.destino}" for e in veiculo.carga]

            print(f"Veículo {veiculo.id}: "
                  f"Carga: [{', '.join(carga_formatada)}], "
                  f"Localização: {localizacao}")
        
        # Pausa para o próximo ciclo de atualização
        time.sleep(5)

# Função auxiliar para verificar se todas as encomendas foram entregues
def todas_encomendas_entregues(encomendas):
    return all(encomenda.descarregada_em is not None for encomenda in encomendas)

# Início do programa
if __name__ == "__main__":
    # Inputs do usuário garantindo que P > A > C
    while True:
        S = int(input("Digite o número de pontos de redistribuição (S): "))
        C = int(input("Digite o número de veículos (C): "))
        P = int(input("Digite o número de encomendas (P): "))
        A = int(input("Digite a capacidade de carga de cada veículo (A): "))
        if P > A > C:
            break
        else:
            print("Erro: Certifique-se de que P > A > C. Tente novamente.")

    # Inicialização
    encomendas_ativas = threading.Event()
    encomendas_ativas.set()
    pontos = [PontoRedistribuicao(i) for i in range(S)]
    encomendas = [
        Encomenda(
            i,
            origem := random.randint(0, S - 1),
            random.choice([d for d in range(S) if d != origem])
        )
        for i in range(P)
    ]
    veiculos = [Veiculo(i, pontos, A) for i in range(C)]

    # Inicializa threads
    for ponto in pontos:
        ponto.start()
    for encomenda in encomendas:
        threading.Thread(target=encomenda_thread, args=(encomenda, pontos)).start()
    for veiculo in veiculos:
        veiculo.start()
    monitoramento_thread = threading.Thread(target=monitoramento_real, args=(pontos, veiculos, encomendas))
    monitoramento_thread.start()

    # Espera até que todas as encomendas sejam entregues
    while not todas_encomendas_entregues(encomendas):
        time.sleep(1)

    # Encerra threads
    encomendas_ativas.clear()
    for ponto in pontos:
        ponto.join()
    for veiculo in veiculos:
        veiculo.join()

    print("Todas as encomendas foram entregues.")