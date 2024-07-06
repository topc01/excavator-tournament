from os import getcwd
from os.path import isfile
from abc import ABC

FOLDER = getcwd() + '/Partidas/'
# FOLDER = getcwd() + '/Partidas_test/'

class ObjectFromCSV(ABC):
    """clase base para los objetos que se crean a partir de un archivo csv
    
    Attributes:
    -----------
    depende del diccionario pasado como argumento
    
    """
    def __init__(self, **kwargs) -> None:
        for key, value in kwargs.items():
            if (not isinstance(value, (int, float))) and (value.isnumeric() or (value.startswith('-') and value[1:].isnumeric())):
                value = int(value)
            if key in ('edad', 'energia', 'fuerza', 'suerte', 'felicidad'):
                key = '_' + key
            setattr(self, key, value)
    
    def __str__(self) -> str:
        tipo = type(self).__name__
        data = ''
        for key, value in self.__dict__.items():
            if key.startswith('__'):
                continue
            data += f'{key}$:${value}$, $'
        return f"{tipo}$->${data[:-4]}"
    
    def __repr__(self) -> str:
        data = type(self).__name__ + '('
        for key, value in self.__dict__.items():
            if key.startswith('_'):
                continue
            data += f'{key}: {value}, '
        return data[:-2] + ')'
    
    def get(self, key: str):
        return getattr(self, key, 0)
    
    def next_day(self):
        pass

def parse_object(obj_repr: str):
    """funcion que parsea un objeto a partir de su representacion en string
    """
    from torneo import Torneo
    from arena import Normal, Mojada, Magnetica, Rocosa
    from item import Tesoro, Consumible
    from excavador import Tareo, Docencio, Hibrido

    objects = {
        'Torneo': Torneo,
        'Normal': Normal,
        'Mojada': Mojada,
        'Magnetica': Magnetica,
        'Rocosa': Rocosa,
        'Tesoro': Tesoro,
        'Consumible': Consumible,
        'Tareo': Tareo,
        'Docencio': Docencio,
        'Hibrido': Hibrido
    }

    arena_data, equipo_data, mochila_data, tipo_arena, metros_cavados, meta, dias_transcurridos, dias_totales = obj_repr.split('\n')
    
    arena_tipo, arena_kwargs_data = arena_data.split('$->$')
    arena_kwargs = {}
    for data in arena_kwargs_data.split('$, $'):
        key, value = data.split('$:$')
        arena_kwargs[key] = value
    if arena_tipo == 'Arena':
        arena_tipo = tipo_arena.title()
    arena = objects[arena_tipo](**arena_kwargs)

    equipo = []
    for excavador in equipo_data.split(' | '):
        excavador_tipo, excavador_kwargs_data = excavador.split('$->$')
        excavador_kwargs = {}
        for data in excavador_kwargs_data.split('$, $'):
            key, value = data.split('$:$')
            excavador_kwargs[key] = value
        if excavador_tipo == 'Excavador':
            excavador_tipo = excavador_kwargs['tipo'].title()
        equipo.append(objects[excavador_tipo](**excavador_kwargs))

    mochila = []
    print(f'======>{mochila_data}<======')
    if mochila_data != '':
        for item in mochila_data.split(' | '):
            item_tipo, item_kwargs_data = item.split('$->$')
            item_kwargs = {}
            for data in item_kwargs_data.split('$, $'):
                key, value = data.split('$:$')
                item_kwargs[key] = value
            if item_tipo == 'Item':
                item_tipo = item_kwargs['tipo'].title()
            mochila.append(objects[item_tipo](**item_kwargs))
    
    return Torneo(arena, equipo, mochila, tipo_arena, int(metros_cavados), int(meta), int(dias_transcurridos), int(dias_totales))

def guardar_partida(torneo, file_name: str = None):
    """funcion que guarda la partida en un archivo de texto
    """
    r_torneo = str(torneo)
    if not file_name:
        file_name = input('ingrese el nombre: ')
    with open(FOLDER + file_name + '.txt', 'w') as file:
        file.write(f'{r_torneo}')

def cargar_partida(file_name: str):
    """funcion que carga la partida desde un archivo de texto
    """
    with open(FOLDER + file_name, 'r') as file:
        data = ''.join(file.readlines())
    torneo = parse_object(data)
    return torneo
    

def get_data_from_CSV(file_name: str) -> dict:
    """funcion que obtiene los datos de un archivo csv
    y los devuelve como un diccionario donde las llaves
    son los nombres de las columnas dadas en la primera fila
    del archivo y los valores son las columnas de cada fila
    """
    data = []
    with open(file=file_name, encoding='utf-8-sig') as file:
        keys = file.readline().strip().split(',')
        filas = file.readlines()
        for fila in filas:
            values = fila.strip().split(',')
            data.append(dict(zip(keys, values)))
    return data

def check_file(file_path: str):
    """funcion que verifica si el archivo existe. 
    Primero verifica que exista en el directorio './data/',
    si no existe, verifica que exista en el directorio actual.
    Si tampoco lo encuentre, avisa y termina el programa.
    """
    file_path = getcwd() + file_path
    if isfile(file_path):
        return file_path
    file_without_directory = file_path.split('/')[-1]
    if isfile(file_without_directory):
        return file_without_directory
    class_data = file_without_directory.split('.')[0]
    exit(f'Data for {class_data} entity not found. Set file name in the {class_data}.py file.')

def inside(min_max: tuple[int, int], value: int) -> int:
    """Si el valor esta fuera del intervalo, devuelve el 
    maximo o el minimo, dependiendo el caso
    """
    return max(min(value, min_max[1]), min_max[0])
    


def main():
    from torneo import Torneo
    from arena import Normal, Mojada, Magnetica, Rocosa
    from item import Tesoro, Consumible
    from excavador import Tareo, Docencio, Hibrido

    excavador1 = Tareo(**{
        'nombre': 'Tareo',
        'edad': 20
    })
    excavador2 = Docencio(**{
        'nombre': 'Docencio',
        'edad': 21
    })
    excavador3 = Hibrido(**{
        'nombre': 'Hibrido',
        'edad': 22
    })
    equipo = [
        excavador1,
        excavador2,
        excavador3
    ]

    arena = Normal(**{
        'nombre': 'Garden',
        'dificultad': 1,
        'color': 'verde'
    })

    tesoro1 = Tesoro(**{
        'nombre': 'cofre',
        'valor': 100
    })
    tesoro2 = Tesoro(**{
        'nombre': 'botiquin',
        'valor': 50
    })
    consumible1 = Consumible(**{
        'nombre': 'pocion',
        'valor': 10
    })
    consumible2 = Consumible(**{
        'nombre': 'elixir',
        'valor': 20
    })
    mochila = [
        tesoro1,
        tesoro2,
        consumible1,
        consumible2
    ]

    torneo = Torneo(
        arena=arena,
        equipo=equipo,
        mochila=mochila
    )
    r_torneo = str(torneo)
    print('TORNEO:\n')
    print(r_torneo)
    print('------------------------')
    # t = parse_object(r_torneo)
    
    file_name = 'partida'
    guardar_partida(torneo, file_name)

    t = cargar_partida(file_name + '.txt')
    print(t.arena.nombre)
    print(t.equipo[0].nombre)
    print(t.mochila[3].valor)

    # with open(getcwd() + '/Partidas/partida.txt', 'r') as file:
    #     data = ''.join(file.readlines())
    # print(data)
    # t = parse_object(data)

    # print(t)

def main2():
    a = 1039293
    a1 = inside((1, 10), a)
    print(a1)


if __name__ == '__main__':
    main2()