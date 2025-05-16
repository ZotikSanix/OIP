from __future__ import annotations

import math
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import MultipleLocator

DATA_DIR: Path = Path(".")
SETTINGS_FILE: Path = DATA_DIR / "settings.txt"
DATA_FILE: Path = DATA_DIR / "data.txt"
OUTPUT_FILE: Path = DATA_DIR / "graph.svg"

FIGSIZE = (16, 10)
DPI = 400
Y_LIMITS = (0.0, 3.5)

def load_settings(path: Path) -> tuple[float, float]:
    return tuple(np.loadtxt(path, dtype=float))

def load_adc_samples(path: Path) -> np.ndarray:
    return np.loadtxt(path, dtype=int)

def prepare_axes(ax):
    ax.set_xlabel("Time, s", fontsize=16)
    ax.set_ylabel("Voltage, V", fontsize=16)
    ax.set_title("Capacitor charge–discharge graph in RC‑circuit", fontsize=20)
    ax.xaxis.set_minor_locator(MultipleLocator(0.5))
    ax.xaxis.set_major_locator(MultipleLocator(1.0))
    ax.yaxis.set_minor_locator(MultipleLocator(0.25))
    ax.yaxis.set_major_locator(MultipleLocator(0.5))
    ax.grid(color="blue", which="both", linestyle=":", linewidth=0.5)

def compute_arrays(adc: np.ndarray, time_step: float, volt_step: float):
    volt_arr = adc * volt_step
    time_arr = np.arange(adc.size) * time_step
    return time_arr, volt_arr

def annotate_plot(ax, charge_time: float, discharge_time: float, volt_max: float):
    ax.axvline(x=charge_time, ymin=0, ymax=volt_max / Y_LIMITS[1], color="green", linestyle="dashed")
    ax.axhline(y=volt_max, xmin=0, xmax=charge_time / (charge_time + discharge_time), color="green", linestyle="dashed")
    ax.scatter([0.0, charge_time], [volt_max, 0.0], color="green")
    ax.scatter(charge_time, 0.0, color="green")
    ax.text(charge_time + 0.1, 0.05, f"{charge_time:.2f}", fontsize=12)
    ax.text(0.1, volt_max + 0.05, f"{volt_max:.2f}", fontsize=12)
    ax.text(charge_time / 2 - 0.8, volt_max / 2, f"Charge time: {charge_time:.2f} s", color="blue", fontsize=14)
    ax.text(charge_time + discharge_time / 2 - 0.8, volt_max / 2, f"Discharge time: {discharge_time:.2f} s", color="red", fontsize=14)

def main():
    time_step, volt_step = load_settings(SETTINGS_FILE)
    adc_samples = load_adc_samples(DATA_FILE)
    time_arr, volt_arr = compute_arrays(adc_samples, time_step, volt_step)
    idx_max = int(np.argmax(volt_arr))
    volt_max = float(volt_arr[idx_max])
    charge_time = time_arr[idx_max]
    discharge_time = float(time_arr[-1] - time_arr[idx_max])
    fig, ax = plt.subplots(figsize=FIGSIZE, dpi=DPI)
    prepare_axes(ax)
    ax.plot(time_arr[:idx_max], volt_arr[:idx_max], label="Capacitor charge")
    ax.plot(time_arr[idx_max:], volt_arr[idx_max:], label="Capacitor discharge")
    ax.legend(prop={"size": 16})
    ax.set_xlim(0.0, math.ceil(time_arr[-1]))
    ax.set_ylim(*Y_LIMITS)
    annotate_plot(ax, charge_time, discharge_time, volt_max)
    fig.savefig(OUTPUT_FILE)

if __name__ == "__main__":
    main()
