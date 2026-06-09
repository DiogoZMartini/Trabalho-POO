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
                                sucesso = item.aplicarEfeitoItem(item, self.jogadorObjeto)
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

            # ALTERADO: 3. Processa e desenha a seção de "Uso" se ela existir no item
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
        largura, altura = tela.get_size()
        self.slotsRegiao = []

        # Fontes de renderização
        fonteInfo = pygame.font.SysFont("Arial", 14, bold=True)
        fonteTexto = pygame.font.SysFont("Arial", 16)
        fonteDestaque = pygame.font.SysFont("Arial", 14, bold=True, italic=True)

        # 1. DEFINIÇÃO DAS CORES E GEOMETRIA PRINCIPAL
        corBorda = (0, 0, 0)
        corFundoAbas = (50, 50, 50)
        corFundoDesc = (35, 35, 35)
        alturaHUD = 50
        alturaGradeCombate = altura - 120

        # Dados simulados do Inimigo
        nomeInimigo = "Zumbie"
        vidaInimigo, vidaMaxInimigo = 30, 30
        lvlInimigo = 5

        # ALTERADO: Coleta de dados usando os Métodos Getters da sua Classe Jogador
        if hasattr(self, 'jogadorObjeto') and self.jogadorObjeto:
            nomeJogador = self.jogadorObjeto.getNome()
            vidaJogador = self.jogadorObjeto.getVida()
            lvlJogador = self.jogadorObjeto.getLvl()
            dinheiroJogador = self.jogadorObjeto.getDinheiro()
            expAtual = self.jogadorObjeto.getExp()
            # Vida máxima pode vir de um atributo estático ou do dicionário base seguro
            vidaMaxJogador = self.dadosJogador.get('vidaMaxima', 100) if self.dadosJogador else 100
        else:
            # Fallback de segurança caso o objeto não tenha sido inicializado
            nomeJogador = "Herói"
            vidaJogador = 100
            vidaMaxJogador = 100
            lvlJogador = 1
            dinheiroJogador = 0
            expAtual = 0

        # 2. RENDERIZAR PARTE SUPERIOR: HUDs E ÁREA DOS BONECOS

        # Borda externa do template geral
        pygame.draw.rect(tela, corBorda, (0, 0, largura, altura), 4)

        # HUD Jogador
        hudJogadorRect = pygame.Rect(10, 10, 250, 65)
        pygame.draw.rect(tela, corFundoAbas, hudJogadorRect, border_radius=4)
        pygame.draw.rect(tela, corBorda, hudJogadorRect, 2, border_radius=4)
        txtJog = fonteInfo.render(f"{nomeJogador} - Lv.{lvlJogador} | R$ {dinheiroJogador}", True, (255, 255, 255))
        tela.blit(txtJog, (hudJogadorRect.x + 8, hudJogadorRect.y + 4))

        # Barra de Vida Jogador
        pygame.draw.rect(tela, (100, 0, 0), (hudJogadorRect.x + 8, hudJogadorRect.y + 22, 234, 12))
        larguraBarraJog = int(234 * (vidaJogador / vidaMaxJogador))
        pygame.draw.rect(tela, (0, 200, 80), (hudJogadorRect.x + 8, hudJogadorRect.y + 22, larguraBarraJog, 12))

        # Cálculo dinâmico do XP baseado no getter
        expNecessaria = 100 * lvlJogador

        # Barra de XP desenhada
        pygame.draw.rect(tela, (40, 40, 40), (hudJogadorRect.x + 8, hudJogadorRect.y + 38, 234, 8))
        larguraBarraXp = int(234 * min(1.0, (expAtual / max(1, expNecessaria))))
        pygame.draw.rect(tela, (0, 150, 255), (hudJogadorRect.x + 8, hudJogadorRect.y + 38, larguraBarraXp, 8))

        # Texto do EXP desenhado
        txtXp = pygame.font.SysFont("Arial", 10, bold=True).render(f"EXP: {expAtual}/{expNecessaria}", True,
                                                                   (180, 180, 180))
        tela.blit(txtXp, (hudJogadorRect.x + 8, hudJogadorRect.y + 48))

        # HUD Inimigo (Superior Direito)
        hudInimigoRect = pygame.Rect(largura - 260, 10, 250, alturaHUD)
        pygame.draw.rect(tela, corFundoAbas, hudInimigoRect, border_radius=4)
        pygame.draw.rect(tela, corBorda, hudInimigoRect, 2, border_radius=4)
        txtInim = fonteInfo.render(f"{nomeInimigo} - Lv.{lvlInimigo}", True, (255, 255, 255))
        tela.blit(txtInim, (hudInimigoRect.x + 8, hudInimigoRect.y + 6))

        # Barra de Vida Inimigo
        pygame.draw.rect(tela, (100, 0, 0), (hudInimigoRect.x + 8, hudInimigoRect.y + 26, 234, 14))
        larguraBarraInim = int(234 * (vidaInimigo / vidaMaxInimigo))
        pygame.draw.rect(tela, (220, 50, 50), (hudInimigoRect.x + 8, hudInimigoRect.y + 26, larguraBarraInim, 14))

        # Box Boneco Jogador (Esquerda)
        bonecoJogadorRect = pygame.Rect(10, 70, 200, 200)
        pygame.draw.rect(tela, (70, 70, 70), bonecoJogadorRect, border_radius=4)
        pygame.draw.rect(tela, corBorda, bonecoJogadorRect, 2, border_radius=4)
        txtBoxJog = fonteTexto.render("Boneco Jogador", True, (200, 200, 200))
        tela.blit(txtBoxJog, (bonecoJogadorRect.centerx - txtBoxJog.get_width() // 2, bonecoJogadorRect.centery - 10))

        # Box Boneco Inimigo (Direita)
        bonecoInimigoRect = pygame.Rect(largura - 210, 70, 200, 200)
        pygame.draw.rect(tela, (70, 70, 70), bonecoInimigoRect, border_radius=4)
        pygame.draw.rect(tela, corBorda, bonecoInimigoRect, 2, border_radius=4)
        txtBoxInim = fonteTexto.render("Boneco Inimigo", True, (200, 200, 200))
        tela.blit(txtBoxInim, (bonecoInimigoRect.centerx - txtBoxInim.get_width() // 2, bonecoInimigoRect.centery - 10))

        # 3. RENDERIZAR REGIAO INFERIOR: MENU DE AÇÕES & DESCRIÇÕES
        pygame.draw.line(tela, corBorda, (0, alturaGradeCombate), (largura, alturaGradeCombate), 4)
        larguraMetade = largura // 2
        rectDescricao = pygame.Rect(0, alturaGradeCombate, larguraMetade, altura - alturaGradeCombate)
        rectAcoes = pygame.Rect(larguraMetade, alturaGradeCombate, larguraMetade, altura - alturaGradeCombate)
        pygame.draw.rect(tela, corFundoDesc, rectDescricao)
        pygame.draw.rect(tela, corFundoAbas, rectAcoes)
        pygame.draw.line(tela, corBorda, (larguraMetade, alturaGradeCombate), (larguraMetade, altura), 4)

        opcoesMenu = [
            {"nome": "ATAQUE", "id": "ataque"},
            {"nome": "ITEM", "id": "item"},
            {"nome": "HABILIDADE", "id": "habilidade"},
            {"nome": "FUGIR", "id": "fugir"}
        ]
        startX = rectAcoes.x + 30
        startY = rectAcoes.y + 25
        espacamentoX = 160
        espacamentoY = 40
        mousePos = pygame.mouse.get_pos()
        acaoFocada = None

        for i, opcao in enumerate(opcoesMenu):
            coluna = i % 2
            linha = i // 2
            posX = startX + (coluna * espacamentoX)
            posY = startY + (linha * espacamentoY)
            rectOpcao = pygame.Rect(posX, posY, 140, 30)
            self.slotsRegiao.append((rectOpcao, "botao_combate", opcao["id"]))
            if rectOpcao.collidepoint(mousePos):
                acaoFocada = opcao["id"]
                ponto1 = (posX - 15, posY + 6)
                ponto2 = (posX - 15, posY + 18)
                ponto3 = (posX - 5, posY + 12)
                pygame.draw.polygon(tela, (255, 255, 255), [ponto1, ponto2, ponto3])
            corTextoBotao = (255, 215, 0) if acaoFocada == opcao["id"] else (240, 240, 240)
            txtOpcao = fonteTexto.render(opcao["nome"], True, corTextoBotao)
            tela.blit(txtOpcao, (posX, posY))

        # 4. EXIBIÇÃO DINÂMICA DA DESCRIÇÃO (PAINEL INFERIOR ESQUERDO)
        tituloDesc = "Menu de Combate"
        corpoDesc = "Escolha uma ação para iniciar seu turno."
        efeitoDesc = ""

        if acaoFocada == "ataque":
            tituloDesc = "Ação: Realizar Ataque"
            corpoDesc = "Usa sua arma equipada para golpear diretamente a criatura inimiga."
            armaEquipada = self.equipamentos.get("Arma")

            # Soma o dano base do Objeto Jogador com o modificador da arma ativa
            danoBase = self.jogadorObjeto.getDano() if hasattr(self, 'jogadorObjeto') else 5
            danoArma = armaEquipada.getDano() if armaEquipada else 0
            efeitoDesc = f"Dano Estimado: {danoBase + danoArma} PTs"

        elif acaoFocada == "item":
            tituloDesc = "Ação: Abrir Mochila"
            corpoDesc = "Acessa seus consumíveis rápidos de recuperação, buffs ou arremessáveis."
            # Usa a lista do objeto via getter
            tamanhoInv = len(self.jogadorObjeto.getInv()) if hasattr(self, 'jogadorObjeto') else len(self.mochila)
            efeitoDesc = f"Itens carregados no inventário: {tamanhoInv}/15"

        elif acaoFocada == "habilidade":
            tituloDesc = "Ação: Habilidades Especiais"
            corpoDesc = f"Gasta pontos do seu recurso ativo de {self.jogadorObjeto.getClasse() if hasattr(self, 'jogadorObjeto') else 'Classe'}."
            efeitoDesc = f"Recurso Disponível: {self.jogadorObjeto.getRecurso() if hasattr(self, 'jogadorObjeto') else 0} Pts"

        elif acaoFocada == "fugir":
            tituloDesc = "Ação: Retirada"
            corpoDesc = "Tenta escapar da batalha atual e retornar ao mapa de exploração seguro."
            efeitoDesc = "Chance de sucesso baseada na sua Velocidade."

        txtTit = fonteInfo.render(tituloDesc, True, (255, 215, 0))
        tela.blit(txtTit, (rectDescricao.x + 20, rectDescricao.y + 15))
        palavras = corpoDesc.split(' ')
        linhaLog = ""
        yLinha = rectDescricao.y + 40
        for pal in palavras:
            if fonteTexto.size(linhaLog + pal + " ")[0] < rectDescricao.width - 40:
                linhaLog += pal + " "
            else:
                tela.blit(fonteTexto.render(linhaLog, True, (220, 220, 220)), (rectDescricao.x + 20, yLinha))
                yLinha += 20
                linhaLog = pal + " "
        if linhaLog:
            tela.blit(fonteTexto.render(linhaLog, True, (220, 220, 220)), (rectDescricao.x + 20, yLinha))
            yLinha += 22
        if efeitoDesc:
            txtEf = fonteDestaque.render(efeitoDesc, True, (0, 230, 150))
            tela.blit(txtEf, (rectDescricao.x + 20, yLinha))