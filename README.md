# Simulação de Logística com Veículos e Pontos de Redistribuição

Este projeto é uma simulação de um sistema logístico envolvendo veículos, encomendas e pontos de redistribuição. Ele utiliza **programação concorrente** para simular o transporte de encomendas entre diferentes locais com uso de veículos. Cada elemento interage dinamicamente, permitindo monitoramento em tempo real das operações.

---

## Funcionalidades

- **Criação de encomendas** com origem e destino definidos aleatoriamente.
- **Veículos** que transportam encomendas entre pontos de redistribuição com capacidade limitada.
- **Pontos de redistribuição** que armazenam encomendas aguardando transporte.
- **Monitoramento em tempo real**, exibindo o status de veículos, cargas e estoques nos pontos.
- Salvamento de **rastros de encomendas** em arquivos de texto (`encomenda_X.txt`) contendo detalhes do transporte.

---

## Estrutura do Código

### Classes principais

- **`Encomenda`**: Representa uma encomenda com ID, origem, destino e timestamps para registrar os eventos de transporte.
- **`PontoRedistribuicao`**: Thread que gerencia uma fila de encomendas em um ponto.
- **`Veiculo`**: Thread que simula um veículo transportando encomendas entre os pontos.

### Outras funções importantes

- **`monitoramento_real`**: Atualiza e exibe o estado dos veículos e pontos de redistribuição em tempo real.
- **`salvar_rastro`**: Grava informações sobre cada encomenda entregue em um arquivo de texto.
- **`todas_encomendas_entregues`**: Verifica se todas as encomendas foram entregues.

---

## Como usar

1. Insira os parâmetros solicitados:
   - **S**: Número de pontos de redistribuição.
   - **C**: Número de veículos.
   - **P**: Número de encomendas.
   - **A**: Capacidade de carga dos veículos.

   **Nota**: Certifique-se de que `P > A > C`.

2. O monitoramento será exibido no terminal, e os arquivos de rastros serão gerados no diretório do projeto.

---

## Exemplo de execução

Entrada no terminal:
```
Digite o número de pontos de redistribuição (S): 5
Digite o número de veículos (C): 3
Digite o número de encomendas (P): 20
Digite a capacidade de carga de cada veículo (A): 10
```

Saída no terminal (parcial):
```
Monitoramento em tempo real
==================================================
Pontos de Redistribuição:
Ponto 0: Estoque: 3
Ponto 1: Estoque: 5
...

Veículos:
Veículo 0: Carga: [2 -> P3, 4 -> P0], Localização: 0 -> 1
Veículo 1: Carga: [], Localização: 1 -> 2
...
```

Arquivos gerados:
- `encomenda_0.txt`
- `encomenda_1.txt`

---

## Requisitos

- Python 3.8 ou superior.
- Módulos padrão: `threading`, `random`, `time`, `os`.
