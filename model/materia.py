class Materia:
    def __init__(self, grado, nombre, num_corr="0", fecha=None):
        self.grado = grado
        self.nombre = nombre
        self.num_corr = num_corr
        self.fecha = fecha

    def __str__(self):
        return f"Nombre: {self.nombre}, Grado: {self.grado}, Numero: {self.num_corr}"

    def __repr__(self):
        return f"Nombre: {self.nombre}"

