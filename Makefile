.DEFAULT_GOAL := all
.PHONY: all env install api build client

VENV_DIR ?= .venv
API_FILEPATH ?= api/app.py
PYTHON :=$(VENV_DIR)/bin/python3

all: install

env:
	@echo "Verificando ambiente virtual python..."
	test -d $(VENV_DIR) || python3 -m venv $(VENV_DIR)

install: env
	@echo "Instalando dependências Python..."
	$(PYTHON) -m pip install -r requirements.txt
	@echo "Dependências instaladas com sucesso!"

api: env
	@echo "Iniciando API (backend)..."
	$(PYTHON) $(API_FILEPATH)

build:
	@echo "Realizando build do cliente..."
	cd client && pnpm generate:latest
	@echo "Build concluído com sucesso!"

client:
	@echo "Iniciando cliente (frontend)..."
	$(PYTHON) -m http.server 3000 -d ./client/latest