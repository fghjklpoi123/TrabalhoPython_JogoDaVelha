import random
from jogo_da_velha import branco, token, verifica_ganhador, faz_movimento

score = {
    "EMPATE": 0,
    "X": 1,
    "O": -1
}

# Função de posições
def get_posicoes(board):
    posicoes = []

    for i in range(3):
        for j in range(3):
            if (board[i][j] == branco):
                posicoes.append([i, j])

    return posicoes

# Função de movimento da I.A. (Difícil - Minimax)
def movimento_ia(board, jogador):
    possibilidades = get_posicoes(board)
    melhor_valor = None
    melhor_movimento = None

    for possibilidade in possibilidades:
        board[possibilidade[0]][possibilidade[1]] = token[jogador]
        valor = minimax(board, jogador)
        board[possibilidade[0]][possibilidade[1]] = branco

        if melhor_valor is None:
            melhor_valor = valor
            melhor_movimento = possibilidade
        elif jogador == 0:
            if (valor > melhor_valor):
                melhor_valor = valor
                melhor_movimento = possibilidade
        elif jogador == 1:
            if (valor < melhor_valor):
                melhor_valor = valor
                melhor_movimento = possibilidade

    return melhor_movimento[0], melhor_movimento[1]

def minimax(board, jogador):
    ganhador = verifica_ganhador(board)

    if (ganhador):
        return score[ganhador]

    jogador = (jogador + 1) % 2

    possibilidades = get_posicoes(board)
    melhor_valor = None

    for possibilidade in possibilidades:
        board[possibilidade[0]][possibilidade[1]] = token[jogador]
        valor = minimax(board, jogador)
        board[possibilidade[0]][possibilidade[1]] = branco

        if melhor_valor is None:
            melhor_valor = valor
        elif jogador == 0:
            if (valor > melhor_valor):
                melhor_valor = valor
        elif jogador == 1:
            if (valor < melhor_valor):
                melhor_valor = valor

    return melhor_valor

# Tarefa 2: IA Fácil — seleciona posição aleatória e executa o movimento
def movimentoIA_facil(board, jogador):
    posicoes_vazias = get_posicoes(board)
    escolha = random.choice(posicoes_vazias)
    faz_movimento(board, escolha[0], escolha[1], jogador)
    return escolha[0], escolha[1]

# Tarefa 3: IA Média — 50% Minimax, 50% aleatório
def movimentoIA_medio(board, jogador):
    if random.random() < 0.5:
        # Minimax não faz o movimento, precisamos fazê-lo aqui
        i, j = movimento_ia(board, jogador)
        faz_movimento(board, i, j, jogador)
        return i, j
    else:
        # movimentoIA_facil já faz o movimento internamente
        return movimentoIA_facil(board, jogador)
