import cv2
import pytesseract
import os

# Configure o caminho do executável do Tesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Users\italo\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'


def process_image(file_path, output_folder):
    # Carregar a imagem
    image = cv2.imread(file_path)

    if image is None:
        print(f"Erro ao carregar a imagem: {file_path}")
        return

    # Dimensões da imagem
    height, width, _ = image.shape

    # Dividir a imagem em 2 partes horizontais
    half_height = height // 2
    upper_part = image[0:half_height, :]
    lower_part = image[half_height:height, :]

    # Processar cada parte
    for i, part in enumerate([upper_part, lower_part]):
        # Converter para escala de cinza
        gray_part = cv2.cvtColor(part, cv2.COLOR_BGR2GRAY)
        _, thresh_part = cv2.threshold(gray_part, 50, 255, cv2.THRESH_BINARY)
        contours, _ = cv2.findContours(thresh_part, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Verificar se há contornos de 4 lados
        for contour in contours:
            approx = cv2.approxPolyDP(contour, 0.02 * cv2.arcLength(contour, True), True)
            if len(approx) == 4:
                # Se houver contornos de 4 lados, reduzir a altura da imagem
                new_height = part.shape[0] // 2
                part = part[0:new_height, :]
                break

        # Salvar a parte da imagem
        part_output_path = os.path.join(output_folder,
                                        f"{os.path.splitext(os.path.basename(file_path))[0]}_part_{i + 1}.png")
        cv2.imwrite(part_output_path, part)

        # Aplicar OCR na parte processada
        text = pytesseract.image_to_string(part, config='--psm 7')
        print(f'OCR Resultado para parte {i + 1} da imagem {file_path}: {text}')


# Caminho da imagem individual
image_path = r'C:\Users\italo\PycharmProjects\Leitor de cd barras e numerico\imagens\SegundoLeitor.png'
output_folder = r'C:\Users\italo\PycharmProjects\Leitor de cd barras e numerico\Recortes'

# Criar a pasta de saída se não existir
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Processar a imagem individualmente
process_image(image_path, output_folder)
