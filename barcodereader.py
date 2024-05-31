from pyzbar.pyzbar import decode
import cv2
from PIL import Image
import os


def BarcodeReader(image_path):
    if not os.path.exists(image_path):
        raise FileExistsError(f"O arquivo {image_path} não foi encontrado.")

    img = Image.open(image_path)
    detectedbardecode = decode(img)

    if not detectedbardecode:
        return False
    else:
        for barcode in detectedbardecode:
            if barcode.data != "" and barcode.type == "CODE128":
               return barcode.data.decode('utf-8')


if __name__ == '__main__':
    # Lista todos os arquivos de imagem no diretório atual
    imagens = [i for i in os.listdir() if i.lower().endswith('.jpg')]

    # Itera sobre cada imagem e decodifica os códigos de barras
    for imagem in imagens:
        print(f"Lendo a imagem: {imagem}, ", BarcodeReader(imagem))

