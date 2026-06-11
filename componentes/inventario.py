import pygame
from banco import tabela_jogador
from utilidade.itens import Item
from tinydb import Query

class Inventario:
    def __init__(self, jogador, modo):
        self.jogadorObjeto = jogador
        self.nomeJogador = jogador.getNome()
        self.modo = modo
        self.slotSelecionado = None
        self.tipoSlotSelecionado = None
        self.mochila = []
        self.equipamentos = {}
        self.dadosJogador = None
        self.slotsRegiao = []
        self.scroll_y = 0
        self.carregarInventario()

    def carregarInventario(self):
        resultado = tabela_jogador.search(Query().nome == self.nomeJogador)
        if resultado:
            dados_brutos = resultado[0]
            self.dadosJogador = dados_brutos
            itensBanco = dados_brutos.get('inv', [])
            self.mochila = []
            for itemDit in itensBanco:
                if itemDit:
                    self.mochila.append(self.dicionarioParaObjeto(itemDit))
            eqBanco = dados_brutos.get('equipamentos', {})
            self.equipamentos = {k: None for k in ["Capacete", "Colar", "Arma", "Armadura", "Bota", "Anel"]}
            for chave, itemDit in eqBanco.items():
                if itemDit:
                    self.equipamentos[chave] = self.dicionarioParaObjeto(itemDit)
            self.jogadorObjeto.setInv(self.mochila)

    def dicionarioParaObjeto(self, d):
        return Item(
            nome=d['nome'],
            dano=int(d.get('dano', 0)),
            descricao=d['descricao'],
            quantidadeMaxima=d.get('quantidadeMaxima', 1),
            efeito=d['efeito'],
            preco=d['preco'],
            raridade=d.get('raridade', 'Comum'),
            tipo=d['tipo'],
            img=d.get('img', None),
            uso=d.get('uso', None)
        )

    def salvarInventario(self):
        if self.dadosJogador:
            invSalvavel = [self.objetoParaDicionario(i) for i in self.mochila]
            eqSalvavel = {k: self.objetoParaDicionario(v) for k, v in self.equipamentos.items()}
            tabela_jogador.update(
                {
                    'inv': invSalvavel,
                    'equipamentos': eqSalvavel,
                    'vida': self.jogadorObjeto.getVida()
                },
                Query().nome == self.nomeJogador
            )

    def objetoParaDicionario(self, item):
        if not item: return None
        return {
            'nome': item.getNome(),
            'dano': item.getDano(),
            'descricao': item.getDescricao(),
            'quantidadeMaxima': item.getQuantidadeMaxima(),
            'efeito': item.getEfeito(),
            'preco': item.getPreco(),
            'raridade': item.getRaridade(),
            'tipo': item.getTipo(),
            'img': getattr(item, 'img', None),
            'uso': getattr(item, 'uso', None)
        }

    def tratarEventos(self, eventos):
        from entidades.jogador import Jogador
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
                    if idx < len(self.mochila):
                        item = self.mochila[idx]
                        if evento.button == 1: # Clique Esquerdo: Usar / Equipar
                            if item.getTipo() == 'Consumivel':
                                sucesso = item.aplicarEfeitoItem(self.dadosJogador)
                                if sucesso:
                                    self.jogadorObjeto.setVida(self.dadosJogador['vida'])
                                    self.mochila.pop(idx)
                                    self.salvarInventario()
                            else:
                                depara_slots = {
                                    "Capacete": "Capacete",
                                    "Colar": "Colar",
                                    "Arma": "Arma",
                                    "Armadura": "Armadura",
                                    "Bota": "Bota",
                                    "Anel": "Anel"
                                }
                                tipoItem = item.getTipo()
                                if tipoItem in depara_slots:
                                    slotDestino = depara_slots[tipoItem]
                                    itemAntigo = self.equipamentos[slotDestino]
                                    self.equipamentos[slotDestino] = item
                                    if itemAntigo:
                                        self.mochila[idx] = itemAntigo
                                    else:
                                        self.mochila.pop(idx)
                                    self.salvarInventario()
                        elif evento.button == 3:  # Clique Direito: Remove
                            self.mochila.pop(idx)
                            self.salvarInventario()
                elif self.tipoSlotSelecionado == "equipamento":
                    chave = self.slotSelecionado
                    if self.equipamentos[chave] and evento.button == 3:  # Clique direito desequipa
                        if len(self.mochila) < 15:
                            self.mochila.append(self.equipamentos[chave])
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
        fonteUso = pygame.font.SysFont("Arial", 13, bold=True, italic=True)

        # Painel de Equipamentos
        painelEq = pygame.Rect(20, 40, (largura // 2) - 30, altura - 80)
        pygame.draw.rect(tela, (50, 50, 50), painelEq, border_radius=5)
        posicoesEquipamentos = {
            "Capacete": (painelEq.centerx - 25, painelEq.y + 40),
            "Colar": (painelEq.centerx - 75, painelEq.y + 90),
            "Arma": (painelEq.centerx - 100, painelEq.y + 160),
            "Armadura": (painelEq.centerx - 25, painelEq.y + 160),
            "Bota": (painelEq.centerx - 25, painelEq.y + 280),
            "Anel": (painelEq.centerx + 55, painelEq.y + 280)
        }
        for nomeEq, (x, y) in posicoesEquipamentos.items():
            tam = 50 if nomeEq in ["Armadura", "Bota"] else 40
            rectEq = pygame.Rect(x, y, tam, tam)
            self.slotsRegiao.append((rectEq, "equipamento", nomeEq))
            focado = (self.tipoSlotSelecionado == "equipamento" and self.slotSelecionado == nomeEq)
            corBorda = (200, 200, 200) if focado else (100, 100, 100)
            pygame.draw.rect(tela, corBorda, rectEq, border_radius=3)
            item = self.equipamentos.get(nomeEq)
            if item:
                if hasattr(item, 'img') and item.img:
                    try:
                        imgSurface = pygame.image.load(item.img).convert_alpha()
                        areaInterna = rectEq.inflate(-8, -8)
                        imgRedimensionada = pygame.transform.scale(imgSurface, (areaInterna.width, areaInterna.height))
                        tela.set_clip(areaInterna)
                        tela.blit(imgRedimensionada, (areaInterna.x, areaInterna.y))
                        tela.set_clip(None)
                    except:
                        pygame.draw.rect(tela, (140, 140, 140), rectEq.inflate(-6, -6))
                else:
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
                if idx < len(self.mochila):
                    itemMochila = self.mochila[idx]
                    if hasattr(itemMochila, 'img') and itemMochila.img:
                        try:
                            imgSurface = pygame.image.load(itemMochila.img).convert_alpha()
                            areaInternaMochila = rectSlot.inflate(-8, -8)
                            imgRedimensionada = pygame.transform.scale(imgSurface, (areaInternaMochila.width,areaInternaMochila.height))
                            tela.set_clip(areaInternaMochila)
                            tela.blit(imgRedimensionada, (areaInternaMochila.x, areaInternaMochila.y))
                            tela.set_clip(None)
                        except:
                            pygame.draw.rect(tela, (160, 160, 160), rectSlot.inflate(-6, -6), border_radius=2)
                    else:
                        pygame.draw.rect(tela, (160, 160, 160), rectSlot.inflate(-6, -6), border_radius=2)

        # Caixa de descrição
        painelDesc = pygame.Rect(xBlocoItens, painelItens.bottom + 15, painelItens.width,altura - painelItens.bottom - 55)
        pygame.draw.rect(tela, (35, 35, 35), painelDesc, border_radius=5)
        itemParaDescrever = None
        if self.tipoSlotSelecionado == "mochila" and self.slotSelecionado < len(self.mochila):
            itemParaDescrever = self.mochila[self.slotSelecionado]
        elif self.tipoSlotSelecionado == "equipamento":
            itemParaDescrever = self.equipamentos.get(self.slotSelecionado)
        if not itemParaDescrever:
            self.scroll_y = 0
        if itemParaDescrever:
            areaRecorte = painelDesc.inflate(-20, -20)
            tela.set_clip(areaRecorte)
            yAtual = areaRecorte.y + self.scroll_y

            # 1. Desenha o Nome do Item
            txtNome = fonteTitulo.render(itemParaDescrever.getNome(), True, (255, 215, 0))
            tela.blit(txtNome, (areaRecorte.x, yAtual))
            yAtual += 30

            # 2. Processa e desenha a Descrição Padrão (com quebra de linha automática)
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
                yAtual += 25

            # 3. Processa e desenha a seção de "Uso" se ela existir no item
            if hasattr(itemParaDescrever, 'uso') and itemParaDescrever.uso:
                textoUso = f"Efeito: {itemParaDescrever.uso}"
                palavrasUso = textoUso.split(' ')
                linhaUso = ""
                for pal in palavrasUso:
                    testarLinhaUso = linhaUso + pal + " "
                    if fonteUso.size(testarLinhaUso)[0] < larguraMaxima:
                        linhaUso = testarLinhaUso
                    else:
                        txtLinhaUso = fonteUso.render(linhaUso, True, (0, 230, 150))  # Cor verde/ciano para destaque
                        tela.blit(txtLinhaUso, (areaRecorte.x, yAtual))
                        yAtual += 18
                        linhaUso = pal + " "
                if linhaUso:
                    txtLinhaUso = fonteUso.render(linhaUso, True, (0, 230, 150))
                    tela.blit(txtLinhaUso, (areaRecorte.x, yAtual))
                    yAtual += 18
            tela.set_clip(None)
            alturaConteudoTotal = yAtual - (areaRecorte.y + self.scroll_y)

            # Barra de rolagem dinâmica ajustada para englobar a descrição + o uso
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
        pass