import sys

import pygame

from game import Game


def main():
    pygame.init()
    game = Game()
    width = 800
    height = 600
    altura_menu = 40

    image_path = "data/imagem.jpg"
    icon_path = "data/icone.png"
    pygame.display.set_caption("Snake Game")

    imagem = pygame.image.load(image_path)
    imagem = pygame.transform.scale(imagem, (width, height + altura_menu))
    icon_surface = pygame.image.load(icon_path)
    icon_surface = pygame.transform.scale(icon_surface, (40, 40))
    pygame.display.set_icon(icon_surface)

    running = True
    clock = pygame.time.Clock()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                game.clique_do_mouse()

        game.renderizar_tela_jogo(imagem)
        clock.tick(60)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
