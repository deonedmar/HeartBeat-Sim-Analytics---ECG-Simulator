import numpy as np
import matplotlib.pyplot as plt

# simulação necessita ajuste
def generate_ecg_beat(amplitude_scale=1.0, duration_scale=1.0):
    """
    Gera dados simulados para um único batimento cardíaco de ECG.
    amplitude_scale: Fator para ajustar a altura das ondas.
    duration_scale: Fator para ajustar a duração do batimento (1.0 = normal).
    """
    time_points = np.linspace(0, 1.0 * duration_scale, 500)  # 500 pontos em 1 segundo (normal)

    # Onda P (pequena deflexão positiva)
    p_wave_center = 0.1 * duration_scale
    p_wave_std = 0.02 * duration_scale
    p_wave = amplitude_scale * 0.15 * np.exp(-((time_points - p_wave_center) ** 2) / (2 * p_wave_std ** 2))

    # Complexo QRS (grande e rápido)
    qrs_center = 0.25 * duration_scale
    qrs_std = 0.02 * duration_scale

    # Onda Q (deflexão negativa inicial)
    q_wave = -amplitude_scale * 0.3 * np.exp(
        -((time_points - (qrs_center - 0.02 * duration_scale)) ** 2) / (2 * (qrs_std * 0.5) ** 2))
    # Onda R (pico positivo alto)
    r_wave = amplitude_scale * 1.5 * np.exp(-((time_points - qrs_center) ** 2) / (2 * qrs_std ** 2))
    # Onda S (deflexão negativa final)
    s_wave = -amplitude_scale * 0.4 * np.exp(
        -((time_points - (qrs_center + 0.02 * duration_scale)) ** 2) / (2 * (qrs_std * 0.5) ** 2))

    qrs_complex = q_wave + r_wave + s_wave

    # Onda T (deflexão positiva, mais larga que P)
    t_wave_center = 0.45 * duration_scale
    t_wave_std = 0.06 * duration_scale
    t_wave = amplitude_scale * 0.25 * np.exp(-((time_points - t_wave_center) ** 2) / (2 * t_wave_std ** 2))

    # Combinar todas as ondas
    ecg_signal = p_wave + qrs_complex + t_wave

    return time_points, ecg_signal


def plot_ecg(ax, time, signal, title, normal_heart_rate=70):
    """Plota um sinal de ECG em um determinado eixo."""
    ax.plot(time, signal, color='blue')
    ax.set_title(title, fontsize=14)
    ax.set_xlabel('Tempo (s)', fontsize=12)
    ax.set_ylabel('Amplitude (mV)', fontsize=12)
    ax.grid(True, linestyle='--', alpha=0.7)
    ax.set_ylim(-0.7, 1.8)  # Limites fixos para comparação

    # Adicionar os rótulos P, QRS, T ao primeiro batimento
    # (Ajuste as posições para o batimento normal, ou dinamicamente se necessário)
    if "Normal" in title:
        ax.annotate('P', xy=(0.1, 0.15), xytext=(0.05, 0.25),
                    arrowprops=dict(facecolor='black', shrink=0.05), fontsize=10)
        ax.annotate('QRS', xy=(0.25, 1.5), xytext=(0.2, 1.0),
                    arrowprops=dict(facecolor='black', shrink=0.05), fontsize=10)
        ax.annotate('T', xy=(0.45, 0.25), xytext=(0.4, 0.45),
                    arrowprops=dict(facecolor='black', shrink=0.05), fontsize=10)

    # Calcular e exibir frequência cardíaca aproximada
    # Assumimos que o tempo total do batimento é o intervalo R-R
    rr_interval = time[-1]  # Duração de um batimento simulado
    heart_rate_bpm = 60 / rr_interval if rr_interval > 0 else 0

    ax.text(0.7, 1.6, f'FC: {heart_rate_bpm:.0f} bpm',
            bbox=dict(boxstyle="round,pad=0.3", fc="yellow", ec="b", lw=0.5, alpha=0.8),
            transform=ax.transAxes, fontsize=10)


# --- Geração e Plotagem dos Diferentes Cenários de ECG ---
fig, axes = plt.subplots(3, 1, figsize=(12, 10), sharex=True)  # Compartilha o eixo X
fig.suptitle('Exemplos de Eletrocardiogramas (ECG) Simulados', fontsize=16)

# 1. ECG Normal (Frequência Cardíaca ~60-100 bpm)
# Um batimento a cada 1 segundo = 60 bpm
time_normal, signal_normal = generate_ecg_beat(duration_scale=1.0)
plot_ecg(axes[0], time_normal, signal_normal, 'ECG Normal (FC ~60 bpm)', normal_heart_rate=60)

# 2. Taquicardia (Frequência Cardíaca >100 bpm)
# Um batimento mais rápido, por exemplo, 0.5s = 120 bpm
time_tachy, signal_tachy = generate_ecg_beat(duration_scale=0.5)
plot_ecg(axes[1], time_tachy, signal_tachy, 'Taquicardia (FC ~120 bpm)', normal_heart_rate=120)

# 3. Bradicardia (Frequência Cardíaca <60 bpm)
# Um batimento mais lento, por exemplo, 1.5s = 40 bpm
time_brady, signal_brady = generate_ecg_beat(duration_scale=1.5)
plot_ecg(axes[2], time_brady, signal_brady, 'Bradicardia (FC ~40 bpm)', normal_heart_rate=40)

plt.tight_layout(rect=[0, 0.03, 1, 0.95])  # Ajusta o layout para evitar sobreposição de títulos
plt.show()
