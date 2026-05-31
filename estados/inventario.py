import pygame
from .base import EstadoBase
from banco import tabela_jogador
from utilidade.itens import Item

from tinydb import Query
class EstadoInventario(EstadoBase):
    def __init__(self, nomeJogador):
        super().__init__()
        self.col = 1
        self.linha = 15
        self.tamanhoDeSlot = 30
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
            itensBanco = self.dadosJogador.get('inv', [])
            self.inventario = []
            for itemDit in itensBanco:
                objetoItem = Item(
                    nome=itemDit['nome'],
                    dano=itemDit.get('dano', 0),
                    descricao=itemDit['descricao'],
                    quantidadeMaxima=itemDit.get('quantidadeMaxima', 1),
                    efeito=itemDit['efeito'],
                    preco=itemDit['preco'],
                    raridade=itemDit.get('raridade', 'Comum'),
                    tipo=itemDit['tipo']
                )
                self.inventario.append(objetoItem)
        else:
            self.inventario = []
    def fechar(self):
        if self.dadosJogador:
            itensSalvaveis = []
            for item in self.inventario:
                itensSalvaveis.append({
                    'nome': item.nome,
                    'dano': item.dano,
                    'descricao': item.descricao,
                    'quantidadeMaxima': item.quantidadeMaxima,
                    'efeito': item.efeito,
                    'preco': item.preco,
                    'raridade': item.raridade,
                    'tipo': item.tipo
                })
            tabela_jogador.update(
                {
                    'inv': itensSalvaveis,
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
                slotY = self.startY + l * (self.tamanhoDeSlot + self.espacamento)
                if slotY <= y <= slotY + self.tamanhoDeSlot:
                    return l
        return None

    def desenhar(self, tela):
        tela.fill((40, 40, 40))

        if not self.posicoesCalculadas:
            largura_tela, altura_tela = tela.get_size()
            grid_width = (self.col * self.tamanhoDeSlot) + ((self.col - 1) * self.espacamento)
            grid_height = (self.linha * self.tamanhoDeSlot) + ((self.linha - 1) * self.espacamento)
            self.startX = (largura_tela - grid_width) // 2
            self.startY = (altura_tela - grid_height) // 2
            self.posicoesCalculadas = True

        for l in range(self.linha):
            slot_x = self.startX
            slot_y = self.startY + l * (self.tamanhoDeSlot + self.espacamento)

            # Borda/Fundo do slot sendo selecionado
            cor_borda = (200, 200, 200) if self.slotSelecionado == l else (80, 80, 80)
            pygame.draw.rect(tela, cor_borda, (slot_x, slot_y, self.tamanhoDeSlot, self.tamanhoDeSlot))

            # Se houver item nesse índice do inventário
            if l < len(self.inventario):
                item = self.inventario[l]

                # 🔥 USANDO A RARIDADE NO VISUAL:
                # Busca a cor correspondente à raridade do objeto Item. Se não achar, usa cinza.
                cor_item = self.cores_raridade.get(item.raridade, (120, 120, 120))

                # Desenha o miolo do slot com a cor baseada na raridade do item
                pygame.draw.rect(
                    tela,
                    cor_item,
                    (slot_x + 3, slot_y + 3, self.tamanhoDeSlot - 6, self.tamanhoDeSlot - 6)
                )