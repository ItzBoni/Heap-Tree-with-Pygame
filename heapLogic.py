"""Max-heap implementation refactorizada en una clase `MaxHeap`.

El array interno usa índice 1..capacity (índice 0 no se usa) para facilitar
las fórmulas padre/hijo. Los métodos mantienen la semántica original pero
ahora como comportamiento de instancia.
"""

class heapLogic:
    def __init__(self, capacity: int = 15):
        # capacity = número máximo de elementos activos que puede contener el heap
        self.capacity = capacity
        self.monti = [""] * (capacity + 1)  # índice 0 no se usa
        self.tam = 0

    def insertar(self, n):
        if self.tam >= self.capacity:
            raise IndexError(f"Heap lleno (capacidad: {self.capacity})")
        self.tam += 1
        self.monti[self.tam] = n
        self.flotar(self.tam)

    def flotar(self, x):
        padre = x // 2
        while padre >= 1:
            if self.monti[padre] < self.monti[x]:
                self.monti[padre], self.monti[x] = self.monti[x], self.monti[padre]
                x = padre
                padre = x // 2
            else:
                break

    def hundir(self, n):
        while 2 * n <= self.tam:
            izq = 2 * n
            der = 2 * n + 1
            if der <= self.tam and self.monti[der] > self.monti[izq]:
                grande = der
            else:
                grande = izq

            if self.monti[n] < self.monti[grande]:
                self.monti[n], self.monti[grande] = self.monti[grande], self.monti[n]
                n = grande
            else:
                break

    def pop(self):
        if self.tam == 0:
            raise IndexError("pop from empty heap")
        self.monti[1], self.monti[self.tam] = self.monti[self.tam], self.monti[1]
        self.tam -= 1
        self.hundir(1)
        r = self.monti[self.tam + 1]
        self.monti[self.tam + 1] = 0
        return r

    def mostrar(self):
        if self.tam == 0:
            print("Heap vacío")
            return

        print(f"Heap inicial: {self.monti[1:self.tam+1]}")
        resultado = []
        while self.tam > 0:
            resultado.append(self.pop())

        print(f"Heap ordenado: {resultado}")

        # reconstruir
        for n in resultado[::-1]:
            self.insertar(n)

    def agregar(self, elemento):
        if self.tam >= self.capacity:
            print(f"Error: heap lleno (capacidad: {self.capacity})")
            return False
        self.insertar(elemento)
        print(f"Heap después de agregar {elemento}: {self.monti[1:self.tam+1]}")
        return True

    def quitar(self, valor):
        if self.tam == 0:
            print("Heap vacío")
            return False

        indice = -1
        for i in range(1, self.tam + 1):
            if self.monti[i] == valor:
                indice = i
                break

        if indice == -1:
            print(f"Valor {valor} no existe en heap")
            return False

        if indice == self.tam:
            self.monti[self.tam] = 0
            self.tam -= 1
            print(f"Heap después de quitar {valor}: {self.monti[1:self.tam+1]}")
            return True

        ultimo = self.monti[self.tam]
        self.monti[indice] = ultimo
        self.monti[self.tam] = 0
        self.tam -= 1

        if indice > 1 and self.monti[indice] > self.monti[indice // 2]:
            self.flotar(indice)
        else:
            self.hundir(indice)

        print(f"Heap después de quitar {valor}: {self.monti[1:self.tam+1]}")
        return True


if __name__ == "__main__":
    # Demo rápido: crear heap, insertar algunos valores y mostrar estado
    h = heapLogic()
    lista = [1, 2, 3, 4, 5, 6, 7, 8]
    for n in lista:
        h.insertar(n)

    print(f"Heap inicial: {h.monti[1:h.tam+1]}")