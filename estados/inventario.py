import pygame
from .base import EstadoBase
class EstadoInventario(EstadoBase):
    def __init__(self, tela):
        super().__init__()
        self.col = 1
        self.linha = 15
        self.tamanhoDeSlot = 15
        self.espacamento = 5

        # Centralizar a grade do inventário na tela
        self.grid_width = (self.col * self.tamanhoDeSlot) + ((self.col - 1) * self.espacamento)
        self.grid_height = (self.linha * self.tamanhoDeSlot) + ((self.linha - 1) * self.espacamento)
        self.start_x = (tela - self.grid_width) // 2
        self.start_y = (tela - self.grid_height) // 2

        self.slot_selecionado = None

    def tratarEventos(self, eventos):
        ponteiroMouse = pygame.mouse.get_pos()
        for evento in eventos:
            if evento.type == pygame.QUIT:
                pygame.quit()
                pass
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                    self.proximo_estado = "" #SAIR DO INV

            if evento.type == pygame.MOUSEBUTTONDOWN:
                if self.slot_selecionado is not None:
                    idx = self.slot_selecionado[1]
                    if evento.button == 1:
                        if idx < len('''DICIONARIO DE ITENS'''):
                            print(f"Usou: '''Item.pop(idx)'''")
                    elif evento.button == 3:
                        if idx < len('''DICIONARIO DE ITENS'''):
                            removido = '''DICIONARIO DE ITENS.pop(idx)'''
                            print(f"Removeu {removido}")
