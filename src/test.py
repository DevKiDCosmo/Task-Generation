from concurrent.futures import ThreadPoolExecutor, as_completed
import time
import psutil
import struct

def task_function(task_id):
    threehalfs = 1.5

    # Bit-Level Manipulation
    x2 = task_id * 0.5
    y = task_id
    packed_y = struct.pack('f', y)  # Float in Bytes umwandeln
    i = struct.unpack('i', packed_y)[0]  # Bytes als Integer interpretieren
    i = 0x5f3759df - (i >> 1)  # Magische Konstante und Bit-Shift
    packed_i = struct.pack('i', i)  # Integer zurück in Bytes
    y = struct.unpack('f', packed_i)[0]  # Bytes zurück in Float

    # Eine Iteration des Newton-Verfahrens
    y = y * (threehalfs - (x2 * y * y))
    return f"Task {task_id} completed"

def main():
    tasks = range(100)  # 100 tasks
    results = []
    max_cpu_usage = 0

    with ThreadPoolExecutor(max_workers=10) as executor:  # Adjust workers as needed
        future_to_task = {executor.submit(task_function, task): task for task in tasks}

        for future in as_completed(future_to_task):
            results.append(future.result())
            # Measure CPU usage
            current_cpu_usage = psutil.cpu_percent(interval=0.1)
            max_cpu_usage = max(max_cpu_usage, current_cpu_usage)

    print("All tasks completed!")
    print(results)
    print(f"Max CPU usage during execution: {max_cpu_usage}%")

if __name__ == "__main__":
    main()