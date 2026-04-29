# Análise Cinemática da 1ª Lei de Newton com Visão Computacional

Este projeto utiliza **Python + OpenCV** para rastrear objetos em tempo real e analisar seu movimento, validando experimentalmente a **Primeira Lei de Newton (Lei da Inércia)**.

Através de técnicas de **Visão Computacional**, o sistema captura a trajetória de um objeto, calcula sua **velocidade** e **aceleração**, e gera gráficos automaticamente para análise física.

Projeto voltado para Engenharia de Computação, integrando Física Experimental e Processamento de Imagens.

---

## Funcionalidades

* Rastreamento de Cor: Detecção de objetos (azul/roxo, amarelo, etc.) usando espaço de cor HSV
* Cálculo Físico: Conversão de pixels para metros
* Velocidade: Cálculo automático em m/s
* Aceleração: Cálculo automático em m/s²
* Geração de Gráficos com Matplotlib
* Suavização de Dados com média móvel

---

## Tecnologias Utilizadas

* Python 3
* OpenCV
* NumPy
* Matplotlib
* DroidCam

---

## Estrutura do Projeto

```id="projstruct"
newton-cv/
│
├── src/
│   ├── app.py
│   ├── utils.py
│   └── requirements.txt
│
├── images/
│   ├── grafico_velocidade.png
│   ├── grafico_aceleracao.png
│   └── demo.gif
│
└── README.md
```

---

## Pré-requisitos e Instalação (Linux/Ubuntu)

### 1. Dependências do Sistema

```bash id="depsys"
sudo apt update
sudo apt install python3-pip python3-tk ffmpeg libsm6 libxext6 -y
```

---

### 2. Bibliotecas Python

```bash id="deppy"
cd newton-cv/src
pip3 install -r requirements.txt --break-system-packages
```

---

## Configuração de Hardware (DroidCam)

Para melhor qualidade de imagem, utilize o celular como webcam.

### Passos:

1. Instale o app DroidCam no celular
2. Conecte celular e PC na mesma rede Wi-Fi
3. No PC, execute:

```bash id="droidrun"
droidcam
```

4. Insira o IP mostrado no celular e clique em Connect

Observação: O script tenta usar a câmera no índice `2`. Caso não funcione, ele usa `0`.

---

## Como Executar

Você precisará de dois terminais:

### Terminal 1 — Câmera

```bash id="term1"
droidcam
```

---

### Terminal 2 — Programa

```bash id="term2"
cd newton-cv/src
python3 app.py
```

---

## Resultados

### Velocidade

![Velocidade](images/grafico_velocidade.png)

### Aceleração

![Aceleração](images/grafico_aceleracao.png)

### Rastreamento em Tempo Real

![Demo](images/demo.gif)

---

## Calibração

Ajuste a variável no `app.py`:

```python id="calib"
PIXELS_POR_METRO = 1000
```

Sugestões:

* Mesa (perto): ~2000
* Chão (longe): ~500

---

## Ajuste de Cores (HSV)

Caso o objeto não seja detectado:

### Roxo / Violeta

```python id="roxo"
COR_MINIMA = np.array([125, 50, 50])
COR_MAXIMA = np.array([155, 255, 255])
```

### Amarelo

```python id="amarelo"
COR_MINIMA = np.array([20, 100, 100])
COR_MAXIMA = np.array([35, 255, 255])
```

### Salmão / Laranja

```python id="laranja"
COR_MINIMA = np.array([0, 50, 50])
COR_MAXIMA = np.array([15, 188, 255])
```

---

## Aplicações

* Ensino de Física
* Experimentos de baixo custo
* Visão Computacional
* Análise de movimento
* Projetos educacionais

---

