import pygame
from .base import EstadoBase
from banco import tabela_jogador
from utilidade.itens import aplicarEfeitoItem
from tinydb import Query
class EstadoInventario(EstadoBase):
    def __init__(self, nomeJogador):
        super().__init__()
        self.col = 1
        self.linha = 15
        self.tamanhoDeSlot = 15
        self.espacamento = 5
        self.nomeJogador = nomeJogador
        self.dadosJogador = None
        self.inventario = []
        self.slotSelecionado = None
        self.posicoesCalculadas = False
        self.startX = 0
        self.startY = 0

    def abrir(self):
        super().abrir()
        self.slotSelecionado = None
        resultado = tabela_jogador.search(Query().nome == self.nomeJogador)
        if resultado:
            self.dadosJogador = resultado[0]
            self.inventario = self.dadosJogador.get('inv', [])
        else:
            self.inventario = []
    def fechar(self):
        if self.dadosJogador:
            tabela_jogador.update(
                {
                    'inv': self.inventario,
                    'vida': self.dadosJogador['vida']
                 },
                Query().nome == self.nomeJogador
            )
        super().fechar()
    def tratarEventos(self, eventos):
        ponteiroMouse = pygame.mouse.get_pos()
        self.slotSelecionado = self.obterSlotPorPosicao(ponteiroMouse)
        for evento in eventos:
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                    self.proximo_estado = "Teste"
                    self.concluido = True

            if evento.type == pygame.MOUSEBUTTONDOWN and self.slotSelecionado is not None:
                    idx = self.slotSelecionado
                    if idx < len(self.inventario):
                        item = self.inventario[idx]
                        if evento.button == 1: #Clique esquerdo do mause
                            sucesso = aplicarEfeitoItem(item, self.dadosJogador)
                            if sucesso:
                                self.inventario.pop(idx)
                            elif evento.button == 3: #Clique direito do mause
                                removido = self.inventario.pop(idx)
                                print(f"Removeu {removido['nome']}")
    def atualizar(self, dt):
        pass
    def obterSlotPorPosicao(self, pos):
        x, y = pos
        if self.startX <= x <= self.startX + self.tamanhoDeSlot:
            for l in range(self.linha):
                slotY = self.startY + l*(self.tamanhoDeSlot + self.espacamento)
                if slotY <= y <= slotY + self.tamanhoDeSlot:
                    return l
        return None
    def desenhar(self, tela):
        tela.fill((40, 40, 40))
        # Calcula a centralização baseado no tamanho real da janela (Ex: 800x600)
        if not self.posicoesCalculadas:
            largura_tela, altura_tela = tela.get_size()
            grid_width = (self.col * self.tamanhoDeSlot) + ((self.col - 1) * self.espacamento)
            grid_height = (self.linha * self.tamanhoDeSlot) + ((self.linha - 1) * self.espacamento)
            self.startX = (largura_tela - grid_width) // 2
            self.startY = (altura_tela - grid_height) // 2
            self.posicoesCalculadas = True

        # Desenha os 15 slots verticais
        for l in range(self.linha):
            slot_x = self.startX
            slot_y = self.startY + l * (self.tamanhoDeSlot + self.espacamento)

            # Cor de destaque se o mouse estiver em cima
            cor = (200, 200, 200) if self.slotSelecionado == l else (100, 100, 100)
            pygame.draw.rect(tela, cor, (slot_x, slot_y, self.tamanhoDeSlot, self.tamanhoDeSlot))

            # Se houver item salvo no banco para esse índice
            if l < len(self.inventario):
                # Desenha o miolo verde indicador de item
                pygame.draw.rect(tela, (0, 255, 0),
                                 (slot_x + 3, slot_y + 3, self.tamanhoDeSlot - 6, self.tamanhoDeSlot - 6))