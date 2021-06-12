from math import sqrt
from random import randrange
from itertools import combinations
import matplotlib.pyplot as plt

class Ponto:
    def __init__(self,x:float=0,y:float=0) -> None:
        self._x = x
        self._y = y

    @property
    def x(self)->float:
        return self._x
    @x.setter
    def x(self,x:float)->float:
        self._x = x

    @property
    def y(self)->float:
        return self._y
    @y.setter
    def y(self,y:float)->None:
        self._y = y
    
    def distancia(self,ponto)->float:
        return sqrt((self.x - ponto.x)**2 + (self.y - ponto.y)**2)
    
    def __repr__(self) -> str:
        return f"P({self.x},{self.y})"


def plota_circulo(p:Ponto,raio:float):
    circulo = plt.Circle((p.x,p.y),raio,fill=False,alpha=0.3)
    ax = plt.gca()
    ax.add_patch(circulo)

def plota_seta(p1:Ponto,p2:Ponto):
    seta = plt.arrow(p1.x,p1.y,p2.x-p1.x,p2.y-p1.y,alpha=0.2,color='g')
    ax=plt.gca()
    ax.add_patch(seta)

def plota_ponto(p:Ponto,cor:str):
    circulo = plt.Circle((p.x,p.y),0.1,fill=True,color=cor)
    ax = plt.gca()
    ax.add_patch(circulo)

def calculo_trilateracao(pontos:list):
    x1 = pontos[0][0].x
    y1 = pontos[0][0].y
    x2 = pontos[1][0].x
    y2 = pontos[1][0].y
    x3 = pontos[2][0].x
    y3 = pontos[2][0].y
    r1 = pontos[0][1]
    r2 = pontos[1][1]
    r3 = pontos[2][1]
    A = 2*x2 - 2*x1
    B = 2*y2 - 2*y1
    C = r1**2 - r2**2 - x1**2 + x2**2 - y1**2 + y2**2
    D = 2*x3 - 2*x2
    E = 2*y3 - 2*y2
    F = r2**2 - r3**2 - x2**2 + x3**2 - y2**2 + y3**2
    x = (C*E - F*B) / (E*A - B*D)
    y = (C*D - A*F) / (B*D - A*E)
    return x,y


def trilateracao(pontos:list):
    if len(pontos)<3:
        raise Exception("São necessários pelo menos 3 pontos")
    if len(pontos) == 3:
        return trilateracao(pontos)
    # Caso tenha mais de 3 pontos, calcula a média com as combinações de 3 pontos
    x = []
    y = []
    for combinacao in combinations(list(range(len(pontos))),3):
        x_temp,y_temp = calculo_trilateracao([pontos[combinacao[0]],pontos[combinacao[1]],pontos[combinacao[2]]])
        x.append(x_temp)
        y.append(y_temp)
    return sum(x)/len(x),sum(y)/len(y)

def plota_pontos_ancora(pontos):
    for ponto in pontos:
        plota_ponto(ponto,'b')

def plota_distancias(pontos,alvo):
    for ponto in pontos:
        plota_circulo(ponto,ponto.distancia(alvo))
        plota_seta(ponto,alvo)

def estima_coordenadas(pontos,alvo):
    return trilateracao([(ponto,ponto.distancia(alvo)) for ponto in pontos])
    
if __name__ == "__main__":
    
    p1 = Ponto()
    p2 = Ponto(2,2)
    p3 = Ponto(5,8)
    p4 = Ponto(-5,5)
    p5 = Ponto(-10,-5)

    p_alvo = Ponto(randrange(-15,15),randrange(-15,15))
    pontos = [p1,p2,p3,p4,p5]
    
    plt.figure()
    plt.cla()
    ax = plt.gca()
    ax.set_xlim((-20,20))
    ax.set_ylim((-20,20))
    plota_pontos_ancora(pontos)
    plota_ponto(p_alvo,'r')
    plota_distancias(pontos,p_alvo)
    coord_estimada = estima_coordenadas(pontos,p_alvo)
    print(f'Coordenadas estimadas: x:{coord_estimada[0]:.2f} y:{coord_estimada[1]:.2f}')
    print(f'Coordenadas reais: x:{p_alvo.x:.2f} y:{p_alvo.y:.2f}')
    plt.show()
