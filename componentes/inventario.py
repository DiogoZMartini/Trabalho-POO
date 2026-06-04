import pygame
from banco import tabela_jogador
from utilidade.itens import Item
from tinydb import Query

class Inventario:
    def __init__(self, nomeJogador, modo):
        self.nomeJogador = nomeJogador
        self.modo = modo  # "padrao" (tela cheia), "combate" (mini-hud), "loja" (lista)
        self.slotSelecionado = None
        self.tipoSlotSelecionado = None
        self.inventario = []
        self.equipamentos = {}
        self.dadosJogador = None
        self.slotsRegiao = []
        self.scroll_y = 0
        self.carregarInventario()

    def carregarInventario(self):
        resultado = tabela_jogador.search(Query().nome == self.nomeJogador)
        if resultado:
            self.dadosJogador = resultado[0]
            itensBanco = self.dadosJogador.get('inv', [])
            self.inventario = []
            for itemDit in itensBanco:
                if itemDit:
                    self.inventario.append(self.dicionarioParaObjeto(itemDit))
            eqBanco = self.dadosJogador.get('equipamentos', {})
            self.equipamentos = {k: None for k in ["Aapacete", "Aolar", "Arma", "Armadura", "Bota", "Anel"]}
            for chave, itemDit in eqBanco.items():
                if itemDit:
                    self.equipamentos[chave] = self.dicionarioParaObjeto(itemDit)

    def dicionarioParaObjeto(self, d):
        return Item(
            nome=d['nome'], dano=d.get('dano', 0), descricao=d['descricao'],
            quantidadeMaxima=d.get('quantidadeMaxima', 1), efeito=d['efeito'],
            preco=d['preco'], raridade=d.get('raridade', 'Comum'), tipo=d['tipo']
        )

    def salvarInventario(self):
        if self.dadosJogador:
            invSalvavel = [self.objetoParaDicionario(i) for i in self.inventario]
            eqSalvavel = {k: self.objetoParaDicionario(v) for k, v in self.equipamentos.items()}
            tabela_jogador.update(
                {
                    'inv': invSalvavel,
                    'equipamentos': eqSalvavel,
                    'vida': self.dadosJogador['vida']
                },
                Query().nome == self.nomeJogador
            )

    def objetoParaDicionario(self, item):
        if not item: return None
        return {
            'nome': item.getNome(), 'dano': item.getDano(), 'descricao': item.getDescricao(),
            'quantidadeMaxima': item.getQuantidadeMaxima(), 'efeito': item.getEfeito(),
            'preco': item.getPreco(), 'raridade': item.getRaridade(), 'tipo': item.getTipo()
        }

    def tratarEventos(self, eventos):
        ponteiroMouse = pygame.mouse.get_pos()
        resultadoFoco = self.obterSlotPorPosicao(ponteiroMouse)
        if resultadoFoco:
            self.tipoSlotSelecionado, self.slotSelecionado = resultadoFoco
        else:
            self.tipoSlotSelecionado, self.slotSelecionado = None, None
        for evento in eventos:
            if evento.type == pygame.MOUSEBUTTONDOWN:
                largura, altura = pygame.display.get_surface().get_size()
                if ponteiroMouse[0] > largura // 2 and ponteiroMouse[1] > altura // 2:
                    if evento.button == 4:  # Scroll para CIMA
                        self.scroll_y = min(0, self.scroll_y + 15)
                    elif evento.button == 5:  # Scroll para BAIXO
                        self.scroll_y -= 15
            if evento.type == pygame.MOUSEBUTTONDOWN and self.slotSelecionado is not None:
                if self.tipoSlotSelecionado == "mochila":
                    idx = self.slotSelecionado
                    if idx < len(self.inventario):
                        item = self.inventario[idx]
                        if evento.button == 1:
                            if item.getTipo() == 'Consumivel':
                                sucesso = item.aplicarEfeitoItem(item, self.dadosJogador)
                                if sucesso:
                                    self.inventario.pop(idx)
                                    self.salvarInventario()
                            else:
                                depara_slots = {
                                    "Capacete": "capacete",
                                    "Colar": "colar",
                                    "Arma": "arma",
                                    "Armadura": "armadura",
                                    "Bota": "bota",
                                    "Anel": "anel"
                                }
                                tipoItem = item.getTipo()
                                if tipoItem in depara_slots:
                                    slotDestino = depara_slots[tipoItem]
                                    itemAntigo = self.equipamentos[slotDestino]
                                    self.equipamentos[slotDestino] = item
                                    if itemAntigo:
                                        self.inventario[idx] = itemAntigo
                                    else:
                                        self.inventario.pop(idx)
                                    self.salvarInventario()
                        elif evento.button == 3:  # Clique Direito: Remove
                            self.inventario.pop(idx)
                            self.salvarInventario()
                elif self.tipoSlotSelecionado == "equipamento":
                    chave = self.slotSelecionado
                    if self.equipamentos[chave] and evento.button == 3:  # Clique direito desequipa
                        if len(self.inventario) < 15:
                            self.inventario.append(self.equipamentos[chave])
                            self.equipamentos[chave] = None
                            self.salvarInventario()
                        else:
                            print("Mochila cheia para desequipar!")

    def obterSlotPorPosicao(self, pos):
        for rect, tipo, identificador in self.slotsRegiao:
            if rect.collidepoint(pos):
                return tipo, identificador
        return None

    def desenhar(self, tela):
        self.slotsRegiao = []
        if self.modo == "padrao":
            self.desenharPaginaInventario(tela)
        elif self.modo == "combate":
            self.desenharPaginaCombate(tela)

    def desenharPaginaInventario(self, tela):
        largura, altura = tela.get_size()

        # Fontes
        fonteTitulo = pygame.font.SysFont("Arial", 16, bold=True)
        fonteDesc = pygame.font.SysFont("Arial", 14)

        # Painel de Equipamentos
        painelEq = pygame.Rect(20, 40, (largura // 2) - 30, altura - 80)
        pygame.draw.rect(tela, (50, 50, 50), painelEq, border_radius=5)
        posicoesEquipamentos = {
            "capacete": (painelEq.centerx - 25, painelEq.y + 40),
            "colar": (painelEq.centerx - 75, painelEq.y + 90),
            "arma": (painelEq.centerx - 100, painelEq.y + 160),
            "armadura": (painelEq.centerx - 25, painelEq.y + 160),
            "bota": (painelEq.centerx - 25, painelEq.y + 280),
            "anel": (painelEq.centerx + 55, painelEq.y + 280)
        }
        for nomeEq, (x, y) in posicoesEquipamentos.items():
            tam = 50 if nomeEq in ["armadura", "bota"] else 40
            rectEq = pygame.Rect(x, y, tam, tam)
            self.slotsRegiao.append((rectEq, "equipamento", nomeEq))
            focado = (self.tipoSlotSelecionado == "equipamento" and self.slotSelecionado == nomeEq)
            corBorda = (200, 200, 200) if focado else (100, 100, 100)
            pygame.draw.rect(tela, corBorda, rectEq, border_radius=3)
            item = self.equipamentos.get(nomeEq)
            if item:
                pygame.draw.rect(tela, (140, 140, 140), rectEq.inflate(-6, -6))
            else:
                txtSlug = fonteDesc.render(nomeEq[:4], True, (80, 80, 80))
                tela.blit(txtSlug, (rectEq.x + 4, rectEq.y + 10))

        # Painel de Itens
        xBlocoItens = (largura // 2) + 10
        painelItens = pygame.Rect(xBlocoItens, 40, (largura // 2) - 30, (altura // 2) + 40)
        pygame.draw.rect(tela, (50, 50, 50), painelItens, border_radius=5)
        colunasGrid = 4
        linhasGrid = 4
        tamSlot = 45
        espaca = 10
        gradeW = (colunasGrid * tamSlot) + ((colunasGrid - 1) * espaca)
        startGridX = painelItens.x + (painelItens.width - gradeW) // 2
        startGridY = painelItens.y + 20
        for l in range(linhasGrid):
            for c in range(colunasGrid):
                idx = (l * colunasGrid) + c
                if idx >= 15: break
                slotX = startGridX + c * (tamSlot + espaca)
                slotY = startGridY + l * (tamSlot + espaca)
                rectSlot = pygame.Rect(slotX, slotY, tamSlot, tamSlot)
                self.slotsRegiao.append((rectSlot, "mochila", idx))
                focado = (self.tipoSlotSelecionado == "mochila" and self.slotSelecionado == idx)
                corBorda = (200, 200, 200) if focado else (90, 90, 90)
                pygame.draw.rect(tela, corBorda, rectSlot, border_radius=4)
                if idx < len(self.inventario):
                    pygame.draw.rect(tela, (160, 160, 160), rectSlot.inflate(-6, -6), border_radius=2)

        # Caixa de descrição
            # Caixa de descrição
            painelDesc = pygame.Rect(xBlocoItens, painelItens.bottom + 15, painelItens.width,altura - painelItens.bottom - 55)
            pygame.draw.rect(tela, (35, 35, 35), painelDesc, border_radius=5)
            itemParaDescrever = None
            if self.tipoSlotSelecionado == "mochila" and self.slotSelecionado < len(self.inventario):
                itemParaDescrever = self.inventario[self.slotSelecionado]
            elif self.tipoSlotSelecionado == "equipamento":
                itemParaDescrever = self.equipamentos.get(self.slotSelecionado)

            if not itemParaDescrever:
                self.scroll_y = 0
            if itemParaDescrever:
                areaRecorte = painelDesc.inflate(-20, -20)
                tela.set_clip(areaRecorte)
                yAtual = areaRecorte.y + self.scroll_y
                txtNome = fonteTitulo.render(itemParaDescrever.getNome(), True, (255, 215, 0))
                tela.blit(txtNome, (areaRecorte.x, yAtual))
                yAtual += 30
                textoCompleto = itemParaDescrever.getDescricao()
                palavras = textoCompleto.split(' ')
                linhaAtual = ""
                larguraMaxima = areaRecorte.width
                for palavra in palavras:
                    testarLinha = linhaAtual + palavra + " "
                    if fonteDesc.size(testarLinha)[0] < larguraMaxima:
                        linhaAtual = testarLinha
                    else:
                        txtLinha = fonteDesc.render(linhaAtual, True, (220, 220, 220))
                        tela.blit(txtLinha, (areaRecorte.x, yAtual))
                        yAtual += 20
                        linhaAtual = palavra + " "
                if linhaAtual:
                    txtLinha = fonteDesc.render(linhaAtual, True, (220, 220, 220))
                    tela.blit(txtLinha, (areaRecorte.x, yAtual))
                    yAtual += 20
                tela.set_clip(None)
                alturaConteudoTotal = yAtual - (areaRecorte.y + self.scroll_y)
                if alturaConteudoTotal > areaRecorte.height:
                    canaletaRect = pygame.Rect(painelDesc.right - 12, painelDesc.y + 10, 6, painelDesc.height - 20)
                    pygame.draw.rect(tela, (20, 20, 20), canaletaRect, border_radius=3)
                    proporcao = areaRecorte.height / alturaConteudoTotal
                    tamBotao = max(20, canaletaRect.height * proporcao)
                    percentualRolagem = -self.scroll_y / (alturaConteudoTotal - areaRecorte.height)
                    percentualRolagem = max(0.0, min(1.0, percentualRolagem))
                    posYBotao = canaletaRect.y + (canaletaRect.height - tamBotao) * percentualRolagem
                    botaoRect = pygame.Rect(canaletaRect.x, posYBotao, canaletaRect.width, tamBotao)
                    pygame.draw.rect(tela, (100, 100, 100), botaoRect, border_radius=3)

    def desenharPaginaCombate(self, tela):
        largura, altura = tela.get_size()
        tamanho = 45
        espacamento = 10
        total_slots = 5
        startX = (largura - (total_slots * tamanho + (total_slots - 1) * espacamento)) // 2
        startY = altura - 80
        fonteCombate = pygame.font.SysFont("Arial", 12, italic=True)
        textoAjuda = fonteCombate.render("[1-5] Atalhos Rápidos de Itens", True, (180, 180, 180))
        tela.blit(textoAjuda, (startX, startY - 20))
        for c in range(total_slots):
            slotX = startX + c * (tamanho + espacamento)
            rectSlot = pygame.Rect(slotX, startY, tamanho, tamanho)
            self.slotsRegiao.append(rectSlot)
            corBorda = (255, 215, 0) if self.slotSelecionado == c else (50, 50,50)
            pygame.draw.rect(tela, corBorda, rectSlot, border_radius=5)
            if c < len(self.inventario):
                pygame.draw.rect(tela, (100, 100, 120), rectSlot.inflate(-6, -6), border_radius=3)