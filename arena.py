from functions import ObjectFromCSV, check_file, get_data_from_CSV
import parametros as p
from random import randint

ARENAS_DATA_FILE_NAME = '/data/arenas.csv'

arenas_file_name = check_file(ARENAS_DATA_FILE_NAME)

class Arena(ObjectFromCSV):
    """clase Arena

    todas las propiedades deben mantenerse entre 1 y 10

    Attributes:
    -----------
    name : str
        nombre de la arena
    tipo : str {normal | mojada | rocosa | magnetica}
        tipo de la arena
    rareza : int [1, 10]
        rareza de la arena (1 es menos raro)
    humedad : int [1, 10]
        humedad de la arena
    dureza : int [1, 10]
        dureza de la arena
    estatica : int [1, 10]
        estatica de la arena
    dificultad : float [0.10, 1.00]
        afecta la velocidad de excavacion
    """
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        setattr(self, 'dificultad', round(
            (self.get('rareza') + self.get('humedad') + self.get('dureza') + self.get('estatica'))/40,
            2
        ))
        self.PROB_ENCONTRAR_ITEM = p.PROB_ENCONTRAR_ITEM

    def to_Normal(self):
        return Normal(**self.__dict__)

    def to_Mojada(self):
        return Mojada(**self.__dict__)

    def to_Rocosa(self):
        return Rocosa(**self.__dict__)

    def to_Magnetica(self):
        return Magnetica(**self.__dict__)
    
    def next_day(self):
        pass

class Normal(Arena):
    """clase Arena Normal

    la dificultad se multiplica por la constante POND_ARENA_NORMAL dada en
    los parametros, haciendola mas facil

    Attributes:
    -----------
    dificultad : float 
        dificultad = round(
            dificultad * POND_ARENA_NORMAL,
            2
        )
    """
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        setattr(self, 'tipo', 'normal')
        self.set_dificultad()

    def set_dificultad(self):
        setattr(self, 'dificultad', round(self.get('dificultad') * p.POND_ARENA_NORMAL, 2))

class Mojada(Arena):
    """clase Arena Mojada

    un excavador SIEMPRE va a encontrar un item.
    El item encontrado tiene la misma probabilidad de ser Tesoro o Consumible.
    """
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        setattr(self, 'tipo', 'mojada')
       
class Rocosa(Arena):
    """clase Arena Rocosa

    la dureza afecta mas a la dificultad

    Attributes:
    -----------
    dificultad : float
        dificultad = round(
            (rareza + humedad + 2*dureza + estatica)/50,
            2
        )
    """
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        setattr(self, 'tipo', 'rocosa')
        self.set_dificultad()

    def set_dificultad(self):
        setattr(self, 'dificultad', round(
            (self.get('rareza') + self.get('humedad') + 2*self.get('dureza') + self.get('estatica'))/50,
            2
        ))

class Magnetica(Mojada, Rocosa):
    """clase Arena Magnetica

    se forma cuando hay un terremoto sobre arena mojada, 
    o cuando llueve sobre arena rocosa.

    Mismo comportamiento de las arenas Mojada y Rocosa

    Attributes:
    -----------
    humedad : int randint(1, 10)
        valor aleatorio entre 1 y 10 cada vez que se simule un dia
    dureza : int randint(1, 10)
        valor aleatorio entre 1 y 10 cada vez que se simule un dia
    """
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        setattr(self, 'tipo', 'magnetica')
        self.set_dificultad()
        # self.next_day()
    
    def next_day(self):
        setattr(self, 'humedad', randint(1, 10))
        setattr(self, 'dureza', randint(1, 10))
      

data_arenas = get_data_from_CSV(arenas_file_name)
arenas = []
for data in data_arenas:
    tipo = data.get('tipo')
    if tipo == 'normal':
        TipoArena = Normal
    elif tipo == 'mojada':
        TipoArena = Mojada
    elif tipo == 'rocosa':
        TipoArena = Rocosa
    else:
        TipoArena = Magnetica

    arenas.append(TipoArena(**data))

arenas = [Arena(**arena) for arena in data_arenas]
