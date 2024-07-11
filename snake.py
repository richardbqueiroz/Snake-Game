import pygame


class Snake:
    def __init__(self, game_active, altura_menu):
        self.tamanho = (15, 15)
        self.raio_cabeca = 7
        self.velocidade = 10
        self.tamanho_maximo = 49 * 49
        self.textura = pygame.Surface(self.tamanho)
        self.corpo = [(100, 100), (90, 100), (80, 100)]
        self.direcao = "direita"
        self.pontos = 0
        self.white = (255, 255, 255)
        self.altura_menu = altura_menu
        self.volume_on = True
        self.game_active = game_active
        self.comer_som = pygame.mixer.Sound("data/song.wav")

    def blit(self, screen):
        cabeca = self.corpo[0]
        pygame.draw.circle(
            screen,
            self.white,
            (cabeca[0] + self.raio_cabeca, cabeca[1] + self.raio_cabeca),
            self.raio_cabeca)

        for i in range(1, len(self.corpo) - 1):
            posicao = self.corpo[i]
            pygame.draw.rect(
                screen,
                self.white,
                (posicao[0], posicao[1], self.tamanho[0], self.tamanho[1]))

        if len(self.corpo) > 1:
            cauda = self.corpo[-1]
            pygame.draw.circle(
                screen,
                self.white,
                (cauda[0] + self.raio_cabeca, cauda[1] + self.raio_cabeca),
                self.raio_cabeca)

    def andar(self):
        x, y = self.corpo[0]

        if self.direcao == "direita":
            x += self.velocidade
        elif self.direcao == "esquerda":
            x -= self.velocidade
        elif self.direcao == "cima":
            y -= self.velocidade
        elif self.direcao == "baixo":
            y += self.velocidade

        self.corpo.insert(0, (x, y))
        self.corpo.pop(-1)

    def mudar_direcao(self, nova_direcao):
        direcoes = {"cima": "baixo", "baixo": "cima",
                    "esquerda": "direita", "direita": "esquerda"}
        if self.direcao != direcoes[nova_direcao]:
            self.direcao = nova_direcao

    def colisao_frutinha(self, frutinha):
        x_cabeca, y_cabeca = self.corpo[0]
        frutinha_x, frutinha_y = frutinha.posicao
        tamanho_frutinha = frutinha.imagem.get_size()

        horizontal = (
            x_cabeca < frutinha_x + tamanho_frutinha[0] and
            x_cabeca + self.tamanho[0] > frutinha_x)

        vertical = (
            y_cabeca < frutinha_y + tamanho_frutinha[1] and
            y_cabeca + self.tamanho[1] > frutinha_y)

        return horizontal and vertical

    def comer(self):
        if self.volume_on:
            pygame.mixer.Sound.play(self.comer_som)
        self.corpo.append((0, 0))
        self.pontos += 1

    def set_volume(self, volume_state):
        self.volume_on = volume_state
        if not self.volume_on:
            pygame.mixer.stop()
        else:
            pygame.mixer.unpause()

    def colisao(self):
        x, y = self.corpo[0]

        if (
            x < 0
            or y < self.altura_menu
            or x > 790
            or y > 620
            or self.corpo[0] in self.corpo[1:]
            or len(self.corpo) > self.tamanho_maximo
        ):
            self.pontos = 0
            return True
        return False
