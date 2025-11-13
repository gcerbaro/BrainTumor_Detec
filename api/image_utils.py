import os
from utils import log_error
from constants import IMAGE_SIZE, PADDING
import cv2
import os
import cv2
from cv2.typing import MatLike
import numpy as np

def load_img(path: str | MatLike):
  if isinstance(path, str):
    if (not os.path.exists(path)):
      log_error(f"A imagem '{path}' não existe.")
      exit(1)
    
    img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
  else:
     img = cv2.imdecode(path, cv2.IMREAD_GRAYSCALE)


  if img is None:
    log_error(f"Não foi possível carregar a imagem '{path}'.")
    exit(1)

  img = cv2.resize(img, (IMAGE_SIZE + (PADDING * 2), IMAGE_SIZE + (PADDING * 2)))
  return img

# Prepara as imagens para o modelo
def normalize_background(img: MatLike):
  region_size = 20
  h, w = img.shape

  # Pega as 4 regiões de canto
  corner_tl = img[0:region_size, 0:region_size]
  corner_tr = img[0:region_size, (w - region_size):w]
  corner_bl = img[(h - region_size):h, 0:region_size]
  corner_br = img[(h - region_size):h, (w - region_size):w]

  # Concatena todas as regiões e calcula a média de brilho
  corner_mean = np.array([corner_tl, corner_tr, corner_bl, corner_br]).mean()

  # Se os cantos são brilhantes, inverta a imagem
  if corner_mean > 128: # 128 é um valor de corte (metade de 255)
      return cv2.bitwise_not(img)
  else:
      return img

def remove_dark_background(img: MatLike):
  h, w = img.shape
  img_smooth = cv2.GaussianBlur(img, (5, 5), 0)
  # Detecção de Bordas (Canny)
  borders = cv2.Canny(img_smooth, 50, 150)

  # Conectar as Bordas
  kernel = np.ones((7, 7), np.uint8)
  borders = cv2.morphologyEx(borders, cv2.MORPH_CLOSE, kernel, iterations=3)

  # Encontrar Contornos
  contours, _ = cv2.findContours(borders, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

  if contours:
      largest_countour = max(contours, key=cv2.contourArea)
      mask = np.zeros_like(img, dtype=np.uint8)
      cv2.drawContours(mask, [largest_countour], -1, (255), thickness=cv2.FILLED)

      # Aplicar a máscara na imagem original para obter o cérebro isolado
      masked_img = cv2.bitwise_and(img, img, mask=mask)

      # Remove pequena parte das bordas da imagem para remover possíveis quadros brancos
      padding = 8
      masked_img = masked_img[padding:h-padding, padding:w-padding]
      return cv2.resize(masked_img, (IMAGE_SIZE, IMAGE_SIZE), interpolation=cv2.INTER_AREA)
  else:
      return img

def preprocess_img(img: MatLike):
  img = normalize_background(img)
  img = remove_dark_background(img)
  # Converte de volta para o formato RGB que o modelo aceita
  return cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)