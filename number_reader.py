import cv2
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Users\italo\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'
img_path = "imagens/SegundoLeitor.png"

imag = cv2.imread(img_path)

cinza = cv2.cvtColor(imag, cv2.COLOR_BGR2GRAY)

_, img_binaria = cv2.threshold(cinza, 55, 255, cv2.THRESH_BINARY_INV)

desfoque = cv2.GaussianBlur(img_binaria,(5,5),0)

contorno, hier= cv2.findContours(desfoque, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
#cv2.drawContours(imag, contorno,-1,(0,255,0),2)
min_largura = 200
max_largura = 400
min_altura = 20
max_altura = 50


for con in contorno:
    perimetro = cv2.arcLength(con, True)
    aprox = cv2.approxPolyDP(con, 0.02 * perimetro, True)
    if len(aprox) != 4:
        (x, y, lar, alt) = cv2.boundingRect(aprox)
        area = lar * alt
        # Filtrar os retângulos com base em largura, altura e área
        if min_largura < lar < max_largura and min_altura < alt < max_altura:
            recorte = imag[y:y + alt, x:x + lar]
            # Salvar a imagem recortada
            cv2.imwrite('Recortes/recorte.png', recorte)
            cv2.rectangle(imag, (x, y), (x + lar, y + alt), (0, 255, 0), 2)

def preprocessamento():
    img_re = cv2.imread("Recortes/recorte.png")

    if img_re is None:
        return

    resize_img_roi = cv2.resize(img_re, None, fx=4, fy=4, interpolation=cv2.INTER_CUBIC)

    # Converte para escala de cinza
    img_cinza = cv2.cvtColor(resize_img_roi, cv2.COLOR_BGR2GRAY)

    # Binariza imagem
    _, img_binary = cv2.threshold(img_cinza, 70, 255, cv2.THRESH_BINARY_INV)

    # Desfoque na Imagem
    img_desfoque = cv2.GaussianBlur(img_binary, (5, 5), 0)

    # Grava o pre-processamento para o OCR
    cv2.imwrite("Recortes/recorte.png", img_desfoque)

    return img_desfoque

preprocessamento()
def oCR():
    img = cv2.imread('Recortes/recorte.png')
    config = r'-c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 --psm 6'
    text = pytesseract.image_to_string(img, lang='eng', config=config)
    print(f'OCR Resultado da imagem : {text}')

oCR()
if __name__ == '__main__':
    if imag is None:
        print("Não carregou a imagem")
    else:
        print("Imagem carregada")

        cv2.imshow("Imagem de teste",imag)
        cv2.waitKey(0)
        cv2.destroyAllWindows()