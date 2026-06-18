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
        inimigosValidos = None
        todosInimigos = tabela_inimigos.all()
        if nomeInimigoAlvo != "Mercador":
            inimigosValidos = [i for i in todosInimigos if i['nome'] != 'Mercador']
            if not inimigosValidos:
                return cls(nome="Zumbie", dano=5, vida=30,vidaMaxima=30, lvl=lvlJogador, recurso=0, spa="Mordida")
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
        dropDinheiroCalculado = lvlSorteado * random.randint(5, 15)
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
    def __init__(self, nome, dano, vida, vidaMaxima, spa, spaEnergia, lvl, dropExp, dropdinheiro):
        super().__init__(nome, dano, vida, vidaMaxima, lvl, spa, spaEnergia, dropExp, dropdinheiro)
        self.mercadoria = []

    def getNome(self):
        return super().getNome()
    def getDano(self):
        return super().getDano()
    def getVida(self):
        return super().getVida()
    def setVidaMaxima(self, vidaMaxima):
        super().setVidaMaxima(vidaMaxima)
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
    def setDropExp(self, dropexp):
        super().setDropExp(dropexp)
    def setDropItem(self, dropitem):
        super().setDropItem(dropitem)
    def setDropDinheiro(self, dropdinheiro):
        super().setDropDinheiro(dropdinheiro)
    def setMercadoria(self, mercadoria):
        self.mercadoria = mercadoria

    def tomarDano(self, dano):
        super().tomarDano(dano)
    def expDropado(self):
        super().expDropado()
    def expDropItem(self):
        super().expDropItem()
    def expDropDinheiro(self):
        super().expDropDinheiro()
    def gerarInimigoAleatorio():
        super().gerarInimigoAleatorio()    

    def comparItem(self, item, dinheiro, inv, mercadoria):
        pass
    def venderItem(self, item, dinheiro, inv, mercadoria):
        pass