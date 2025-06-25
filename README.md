# 📄 Projeto OCR com PaddleOCR + Matplotlib

Bem-vindo ao projeto de Reconhecimento Óptico de Caracteres (OCR) utilizando **PaddleOCR** integrado ao **Matplotlib** para visualização. Este repositório foi pensado para funcionar de forma prática, com execução automatizada via Shell Script e suporte a interface gráfica para testes manuais.

---

## 🚀 Objetivo

Este projeto tem como foco identificar e extrair texto de imagens, utilizando PaddleOCR. Além disso, apresenta visualizações dos resultados com Matplotlib, salvando tanto as imagens plotadas quanto os dados em arquivos `.txt` e `.json`.

---

## 🧠 Tecnologias e Estrutura

- **PaddleOCR**: Motor OCR para identificação dos textos nas imagens.
- **Matplotlib**: Para exibir visualmente os resultados com bounding boxes.
- **EasyGUI**: Interface gráfica simples para uso manual.
- **Shell Script**: Automatização da instalação e execução.

---

## 🛠️ Instalação

Clone o repositório e execute o script de instalação:

```bash
git clone https://github.com/Atn4s/JP_Paddle_OCR
cd JP_Paddle_OCR
bash install.sh
```

Esse script:

    Cria um ambiente virtual .venv chamado PaddleOCR

    Instala todas as dependências necessárias

    Prepara a estrutura de pastas

## 🖼️ Como usar
## 1. Preparando as imagens

Coloque as imagens que deseja processar na pasta:

OCRDatabase/

## 2. Execução
   
⚠️ Atenção! Verifique se você está dentro do venv ```PaddleOCR```, se não estiver ative via ```source bin/activate```
## 📌 Modo automático (recomendado):

```bash processa_imagens.sh```

Este comando irá:

    Executar PaddleGUI.py dentro do ambiente virtual

    Processar todas as imagens em OCRDatabase

    Salvar para cada imagem:

        Uma imagem plotada com os bounding boxes

        Um arquivo .txt com:

            O conteúdo identificado

            O score de confiança

            A posição dos bounding boxes

Depois disso, será executado OCR_schema.py, que:

    Lê todos os .txt gerados

    Constrói um .json estruturado com os resultados

    Salva na pasta saida_processada/
    ⚠️ Essa parte ainda está sendo aprimorada

## ✋ Modo manual:

Rode o script principal com interface gráfica:

python PaddleGUI.py

Isso abrirá uma interface com o EasyGUI para você selecionar uma imagem e processá-la individualmente.
📁 Estrutura dos arquivos

```
PaddleGUI.py              # Script principal do OCR + visualização
OCR_schema.py             # Gera JSON estruturado a partir dos resultados
Modulos/
├── config.py             # Configurações gerais (OCR, fonte, validações)
├── image_processing.py   # Lógica de plotagem com Matplotlib
└── path.py               # Manipulação de diretórios e caminhos
OCRDatabase/              # Pasta onde você coloca suas imagens
saida_processada/         # Resultados processados em .json
```
##  📌 Observações finais

    O projeto ainda está em desenvolvimento — fique à vontade para sugerir melhorias!
