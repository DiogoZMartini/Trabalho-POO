import random
from classe import Personagem
from banco import tabela_inimigos

class Inimigo (Personagem):
    def __init__(self, nome, dano, vida, lvl, recurso, spa, dropExp, dropDinheiro, spaEnergia):
        super().__init__(nome, dano, vida, lvl, recurso, spa, spaEnergia)
        self.dropExp = dropExp
        self.dropItem = []
        self.dropDinheiro = dropDinheiro

    def getNome(self):
        return super().getNome()
    def getDano(self):
        return super().getDano()
    def getVida(self):
        return super().getVida()
    def getLvl(self):
        return super().getLvl()
    def getRecurso(self):
        return super().getRecurso()
    def getSpa(self):
        return super().getSpa()
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
    def setLvl(self, lvl):
        super().setLvl(lvl)
    def setRecurso(self, recurso):
        super().setRecurso(recurso)
    def setSpa(self, spa):
        super().setSpa(spa)
    def setDropExp(self, dropexp):
        self.dropExp = dropexp
    def setDropItem(self, dropitem):
        self.dropItem = dropitem
    def setDropDinheiro(self, dropdinheiro):
        self.dropDinheiro = dropdinheiro

    def ataque(self, dano):
        super().ataque(dano)
    def ataqueSpe(self, dano):
        super().ataqueSpe(dano)
    def curarVida(self, dano):
        super().curarVida(dano)
    def tomarDano(self, dano):
        super().tomarDano(dano)
    def expDropado(self):
        pass
    def expDropItem(self):
        pass
    def expDropDinheiro(self):
        pass

    def defesa(self):
        defesaTotal = 0
        return defesaTotal

    @classmethod
    def gerarInimigoAleatorio(cls, lvl_jogador):
        todos_inimigos = tabela_inimigos.all()
        inimigos_validos = [i for i in todos_inimigos if i['nome'] != 'Mercador']
        if not inimigos_validos:
            return cls(nome="Zumbie", dano=5, vida=30, lvl=lvl_jogador, recurso=0, spa="Mordida")
        dados_base = random.choice(inimigos_validos)
        lvl_sorteado = random.randint(lvl_jogador - 1, lvl_jogador + 1)
        if lvl_sorteado < 1:
            lvl_sorteado = 1
        multiplicador_status = 1 + (lvl_sorteado - 1) * 0.1
        vida_final = int(dados_base['vida'] * multiplicador_status)
        dano_final = int(dados_base['dano'] * multiplicador_status)
        dropExpCalculado = lvl_sorteado * 25
        dropDinheiroCalculado = lvl_sorteado * random.randint(5, 15)
        return cls(
            nome=dados_base['nome'],
            dano=dano_final,
            vida=vida_final,
            lvl=lvl_sorteado,
            recurso=0,
            spa=dados_base.get('spa', 'Ataque Básico'),
            spaEnergia= 0,
            dropExp = dropExpCalculado,
            dropDinheiro = dropDinheiroCalculado
        )

class Mercador(Inimigo):
    def __init__(self, nome, dano, vida, lvl, recurso, dropExp, dropdinheiro):
        super().__init__(nome, dano, vida, lvl, recurso, dropExp, dropdinheiro)
        self.mercadoria = []

    def getNome(self):
        return super().getNome()
    def getDano(self):
        return super().getDano()
    def getVida(self):
        return super().getVida()
    def getLvl(self):
        return super().getLvl()
    def getRecurso(self):
        return super().getRecurso()
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
    def setLvl(self, lvl):
        super().setLvl(lvl)
    def setRecurso(self, recurso):
        super().setRecurso(recurso)
    def setDropExp(self, dropexp):
        super().setDropExp(dropexp)
    def setDropItem(self, dropitem):
        super().setDropItem(dropitem)
    def setDropDinheiro(self, dropdinheiro):
        super().setDropDinheiro(dropdinheiro)
    def setMercadoria(self, mercadoria):
        self.mercadoria = mercadoria

    def ataque(self, dano):
        super().ataque(dano)
    def ataqueSpe(self, dano):
        super().ataqueSpe(dano)
    def curarVida(self, dano):
        super().curarVida(dano)
    def tomarDano(self, dano):
        super().tomarDano(dano)
    def expDropado(self):
        super().expDropado()
    def expDropItem(self):
        super().expDropItem()
    def expDropDinheiro(self):
        super().expDropDinheiro()
    def comparItem(self, item, dinheiro, inv, mercadoria):
        pass
    def venderItem(self, item, dinheiro, inv, mercadoria):
        pass