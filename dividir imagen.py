from PIL import Image
import os

def dividir_guardar_imagen(ruta_imagen, carpeta_destino, divisiones_por_columna):
    #Cargar la imagen
    with Image.open(ruta_imagen) as img:
        ancho, alto = img.size#Creamos una variable donde se almacene las dimenciones de la imagen 
        print(ancho, alto)   

        #Calcular el numero de divisiones por fila para mantener la forma cuadrada
        tamaño_cuadrado = ancho // divisiones_por_columna  #Cuando ponemos "//" le estamos diciendo que es una division entera
        divisiones_por_fila = alto // tamaño_cuadrado 

        #Crear la carpeta de destino si no existe
        os.makedirs(carpeta_destino, exist_ok=True)

        #Dividir y guardar cada tiled
        contador = 0
        for i in range(divisiones_por_fila):
            for j in range(divisiones_por_columna):
                #Coordenadas del cuadrado
                izquierda = j * tamaño_cuadrado
                superior = i * tamaño_cuadrado
                derecha = izquierda + tamaño_cuadrado
                inferior = superior + tamaño_cuadrado

                #Cortar y guardar el cuadrado
                cuadrado = img.crop((izquierda, superior, derecha, inferior))
                nombre_archivo = f"tile ({contador+1}).png" 
                cuadrado.save(os.path.join(carpeta_destino, nombre_archivo))
                contador += 1

print(os.getcwd())
dividir_guardar_imagen("assets//images//tiles//tile_definitivo.png ", "assets//images//tiles", 48)  #IMPORTANTE COLOCAR BIEN LA CANTIDAD DE COLUMNAS, SIEMPRE ES UNA MAS QUE EN TILED   #Dungeon_Tileset.png    mainlevbuild.png


