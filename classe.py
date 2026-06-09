class Geral:
    def __init__(self, nome, dano):
        self.nome = nome
        self.dano = dano

    def getNome(self):
        return self.nome
    def getDano(self):
        return self.dano
    def setNome(self, nome):
        self.nome = nome
    def setDano(self, dano):
        self.dano = dano

class Personagem(Geral):
    def __init__(self, nome, dano, vida, lvl, recurso):
        super().__init__(nome, dano)
        self.vida = vida
        self.lvl = lvl
        self.recurso = recurso

    def getNome(self):
        return super().getNome()
    def getDano(self):
        return super().getDano()
    def getVida(self):
        return self.vida
    def getLvl(self):
        return self.lvl
    def getRecurso(self):
        return self.recurso
    def setNome(self, nome):
        super().setNome(nome)
    def setDano(self, dano):
        super().setDano(dano)
    def setVida(self, vida):
        self.vida = vida
    def setLvl(self, lvl):
        self.lvl = lvl
    def setRecurso(self, recurso):
        self.recurso = recurso

    def ataque(self, dano):
        pass
    def ataqueSpe(self, dano):
        pass
    def curarVida(self, dano):
        pass
    def tomarDano(self, dano):
        pass






