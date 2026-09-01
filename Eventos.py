class Eventos:           #Poner una validacion para que el evento que estamos metiendo en el historia ya esté cerrado
    def __init__(self,fecha,evento,descripcion,personal):
        self.fecha=fecha
        self.evento=evento
        self.descripcion=descripcion
        self.personal=personal