from src.generation import generar_mapa_alturas
import numpy as np
import matplotlib.pyplot as plt

if __name__ == "__main__":
    terreno = generar_mapa_alturas((256, 256), 3)
    plt.imshow(terreno, cmap="terrain", interpolation="nearest")
    plt.show()