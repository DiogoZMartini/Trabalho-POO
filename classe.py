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
    def __init__(self, nome, dano, vida, lvl, recurso, spa, spaEnergia):
        super().__init__(nome, dano)
        self.vida = vida
        self.vidaMaxima = vida
        self.lvl = lvl
        self.recurso = recurso
        self.spa = spa
        self.spaEnergia = spaEnergia

    def getNome(self):
        return super().getNome()
    def getDano(self):
        return super().getDano()
    def getVida(self):
        return self.vida
    def getVidaMaxima(self):
        return self.vidaMaxima
    def getLvl(self):
        return self.lvl
    def getRecurso(self):
        return self.recurso
    def getSpa(self):
        return self.spa
    def getSpaEnergia(self):
        return self.spaEnergia
    def setNome(self, nome):
        super().setNome(nome)
    def setDano(self, dano):
        super().setDano(dano)
    def setVida(self, vida):
        self.vida = vida
    def setVidaMaxima(self, vidaMaxima):
        self.vidaMaxima = vidaMaxima
    def setLvl(self, lvl):
        self.lvl = lvl
    def setRecurso(self, recurso):
        self.recurso = recurso
    def setSpa(self, spa):
        self.spa = spa
    def setSpaEnergia(self, spaEnergia):
        self.spaEnergia = spaEnergia

    def ataque(self, dano):
        pass
    def ataqueSpe(self, dano):
        pass
    def curarVida(self, dano):
        pass

    def tomarDano(self, quantidadeDano):
        danoReal = quantidadeDano + self.defesa()
        if danoReal < 1:
            danoReal = 1
        self.vida -= danoReal
        if self.vida < 0:
            self.vida = 0




