import pygame
import random
from .estado_base import EstadoBase
from entidades.inimigo import Inimigo


class EstadoCombate(EstadoBase):
    def __init__(self, jogador, nomeInimigoAlvo=None):
        super().__init__()
        self.jogador = jogador
        self.inimigo = None  # Armazena o objeto da classe Inimigo
        self.carregarInimigo(nomeInimigoAlvo)  # Corrigido: Passando o argumento
        if self.jogador and hasattr(self.jogador, 'inv') and self.jogador.inv:
            self.jogador.inv.modo = "combate"

    def carregarInimigo(self, carregarInimigo=None):  # Corrigido: Aceitando o argumento
        lvlJogador = self.jogador.getLvl()
        self.inimigo = Inimigo.gerarInimigoAleatorio(lvlJogador)

        # Sincroniza o dicionário de foco do jogador para leitura externa se necessário
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
                # Corrigido: ID agora bate com o que foi registrado no desenhar
                if slotFocado and slotFocado[0] == "botaoCombate":
                    acao = slotFocado[1]
                    self.executarAcaoCombate(acao)

    def executarAcaoCombate(self, acao):
        acao = acao.upper()
        match acao:
            case "ATAQUE":
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
                self.inimigo.tomarDano(danoFinal)
                print(f"Você atacou causando {danoFinal} de dano!")
                if self.jogador.getSpaEnergia() < 5:
                    self.jogador.setSpaEnergia(self.jogador.getSpaEnergia() + 1)

                if self.inimigo.getVida() <= 0:
                    print(f"Vitória! {self.inimigo.getNome()} foi derrotado!")

            case "ESPECIAL":
                print(f"\n[ESPECIAL] Você conjurou sua habilidade: {self.jogador.getSpa()}!")
                # Aqui vai a lógica do ataque especial (ex: gasta recurso e dá mais dano)

            case "ITENS":
                print("\n[INVENTÁRIO] Abrindo bolsa de consumíveis no combate...")
                # Aqui vai a lógica para abrir o mini-menu de poções ou bombinhas

            case "FUGIR":
                print("\n[FUGA] Você tenta escapar da batalha!")
                # Aqui vai a lógica de sorteio de fuga (ex: random.random() > 0.5)

            case _:
                # O 'case _' funciona como o 'default' do switch-case tradicional
                print(f"Aviso: Ação desconhecida recebida no combate: {acao}")

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


        # 1. HUD JOGADOR (Topo Esquerdo)

        rectHudJogador = pygame.Rect(10, 10, 320, 85)
        pygame.draw.rect(tela, corFundoHud, rectHudJogador, border_radius=5)
        pygame.draw.rect(tela, corBorda, rectHudJogador, 2, border_radius=5)
        nomeTexto = fonteMedia.render(f"{self.jogador.getNome()} - Lv.{self.jogador.getLvl()}", True, (255, 215, 0))
        tela.blit(nomeTexto, (rectHudJogador.x + 10, rectHudJogador.y + 5))
        dinheiroTexto = fontePequena.render(f"Dinheiro: R$ {self.jogador.getDinheiro()}", True, (255, 255, 255))
        tela.blit(dinheiroTexto, (rectHudJogador.x + 200, rectHudJogador.y + 5))

        # NOVA BARRA DE VIDA DO JOGADOR

        vidaAtualJogador = self.jogador.getVida()
        vidaMaximaJogador = self.jogador.getVidaMaxima()
        proporcaoVidaJogador = max(0.0, min(1.0, vidaAtualJogador / vidaMaximaJogador))
        pygame.draw.rect(tela, (100, 0, 0),(rectHudJogador.x + 10, rectHudJogador.y + 30, 300, 15))  # Fundo Vermelho Escuro
        pygame.draw.rect(tela, (0, 200, 80),(rectHudJogador.x + 10, rectHudJogador.y + 30, 300 * proporcaoVidaJogador, 15))  # Vida Verde

        # Barra de Especial

        posicaoSpaJogador = (rectHudJogador.x + 10, rectHudJogador.y + 50, 200, 10)
        pygame.draw.rect(tela, (80, 80, 0), posicaoSpaJogador)
        pygame.draw.rect(tela, (255, 215, 0), (posicaoSpaJogador[0], posicaoSpaJogador[1],posicaoSpaJogador[2] * max(0.0,min(1.0, self.jogador.getSpaEnergia() / 5)),posicaoSpaJogador[3]))

        # BARRA DE XP

        xpAtual = self.jogador.getExp()
        xpNecessario = self.jogador.getLvl() * 100
        proporcaoXp = min(1.0, xpAtual / xpNecessario)
        pygame.draw.rect(tela, (40, 40, 40), (rectHudJogador.x + 10, rectHudJogador.y + 55, 300, 8))
        pygame.draw.rect(tela, (0, 150, 255), (rectHudJogador.x + 10, rectHudJogador.y + 55, 300 * proporcaoXp, 8))


        # 2. HUD INIMIGO (Topo Direito)

        rectHudInimigo = pygame.Rect(larguraTela - 330, 10, 320, 60)
        pygame.draw.rect(tela, corFundoHud, rectHudInimigo, border_radius=5)
        pygame.draw.rect(tela, corBorda, rectHudInimigo, 2, border_radius=5)
        nomeInimigoTxt = fonteMedia.render(f"{self.inimigo.getNome()} - Lv.{self.inimigo.getLvl()}", True,(220, 50, 50))
        tela.blit(nomeInimigoTxt, (rectHudInimigo.x + 10, rectHudInimigo.y + 5))

        # BARRA DE VIDA DO INIMIGO
        vidaAtualInimigo = self.inimigo.getVida()
        vidaMaximaInimigo = self.inimigo.getVidaMaxima()
        proporcaoVidaInimigo = max(0.0, min(1.0, vidaAtualInimigo / vidaMaximaInimigo))
        pygame.draw.rect(tela, (100, 0, 0),(rectHudInimigo.x + 10, rectHudInimigo.y + 30, 300, 15))
        pygame.draw.rect(tela, (200, 30, 30), (rectHudInimigo.x + 10, rectHudInimigo.y + 30, 300 * proporcaoVidaInimigo,15))

        # Barra de Especial do Inimigo

        posicaoSpaInimigo = (rectHudInimigo.x + 10, rectHudInimigo.y + 50, 300, 10)
        pygame.draw.rect(tela, (80, 80, 0), posicaoSpaInimigo)
        pygame.draw.rect(tela, (255, 215, 0), (posicaoSpaInimigo[0], posicaoSpaInimigo[1],posicaoSpaInimigo[2] * max(0.0,min(1.0, self.inimigo.getSpaEnergia() / 5)),posicaoSpaInimigo[3]))

        # --- BONECOS ---
        rectBonecoJogador = pygame.Rect(50, 120, 250, 300)
        pygame.draw.rect(tela, (70, 70, 70), rectBonecoJogador, border_radius=10)
        pygame.draw.rect(tela, corBorda, rectBonecoJogador, 2, border_radius=10)
        txtBonecoJog = fonteMedia.render("Boneco Jogador", True, (150, 150, 150))
        tela.blit(txtBonecoJog, (rectBonecoJogador.centerx - txtBonecoJog.get_width() // 2, rectBonecoJogador.centery))

        rectBonecoInimigo = pygame.Rect(larguraTela - 300, 120, 250, 300)
        pygame.draw.rect(tela, (70, 70, 70), rectBonecoInimigo, border_radius=10)
        pygame.draw.rect(tela, corBorda, rectBonecoInimigo, 2, border_radius=10)
        txtBonecoInim = fonteMedia.render("Boneco Inimigo", True, (150, 150, 150))
        tela.blit(txtBonecoInim,
                  (rectBonecoInimigo.centerx - txtBonecoInim.get_width() // 2, rectBonecoInimigo.centery))

        # --- PAINÉIS INFERIORES ---
        alturaPainelInferior = 150
        rectPainelDescricao = pygame.Rect(0, alturaTela - alturaPainelInferior, larguraTela // 2, alturaPainelInferior)
        rectPainelAcoes = pygame.Rect(larguraTela // 2, alturaTela - alturaPainelInferior, larguraTela // 2,
                                      alturaPainelInferior)

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

            # Corrigido: String mudada para "botaoCombate" para casar com o tratarEventos
            self.jogador.inv.slotsRegiao.append((rectBotao, "botaoCombate", opcao["id"]))

            corTexto = (255, 255, 255)
            if rectBotao.collidepoint(posicaoMouse):
                acaoFocada = opcao["id"]
                corTexto = (255, 215, 0)
                pygame.draw.polygon(tela, corTexto, [
                    (xBotao - 15, yBotao + 10),
                    (xBotao - 15, yBotao + 25),
                    (xBotao - 5, yBotao + 17)
                ])

            txtOpcao = fonteGrande.render(opcao["nome"], True, corTexto)
            tela.blit(txtOpcao, (xBotao, yBotao))

        self.renderizarDescricao(tela, rectPainelDescricao, acaoFocada, fonteMedia, fontePequena)

    def renderizarDescricao(self, tela, rect, acao, fonteTitulo, fonteCorpo):
        margem = 20
        titulo = "Menu de Combate"
        corpo = "Passe o mouse sobre uma opção para ver os detalhes."

        if acao == "ataque":
            titulo = "Ação: Ataque Físico"
            corpo = "Ataca o inimigo com sua arma principal causando dano baseado em sua força."
        elif acao == "item":
            titulo = "Ação: Usar Item"
            corpo = "Abre sua mochila para utilizar poções de cura ou itens de suporte."
        elif acao == "habilidade":
            titulo = "Ação: Habilidade Especial"
            corpo = f"Gasta seus pontos de {self.jogador.getClasse()} para realizar um golpe devastador."
        elif acao == "fugir":
            titulo = "Ação: Escapar"
            corpo = "Tenta fugir da batalha. Sucesso baseado na diferença de nível e sorte."

        txtTit = fonteTitulo.render(titulo, True, (255, 215, 0))
        tela.blit(txtTit, (rect.x + margem, rect.y + margem))

        palavras = corpo.split(' ')
        linhaAtual = ""
        yOffset = margem + 30
        for palavra in palavras:
            if fonteCorpo.size(linhaAtual + palavra)[0] < rect.width - (margem * 2):
                linhaAtual += palavra + " "
            else:
                tela.blit(fonteCorpo.render(linhaAtual, True, (200, 200, 200)), (rect.x + margem, rect.y + yOffset))
                yOffset += 20
                linhaAtual = palavra + " "
        tela.blit(fonteCorpo.render(linhaAtual, True, (200, 200, 200)), (rect.x + margem, rect.y + yOffset))