import requests

import subprocess

import threading

import time

import csv

import os

import pandas as pd



# Configuration

OLLAMA_URL = "http://localhost:11434"

TEST_PROMPT = "Explain the physics of a black hole in exactly three sentences."

OUTPUT_FILE = "output.csv"



class GPUTracker(threading.Thread):

    """

    Background thread to monitor dual A100 performance metrics 

    during the exact window of model inference.

    """

    def __init__(self, interval=0.1):

        super().__init__()

        self.interval = interval

        self.stop_event = threading.Event()

        self.stats = {

            'peak_vram_mb': [0, 0],

            'peak_power_w': [0.0, 0.0],

            'power_samples': [[], []]

        }



    def run(self):

        while not self.stop_event.is_set():

            try:

                # Query memory used and power draw for GPUs 0 and 1

                cmd = "nvidia-smi --query-gpu=memory.used,power.draw --format=csv,noheader,nounits"

                output = subprocess.check_output(cmd.split()).decode('utf-8').strip().split('\n')

                

                for i, line in enumerate(output):

                    mem, pwr = line.split(',')

                    mem, pwr = int(mem), float(pwr)

                    

                    if mem > self.stats['peak_vram_mb'][i]:

                        self.stats['peak_vram_mb'][i] = mem

                    if pwr > self.stats['peak_power_w'][i]:

                        self.stats['peak_power_w'][i] = pwr

                    self.stats['power_samples'][i].append(pwr)

            except Exception:

                pass

            time.sleep(self.interval)



    def stop(self):

        self.stop_event.set()


def run_benchmark(model_name):

    print(f"\n>>> Benchmarking: {model_name}")

    

    # 1. Warm-up (Ensures model is loaded into VRAM before timing starts)

    requests.post(f"{OLLAMA_URL}/api/generate", json={"model": model_name, "prompt": "warmup", "stream": False})

    

    # 2. Start GPU Tracking

    tracker = GPUTracker()

    tracker.start()

    

    # 3. Execution

    payload = {"model": model_name, "prompt": TEST_PROMPT, "stream": False}

    start_wall = time.perf_counter()

    response = requests.post(f"{OLLAMA_URL}/api/generate", json=payload)

    end_wall = time.perf_counter()

    

    # 4. Stop Tracking

    tracker.stop()

    tracker.join()

    

    data = response.json()

    

    # --- Metrics Calculation ---

    eval_count = data.get("eval_count", 0)

    # Convert nanoseconds to seconds

    eval_duration_sec = data.get("eval_duration", 0) / 1e9

    prompt_duration_sec = data.get("prompt_eval_duration", 0) / 1e9

    

    # Performance

    tps = eval_count / eval_duration_sec if eval_duration_sec > 0 else 0

    ttft = prompt_duration_sec # Time to First Token proxy

    

    # Power averages

    avg_pwr_0 = sum(tracker.stats['power_samples'][0]) / len(tracker.stats['power_samples'][0]) if tracker.stats['power_samples'][0] else 0

    avg_pwr_1 = sum(tracker.stats['power_samples'][1]) / len(tracker.stats['power_samples'][1]) if tracker.stats['power_samples'][1] else 0



    return {

        "Model": model_name,

        "Response": data['response'],

        "TPS": round(tps, 2),

        "TTFT (s)": round(ttft, 4),

        "Peak VRAM GPU0 (MB)": tracker.stats['peak_vram_mb'][0],

        "Peak VRAM GPU1 (MB)": tracker.stats['peak_vram_mb'][1],

        "Total Peak VRAM (MB)": sum(tracker.stats['peak_vram_mb']),

        "Peak Power GPU0 (W)": tracker.stats['peak_power_w'][0],

        "Peak Power GPU1 (W)": tracker.stats['peak_power_w'][1],

        "Avg Total Power (W)": round(avg_pwr_0 + avg_pwr_1, 2),

        "Wall Time (s)": round(end_wall - start_wall, 2)

    }

def main():

    models = []
    
    with open('modellist.txt', 'r') as file:
        
        for model in file:
            
            models.append(model.strip())

    all_results = []

    for model in models:

        try:

            res = run_benchmark(model)

            all_results.append(res)

            print(f"Done. TPS: {res['TPS']} | VRAM: {res['Total Peak VRAM (MB)']} MB | Power: {res['Avg Total Power (W)']} W")

        except Exception as e:

            print(f"Error testing {model}: {e}")

    # Save Results

    df = pd.DataFrame(all_results)

    df.to_csv(OUTPUT_FILE, index=False)

    print(f"\nBenchmark Complete! Data written to {OUTPUT_FILE}")

    print(df.drop(columns=['TTFT (s)', 'Wall Time (s)']).to_string(index=False))

if __name__ == "__main__":

    main()
