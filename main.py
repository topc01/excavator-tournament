from abc import ABC
from os import getcwd, listdir
from random import choice, sample
import functions as f
import parametros as p
from torneo import Torneo
from excavador import excavadores
from item import Tesoro, Consumible, consumibles, tesoros
from arena import arenas
"""
TODO: que menu item use super().__call__() para imprimir el menu
"""

FOLDER = getcwd() + '/Partidas/'
# FOLDER = getcwd() + '/Partidas_test/'

items = consumibles + tesoros

class Main(ABC):
    """base para la clase de menu
    
    Attributes:
    -----------
    __partidas : list[str]
        lista con los nombres de los archivos donde se guardaron
        las partidas

    Methods:
    --------
    sync_partidas()
        sincroniza la lista con las partidas.
        Llamar despues de guardar un nuevo archivo
    validar_input(opcion: str)
        verifica que la opcion este entre los valores permitidos
        y llama a run() para ejecutar la accion
    __call__()
        imprime el menu y pide la opcion
    run(opcion: str)
        ejecuta la accion correspondiente a la opcion ingresada.
        Se sobreescribe en clases heredadas
    """
    __partidas = []
    for file in listdir(FOLDER):
        if file.endswith('.txt'):
            __partidas.append(file)

    @property
    def partidas(self):
        return self.__partidas

    def sync_partidas(self):
        Main. __partidas = []
        for file in listdir(FOLDER):
            if file.endswith('.txt'):
                Main.__partidas.append(file)
        
    def validar_input(self, opt: str) -> None:
        if opt == 'X':
            print('Cerrando juego...')
            exit(0)
        if opt.isnumeric() and (1 <= int(opt) <= len(self.opciones)):
            self.run(opt)
            return
        print('\nOpcion no valida')
        self.__call__()
    
    def __call__(self, extra_info: str = '') -> None:
        print('\n*** ' + self.name +' ***\n' + '-'*(len(self.name) + 8))
        print(extra_info, end='')
        input_msg = 'Indique su opcion ('
        for i, opcion in enumerate(self.opciones):
            print(f'[{i+1}] {opcion}')
            input_msg += str(i+1) + ', '
        input_msg = input_msg[:-2]
        input_msg += ' o X): '
        print('[X] Salir')
        usr_input = input(input_msg)
        self.validar_input(opt=usr_input)
    
    def run(self, opt):
        self.__getattribute__('_' + opt)()


class MenuInicio(Main):
    def __init__(self) -> None:
        self.name = 'Menu de Inicio'
        self.opciones = [
            'Nueva partida', 
            'Cargar partida'
        ]

    def _1(self):
        MenuPrincipal(torneo=None)()

    def _2(self):
        MenuCarga()()

class MenuPrincipal(Main):
    def __init__(self, torneo: Torneo = None) -> None:
        self.name = 'Menu Principal'
        self.opciones = [
            'Simular dia torneo',
            'Ver estado torneo',
            'Ver items',
            'Guardar partida',
            'Volver'
        ]
        if torneo is None:
            arena = choice(list(filter(lambda a: a.tipo == p.ARENA_INICIAL, arenas)))
            equipo = sample(excavadores, k=p.CANTIDAD_EXCAVADORES_INICIALES)
            self.partida_actual = Torneo(arena=arena, equipo=equipo)
        else:
            self.partida_actual = torneo

    def resumen(self):
        dia = self.partida_actual.dias_transcurridos
        dias_totales = self.partida_actual.dias_totales
        tipo_arena = self.partida_actual.tipo_arena
        return f'Dia torneo DCCavaCava: {dia}/{dias_totales}\nTipo de arena: {tipo_arena.title()}\n\n'
    
    def __call__(self, info_resumen: str = None) -> None:
        if info_resumen is None:
            info_resumen = self.resumen()
        return super().__call__(extra_info=info_resumen)
    
    def run(self, opt):
        super().run(opt)
        MenuPrincipal(torneo=self.partida_actual)()

    def _1(self):
        self.partida_actual.simular_dia(items)
    
    def _2(self):
        self.partida_actual.mostrar_estado()
    
    def _3(self):
        MenuItems(self.partida_actual)()
        
    def _4(self):
        f.guardar_partida(self.partida_actual)
        super().sync_partidas()

    def _5(self):
        MenuInicio()()
        
class MenuCarga(Main):
    def __init__(self) -> None:
        self.name = 'Menu de carga'
        self.opciones = list(map(
            lambda x: x.split('.')[0],
            self.partidas
        ))
        self.opciones += ['Volver']

    def run(self, opt):
        if opt == str(len(self.opciones)):
            MenuInicio()()
        file_name = self.partidas[int(opt)-1].split('.')[0]
        print(f'Cargando partida numero {opt}: {file_name}')
        torneo = f.cargar_partida(file_name+'.txt')
        MenuPrincipal(torneo=torneo)()

class MenuItems(MenuPrincipal):
    def __init__(self, torneo) -> None:
        super().__init__()
        self.partida_actual = torneo
        self.opciones = self.partida_actual.mochila + ['Volver']

    def run(self, opt):
        if opt == str(len(self.partida_actual.mochila)+1):
            MenuPrincipal(torneo=self.partida_actual)()
        item_elegido = self.partida_actual.mochila[int(opt)-1]
        print(f'Item {opt}: {getattr(item_elegido, "nombre")}')
        changed_arena = None
        if isinstance(item_elegido, Tesoro):
            changed_arena = self.partida_actual.abrir_tesoro(item_elegido, excavadores)
        elif isinstance(item_elegido, Consumible):
            self.partida_actual.usar_consumible(item_elegido)
        if changed_arena is not None:
            new_torneo = Torneo(arena=changed_arena, equipo=self.partida_actual.equipo, tipo_arena=changed_arena.get('tipo'))
        else:
            new_torneo = self.partida_actual
        MenuItems(new_torneo)()

    def __call__(self) -> None:
        input_msg = 'Indique su opcion ('
        torneo = self.partida_actual
        if not len(torneo.mochila):
            print('\nmochila vacia')
            # print(torneo.mochila)
            return
        largo = {
            'nombre': len(max(torneo.mochila, key=lambda item: len(item.nombre)).nombre),
            'tipo': len(max(torneo.mochila, key=lambda item: len(item.tipo)).tipo),
            'descripcion': len(max(torneo.mochila, key=lambda item: len(item.descripcion)).descripcion)
        }
        largo_tabla = sum(largo.values()) + 10
        print()
        print('*** Menu Items ***'.center(largo_tabla))
        print('-'*largo_tabla)
        print(' '*(5), end='')
        print(*[attr.center(l) for attr, l in largo.items()], sep=' | ')
        print('-'*largo_tabla)
        for i, item in enumerate(torneo.mochila):
            if i < 9:
                index = f'[{i+1}] '
            else:
                index = f'[{i+1}]'
            print(index, end=' ')
            input_msg += str(i+1) + ', '
            print(*[str(item.get(attr)).center(l) for attr, l in largo.items()], sep=' | ')
        print('-'*largo_tabla)
        print(f'[{len(torneo.mochila)+1}] Volver')
        input_msg = input_msg[:-2]
        input_msg += f', {len(torneo.mochila)+1} o X): '
        print('[X] Salir')
        usr_input = input(input_msg)
        self.validar_input(opt=usr_input)
        

if __name__ == '__main__':
    print()
    MenuInicio()()

