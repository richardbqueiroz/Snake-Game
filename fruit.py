import random

import pygame


class Frutinha:
    def __init__(self, cobrinha):
        self.tamanho = 25, 25
        img_path = "data/apple.png"
        self.imagem = pygame.image.load(img_path)
        imagem_carregada = pygame.image.load(img_path)
        self.imagem = pygame.transform.scale(imagem_carregada, self.tamanho)
        self.posicao = Frutinha.criar_posicao(cobrinha)

    @staticmethod
    def criar_posicao(cobrinha):
        x = random.randint(0, 49) * 10
        y = random.randint(4, 49) * 10

        if (x, y) in cobrinha.corpo:
            return Frutinha.criar_posicao(cobrinha)
        else:
            return x, y

    def blit(self, screen):
        screen.blit(self.imagem, self.posicao)
