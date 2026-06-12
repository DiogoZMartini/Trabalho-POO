from classe import Personagem
from componentes.inventario import Inventario

class Jogador(Personagem):
    def __init__(self, nome, dano, vida, vidaMaxima, lvl, spa, spaEnergia, exp, classe, dinheiro, maxXp = 100):
        super().__init__(nome, dano, vida, vidaMaxima, lvl, spa, spaEnergia)
        self.exp = exp
        self.classe = classe
        self.inv = Inventario(jogador=self, modo="padrao")
        self.dinheiro = dinheiro
        self.maxXp = maxXp

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
    def getExp(self):
        return self.exp
    def getClasse(self):
        return self.classe
    def getInv(self):
        return self.inv
    def getDinheiro(self):
        return self.dinheiro
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
    def setExp(self, exp):
        self.exp = exp
    def setClasse(self, classe):
        self.classe = classe
    def setInv(self, lista_itens):
        if isinstance(lista_itens, list):
            if hasattr(self, 'inv') and self.inv is not None:
                self.inv.mochila = lista_itens
        else:
            self.inv = lista_itens
    def setDinheiro(self, dinheiro):
        self.dinheiro = dinheiro

    def tomarDano(self, dano):
        super().tomarDano(dano)

    def addItem(self, item):
        if len(self.inv.mochila) < 15:
            self.inv.mochila.append(item)
            self.inv.salvarInventario()
            return True
        print("Mochila cheia! Não foi possível adicionar o item.")
        return False

    def defesa(self):
        defesaTotal = 0
        slotsDeDefesa = ["Capacete", "Armadura", "Bota"]
        for slot in slotsDeDefesa:
            item = self.inv.equipamentos.get(slot)
            if item:
                defesaTotal += item.getDano()
        return defesaTotal

    def uparLevel(xp,maxxp):
        pass
