from env import *
import numpy as np
from flask import Flask, request, jsonify
from werkzeug.datastructures import FileStorage
from model import load_model, MODEL_NAME
from image_utils import load_img, preprocess_img
from utils import log_info, log_error, log_success
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Carrega o modelo treinado
try:
    log_info(f"Carregando modelo '{MODEL_NAME}'...")
    model = load_model()
    log_success(f"Modelo '{MODEL_NAME}' carregado com sucesso.")
except Exception as e:
    log_error(f"Erro ao carregar o modelo: {e}")
    exit(1)

def load_image_file(file_stream: FileStorage):
    """
    Lê um file stream, aplica todo o pipeline de pré-processamento
    e prepara a imagem para o modelo.
    """
    
    filestr = file_stream.read()
    npimg = np.frombuffer(filestr, np.uint8)
    img = load_img(npimg)
    img = preprocess_img(img)
    return img

@app.route("/predict", methods=["POST"])
def predict():
    if model is None:
        return jsonify({"erro": "Modelo não carregado"}), 500
        
    if 'files' not in request.files:
        return jsonify({"erro": "Nenhum arquivo enviado. Use a chave 'files'."}), 400

    files = request.files.getlist("files")

    log_info(f"Nova requisição para {len(files)} imagens")
    
    results = []

    for file in files:
        log_info(f"  - {file.filename}")

        if file.filename == '':
            continue

        try:
            # Prepara a imagem
            img = load_image_file(file)
            
            # Faz a predição
            prediction = model.predict(np.expand_dims(img, axis=0))
            
            # Formata o resultado
            prob = float(prediction[0][0])

            log_info(f"  - Predição: {prob}")

            results.append({
                "filename": file.filename,
                "prob": prob
            })

        except Exception as e:
            # Captura erros de pré-processamento ou predição
            results.append({
                "filename": file.filename,
                "erro": str(e)
            })

    # Retorna a lista de resultados como JSON
    return jsonify(results)

if __name__ == "__main__":
    # Executa o app na rede local, porta 5000
    app.run(host="0.0.0.0", port=5000, debug=True)