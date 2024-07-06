from functions import ObjectFromCSV, check_file, get_data_from_CSV

CONSUMIBLES_DATA_FILE_NAME = '/data/consumibles.csv'
TESOROS_DATA_FILE_NAME = '/data/tesoros.csv'

consumibles_file_name = check_file(CONSUMIBLES_DATA_FILE_NAME)
tesoros_file_name = check_file(TESOROS_DATA_FILE_NAME)

class Item(ObjectFromCSV):
    """clase Item

    Attributes:
    -----------
    nombre : str
        nombre del item
    tipo : str {consumible | tesoro}
        tipo de item
    descripcion : str
        breve descripcion del item
    """
    pass
   

class Tesoro(Item):
    """clase Item Tesoro

    Attributes:
    -----------
    calidad : int {1 | 2}
        si es calidad 1, agranda el equipo de excavadores
        si es calidad 2, cambia el tipo de arena
    cambio : str {
        docencio | tareo | hibrido |
        normal | mojada | rocosa | magnetica
    }
        tipo de excavador que se agrega, o tipo de arena a la que se cambia
    """
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.tipo = 'tesoro'
    

class Consumible(Item):
    """clase Item Consumible

    Attributes:
    -----------
    _energia : int
        cambia la energia del excavador
    _fuerza : int
        cambia la fuerza del excavador
    _suerte : int
        cambia la suerte del excavador
    _felicidad : int
        cambia la felicidad del excavador
    """
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.tipo = 'consumible'
    


data_consumibles = get_data_from_CSV(consumibles_file_name)
consumibles = [Consumible(**data) for data in data_consumibles]

data_tesoros = get_data_from_CSV(tesoros_file_name)
tesoros = [Tesoro(**data) for data in data_tesoros]
