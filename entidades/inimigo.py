import random
from classe import Personagem
from banco import tabela_inimigos
from utilidade.itens import Item

class Inimigo (Personagem):
    def __init__(self, nome, dano, vida, vidaMaxima, lvl, spa, spaEnergia, dropExp, dropDinheiro):
        super().__init__(nome, dano, vida, vidaMaxima, lvl, spa, spaEnergia)
        self.dropExp = dropExp
        self.dropItem = None
        self.dropDinheiro = dropDinheiro

    def getNome(self):
        return super().getNome()
    def getDano(self):
        return super().getDano()
    def getVida(self):
        return super().getVida()
    def getVidaMaxima(self):
        return super().getVidaMaxima()
    def getLvl(self):
        return super().getLvl()
    def getSpa(self):
        return super().getSpa()
    def getSpaEnergia(self):
        return super().getSpaEnergia()
    def getDropExp(self):
        return self.dropExp
    def getDropItem(self):
        return self.dropItem
    def getDropDinheiro(self):
        return self.dropDinheiro
    def setNome(self, nome):
        super().setNome(nome)
    def setDano(self, dano):
        super().setDano(dano)
    def setVida(self, vida):
        super().setVida(vida)
    def setVidaMaxima(self, vidaMaxima):
        super().setVidaMaxima(vidaMaxima)
    def setLvl(self, lvl):
        super().setLvl(lvl)
    def setSpa(self, spa):
        super().setSpa(spa)
    def setSpaEnergia(self, spaEnergia):
        super().setSpaEnergia(spaEnergia)
    def setDropExp(self, dropexp):
        self.dropExp = dropexp
    def setDropItem(self, dropitem):
        self.dropItem = dropitem
    def setDropDinheiro(self, dropdinheiro):
        self.dropDinheiro = dropdinheiro

    def tomarDano(self, dano):
        super().tomarDano(dano)

    def dropadoExp(self):
        lvl = self.getLvl()
        exp_base = (lvl * 15) + (lvl - 1) * 5
        variacao_min = int(exp_base * 0.85)
        variacao_max = int(exp_base * 1.15)
        expFinal = random.randint(variacao_min, variacao_max)
        return max(5, expFinal)

    def dropadoItem(self):
        chanceDrop = 0.75
        if random.random() <= chanceDrop:
            itemSorteado = Item.gerarItemAleatorio()
            self.dropItem = itemSorteado
            return self.dropItem
        self.dropItem = None
        return None
    
    def dropadoDinheiro(self):
        minimo = 5
        maximo = 15
        dinheiroFinal = random.randint(minimo, maximo)
        return dinheiroFinal

    def defesa(self):
        defesaTotal = 0
        return defesaTotal

    @classmethod
    def gerarInimigoAleatorio(cls, lvlJogador, nomeInimigoAlvo):
        todosInimigos = tabela_inimigos.all()
        if nomeInimigoAlvo != "Mercador":
            inimigosValidos = [i for i in todosInimigos if i['nome'] != 'Mercador']
        else:
            inimigosValidos = [i for i in todosInimigos if i['nome'] == 'Mercador']
        dadosBase = random.choice(inimigosValidos)
        lvlSorteado = random.randint(lvlJogador - 1, lvlJogador + 1)
        if lvlSorteado < 1:
            lvlSorteado = 1
        multiplicadorStatus = 1 + (lvlSorteado - 1) * 0.1
        vidaFinal = int(dadosBase['vida'] * multiplicadorStatus)
        danoFinal = int(dadosBase['dano'] * multiplicadorStatus)
        dropExpCalculado = lvlSorteado * 25
        dropDinheiroCalculado = random.randint(5, 15)
        return cls(
            nome=dadosBase['nome'],
            dano=danoFinal,
            vida=vidaFinal,
            vidaMaxima=vidaFinal,
            lvl=lvlSorteado,
            spa=dadosBase.get('spa', 'Ataque Básico'),
            spaEnergia= 0,
            dropExp = dropExpCalculado,
            dropDinheiro = dropDinheiroCalculado
        )

class Mercador(Inimigo):
    def __init__(self, nome, dano, vida, vidaMaxima, spa, spaEnergia, lvl, dropExp, dropDinheiro):
        super().__init__(nome, dano, vida, vidaMaxima, lvl, spa, spaEnergia, dropExp, dropDinheiro)

    def getNome(self):
        return super().getNome()
    def getDano(self):
        return super().getDano()
    def getVida(self):
        return super().getVida()
    def getVidaMaxima(self):
        super().getVidaMaxima()
    def getLvl(self):
        return super().getLvl()
    def getSpa(self):
        return super().getSpa()
    def getSpaEnergia(self):
        return super().getSpaEnergia()
    def getDropExp(self):
        return super().getDropExp()
    def getDropItem(self):
        return super().getDropItem()
    def getDropDinheiro(self):
        return super().getDropDinheiro()
    def getMercadoria(self):
        return self.mercadoria
    def setNome(self, nome):
        super().setNome(nome)
    def setDano(self, dano):
        super().setDano(dano)
    def setVida(self, vida):
        super().setVida(vida)
    def setVidaMaxima(self, vidaMaxima):
        super().setVidaMaxima(vidaMaxima)
    def setLvl(self, lvl):
        super().setLvl(lvl)
    def setSpa(self, spa):
        super().setSpa(spa)
    def setSpaEnergia(self, spaEnergia):
        super().setSpaEnergia(spaEnergia)
    def setDropExp(self, dropExp):
        super().setDropExp(dropExp)
    def setDropItem(self, dropItem):
        super().setDropItem(dropItem)
    def setDropDinheiro(self, dropDinheiro):
        super().setDropDinheiro(dropDinheiro)
    def setMercadoria(self, mercadoria):
        self.mercadoria = mercadoria

    def tomarDano(self, dano):
        super().tomarDano(dano)
    def dropadoExp(self):
        super().dropadoExp()
    def dropadoItem(self):
        super().dropadoItem()
    def dropadoDinheiro(self):
        super().dropadoDinheiro()
    @classmethod
    def gerarInimigoAleatorio(cls, lvlJogador, nomeInimigoAlvo):
        inimigo = super().gerarInimigoAleatorio(lvlJogador, nomeInimigoAlvo)
        return inimigo

    def comparItem(self, itemParaComprar, jogador):
        preco = itemParaComprar.getPreco()
        inv = jogador.inv

        if len(inv.mochila) >= 15:
            return False, "Mochila cheia!"

        if jogador.getDinheiro() >= preco:
            jogador.setDinheiro(jogador.getDinheiro() - preco)
            inv.mochila.append(itemParaComprar)
            inv.salvarInventario()
            return True, f"Comprou {itemParaComprar.getNome()}!"
        else:
            return False, "Dinheiro insuficiente!"

    def venderItem(self, indexItem, jogador):
        inv = jogador.inv
        itemParaVender = inv.mochila[indexItem]
        valorVenda = max(1, int(itemParaVender.getPreco() // 2))
        jogador.setDinheiro(jogador.getDinheiro() + valorVenda)
        nomeRemovido = itemParaVender.getNome()
        inv.mochila.pop(indexItem)
        inv.salvarInventario()
        return True, f"Vendeu {nomeRemovido} por {valorVenda}g!"