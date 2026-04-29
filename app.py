import cv2
import numpy as np
import time
import matplotlib.pyplot as plt

# --- CONFIGURAÇÃO DE COR: ROXO (PURPLE) ---
# Ajustado para detectar a bola Roxa
COR_MINIMA = np.array([125, 50, 40])
COR_MAXIMA = np.array([165, 255, 255])

# --- CALIBRAÇÃO DE DISTÂNCIA ---
# Mesa (perto): ~2000 | Chão (longe): ~500
PIXELS_POR_METRO = 2000 

def suavizar_dados(dados, janela=5):
    if len(dados) < janela:
        return dados
    return np.convolve(dados, np.ones(janela)/janela, mode='same')

def main():
    print("--- EXPERIMENTO DE FÍSICA: 1ª LEI DE NEWTON ---")
    print("Cor: ROXO | Gráfico: SUAVIZADO")

    # Conexão com Câmera
    cap = cv2.VideoCapture(2)
    if not cap.isOpened():
        cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("[ERRO] Nenhuma câmera encontrada.")
        return

    # Listas de dados
    historico_tempo = []
    historico_vel = []
    historico_acc = []

    # Variáveis de controle
    tempo_inicio_experimento = time.time()
    tempo_anterior = time.time()
    pos_anterior = None
    vel_anterior = 0
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Processamento de Imagem
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, COR_MINIMA, COR_MAXIMA)
        mask = cv2.erode(mask, None, iterations=2)
        mask = cv2.dilate(mask, None, iterations=2)
        
        contornos, _ = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        estado = "REPOUSO"
        velocidade_inst = 0.0
        aceleracao_inst = 0.0

        if len(contornos) > 0:
            c = max(contornos, key=cv2.contourArea)
            ((x, y), raio) = cv2.minEnclosingCircle(c)
            
            if raio > 20:
                # Desenho na bola
                cv2.circle(frame, (int(x), int(y)), int(raio), (0, 255, 255), 2)
                cv2.circle(frame, (int(x), int(y)), 5, (0, 0, 255), -1)
                
                pos_atual = np.array([x, y])
                tempo_atual = time.time()
                dt = tempo_atual - tempo_anterior
                
                if pos_anterior is not None and dt > 0:
                    # FÍSICA
                    dist_pixels = np.linalg.norm(pos_atual - pos_anterior)
                    dist_metros = dist_pixels / PIXELS_POR_METRO
                    
                    velocidade_inst = dist_metros / dt
                    aceleracao_inst = (velocidade_inst - vel_anterior) / dt

                    if velocidade_inst > 0.05: 
                        estado = "MOVIMENTO"

                    # Salvar dados
                    tempo_decorrido = tempo_atual - tempo_inicio_experimento
                    historico_tempo.append(tempo_decorrido)
                    historico_vel.append(velocidade_inst)
                    historico_acc.append(aceleracao_inst)

                    vel_anterior = velocidade_inst
                
                pos_anterior = pos_atual
                tempo_anterior = tempo_atual

        # --- PAINEL DE DADOS (HUD) ---
        cv2.rectangle(frame, (10, 10), (300, 130), (0, 0, 0), -1)
        cor_status = (0, 255, 0) if "MOVIMENTO" in estado else (0, 0, 255)
        
        cv2.putText(frame, f"Estado: {estado}", (20, 35), cv2.FONT_HERSHEY_SIMPLEX, 0.6, cor_status, 2)
        cv2.putText(frame, f"V: {velocidade_inst:.3f} m/s", (20, 65), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
        # ACELERAÇÃO AO VIVO:
        cv2.putText(frame, f"A: {aceleracao_inst:.3f} m/s2", (20, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (100, 255, 255), 1)
        cv2.putText(frame, f"REC: {len(historico_tempo)} pts", (20, 115), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)

        cv2.imshow("Experimento Fisica 1", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()

    # --- GERAR GRÁFICOS ---
    if len(historico_tempo) > 5:
        print("Gerando gráficos suavizados...")
        
        # APLICANDO FILTRO PARA REMOVER "RABISCOS"
        vel_suave = suavizar_dados(historico_vel, janela=10)
        acc_suave = suavizar_dados(historico_acc, janela=15) # Aceleração precisa de mais filtro

        plt.figure(figsize=(10, 8))

        # Gráfico 1: Velocidade (Azul)
        plt.subplot(2, 1, 1)
        plt.plot(historico_tempo, vel_suave, color='blue', linewidth=2, label='Velocidade (m/s)')
        plt.title('Velocidade x Tempo (Suavizado)')
        plt.ylabel('Velocidade (m/s)')
        plt.grid(True)
        plt.legend()

        # Gráfico 2: Aceleração (Vermelho)
        plt.subplot(2, 1, 2)
        plt.plot(historico_tempo, acc_suave, color='red', linewidth=2, label='Aceleração (m/s²)')
        plt.xlabel('Tempo (s)')
        plt.ylabel('Aceleração (m/s²)')
        plt.grid(True)
        plt.legend()

        print("Pronto! Clique no disquete para salvar.")
        plt.show()
    else:
        print("Poucos dados coletados para gerar gráfico.")

if __name__ == "__main__":
    main()
