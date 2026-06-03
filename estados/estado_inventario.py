import pygame
from .estado_base import EstadoBase
from componentes.inventario import Inventario


class EstadoInventario(EstadoBase):
    def __init__(self, nomeJogador):
        super().__init__()
        self.nomeJogador = nomeJogador
        self.inventario_hud = Inventario(self.nomeJogador)

    def abrir(self):
        super().abrir()
        self.inventario_hud.carregar_inventario()

    def fechar(self):
        self.inventario_hud.salvar_inventario()
        super().fechar()

    def tratarEventos(self, eventos):
        self.inventario_hud.tratarEventos(eventos)
        for evento in eventos:
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                    self.proximo_estado = "Teste"
                    self.concluido = True

    def atualizar(self, dt):
        pass

    def desenhar(self, tela):
        tela.fill((40, 40, 40))
        self.inventario_hud.desenhar(tela)