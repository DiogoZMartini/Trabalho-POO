import pygame
from .estado_base import EstadoBase
from entidades.inimigo import Inimigo


class EstadoCombate(EstadoBase):
    def __init__(self, jogador, nomeInimigoAlvo=None):
        super().__init__()
        self.jogador = jogador
        self.inimigo = None
        self.acaoAtiva = None
        self.carregarInimigo(nomeInimigoAlvo)
        if self.jogador and hasattr(self.jogador, 'inv') and self.jogador.inv:
            self.jogador.inv.modo = "combate"

    def carregarInimigo(self, carregarInimigo=None):
        lvlJogador = self.jogador.getLvl()
        self.inimigo = Inimigo.gerarInimigoAleatorio(lvlJogador)
        self.jogador.inimigoFoco = {
            'nome': self.inimigo.getNome(),
            'vida': self.inimigo.getVida(),
            'vidaMaxima': self.inimigo.getVidaMaxima(),
            'lvl': self.inimigo.getLvl()
        }

    def abrir(self):
        super().abrir()
        if self.jogador.inv:
            self.jogador.inv.modo = "combate"

    def fechar(self):
        if self.jogador.inv:
            self.jogador.inv.modo = "padrao"
        super().fechar()

    def tratarEventos(self, eventos):
        if self.jogador.inv:
            self.jogador.inv.tratarEventos(eventos)

        for evento in eventos:
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    self.proximoEstado = "Teste"
                    self.concluido = True
            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                mousePos = pygame.mouse.get_pos()
                slotFocado = self.jogador.inv.obterSlotPorPosicao(mousePos)
                if slotFocado and slotFocado[0] == "botaoCombate":
                    acao = slotFocado[1]
                    self.executarAcaoCombate(acao)

    def executarAcaoCombate(self, acao):
        acao = acao.upper()
        self.acaoAtiva = None
        danoTotal = self.jogador.getDano()
        equipamentos = self.jogador.inv.equipamentos
        slotsDeAtaque = ["Arma", "Colar", "Anel"]
        danoDosItens = 0
        for slot in slotsDeAtaque:
            itemEquipado = equipamentos.get(slot)
            if itemEquipado:
                danoDoItem = itemEquipado.getDano()
                danoDosItens += danoDoItem
        danoFinal = danoTotal + danoDosItens
        match acao:
            case "ATAQUE":
                self.inimigo.tomarDano(danoFinal)
                print(f"Você atacou causando {danoFinal} de dano!")
                if self.jogador.getSpaEnergia() < 5:
                    self.jogador.setSpaEnergia(self.jogador.getSpaEnergia() + 1)
                if self.inimigo.getVida() <= 0:
                    print(f"Vitória! {self.inimigo.getNome()} foi derrotado!")
                self.turnoInimigo()
            case "HABILIDADE":
                if self.jogador.getSpaEnergia() == 5:
                    danoEspecial = danoFinal * 2
                    self.inimigo.tomarDano(danoEspecial)
                    self.jogador.setSpaEnergia(0)
                    print(f"Você atacou causando {danoEspecial} de dano!")
                    self.turnoInimigo()
                else:
                    self.acaoAtiva = "erro_especial"
            case "ITENS":
                print("\n[INVENTÁRIO] Abrindo bolsa de consumíveis no combate...")
                # Aqui vai a lógica para abrir o mini-menu de poções ou bombinhas
                self.turnoInimigo()
            case "FUGIR":
                print("\n[FUGA] Você tenta escapar da batalha!")
                # Aqui vai a lógica de sorteio de fuga (ex: random.random() > 0.5)
            case _:
                print(f"Aviso: Ação desconhecida recebida no combate: {acao}")

    def turnoInimigo(self):
        if self.inimigo.getVida() <= 0:
            return
        danoDoMonstro = self.inimigo.getDano()
        if self.inimigo.getSpaEnergia() == 5:
            danoEspecial = danoDoMonstro * 2
            self.jogador.tomarDano(danoEspecial)
            self.inimigo.setSpaEnergia(0)
        else:
            self.jogador.tomarDano(danoDoMonstro)
            if self.inimigo.getSpaEnergia() < 5:
                self.inimigo.setSpaEnergia(self.inimigo.getSpaEnergia() + 1)


    def atualizar(self, dt):
        pass

    def desenhar(self, tela):
        larguraTela, alturaTela = tela.get_size()
        tela.fill((30, 30, 30))

        # Fontes e Cores Base

        fonteGrande = pygame.font.SysFont("Arial", 22, bold=True)
        fonteMedia = pygame.font.SysFont("Arial", 16, bold=True)
        fontePequena = pygame.font.SysFont("Arial", 14)
        corBorda = (255, 255, 255)
        corFundoHud = (50, 50, 50)


        # 1. Hud Jogador (Topo Esquerdo)

        rectHudJogador = pygame.Rect(10, 10, 320, 85)
        pygame.draw.rect(tela, corFundoHud, rectHudJogador, border_radius=5)
        pygame.draw.rect(tela, corBorda, rectHudJogador, 2, border_radius=5)
        nomeTexto = fonteMedia.render(f"{self.jogador.getNome()} - Lv.{self.jogador.getLvl()}", True, (255, 215, 0))
        tela.blit(nomeTexto, (rectHudJogador.x + 10, rectHudJogador.y + 5))
        dinheiroTexto = fontePequena.render(f"Dinheiro: R$ {self.jogador.getDinheiro()}", True, (255, 255, 255))
        tela.blit(dinheiroTexto, (rectHudJogador.x + 200, rectHudJogador.y + 5))

        # Barra de Vida do Jogador

        vidaAtualJogador = self.jogador.getVida()
        vidaMaximaJogador = self.jogador.getVidaMaxima()
        proporcaoVidaJogador = max(0.0, min(1.0, vidaAtualJogador / vidaMaximaJogador))
        pygame.draw.rect(tela, (100, 0, 0),(rectHudJogador.x + 10, rectHudJogador.y + 30, 300, 15))  # Fundo Vermelho Escuro
        pygame.draw.rect(tela, (0, 200, 80),(rectHudJogador.x + 10, rectHudJogador.y + 30, 300 * proporcaoVidaJogador, 15))  # Vida Verde

        # Barra de Especial do Jogador

        posicaoSpaJogador = (rectHudJogador.x + 10, rectHudJogador.y + 50, 200, 10)
        pygame.draw.rect(tela, (80, 80, 0), posicaoSpaJogador)
        pygame.draw.rect(tela, (255, 215, 0), (posicaoSpaJogador[0], posicaoSpaJogador[1],posicaoSpaJogador[2] * max(0.0,min(1.0, self.jogador.getSpaEnergia() / 5)),posicaoSpaJogador[3]))

        # Barra de Xp do Jogador

        xpAtual = self.jogador.getExp()
        xpNecessario = self.jogador.getLvl() * 100
        proporcaoXp = min(1.0, xpAtual / xpNecessario)
        pygame.draw.rect(tela, (40, 40, 40), (rectHudJogador.x + 10, rectHudJogador.y + 55, 300, 8))
        pygame.draw.rect(tela, (0, 150, 255), (rectHudJogador.x + 10, rectHudJogador.y + 55, 300 * proporcaoXp, 8))

        # 2. Hud Inimigo (Topo Direito)

        rectHudInimigo = pygame.Rect(larguraTela - 330, 10, 320, 60)
        pygame.draw.rect(tela, corFundoHud, rectHudInimigo, border_radius=5)
        pygame.draw.rect(tela, corBorda, rectHudInimigo, 2, border_radius=5)
        nomeInimigoTxt = fonteMedia.render(f"{self.inimigo.getNome()} - Lv.{self.inimigo.getLvl()}", True,(220, 50, 50))
        tela.blit(nomeInimigoTxt, (rectHudInimigo.x + 10, rectHudInimigo.y + 5))

        # Barra de Vida Inimigo
        vidaAtualInimigo = self.inimigo.getVida()
        vidaMaximaInimigo = self.inimigo.getVidaMaxima()
        proporcaoVidaInimigo = max(0.0, min(1.0, vidaAtualInimigo / vidaMaximaInimigo))
        pygame.draw.rect(tela, (100, 0, 0),(rectHudInimigo.x + 10, rectHudInimigo.y + 30, 300, 15))
        pygame.draw.rect(tela, (200, 30, 30), (rectHudInimigo.x + 10, rectHudInimigo.y + 30, 300 * proporcaoVidaInimigo,15))

        # Barra de Especial do Inimigo

        posicaoSpaInimigo = (rectHudInimigo.x + 10, rectHudInimigo.y + 50, 300, 10)
        pygame.draw.rect(tela, (80, 80, 0), posicaoSpaInimigo)
        pygame.draw.rect(tela, (255, 215, 0), (posicaoSpaInimigo[0], posicaoSpaInimigo[1],posicaoSpaInimigo[2] * max(0.0,min(1.0, self.inimigo.getSpaEnergia() / 5)),posicaoSpaInimigo[3]))

        # Bonecos
        rectBonecoJogador = pygame.Rect(50, 120, 250, 300)
        pygame.draw.rect(tela, (70, 70, 70), rectBonecoJogador, border_radius=10)
        pygame.draw.rect(tela, corBorda, rectBonecoJogador, 2, border_radius=10)
        txtBonecoJog = fonteMedia.render("Boneco Jogador", True, (150, 150, 150))
        tela.blit(txtBonecoJog, (rectBonecoJogador.centerx - txtBonecoJog.get_width() // 2, rectBonecoJogador.centery))
        rectBonecoInimigo = pygame.Rect(larguraTela - 300, 120, 250, 300)
        pygame.draw.rect(tela, (70, 70, 70), rectBonecoInimigo, border_radius=10)
        pygame.draw.rect(tela, corBorda, rectBonecoInimigo, 2, border_radius=10)
        txtBonecoInim = fonteMedia.render("Boneco Inimigo", True, (150, 150, 150))
        tela.blit(txtBonecoInim,(rectBonecoInimigo.centerx - txtBonecoInim.get_width() // 2, rectBonecoInimigo.centery))

        # Painéis inferiores
        alturaPainelInferior = 150
        rectPainelDescricao = pygame.Rect(0, alturaTela - alturaPainelInferior, larguraTela // 2, alturaPainelInferior)
        rectPainelAcoes = pygame.Rect(larguraTela // 2, alturaTela - alturaPainelInferior, larguraTela // 2,alturaPainelInferior)
        pygame.draw.rect(tela, (35, 35, 35), rectPainelDescricao)
        pygame.draw.rect(tela, (45, 45, 45), rectPainelAcoes)
        pygame.draw.rect(tela, corBorda, rectPainelDescricao, 3)
        pygame.draw.rect(tela, corBorda, rectPainelAcoes, 3)
        opcoesMenu = [
            {"nome": "ATAQUE", "id": "ataque"},
            {"nome": "ITEM", "id": "item"},
            {"nome": "HABILIDADE", "id": "habilidade"},
            {"nome": "FUGIR", "id": "fugir"}
        ]
        posicaoMouse = pygame.mouse.get_pos()
        acaoFocada = None
        self.jogador.inv.slotsRegiao = []
        for i, opcao in enumerate(opcoesMenu):
            coluna = i % 2
            linha = i // 2
            xBotao = rectPainelAcoes.x + 40 + (coluna * 180)
            yBotao = rectPainelAcoes.y + 30 + (linha * 50)
            rectBotao = pygame.Rect(xBotao, yBotao, 150, 35)
            self.jogador.inv.slotsRegiao.append((rectBotao, "botaoCombate", opcao["id"]))
            corTexto = (255, 255, 255)
            if rectBotao.collidepoint(posicaoMouse):
                acaoFocada = opcao["id"]
                corTexto = (255, 215, 0)
                if self.acaoAtiva == "erroEspecial" and acaoFocada != "habilidade":
                    self.acaoAtiva = None
                pygame.draw.polygon(tela, corTexto, [
                    (xBotao - 15, yBotao + 10),
                    (xBotao - 15, yBotao + 25),
                    (xBotao - 5, yBotao + 17)
                ])
            txtOpcao = fonteGrande.render(opcao["nome"], True, corTexto)
            tela.blit(txtOpcao, (xBotao, yBotao))
        acaoFinalParaRenderizar = self.acaoAtiva if self.acaoAtiva else acaoFocada
        self.renderizarDescricao(tela, rectPainelDescricao, acaoFinalParaRenderizar, fonteMedia, fontePequena)

    def renderizarDescricao(self, tela, rect, acao, fonteTitulo, fonteCorpo, corTexto=(200, 200, 200)):
        margem = 20
        titulo = "Menu de Combate"
        corpo = "Passe o mouse sobre uma opção para ver os detalhes."
        match acao:
            case "ataque":
                titulo = "Ação: Ataque Físico"
                corpo = "Ataca o inimigo com sua arma principal causando dano baseado em sua força."
            case "item":
                titulo = "Ação: Usar Item"
                corpo = "Abre sua mochila para utilizar poções de cura ou itens de suporte."
            case "habilidade":
                titulo = "Ação: Habilidade Especial"
                corpo = f"Gasta seus pontos de {self.jogador.getClasse()} para realizar um golpe devastador."
            case "fugir":
                titulo = "Ação: Escapar"
                corpo = "Tenta fugir da batalha. Sucesso baseado na diferença de nível e sorte."
            case "erroEspecial":
                titulo = "Aviso: Especial Bloqueado"
                corpo = "Você precisa ter a barra de especial cheia para utilizar a habilidade"
                corTexto = (255, 0, 0)
            case _:
                pass
        txtTit = fonteTitulo.render(titulo, True, (255, 215, 0))
        tela.blit(txtTit, (rect.x + margem, rect.y + margem))
        palavras = corpo.split(' ')
        linhaAtual = ""
        yOffset = margem + 30
        for palavra in palavras:
            if fonteCorpo.size(linhaAtual + palavra)[0] < rect.width - (margem * 2):
                linhaAtual += palavra + " "
            else:
                tela.blit(fonteCorpo.render(linhaAtual, True, corTexto), (rect.x + margem, rect.y + yOffset))
                yOffset += 20
                linhaAtual = palavra + " "
        tela.blit(fonteCorpo.render(linhaAtual, True, corTexto), (rect.x + margem, rect.y + yOffset))
