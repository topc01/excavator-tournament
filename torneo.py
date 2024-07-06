import parametros as p
from functions import ObjectFromCSV
from arena import Arena
from excavador import Excavador
from item import Tesoro, Consumible
from random import random, choice
"""
TODO: cavar
TODO: dias de descanso
"""
class Torneo(ObjectFromCSV):
    """clase Torneo

    Attributes:
    -----------
    arena : Arena
        arena actual
    equipo : list[Excavadores]
        conjunto de todos los excavadores
    mochila : list[Item]
        conjunto de todos los items encontrados
    metros_cavados : float
        cantidad de metros cavados hasta el momento
    meta : float parametros.METROS_META
        cantidad de metros a superar
    dias_transcurridos : int
        dia actual en la competencia
    dias_totales : int parametros.DIAS_TOTALES_TORNEO
        cuantos dias durara el torneo

    Methods:
    --------
    simular_dia()
        simula un dia de excavaciones
    mostrar_estado()
        muestra el estado actual del torneo
    ver_mochila()
        muestra todos los items que se tienen en la mochila
    usar_consumible()
        para cada excavador se aplican los efectos del consumible
    abrir_tesoro()
        se activa el efecto del tesoro encontrado
    iniciar_evento()
        cada dia hay una probabilidad de que ocurra un evento que afecta
        a la arena y los excavadores
    lluvia()
        transforma la arena normal a mojada, y la rocosa a magnetica
    terremoto()
        transforma la arena normal a rocosa, y la mojada a magnetica
    derrumbe()
        transforma cualquier tipo de arena a normal.
        El equipo pierde METROS_PERDIDOS_DERRUMBRE metros de progreso
    """
    def __init__(self,
                arena: Arena,
                equipo: list[Excavador],
                # eventos = [],
                mochila: list[Tesoro | Consumible] = [],
                tipo_arena = p.ARENA_INICIAL,
                metros_cavados = 0,
                meta = p.METROS_META,
                dias_transcurridos = 1,
                dias_totales = p.DIAS_TOTALES_TORNEO) -> None:
        self.arena = arena
        self.equipo = equipo
        # self.eventos = eventos
        self.mochila = mochila
        self.tipo_arena = tipo_arena
        self._metros_cavados = metros_cavados
        self.meta = meta
        self.dias_transcurridos = dias_transcurridos
        self.dias_totales = dias_totales
    
    @property
    def metros_cavados(self):
        return self._metros_cavados
    
    @metros_cavados.setter
    def metros_cavados(self, value):
        # print('====> metros iniciales:', self._metros_cavados)
        self._metros_cavados = value
        # print('====> metros finales:', self._metros_cavados)

    def __str__(self) -> str:
        data = f'{str(self.arena)}\n'
        for i, excavador in enumerate(self.equipo):
            data += str(excavador) + ' | ' * (i < len(self.equipo)-1) # si no es el ultimo, agrega un separador
        data += '\n'
        for i, item in enumerate(self.mochila):
            data += str(item) + ' | ' * (i < len(self.mochila)-1) # si no es el ultimo, agrega un separador
        data += '\n'
        data += f'{self.tipo_arena}\n'
        data += f'{self.metros_cavados}\n'
        data += f'{self.meta}\n'
        data += f'{self.dias_transcurridos}\n'
        data += f'{self.dias_totales}'
        return data 
   
    def simular_dia(self, items: list[Tesoro | Consumible]):
        """ 
        cavar:
            cada excavador que no este descansando tiene que cavar y
            mostrar la cantidad de metros. Si esta descansando se debe
            mostrar.
            Se muestra la cantidad de metros totales cavados en el dia

        encontrar item:
            se muestra el nombre de cada excavador y si consiguio o no algun item,
            dependiendo de PROB_ENCONTRAR_ITEM.
            Muestra el nombre y tipo del item encontrado, depende de
            PROB_ENCONTRAR_TESORO y PROB_ENCONTRAR_CONSUMIBLE.
            Muestra la cantidad de items encontrados en el dia, especifica la
            cantidad de consumibles y tesoros

        ocurrencia evento:
            cada dia tiene una probabilidad PROB_INICIAR_EVENTO de que ocurra un evento.
            Muestra tipo de evento (depende de PROB_LLUVIA, PROB_TERREMOTO y PROB_DERRUMBE),
            tipo de arena resultante y efectos en el equipo

        """
        if self.tipo_arena == 'magnetica':
            if self.arena.get('tipo') != 'magnetica':
                raise 'Error, tipo de arena no coincide'
            self.arena.next_day()

        # CAVAR
        print('\nMetros cavados:')
        metros_totales = 0
        for excavador in self.equipo:
            print(excavador.get('nombre'), end=' ')
            if excavador.dias_descanso > 0:
                print('esta descansando')
                excavador.descanso()
                continue
            metros = excavador.cavar(self.arena.get('dificultad'))
            # if metros > 15:
            #     print(repr(excavador), self.arena.get('dificultad'), metros)
            print('ha cavado', metros, 'metros.', end=' ')
            excavador.gastar_energia()
            if excavador.energia == 0:
                dias = excavador.descansar()
                print(f'Se ha quedado sin energia y debe descansar {dias} dia{"s" if dias > 1 else ""}', end='')
            print()
            metros_totales += metros
        print(f'El equipo ha conseguido excavar {metros_totales} metros')
        self.metros_cavados += metros_totales

        # ENCONTRAR ITEM
        if len(self.mochila) > 10:
            print('\nLa mochila esta llena, no se pueden encontrar mas items')
        else:
            print('\nItems encontrados:')
            cantidad_tesoros = 0
            cantidad_consumibles = 0
            for excavador in self.equipo:
                print(excavador.get('nombre'), end=' ')
                if self.tipo_arena not in ('mojada', 'magnetica') and random() > self.arena.PROB_ENCONTRAR_ITEM:
                    print('no consiguio nada')
                    continue
                prob = random()
                if prob <= p.PROB_ENCONTRAR_TESORO or (self.tipo_arena in ('mojada', 'magnetica') and prob < 0.5):
                    item_obtenido = choice(list(filter(lambda item: item.tipo == 'tesoro', items)))
                    cantidad_tesoros += 1
                else:
                    item_obtenido = choice(list(filter(lambda item: item.tipo == 'consumible', items)))
                    cantidad_consumibles += 1
                print('consiguio', item_obtenido.get('nombre'), 'del tipo', item_obtenido.tipo)
                self.mochila.append(item_obtenido)
            cantidad_total = cantidad_consumibles + cantidad_tesoros
            print(f"Se ha{'n'*(cantidad_total > 1)} encontrado {cantidad_total} item{'s'*(cantidad_total > 1)}:")
            print(f'- {cantidad_consumibles} consumibles.')
            print(f'- {cantidad_tesoros} tesoros.')

        # EVENTO
        print()
        if random() <= p.PROB_INICIAR_EVENTO:
            self.iniciar_evento()
            for excavador in self.equipo:
                excavador.felicidad -= p.FELICIDAD_PERDIDA
    
        self.dias_transcurridos += 1
        self.check()
        # print('dias:', self.dias_transcurridos)

    def mostrar_estado(self):
        largo = {
            'nombre': len(max(self.equipo, key=lambda excavador: len(excavador.nombre)).nombre),
            'tipo': len(max(self.equipo, key=lambda excavador: len(excavador.tipo)).tipo),
            'edad': 4,
            'energia': 7,
            'fuerza': 6,
            'suerte': 6,
            'felicidad': 9
        }
        largo_tabla = sum(largo.values()) + 17
        print()
        print('*** Estado Torneo ***'.center(largo_tabla))
        print('-'*largo_tabla)
        print('Dia actual:', self.dias_transcurridos)
        print('Tipo de arena:', self.arena.get('tipo').title())
        # print(repr(self.arena))
        print(f'Metros excavados: {self.metros_cavados}/{self.meta}')
        print('-'*largo_tabla)
        print('Excavadores'.center(largo_tabla))
        print('-'*largo_tabla)
        print(*[attr.center(l) for attr, l in largo.items()], sep=' | ')
        print('-'*largo_tabla)
        for excavador in self.equipo:
            print(*[str(excavador.get(attr)).center(l) for attr, l in largo.items()], sep=' | ')
        print()

    def ver_mochila(self):
        pass

    def usar_consumible(self, item: Consumible):
        for excavador in self.equipo:
            excavador.consumir(item)
        self.mochila.remove(item)

    def abrir_tesoro(self, item: Tesoro, excavadores: list[Excavador]):
        cambio = item.get('cambio')
        if item.get('calidad') == 1:
            opciones_excavador = list(filter(lambda excavador: (excavador.get('tipo') == cambio) and (excavador not in self.equipo), excavadores))
            if len(opciones_excavador) == 0:
                print('No hay excavadores disponibles para agregar a tu equipo')
                desechar = input('¿Quieres desechar este tesoro? (s/n): ')
                if desechar == 's':
                    self.mochila.remove(item)
                return None
            excavador = choice(opciones_excavador)
            self.equipo.append(excavador)
            self.mochila.remove(item)
            return None
        elif item.get('calidad') == 2:
            if cambio == 'normal':
                arena = self.arena.to_Normal()
            elif cambio == 'mojada':
                arena = self.arena.to_Mojada()
            elif cambio == 'rocosa':
                arena = self.arena.to_Rocosa()
            elif cambio == 'magnetica':
                arena = self.arena.to_Magnetica()
        self.mochila.remove(item)
        return arena

    def iniciar_evento(self):
        # metros_cavados = self.metros_cavados
        tipo_evento = random()
        if tipo_evento <= p.PROB_LLUVIA: # LLUVIA
            print('¡¡Durante el dia de trabajo se puso a Llover!!')
            if self.tipo_arena == 'normal':
                self.tipo_arena = 'mojada'
                self.arena = self.arena.to_Mojada()
                print('La arena se ha vuelto mojada')
            elif self.tipo_arena == 'rocosa':
                self.tipo_arena = 'magnetica'
                self.arena = self.arena.to_Magnetica()
                print('La arena se ha vuelto magnetica')
        elif tipo_evento <= p.PROB_TERREMOTO: # TERREMOTO
            print('¡¡Durante el dia de trabajo ocurrio un Terremoto!!')
            if self.tipo_arena == 'normal':
                self.tipo_arena = 'rocosa'
                self.arena = self.arena.to_Rocosa()
                print('La arena se ha vuelto rocosa')
            elif self.tipo_arena == 'mojada':
                self.tipo_arena = 'magnetica'
                self.arena = self.arena.to_Magnetica()
                print('La arena se ha vuelto magnetica')
        else: # DERRUMBE
            print('¡¡Durante el dia de trabajo ocurrio un Derrumbe!!')
            if self.tipo_arena != 'normal':
                self.tipo_arena = 'normal'
                self.arena = self.arena.to_Normal()
                print('La arena se ha vuelto normal.', end=' ')
            self.metros_cavados -= p.METROS_PERDIDO_DERRUMBE
            print(f'Se han perdido {p.METROS_PERDIDO_DERRUMBE} metros')
            
    def check(self):
        if (self.dias_transcurridos < self.dias_totales) and (self.metros_cavados < self.meta):
            return
        if self.metros_cavados < self.meta:
            print(f'\n¡Se acabo el torneo!\nNo han conseguido derrotar al Dr. Pinto, faltaron {self.meta - self.metros_cavados} metros.')
            exit(0)
        print(f'\n\n¡¡Felicidades!!\nSir Hernan4444 ha derrotado al Dr. Pinto con un total de {self.metros_cavados} metros cavados.')
        exit(0)
            