from classe import Personagem

class Inimigo (Personagem):
    def __init__(self, nome, dano, vida, lvl, recurso, dropExp, dropDinheiro):
        super().__init__(nome, dano, vida, lvl, recurso)
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