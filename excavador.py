from functions import ObjectFromCSV, check_file, get_data_from_CSV, inside
import parametros as p

"""
TODO: ver los dias de descanso
"""

DATA_FILE_NAME = '/data/excavadores.csv'

file_name = check_file(DATA_FILE_NAME)
class Excavador(ObjectFromCSV):
    """clase Excavador

    Attributes:
    -----------
    nombre : str
        nombre del excavador
    tipo : str {docencio | tareo | hibrido}
        tipo de excavador
    edad : int [18, 60]
        edad del excavador. Afecta la velocidad de excavacion
    energia : int [0, 100]
        es afectada tanto por los dias transcurridos, como
        por los items y habilidades usadas
    fuerza : int [1, 10]
        es afectada por los items usados. Afecta la velocidad
        de excavacion
    suerte : int [1, 10]
        es afectada por los items usados. Afecta la probabilidad
        de encontrar objetos
    felicidad : int [1, 10]
        es afectada por eventos y por items. Afecta la velocidad
        de excavacion
    dias_descanso : int = 0
        dias de descanso restantes
            
    Methods:
    --------
    cavar(Arena.dificultad: float) -> metros_cavados: int
        devuelve los metros cavados por el excavador
    descansar() -> dias_descanso: int
        si el excavador se queda sin energia, debe descansar una cierta
        cantidad de dias hasta que la energia llegue a 100
        self.dias_descanso -= 1 por dia
    encontrar_item(Arena.tipo: str, Arena.items: list[Item])
        todos los dias se tiene la probabilidad de encontrar un item
        de los que esten en la arena
    gastar_energia()
        cada dia excavado se pierde energia
    consumir(consumibe: Consumible)
        se usa un consumible y se obtienen los beneficios
    atributos()
    """

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self._dias_descanso = 0

    @property
    def dias_descanso(self):
        return self._dias_descanso
    
    @dias_descanso.setter
    def dias_descanso(self, value):
        self._dias_descanso = value

    def descanso(self):
        if self.dias_descanso == 1:
            self.energia = 100
        self.dias_descanso -= 1
        
    @property
    def edad(self):
        return self.get('_edad')
    
    @edad.setter
    def edad(self, value):
        setattr(self, '_edad', inside((18, 60), value))

    @property
    def energia(self):
        return self.get('_energia')
    
    @energia.setter
    def energia(self, value):
        setattr(self, '_energia', inside((0, 100), value))

    @property
    def fuerza(self):
        return self.get('_fuerza')
    
    @fuerza.setter
    def fuerza(self, value):
        setattr(self, '_fuerza', inside((1, 10), value))

    @property
    def suerte(self):
        return self.get('_suerte')
    
    @suerte.setter
    def suerte(self, value):
        setattr(self, '_suerte', inside((1, 10), value))

    @property
    def felicidad(self):
        return self.get('_felicidad')
    
    @felicidad.setter
    def felicidad(self, value):
        setattr(self, '_felicidad', inside((1, 10), value))

    def cavar(self, dificultad_arena: int) -> int:
        metros = int((30/self.edad + (self.felicidad + 2*self.fuerza)/10)/(10*dificultad_arena))
        return metros

    def descansar(self):
        dias = int(self.get('edad')/20)
        setattr(self, '_dias_descanso', dias)
        return dias

    def gastar_energia(self):
        energia = self.energia - int(10/self.fuerza + self.edad/6)
        self.energia = energia

    def consumir(self, item):
        atributos = [
            'edad',
            'energia',
            'fuerza',
            'suerte',
            'felicidad'
        ]
        for atributo in atributos:
            setattr(self, atributo, self.get(atributo) + item.get('_'+atributo))
           
    # def get(self, key):
    #     return getattr(self, key)

class Docencio(Excavador):
    """clase Excavador Docencio
    
    luego de terminar de cavar, aumenta su felicidad y su fuerza,
    pero pierde mas energia
    
    Attributes:
    -----------
    felicidad : int [1, 10]
        felicidad = felicidad + FELICIDAD_ADICIONAL_DOCENCIO
    fuerza : int [1, 10]
        fuerza = fuerza + FUERZA_ADICIONAL_DOCENCIO
    energia : int [0, 100]
        energia = energia - ENERGIA_PERDIDA_DOCENCIO
    """
    def cavar(self, arena_dificultad: int) -> int:
        metros = super().cavar(dificultad_arena=arena_dificultad)
        self.felicidad += p.FELICIDAD_ADICIONAL_DOCENCIO
        self.fuerza += p.FUERZA_ADICIONAL_DOCENCIO
        self.energia -= p.ENERGIA_PERDIDA_DOCENCIO
        # setattr(self, 'felicidad', self.felicidad + p.FELICIDAD_ADICIONAL_DOCENCIO)
        # setattr(self, 'fuerza', self.fuerza + p.FUERZA_ADICIONAL_DOCENCIO)
        # setattr(self, 'energia', self.get('energia') - p.ENERGIA_PERDIDA_DOCENCIO)
        return metros

class Tareo(Excavador):
    """clase Excavador Tareo
    
    luego de consumir un item Consumible aumenta su energia y suerte,
    pero aumenta la edad y disminuye la felicidad
    
    Methods:
    -----------
    consumir()
        energia = energia + ENERGIA_ADICIONAL_TAREO
        suerte = suerte + SUERTE_ADICIONAL_TAREO
        edad = edad + EDAD_ADICIONAL_TAREO
        felicidad = felicidad - FELICIDAD_PERDIDA_TAREO
    """
    
    def consumir(self, item):
        self.energia += p.ENERGIA_ADICIONAL_TAREO
        self.suerte += p.SUERTE_ADICIONAL_TAREO
        self.edad += p.EDAD_ADICIONAL_TAREO
        self.felicidad -= p.FELICIDAD_PERDIDA_TAREO
        super().consumir(item)

class Hibrido(Docencio, Tareo):
    """clase Excavador Hibrido
    
    mismas propiedades que Tareo y Docencio. La energia perdida se ve reducid
    a la mitad. La energia no baja de los 20. No descansan

    Attributes:
    -----------
    energia : int [20, 100]

    Methods:
    --------
    gastar_energia() = gastar_energia() / 2
    """
    def gastar_energia(self):
        energia = self.energia - int(10/self.fuerza + self.edad/6)/2
        self.energia = max(20, energia)

data_excavadores = get_data_from_CSV(file_name)
excavadores = []
for data in data_excavadores:

    tipo = data.get('tipo')
    if tipo == 'docencio':
        TipoExcavador = Docencio
    elif tipo == 'tareo':
        TipoExcavador = Tareo
    else:
        TipoExcavador = Hibrido

    excavadores.append(TipoExcavador(**data))
