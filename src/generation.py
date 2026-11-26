import numpy as np
import matplotlib.pyplot as plt
from opensimplex import OpenSimplex

# Funciones para la generación de terreno

def iniciar_generador(seed: int):
    gen = OpenSimplex(seed=seed)
    return gen

def noise(nx: float, ny: float, gen):
    """Creamos ruido en una posición del array dada.

    :param nx: Coordenada x normalizada y centrada.
    :type nx: float
    :param ny: Coordenada y noramalizad y centrada.
    :type ny: float
    :param gen: Generador de ruido de opensimplex.
    :type gen: OpenSimplex
    :return: Valor del ruido para las coordenadas.
    :rtype: float
    """

    # Reescalar de -1.0:1:0 a 0.0:1.0
    return gen.noise2(nx, ny) / 2.0 + 0.5

def generar_octava(shape: tuple, freq: int, gen):
    """Genera un mapa de alturas para una octava.

    :param shape: Tupla que contendrá valores enteros para las dimensiones de nuestro mapa
    :type shape: tuple(int, int)
    :param freq: Frecuencia. A mayor frecuencia, mayor tamaño (diferencia de alturas).
    :type freq: float
    :param gen: Generador de ruido de opensimplex.
    :type gen: OpenSimplex
    :return: La misma matriz con cada posición asignada a un valor de alturas entre 0 y 1/freq (amplitud).
    :rtype: np.ndarray
    """

    width, heigh = shape
    terreno = np.zeros(shape)

    for y in range(heigh):
        for x in range(width):
            nx = x/width - 0.5 # Normalizamos y centramos las coordenadas
            ny = y/heigh - 0.5

            # 1/freq es la amplitud
            terreno[x,y] = 1/freq * noise(freq*nx, freq*ny, gen)

    return terreno

def generar_mapa_alturas(shape: tuple[int, int], octavas:int=3, seed=1234):
    """Generar un mapa de alturas suamando octavas

    :param shape: Tupla que contendrá valores enteros para las dimensiones de nuestro mapa
    :type shape: tuple(int, int)
    :param octavas: Número de octavas para añadir más relieve
    :type octavas: int
    :param seed: Semilla aleatoria para generar el mapa
    :type seed: int
    :return: Mapa de alturas
    :rtype: np.ndarray
    """

    print("Generando...")

    gen = iniciar_generador(seed)
    elevacion = np.zeros(shape)
    for i in range(octavas):
        frecuencia: int = 2**i

        elevacion += generar_octava(shape, frecuencia, gen)

    # Para 3 octavas, dividimos entre (1.0 + 0.5 + 0.25) para normalizar la salida
    return elevacion / np.sum(1 / 2 ** np.arange(octavas))

if __name__ == '__main__':
    mapa_alturas = generar_mapa_alturas((256, 256), seed=123456)
    print("Mostrando...")
    plt.imshow(mapa_alturas, cmap="terrain", interpolation="nearest")
    plt.show()