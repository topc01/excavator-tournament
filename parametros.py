# Setup
DIAS_TOTALES_TORNEO = 12
ARENA_INICIAL = 'normal'
CANTIDAD_EXCAVADORES_INICIALES = 3
METROS_META = 42

# Probabilidades de eventos
PROB_INICIAR_EVENTO = 0.5
PROB_LLUVIA = 0.5
PROB_TERREMOTO = 0.2
PROB_DERRUMBE = 1 - PROB_LLUVIA - PROB_TERREMOTO

# Consecuencias de eventos
METROS_PERDIDO_DERRUMBE = 3.0
FELICIDAD_PERDIDA = 1

# Probabilidades de encontrar item
PROB_ENCONTRAR_ITEM = 0.4
PROB_ENCONTRAR_TESORO = 0.3
PROB_ENCONTRAR_CONSUMIBLE = 1 - PROB_ENCONTRAR_TESORO

# Arena
POND_ARENA_NORMAL = 0.8

# Excavador Docencio
FELICIDAD_ADICIONAL_DOCENCIO = 1
FUERZA_ADICIONAL_DOCENCIO = 2
ENERGIA_PERDIDA_DOCENCIO = 15

# Excavador Tareo
ENERGIA_ADICIONAL_TAREO = 8
SUERTE_ADICIONAL_TAREO = 2
EDAD_ADICIONAL_TAREO = 1
FELICIDAD_PERDIDA_TAREO = 1
