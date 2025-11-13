import numpy as np
import keras
from flask import Flask, request, jsonify
from werkzeug.datastructures import FileStorage
from image_utils import load_img, preprocess_img
import os

app = Flask(__name__)

model_filename = 'brain_tumor_model.keras'
model_filepath = os.path.join(os.getcwd(), model_filename)

# Carrega o modelo treinado
try:
    print(f"Carregando modelo '{model_filename}'...")
    print(f"  - {model_filepath}")
    model = keras.models.load_model(model_filepath)
    print(f"Modelo '{model_filename}' carregado com sucesso.")
except Exception as e:
    print(f"Erro ao carregar o modelo: {e}")
    print(f"Certifique-se de que '{model_filename}' está na mesma pasta.")
    model = None

def load_image_file(file_stream: FileStorage):
    """
    Lê um file stream, aplica todo o pipeline de pré-processamento
    e prepara a imagem para o modelo.
    """
    
    # Converte o file stream em um array numpy
    filestr = file_stream.read()
    npimg = np.frombuffer(filestr, np.uint8)
    img = load_img(npimg)
    img = preprocess_img(img)
    return img

# --- 3. Definição do Endpoint da API ---

@app.route("/predict", methods=["POST"])
def predict():
    if model is None:
        return jsonify({"erro": "Modelo não carregado"}), 500
        
    if 'files' not in request.files:
        return jsonify({"erro": "Nenhum arquivo enviado. Use a chave 'files'."}), 400

    # Pega a lista de arquivos enviados (suporta múltiplos)
    files = request.files.getlist("files")
    
    results = [] # Lista para armazenar os resultados

    for file in files:
        if file.filename == '':
            continue # Pula arquivos vazios

        try:
            # Prepara a imagem
            img = load_image_file(file)
            
            # Faz a predição
            prediction = model.predict(np.expand_dims(img, axis=0))
            
            # Formata o resultado
            prob = float(prediction[0][0])

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