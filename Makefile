.DEFAULT_GOAL := all
.PHONY: all env install api build client

VENV_DIR ?= .venv
API_FILEPATH ?= api/app.py
PYTHON := $(VENV_DIR)/bin/python3

all: install

env:
	@echo "Verificando ambiente virtual python..."
	test -d $(VENV_DIR) || python3 -m venv $(VENV_DIR)
	@echo "Virtual environment created at $(VENV_DIR)"

install: env
	@echo "Instalando dependências Python..."
	$(PYTHON) -m pip install -r requirements.txt
	@$(PYTHON) -c "import flask, flask_cors; print('Flask:', flask.__version__, 'Flask-CORS:', flask_cors.__version__)"
	@echo "Dependências instaladas com sucesso!"

api: env
	@echo "Using Python: $(PYTHON)"
	@$(PYTHON) $(API_FILEPATH)

build:
	@echo "Realizando build do cliente..."
	cd client && pnpm generate:latest
	@echo "Build concluído com sucesso!"

client:
	@echo "Iniciando cliente (frontend)..."
	$(PYTHON) -m http.server 3000 -d ./client/latest

client-dev:
	@echo "Iniciando cliente em modo de desenvolvimento..."
	cd client && pnpm dev

clean:
	@echo "Limpando cache da API..."
	@rm -rf .cache
	@echo "Cache eliminado com sucesso!"
