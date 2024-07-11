import sys

import pygame
import pygame.gfxdraw

from fruit import Frutinha
from snake import Snake


class Game():
    def __init__(self):
        self.game_active = True
        self.witdh, self.height = 800, 600
        self.button_radius = 62
        self.altura_menu = 40
        self.tamanho_casa = 67
        self.black = (0, 0, 0)
        self.white = (255, 255, 255)
        self.red = (255, 0, 0)
        self.grey = (105, 105, 105, 50)
        self.light_green = (167, 217, 72)
        self.dark_green = (142, 204, 57)
        self.green = (0, 139, 0)
        self.volume_button_radius = 30
        self.image_path = pygame.image.load("data/imagem.jpg")
        self.volume_on_img = pygame.image.load("data/loud.png")
        self.volume_off_img = pygame.image.load("data/mute.png")
        self.volume_on = True
        self.volume = self.volume_on_img
        self.cobrinha = Snake(self, self.altura_menu)
        self.frutinha = Frutinha(self.cobrinha)
        self.screen = pygame.display.set_mode((self.witdh, self.height + self.altura_menu))

    def game(self):
        pygame.display.set_caption("Snake Game")
        running = True
        clock = pygame.time.Clock()

        while running:
            clock.tick(30)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    self.eventos_teclado(event.key)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.clique_menu(pygame.mouse.get_pos())

            self.atualizar_jogo()

    def iniciar_jogo(self):
        pygame.display.set_caption("Snake Game")
        imagem_fundo = self.image_path
        imagem_fundo = pygame.transform.scale(imagem_fundo, (self.witdh, self.height + self.altura_menu))
        running = True
        clock = pygame.time.Clock()

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.clique_mouse()

            self.renderizar_tela_jogo(imagem_fundo)
            clock.tick(60)

        pygame.quit()
        sys.exit()

    def atualizar_jogo(self):
        if self.game_active:
            if self.cobrinha.colisao_frutinha(self.frutinha):
                self.cobrinha.comer()
                self.frutinha = Frutinha(self.cobrinha)
            if self.cobrinha.colisao():
                self.game_active = False
            self.cobrinha.andar()
            self.screen.fill(self.black)
            self.desenhar_tabuleiro()
            self.menu_opcoes()
            self.pontuacao()
            self.frutinha.blit(self.screen)
            self.cobrinha.blit(self.screen)
        else:
            self.jogo_inativo()
        pygame.display.update()

    def jogo_inativo(self):
        self.screen.fill(self.black)
        self.desenhar_tabuleiro()
        self.menu_opcoes()
        self.pontuacao()
        self.fim_de_jogo()
        pygame.display.update()

    def reiniciar_jogo(self):
        self.cobrinha = Snake(self, self.altura_menu)
        self.frutinha = Frutinha(self.cobrinha)
        self.game_active = True
        self.cobrinha.set_volume(self.volume_on)

    def renderizar_tela_jogo(self, imagem_fundo):
        self.screen.blit(imagem_fundo, (0, 0))
        self.desenhar_botao_redondo("Jogar", (self.witdh // 2, self.height // 2), self.button_radius, self.grey, self.white)
        pygame.display.flip()

    def menu_opcoes(self):
        self.menu_rect = pygame.Rect(0, 0, self.witdh, self.altura_menu)
        pygame.draw.rect(self.screen, self.green, self.menu_rect)
        self.opcoes = ["Inicio", "Reiniciar", "Sair"]
        self.button_rects = []
        posicoes = [(10, 5), (self.witdh // 2 - 280, 5), (self.witdh - 110, 5)]

        for i, opcao in enumerate(self.opcoes):
            fonte = pygame.font.SysFont(None, 30)
            texto = fonte.render(opcao, True, self.black)
            button_rect = pygame.Rect(*posicoes[i], 100, self.altura_menu - 10)
            self.button_rects.append(button_rect)
            pygame.draw.rect(self.screen, self.black, button_rect, 2)
            self.centralizar_menu_opcoes(texto, button_rect)

        self.volume_button_rect = pygame.Rect(self.witdh - 160, 5, 40, self.altura_menu - 10)
        pygame.draw.rect(self.screen, self.black, self.volume_button_rect, 2)
        self.centralizar_menu_opcoes(self.volume, self.volume_button_rect)

    def centralizar_menu_opcoes(self, texto, rect):
        x = rect.x + rect.width // 2 - texto.get_width() // 2
        y = rect.y + rect.height // 2 - texto.get_height() // 2
        self.screen.blit(texto, (x, y))

    def pontuacao(self):
        menu_x = self.witdh // 2
        menu_y = self.altura_menu // 2
        maca_image = pygame.image.load("data/apple.png")
        maca_rect = maca_image.get_rect(center=(menu_x, menu_y))
        self.screen.blit(maca_image, maca_rect.topleft)

        fonte_pontos = pygame.font.SysFont(None, 35)
        pontos_str = f'{self.cobrinha.pontos}'
        pontos_texto = fonte_pontos.render(f': {pontos_str}', True, self.black)
        pontos_rect = pontos_texto.get_rect(center=(menu_x + maca_rect.width // 2 + 20, menu_y))
        self.screen.blit(maca_image, maca_rect.topleft)
        self.screen.blit(pontos_texto, (maca_rect.right + 5, maca_rect.centery - pontos_rect.height // 2))

    def clique_menu(self, mouse_pos):
        for i, opcao in enumerate(self.opcoes):
            if self.button_rects[i].collidepoint(mouse_pos):
                if opcao == "Inicio":
                    pygame.time.delay(200)
                    self.iniciar_jogo()
                elif opcao == "Reiniciar":
                    self.reiniciar_jogo()
                    pygame.time.delay(500)
                elif opcao == "Sair":
                    pygame.time.delay(100)
                    pygame.quit()
                    sys.exit()
            if self.volume_button_rect.collidepoint(mouse_pos):
                self.toggle_volume()

    def clique_mouse(self):
        mouse_pos = pygame.mouse.get_pos()
        if (
            self.witdh // 2 - self.button_radius <= mouse_pos[0] <= self.witdh // 2 + self.button_radius
            and self.height // 2 - self.button_radius <= mouse_pos[1] <= self.height // 2 + self.button_radius
        ):
            if self.game_active or self.cobrinha.colisao():
                self.reiniciar_jogo()
                pygame.time.delay(500)
                self.game()
            if self.volume_button_rect.collidepoint(mouse_pos):
                self.toggle_volume()

    def eventos_teclado(self, key):
        if key == pygame.K_UP or key == pygame.K_w:
            self.cobrinha.mudar_direcao("cima")
        elif key == pygame.K_DOWN or key == pygame.K_s:
            self.cobrinha.mudar_direcao("baixo")
        elif key == pygame.K_LEFT or key == pygame.K_a:
            self.cobrinha.mudar_direcao("esquerda")
        elif key == pygame.K_RIGHT or key == pygame.K_d:
            self.cobrinha.mudar_direcao("direita")

    def desenhar_tabuleiro(self):
        for linha in range(9):
            for coluna in range(12):
                x = coluna * self.tamanho_casa
                y = linha * self.tamanho_casa + self.altura_menu
                rect_params = (x, y, self.tamanho_casa, self.tamanho_casa)
                cor = self.light_green if (linha + coluna) % 2 == 0 else self.dark_green
                pygame.draw.rect(self.screen, cor, rect_params)

    def desenhar_botao_redondo(self, text, center, radius, button_color, text_color):
        pygame.gfxdraw.filled_circle(self.screen, center[0], center[1], radius, button_color)
        pygame.gfxdraw.aacircle(self.screen, center[0], center[1], radius, button_color)
        font = pygame.font.Font(None, 40)
        text_surface = font.render(text, True, text_color)
        text_rect = text_surface.get_rect(center=center)
        self.screen.blit(text_surface, text_rect.topleft)
        return text_rect

    def fim_de_jogo(self):
        self.fonte = pygame.font.SysFont(None, 80)
        game_over_text = self.fonte.render("Fim de Jogo", True, self.red)
        text_rect = game_over_text.get_rect(center=(self.witdh // 2, self.height // 2))
        self.screen.blit(game_over_text, text_rect.topleft)

    def toggle_volume(self):
        self.volume_on = not self.volume_on
        self.volume = self.volume_on_img if self.volume_on else self.volume_off_img
        if not self.volume_on:
            pygame.mixer.stop()
        self.cobrinha.set_volume(self.volume_on)

    def clique_do_mouse(self):
        mouse_pos = pygame.mouse.get_pos()
        if (
            self.witdh // 2 - self.button_radius <= mouse_pos[0] <= self.witdh // 2 + self.button_radius
            and self.height // 2 - self.button_radius <= mouse_pos[1] <= self.height // 2 + self.button_radius
        ):
            pygame.time.delay(500)
            self.game()
