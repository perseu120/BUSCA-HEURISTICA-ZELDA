import pygame
import math
import dg
import cria_terreno
import converte_terreno
import desenha_terreno

# Definir as cores dos diferentes tipos de terreno
GRAMA = (124, 252, 0)
AREIA = (244, 164, 96)
FLORESTA = (34, 139, 34)
MONTANHA = (139, 137, 137)
AGUA = (30, 144, 255)
PRETO = (0, 0, 0)
BRANCO = (255, 255, 255)
AMARELO = (201, 176, 10)

converte_variavel = {
    "GRAMA": GRAMA,
    "AREIA": AREIA,
    "FLORESTA": FLORESTA,
    "MONTANHA": MONTANHA,
    "AGUA": AGUA,
    "PRETO": PRETO,
    "BRANCO": BRANCO,
    "AMARELO": AMARELO

}

# Definir o custo de cada tipo de terrenocl
CUSTO = {
    GRAMA: 10,
    AREIA: 20,
    FLORESTA: 100,
    MONTANHA: 150,
    AGUA: 180
}


# Inicializar o pygame
pygame.init()

# Definir as dimensões da tela e o tamanho dos tiles
LARGURA_TELA = 798
ALTURA_TELA = 798
TAMANHO_TILE = 19

# Criar a janela
screen = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))

# Definir as dimensões da matriz do terreno
LINHAS = 42
COLUNAS = 42

# Definir o terreno manualmente

terreno = cria_terreno.retorna_terreno()
dungeon1 = cria_terreno.retorna_dungeon1()
dungeon2 = cria_terreno.retorna_dungeon2()
dungeon3 = cria_terreno.retorna_dungeon3()
tela_final = cria_terreno.retorna_telaFinal()
terreno_convertido = converte_terreno.converte_terreno(
    terreno, converte_variavel)
final_convertido = converte_terreno.converte_terreno(
    tela_final, converte_variavel)

# Adicionar as coordenadas do ponto de partida e destino
ponto_partida = (27, 24)
ponto_destino1 = (32, 5)
ponto_destino2 = (17, 39)
ponto_destino3 = (1, 24)
ponto_espada = (1, 2)


def calcular_distancia(ponto1, ponto2):
    x1, y1 = ponto1
    x2, y2 = ponto2
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)


class Celula:
    def __init__(self, posicao, custo):
        self.posicao = posicao
        self.custo = custo
        self.vizinhos = []
        self.g = 0
        self.h = 0
        self.f = 0
        self.pai = None
        self.visitada = False

    def reset(self):
        self.g = 0
        self.h = 0
        self.f = 0
        self.pai = None
        self.visitada = False


def heuristica(celula_atual, ponto_destino1):
    return calcular_distancia(celula_atual.posicao, ponto_destino1) * 10


def custo(celula_atual, vizinho):
    if vizinho in celula_atual.vizinhos:
        return celula_atual.custo + vizinho.custo
    else:
        return float('inf')


def desenhar_caminho(caminho_recente, ponto_start, ponto_dest):
    # Desenhar o ponto de partida
    pygame.draw.rect(screen, (0, 255, 242), (ponto_start[1] *
                                             TAMANHO_TILE, ponto_start[0]*TAMANHO_TILE, TAMANHO_TILE-1, TAMANHO_TILE-1))
    # Preencher o caminho com a cor vermelha
    clock = pygame.time.Clock()
    for celula in caminho_recente:
        x, y = celula
        rect = pygame.Rect(y * TAMANHO_TILE, x * TAMANHO_TILE,
                           TAMANHO_TILE-1, TAMANHO_TILE-1)
        screen.fill((255, 0, 0), rect=rect)
        pygame.display.update()
        clock.tick(7)


def algoritmo_a_estrela(terreno_convertido, ponto_start, ponto_destino1):
    # Criar as células do terreno
    celulas = [[Celula((linha, coluna), CUSTO[terreno_convertido[linha][coluna]])
                for coluna in range(COLUNAS)] for linha in range(LINHAS)]

    # Conectar as células aos seus vizinhos
    for linha in range(LINHAS):
        for coluna in range(COLUNAS):
            if linha > 0:
                celulas[linha][coluna].vizinhos.append(
                    celulas[linha-1][coluna])
            if linha < LINHAS-1:
                celulas[linha][coluna].vizinhos.append(
                    celulas[linha+1][coluna])
            if coluna > 0:
                celulas[linha][coluna].vizinhos.append(
                    celulas[linha][coluna-1])
            if coluna < COLUNAS-1:
                celulas[linha][coluna].vizinhos.append(
                    celulas[linha][coluna+1])

    # Inicializar as listas aberta e fechada
    aberta = []
    fechada = []

    # Adicionar o ponto de partida à lista aberta
    celula_atual = celulas[ponto_start[0]][ponto_start[1]]
    aberta.append(celula_atual)

    # Loop principal do algoritmo A*
    while aberta:
        # Encontrar a célula na lista aberta com o menor valor de f + h
        celula_atual = min(aberta, key=lambda celula: celula.f + celula.h)

        # Se a célula atual for o ponto de destino, retornar o caminho encontrado
        if celula_atual.posicao == ponto_destino1:
            caminho = []
            custo_total = 0
            while celula_atual:
                caminho.append(celula_atual.posicao)
                celula_atual = celula_atual.pai
                if celula_atual:
                    custo_total += celula_atual.custo
            return (caminho[::-1], custo_total)

        # Remover a célula atual da lista aberta e adicioná-la à lista fechada
        aberta.remove(celula_atual)
        fechada.append(celula_atual)

        # Verificar todos os vizinhos da célula atual
        for vizinho in celula_atual.vizinhos:
            # Se o vizinho estiver na lista fechada, ignorá-lo
            if vizinho in fechada:
                continue

            # Calcular o custo do caminho da célula atual até o vizinho
            novo_g = celula_atual.g + custo(celula_atual, vizinho)

            # Se o vizinho não estiver na lista aberta, adicioná-lo
            if vizinho not in aberta:
                aberta.append(vizinho)
            # Se o novo caminho para o vizinho for mais longo do que o já calculado, ignorá-lo
            elif novo_g >= vizinho.g:
                continue

            # Atualizar os valores de g, h e f do vizinho
            vizinho.g = novo_g
            vizinho.h = heuristica(vizinho, ponto_destino1)
            vizinho.f = vizinho.g + vizinho.h
            vizinho.pai = celula_atual

    return None


# Loop principal do jogo
# Capturar os eventos do pygame
for event in pygame.event.get():
    if event.type == pygame.QUIT:
        pygame.quit()
        quit()

print('---------- CAMINHO PRINCIPAL ----------')

# Desenhar o terreno_convertido na tela
desenha_terreno.desenha_terreno(terreno_convertido, LINHAS, COLUNAS, GRAMA,
                                AREIA, FLORESTA, MONTANHA, AGUA, PRETO, BRANCO, AMARELO, TAMANHO_TILE, screen, False, False)

pygame.draw.rect(screen, (255, 0, 0), (ponto_partida[1] *
                                       TAMANHO_TILE, ponto_partida[0]*TAMANHO_TILE, TAMANHO_TILE-1, TAMANHO_TILE-1))

pygame.display.update()

pygame.time.delay(2500)


destinos = [ponto_destino1, ponto_destino2, ponto_destino3]
menor = 100000000000
indice_destino = 0
partida = ponto_partida
caminho_atual = []
portaaberta = False
while destinos:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

    for i, destino_melhor in enumerate(destinos):
        # Obter o caminho encontrado pelo algoritmo A*
        caminho, custo_total = algoritmo_a_estrela(
            terreno_convertido, partida, destino_melhor)
        if menor > custo_total:
            menor = custo_total
            indice_destino = i
            caminho_atual = caminho

    # Imprime o caminho até cada dungeon
    caminho_str = ' -> '.join(str(i) for i in caminho)
    print(caminho_str)

    desenhar_caminho(caminho_atual, partida, destinos[indice_destino])
    if destinos[indice_destino] == ponto_destino1:
        dg.dungeons(dungeon1, 1)
    elif destinos[indice_destino] == ponto_destino2:
        dg.dungeons(dungeon2, 2)
    elif destinos[indice_destino] == ponto_destino3:
        portaaberta = True
        dg.dungeons(dungeon3, 3)

    screen = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))

    desenha_terreno.desenha_terreno(terreno_convertido, LINHAS, COLUNAS, GRAMA,
                                    AREIA, FLORESTA, MONTANHA, AGUA, PRETO, BRANCO, AMARELO, TAMANHO_TILE, screen, portaaberta, False)

    partida = destinos[indice_destino]
    destinos.remove(destinos[indice_destino])
    menor = 100000000000

caminho, custo_total = algoritmo_a_estrela(
    terreno_convertido, ponto_destino3, ponto_espada)

if menor > custo_total:
    menor = custo_total
    indice_destino = i
    caminho_atual = caminho

desenhar_caminho(caminho_atual, ponto_destino3, ponto_espada)

pygame.time.delay(500)

desenha_terreno.desenha_terreno(final_convertido, LINHAS, COLUNAS, GRAMA,
                                AREIA, FLORESTA, MONTANHA, AGUA, PRETO, BRANCO, AMARELO, TAMANHO_TILE, screen, portaaberta, True)

# Imprime o caminho até o ponto final
caminho_str = ' -> '.join(str(i) for i in caminho)
print(caminho_str)

# Atualizar a tela
pygame.display.update()
input()
