#Tamñano y escalas
HEIGHT_WINDOW  = 1080  #Alto 
WIDHT_WINDOW = 1920    #Ancho
#HEIGHT_PERSONAJE = 20 
#WIDHT_PERSONAJE = 20 
SCALE_PERSONAJE = 1.45
SCALE_ENEMIGOS = 1.4
SCALE_ARMA = 0.8
SCALE_BALA = 0.15
SCALE_CORAZON = 3
SCALE_POSION = 0.8
SCALE_MONEDA = 1.3
SCALE_PORTAL = 1.5
TILE_SIZE = 40 
TILE_TYPE = 1920       #ES LA CANTIDAD DE TILES QUE SE TIENE EN LA CARPETA 
FILAS = 240 
COLUMNAS = 240 
LIMITE_PANTALLA_X = 920        #Jugamos con esto, modifica en que momento se movera la camara para seguir al personaje 
LIMITE_PANTALLA_Y = 500        #Jugamos con esto, modifica en que momento se movera la camara para seguir al personaje 

#Colores
COLOR_PERSONAJE= (255, 255, 0)
COLOR_ARMA = (255, 0, 0)
COLOR_BG = (0, 0, 20)  #Color del fondo
ROJO = (203, 50, 52)
AMARILLO = (255, 255, 0)
BLANCO = (255, 255, 255)
ROJO_OSCURO = (139, 0, 0)
NEGRO = (0, 0, 0)
AMARILLO = (255, 255, 0)
COLOR_FONDO = (0, 0, 0)

#Fondos
BACKGROUND_MENU_INICIO = "assets/images/fondo/menu.png"
BACKGROUND_GAME_OVER = "assets/images/fondo/game_over.png"
BACKGROUND_WIN = "assets/images/fondo/win.png"

#Otros 
VELOCIDAD = 15  #Velocidad del personaje
VELOCIDAD_ENEMIGOS = 5 #Velocidad de los enemigos 
RANGO = 4000    #Que usaremos para determinar hasta que punto los enemigos nos detectan
RANGO_ATAQUE = 100 #Distancia a al que los enemigos empezaran a atacar 
VELOCIDAD_BALAS = 40
COOLDOWN_BALAS = 200
FPS = 120
COORDENADAS = {"1":(800,2200), "2":(800,2200), "3":(800,2200)}  #Creamos una constante que este guardando las coordenadas donde queremos que aparezca nuestro personaje 
NIVEL_MAXIMO = 2