# Tarea 1: DCCavaCava 🏖⛏


Un buen ```README.md``` puede marcar una gran diferencia en la facilidad con la que corregimos una tarea, y consecuentemente cómo funciona su programa, por lo en general, entre más ordenado y limpio sea éste, mejor será 

Para nuestra suerte, GitHub soporta el formato [MarkDown](https://es.wikipedia.org/wiki/Markdown), el cual permite utilizar una amplia variedad de estilos de texto, tanto para resaltar cosas importantes como para separar ideas o poner código de manera ordenada ([pueden ver casi todas las funcionalidades que incluye aquí](https://github.com/adam-p/markdown-here/wiki/Markdown-Cheatsheet))

Un buen ```README.md``` no tiene por que ser muy extenso tampoco, hay que ser **concisos** (a menos que lo consideren necesario) pero **tampoco pueden** faltar cosas. Lo importante es que sea claro y limpio 

**Dejar claro lo que NO pudieron implementar y lo que no funciona a la perfección. Esto puede sonar innecesario pero permite que el ayudante se enfoque en lo que sí podría subir su puntaje.**

## Consideraciones generales :octocat:

<Descripción de lo que hace y que **_no_** hace la tarea que entregaron junto
con detalles de último minuto y consideraciones como por ejemplo cambiar algo
en cierta línea del código o comentar una función>

### Cosas implementadas y no implementadas :white_check_mark: :x:

Explicación: mantén el emoji correspondiente, de manera honesta, para cada item. Si quieres, también puedes agregarlos a los títulos:
- ❌ si **NO** completaste lo pedido
- ✅ si completaste **correctamente** lo pedido
- 🟠 si el item está **incompleto** o tiene algunos errores

**⚠️⚠️NO BASTA CON SOLO PONER EL COLOR DE LO IMPLEMENTADO**,
SINO QUE SE DEBERÁ EXPLICAR QUÉ SE REALIZO DETALLADAMENTE EN CADA ITEM.
⚠️⚠️

#### Programación Orientada a Objetos: 42 pts (35%)
##### ✅  Diagrama
##### ✅ Definición de clases, atributos, métodos y properties. >> Las definiciones estan en los archivos
##### ✅ Relaciones entre clases >> Se definen en el diagrama
#### Preparación programa: 11 pts (9%)
##### ✅ Creación de partidas
#### Entidades: 22 pts (18%)
##### ✅ Excavador
##### ✅ Arena
##### ✅ Torneo
#### Flujo del programa: 31 pts (26%)
##### ✅ Menú de Inicio
##### ✅ Menú Principal
##### ✅ Simulación día Torneo
##### ✅ Mostrar estado torneo
##### ✅ Menú Ítems
##### ✅ Guardar partida
##### ✅ Robustez
#### Manejo de archivos: 14 pts (12%)
##### ✅ Archivos CSV 
##### ✅ Archivos TXT
##### ✅ parametros.py
#### Bonus: 3 décimas máximo
##### ✅ Guardar Partida

## Ejecución :computer:
El módulo principal de la tarea a ejecutar es  ```main.py```. Además se debe crear los siguientes archivos y directorios adicionales:
1. ```tesoros.csv``` en ```data```, o en el directorio actual
2. ```consumibles.csv``` en ```data```, o en el directorio actual
3. ```arenas.csv``` en ```data```, o en el directorio actual
4. ```excavadores.csv``` en ```data```, o en el directorio actual


## Librerías :books:
### Librerías externas utilizadas
La lista de librerías externas que utilicé fue la siguiente:

1. ```abc```: ```ABC``` 
2. ```random```: ```choice()```, ```sample()```, ```random()```, ```randint()```
3. ```os```: ```getcwd()```, ```listdir()```
4. ```os.path```: ```isfile()```

### Librerías propias
Por otro lado, los módulos que fueron creados fueron los siguientes:

1. ```torneo```: Hecha para la clase ```Torneo```, que usa a todas las otras clases.
2. ```item```: Contiene a ```Item```, ```Tesoro```, ```Consumible```.
3. ```arena```: Contiene a la clase abstracta ```Arena``` y sus cuatro clases derivadas: ```Normal```, ```Mojada```, ```Rocosa``` y ```Magnetica```.
4. ```excavador```: Contiene a la clase abstracta ```Excavador``` y sus tres clases derivadas: ```Tareo```, ```Docencio``` e ```Hibrido```.
5. ```functions```: Contiene a la clase base ```ObjectFromCSV```, que permite crear los atributos de las clases a partir de un diccionario, ```parse_object``` que recibe un cierto tipo de string y devuelve un objeto, una funcion que lee un csv y devuelve un diccionario, otras funciones que permiten guardar y cargar partidas, una funcion que verifica que los archivos con los datos existan, y otras funciones utiles.
6. ```main```: Hecha para crear las clases de los menus. Contiene a la clase abstracta ```Main```, de la que heredan ```MenuInicio```, ```MenuCarga``` y ```MenuPrincipal```. De esta ultima hereda ```MenuItems```.

## Supuestos y consideraciones adicionales :thinking:
Los supuestos que realicé durante la tarea son los siguientes:

1. Si la mochila tiene más de 10 items, no se van a seguir encontrando items

-------



**EXTRA:** si van a explicar qué hace específicamente un método, no lo coloquen en el README mismo. Pueden hacerlo directamente comentando el método en su archivo. Por ejemplo:

```python
class Corrector:

    def __init__(self):
          pass

    # Este método coloca un 6 en las tareas que recibe
    def corregir(self, tarea):
        tarea.nota  = 6
        return tarea
```

Si quieren ser más formales, pueden usar alguna convención de documentación. Google tiene la suya, Python tiene otra y hay muchas más. La de Python es la [PEP287, conocida como reST](https://www.python.org/dev/peps/pep-0287/). Lo más básico es documentar así:

```python
def funcion(argumento):
    """
    Mi función hace X con el argumento
    """
    return argumento_modificado
```
Lo importante es que expliquen qué hace la función y que si saben que alguna parte puede quedar complicada de entender o tienen alguna función mágica usen los comentarios/documentación para que el ayudante entienda sus intenciones.

## Referencias de código externo :book:

Para realizar mi tarea saqué código de:
1. \<link de código>: este hace \<lo que hace> y está implementado en el archivo <nombre.py> en las líneas <número de líneas> y hace <explicación breve de que hace>

## Descuentos
La guía de descuentos se encuentra [link](https://github.com/IIC2233/syllabus/blob/main/Tareas/Descuentos.md).
