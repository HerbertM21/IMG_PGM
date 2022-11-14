import numpy as np
import PIL as pil
from PIL import Image

def CreaImagen():
    imagen = {
        'magica': 'XX',   # P2 o P5
        'comentario': [], # lista de comentarios
        'ancho': 0,      # ancho de la imagen
        'alto': 0,      # alto de la imagen
        'gris': 0,     # numero de grises
        'pixeles': []   # lista de pixeles
    }
    return imagen

def LeerImagen(nombre):
    im = open(nombre) 
    magica = im.readline().rstrip('\n')  # lee la primera linea
    comentario = [] # lista de comentarios
    linea = im.readline().rstrip('\n') # lee la segunda linea
    while linea[0] == '#': 
        comentario.append(linea)
        linea = im.readline().rstrip('\n')
    sep = ' '
    dimension = linea.split(sep) # ejemplo: ['512', '512']
    ancho = int(dimension[0])  # ancho de la imagen
    if len(dimension[1]) == 0: # si no hay espacio en blanco
        alto = int(dimension[2]) # alto de la imagen    
    else: 
        alto = int(dimension[1]) # alto de la imagen 
    grises = int(im.readline().rstrip('\n'))
    pixeles = []
    for linea in im: 
        linea = linea.rstrip('\n') # quitar el salto de linea
        lista = linea.split(' ')
        for pixel in lista:
            if pixel != '':
                pixeles.append(int(pixel)) 
    imagen = CreaImagen()
    imagen['magica'] = magica
    imagen['comentario'] = comentario[:]
    imagen['ancho'] = ancho
    imagen['alto'] = alto
    imagen['gris'] = grises
    imagen['pixeles'] = pixeles[:]
    im.close()
    return imagen

def GuardarImagen(imagen, nombre):
    im = open(nombre, 'w') 
    im.write(imagen['magica']+'\n')
    for linea in imagen['comentario']:
        im.write(linea+'\n')
    im.write(str(imagen['ancho'])+' '+str(imagen['alto'])+'\n')
    im.write(str(imagen['gris'])+'\n')    
    for pixel in imagen['pixeles']:
        im.write(str(pixel)+' ')
    im.close()
    

def DisminuirTamano(imagen, factor):
    ancho = imagen['ancho']
    alto = imagen['alto']
    pixeles = imagen['pixeles'] # lista de pixeles
    pixeles = np.array(pixeles)  # convertir a array
    pixeles = pixeles.reshape(alto, ancho) # convertir a matriz
    pixeles = pixeles[::factor, ::factor] # 
    pixeles = pixeles.flatten() # convertir a lista
    imagen['ancho'] = int(ancho/factor) # actualizar ancho
    imagen['alto'] = int(alto/factor) # actualizar alto
    imagen['pixeles'] = pixeles[:] # actualizar pixeles
    return imagen

def AumentarTamano(imagen, factor):
    ancho = imagen['ancho']
    alto = imagen['alto']
    pixeles = imagen['pixeles']
    pixeles = np.array(pixeles)
    pixeles = pixeles.reshape(alto, ancho)
    pixeles = np.repeat(pixeles, factor, axis=0) # duplica filas
    pixeles = np.repeat(pixeles, factor, axis=1) # duplica columnas
    pixeles = pixeles.flatten()
    imagen['ancho'] = int(ancho*factor)
    imagen['alto'] = int(alto*factor)
    imagen['pixeles'] = pixeles[:]
    return imagen

def RotarImagen45(imagen):
    ancho = imagen['ancho']
    alto = imagen['alto']
    pixeles = imagen['pixeles']
    pixeles = np.array(pixeles) # convertir a numpy array
    pixeles = pixeles.reshape(alto, ancho) # convertir a matriz
    imagenR1 = Image.fromarray(pixeles) # convertir a imagen con pillow
    imagenR2 = imagenR1.rotate(45) # rotar la imagen 45 grados
    pixeles = np.array(imagenR2) # Convertir la imagen rotada a una array
    pixeles = pixeles.flatten() # convertir a lista
    imagen['ancho'] = int(ancho)
    imagen['alto'] = int(alto)
    imagen['pixeles'] = pixeles[:]
    return imagen


def main():
    imagen = LeerImagen('Lena.pgm')
    imagen = DisminuirTamano(imagen, 2)
    GuardarImagen(imagen, 'lenaMinimizada.pgm')
    imagen = AumentarTamano(imagen, 2)
    GuardarImagen(imagen, 'lenaAumentada.pgm')
    imagen = RotarImagen45(imagen)
    GuardarImagen(imagen, 'lenaRotada45.pgm')
    
if __name__ == '__main__':
    main()
    