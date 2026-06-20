import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import pygame

from jogo_da_velha import criar_board, faz_movimento, get_input_valido, \
    print_board, verifica_ganhador, verica_movimento

from minimax import movimento_ia, movimentoIA_facil, movimentoIA_medio

pygame.mixer.init()
pygame.mixer.music.load('musica.mp3')
pygame.mixer.music.play()

pygame.font.init()

# Tarefa 4: Cor de fundo customizada (azul petróleo)
COR_FUNDO = (0, 128, 128)

def draw_board(win, board):
    height = 600
    width = 600
    tamanho = 600 / 3  # 200px por célula

    # Linhas do tabuleiro
    for i in range(1, 3):
        pygame.draw.line(win, (0, 0, 0), (0, i * tamanho),
                         (width, i * tamanho), 3)
        pygame.draw.line(win, (0, 0, 0), (i * tamanho, 0),
                         (i * tamanho, height), 3)

    # Tarefa 1: Corrigido para range(3) — todas as 9 células são desenhadas
    font = pygame.font.SysFont('comicsans', 100)
    for i in range(3):
        for j in range(3):
            if board[i][j] != " ":
                x = j * tamanho
                y = i * tamanho
                text = font.render(board[i][j], 1, (0, 0, 0))
                win.blit(text, (x + 65, y + 50))

def draw_dificuldade(win, dificuldade):
    nomes = {1: "Facil", 2: "Medio", 3: "Dificil"}
    nome = nomes.get(dificuldade, "")
    font = pygame.font.SysFont('comicsans', 28)
    texto = font.render(f"Dificuldade: {nome}", 1, (255, 255, 255))
    win.blit(texto, (10, 10))

def draw_tela_selecao(win):
    win.fill(COR_FUNDO)
    font_titulo = pygame.font.SysFont('comicsans', 50)
    font_opcoes = pygame.font.SysFont('comicsans', 36)

    titulo = font_titulo.render("Jogo da Velha", 1, (255, 255, 255))
    win.blit(titulo, (600 // 2 - titulo.get_width() // 2, 120))

    sub = font_opcoes.render("Escolha a dificuldade:", 1, (220, 220, 220))
    win.blit(sub, (600 // 2 - sub.get_width() // 2, 220))

    op1 = font_opcoes.render("1 - Facil", 1, (200, 255, 200))
    op2 = font_opcoes.render("2 - Medio", 1, (255, 255, 180))
    op3 = font_opcoes.render("3 - Dificil", 1, (255, 160, 160))

    win.blit(op1, (600 // 2 - op1.get_width() // 2, 300))
    win.blit(op2, (600 // 2 - op2.get_width() // 2, 360))
    win.blit(op3, (600 // 2 - op3.get_width() // 2, 420))

    pygame.display.update()

def redraw_window(win, board, dificuldade):
    win.fill(COR_FUNDO)
    draw_board(win, board)
    draw_dificuldade(win, dificuldade)

def main():
    win = pygame.display.set_mode((600, 600))
    pygame.display.set_caption("Jogo da Velha")

    # Tarefa 4: Tela de seleção de dificuldade (1=Fácil, 2=Médio, 3=Difícil)
    dificuldade = None
    draw_tela_selecao(win)

    while dificuldade is None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    dificuldade = 1
                elif event.key == pygame.K_2:
                    dificuldade = 2
                elif event.key == pygame.K_3:
                    dificuldade = 3

    board = criar_board()
    redraw_window(win, board, dificuldade)
    pygame.display.update()

    jogador = 0
    ganhador = verifica_ganhador(board)

    while not ganhador:
        i = None
        j = None
        print_board(board)

        if jogador == 0:
            # Vez do humano — aguarda clique do mouse
            jogou = False
            while not jogou:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        return
                    elif event.type == pygame.MOUSEBUTTONUP:
                        pos = pygame.mouse.get_pos()
                        # Tarefa 1: mapeamento correto (células de 200px)
                        i = int(pos[1] / 200)
                        j = int(pos[0] / 200)
                        jogou = True

            if verica_movimento(board, i, j):
                faz_movimento(board, i, j, jogador)
                jogador = (jogador + 1) % 2

        else:
            # Tarefa 4: condicional por dificuldade
            # movimentoIA_facil e movimentoIA_medio já chamam faz_movimento internamente
            # movimento_ia (difícil) não faz o movimento, precisamos chamar faz_movimento
            if dificuldade == 1:
                movimentoIA_facil(board, jogador)
            elif dificuldade == 2:
                movimentoIA_medio(board, jogador)
            else:
                i, j = movimento_ia(board, jogador)
                faz_movimento(board, i, j, jogador)

            jogador = (jogador + 1) % 2

        ganhador = verifica_ganhador(board)
        redraw_window(win, board, dificuldade)
        pygame.display.update()

    # Mostrar resultado final
    font_res = pygame.font.SysFont('comicsans', 60)
    if ganhador == "EMPATE":
        msg = "Empate!"
    else:
        msg = f"{ganhador} venceu!"
    texto = font_res.render(msg, 1, (255, 255, 255))
    win.blit(texto, (600 // 2 - texto.get_width() // 2, 260))
    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

main()
