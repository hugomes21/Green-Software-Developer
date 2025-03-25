import matplotlib.pyplot as plt
import csv
import os
import numpy as np
import subprocess
import re

def open_read_csv(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            data = [{key.strip(): value.strip() for key, value in row.items()} for row in reader]

            # Verifica se os dados foram lidos corretamente
            if not data:
                print(f"Aviso: O ficheiro {file_path} está vazio ou não foi lido corretamente.")
            else:
                print(f"Sucesso: {len(data)} linhas lidas de {file_path}.")
            return data

    except Exception as e:
        print(f"Erro ao ler {file_path}: {e}")
        return []


def plot_multiple_metrics(data, output_dir, title, metrics, ylabel):
    if not data:
        print(f"No data found for {title}")
        return

    headers = data[0].keys()
    print(f"Headers for {title}: {headers}")

    # Ordenar os dados pelo tempo de execução
    data.sort(key=lambda row: float(row['Time (ms)']))

    plt.figure(figsize=(10, 6))

    colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k']  # Lista de cores para diferenciar os dados
    markers = ['o', 's', 'D', '^', 'v', '*', 'x']  # Diferentes marcadores
    color_index = 0

    # Criar um conjunto de identificadores únicos para diferenciar _O0_, _O2_ e os inputs
    unique_versions = set(row['Program'].strip() for row in data)

    for version in unique_versions:
        version_data = [row for row in data if row['Program'].strip() == version]
        version_data.sort(key=lambda row: float(row['Time (ms)']))
        
        times = [float(row['Time (ms)']) for row in version_data]

        for i, metric in enumerate(metrics):
            try:
                values = [float(row[metric]) for row in version_data]
                label = f"{version} - {metric}"
                plt.plot(times, values, label=label, color=colors[color_index % len(colors)], 
                         marker=markers[color_index % len(markers)], linestyle='-')
                color_index += 1
            except KeyError:
                print(f"Warning: Metric '{metric}' not found in dataset.")

    plt.xlabel('Time (ms)')
    plt.ylabel(ylabel)
    plt.title(f"{title} - Performance Metrics")
    plt.legend()
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()

    os.makedirs(output_dir, exist_ok=True)
    plt.savefig(f'{output_dir}/{title}_performance_metrics.png')
    plt.close()

def collect_data_from_directories(filename):
    all_data = {}
    file_path = os.path.join(os.path.dirname(__file__), filename)
    if os.path.exists(file_path):
        data = open_read_csv(file_path)
        title = 'measurements'
        all_data[title] = data
    return all_data

def calculate_metrics(data, variable):
    non_optimized = [float(row[variable]) for row in data if '_O0_' in row['Program']]
    optimized = [float(row[variable]) for row in data if '_O2_' in row['Program']]
    
    if not non_optimized or not optimized:
        return None, None, None
    
    avg_non_optimized = sum(non_optimized) / len(non_optimized)
    avg_optimized = sum(optimized) / len(optimized)
    
    speedup = avg_non_optimized / avg_optimized
    greenup = avg_optimized / avg_non_optimized
    powerup = (avg_non_optimized / avg_optimized) if avg_optimized != 0 else None
    
    return speedup, greenup, powerup

# Função para calcular média e desvio-padrão
def compute_avg_std(group, metric):
    values, stds = [], []
    for size in sorted(set(int(row['Program'].split('_')[-1]) for row in group)):
        subset = [float(row[metric]) for row in group if int(row['Program'].split('_')[-1]) == size]
        if subset:
            values.append(np.mean(subset))
            stds.append(np.std(subset))
        else:
            values.append(None)  # Caso não tenha dados para este input
            stds.append(None)
    return values, stds

def plot_comparative_metrics(all_data, output_dir):
    metrics = ['Time (ms)', 'Package', 'Core(s)', 'Temperature', 'Memory']
    
    # Obter programas únicos do CSV
    all_programs = set(row['Program'] for row in all_data['measurements'])

    # Separar dados por tipo de dado
    data_types = ['string', 'int', 'float', 'double']
    data_by_type = {data_type: [row for row in all_data['measurements'] if data_type in row['Program']] for data_type in data_types}

    for data_type, data in data_by_type.items():
        if not data:
            print(f"Faltam dados para o tipo {data_type}!")
            continue

        for metric in metrics:
            plt.figure(figsize=(10, 6))

            # Comparar diferentes algoritmos dentro do mesmo tipo de dado
            algorithms = sorted(set(row['Program'].split('_')[0] for row in data))

            for algorithm in algorithms:
                algorithm_data = [row for row in data if algorithm in row['Program']]
                algorithm_data.sort(key=lambda row: float(row['Time (ms)']))

                # Comparar otimizações O0 e O2
                non_optimized_data = [row for row in algorithm_data if '_O0_' in row['Program']]
                optimized_data = [row for row in algorithm_data if '_O2_' in row['Program']]

                if not non_optimized_data or not optimized_data:
                    print(f"Faltam dados para comparação de otimizações no algoritmo {algorithm} do tipo {data_type}!")
                    continue

                # O0 vs O2 (média e std)
                values_O0, std_O0 = compute_avg_std(non_optimized_data, metric)
                values_O2, std_O2 = compute_avg_std(optimized_data, metric)

                sizes = sorted(set(int(row['Program'].split('_')[-1]) for row in algorithm_data))

                # Plot O0 vs O2
                plt.errorbar(sizes, values_O0, yerr=std_O0, fmt='o-', label=f"{algorithm} - O0", capsize=5)
                plt.errorbar(sizes, values_O2, yerr=std_O2, fmt='x--', label=f"{algorithm} - O2", capsize=5)

            # Finalizar gráfico
            plt.xlabel('Input Size')
            plt.ylabel(metric)
            plt.title(f"Comparação de Algoritmos - {data_type} - {metric}")
            plt.legend()
            plt.grid(True)
            plt.xticks(rotation=45)
            plt.tight_layout()

            os.makedirs(output_dir, exist_ok=True)
            plt.savefig(f'{output_dir}/Comparacao_Algoritmos_{data_type}_{metric}.png')
            plt.close()

def plot_gps_up(data, output_dir):
    programs = ['fibonacci_linear', 'fibonacci_recursive']
    metrics = ['Time (ms)', 'Package', 'Core(s)']

    for program in programs:
        for metric in metrics:
            # Limpar espaços nos nomes das colunas
            non_optimized_data = [row for row in data if f'{program}_O0' in row['Program']]
            optimized_data = [row for row in data if f'{program}_O2' in row['Program']]

            if not non_optimized_data or not optimized_data:
                continue  # Ignorar se não houver dados suficientes

            # Calcular speedup, greenup e powerup apenas com os dados filtrados
            speedup, greenup, powerup = calculate_metrics(non_optimized_data + optimized_data, metric)

            # Verificar se os valores são válidos
            if speedup is None or greenup is None or powerup is None:
                continue

            plt.figure(figsize=(10, 6))
            plt.scatter(speedup, greenup, label=f'{program} - {metric}', marker='o')

            # Aplicar escala logarítmica apenas se os valores forem positivos
            if speedup > 0 and greenup > 0:
                plt.xscale('log')
                plt.yscale('log')

            plt.xlabel('Speedup')
            plt.ylabel('Greenup')
            plt.title(f"GPS-UP Software Energy Efficiency Quadrant - {program}")
            plt.legend()
            plt.grid(True)
            plt.tight_layout()

            # Criar diretório se não existir
            os.makedirs(output_dir, exist_ok=True)

            # Salvar gráfico
            plt.savefig(f'{output_dir}/{program}_{metric}_gps_up_quadrant.png')
            plt.close()


def plot_comparative_metrics_powercaps(all_data, output_dir, powercaps):
    for powercap in powercaps:
        # Filtrar os dados para as funções Fibonacci e PowerLimit == powercap
        data = all_data['measurements']
        fibonacci_data = [row for row in data if 'fibonacci' in row['Program'] and int(row['PowerLimit']) == powercap]

        if not fibonacci_data:
            print(f"No data found for PowerLimit = {powercap}")
            continue

        # Calcular energia consumida (Joules)
        for row in fibonacci_data:
            row['Energy (J)'] = float(row['Package']) * (float(row['Time (ms)']) / 1000)

        # Agrupar por Program e Optimization
        grouped_data = {}
        for row in fibonacci_data:
            program = row['Program'].split('_')[0]
            optimization = 'O0' if '_O0_' in row['Program'] else 'O2'

            if program not in grouped_data:
                grouped_data[program] = {'O0': [], 'O2': []}

            grouped_data[program][optimization].append(row)

        # Calcular Speedup, Greenup e Powerup
        results = []
        for program, optimizations in grouped_data.items():
            if optimizations['O0'] and optimizations['O2']:
                # Calcular métricas usando a função calculate_metrics
                speedup, _, _ = calculate_metrics(optimizations['O0'] + optimizations['O2'], 'Time (ms)')

                # Calcular Greenup para energia
                avg_energy_O0 = sum(float(row['Energy (J)']) for row in optimizations['O0']) / len(optimizations['O0'])
                avg_energy_O2 = sum(float(row['Energy (J)']) for row in optimizations['O2']) / len(optimizations['O2'])
                greenup = avg_energy_O0 / avg_energy_O2

                # Calcular Powerup para potência
                avg_power_O0 = sum(float(row['Package']) for row in optimizations['O0']) / len(optimizations['O0'])
                avg_power_O2 = sum(float(row['Package']) for row in optimizations['O2']) / len(optimizations['O2'])
                powerup = avg_power_O0 / avg_power_O2

                results.append({
                    'PowerLimit': powercap,
                    'Program': program,
                    'Speedup': speedup,
                    'Greenup': greenup,
                    'Powerup': powerup
                })

        # Imprimir os resultados
        print(f"\nResults for PowerLimit = {powercap}:")
        if not results:
            print("No valid data for comparison.")
        for result in results:
            print(f"Program: {result['Program']}")
            print(f"  Speedup: {result['Speedup']:.2f}")
            print(f"  Greenup: {result['Greenup']:.2f}")
            print(f"  Powerup: {result['Powerup']:.2f}")

def plot_gps_up_powercaps(data, output_dir, powercaps):
    programs = ['fibonacci_linear', 'fibonacci_recursive']
    metrics = ['Time (ms)', 'Package', 'Core(s)']

    for powercap in powercaps:
        for program in programs:
            for metric in metrics:
                # Filtrar dados para o programa e PowerCap
                non_optimized_data = [row for row in data if f'{program}_O0' in row['Program'] and int(row['PowerLimit']) == powercap]
                optimized_data = [row for row in data if f'{program}_O2' in row['Program'] and int(row['PowerLimit']) == powercap]

                if not non_optimized_data or not optimized_data:
                    continue  # Ignorar se não houver dados suficientes

                # Calcular Speedup, Greenup e Powerup
                speedup, greenup, powerup = calculate_metrics(non_optimized_data + optimized_data, metric)

                # Verificar se os valores são válidos
                if speedup is None or greenup is None or powerup is None:
                    continue

                plt.figure(figsize=(10, 6))
                plt.scatter(speedup, greenup, label=f'{program} - {metric}', marker='o')

                # Aplicar escala logarítmica apenas se os valores forem positivos
                if speedup > 0 and greenup > 0:
                    plt.xscale('log')
                    plt.yscale('log')

                plt.xlabel('Speedup')
                plt.ylabel('Greenup')
                plt.title(f"GPS-UP Quadrant - {program} (PowerLimit = {powercap})")
                plt.legend()
                plt.grid(True)
                plt.tight_layout()

                # Criar diretório se não existir
                os.makedirs(output_dir, exist_ok=True)

                # Salvar gráfico
                plt.savefig(f'{output_dir}/{program}_{metric}_gps_up_quadrant_powercap_{powercap}.png')
                plt.close()

# Exercício 1.7.
def plot_energy_consumption(data, output_dir, title):
    if not data:
        print(f"No data found for {title}")
        return

    # Calcular energia consumida (Joules)
    for row in data:
        row['Energy (J)'] = float(row['Package']) * (float(row['Time (ms)']) / 1000)

    # Filtrar dados para otimizações O0 e O2
    non_optimized_data = [row for row in data if '_O0_' in row['Program']]
    optimized_data = [row for row in data if '_O2_' in row['Program']]

    if not non_optimized_data or not optimized_data:
        print(f"Not enough data for energy consumption comparison in {title}")
        return

    # Calcular valores médios de energia
    avg_energy_O0 = sum(float(row['Energy (J)']) for row in non_optimized_data) / len(non_optimized_data)
    avg_energy_O2 = sum(float(row['Energy (J)']) for row in optimized_data) / len(optimized_data)

    # Criar gráfico
    plt.figure(figsize=(10, 6))
    bars = plt.bar(['O0', 'O2'], [avg_energy_O0, avg_energy_O2], color=['blue', 'green'], edgecolor='black')

    # Adicionar valores no topo das barras
    for bar, value in zip(bars, [avg_energy_O0, avg_energy_O2]):
        plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height(), f'{value:.2f}', ha='center', va='bottom')

    plt.xlabel('Optimization Level')
    plt.ylabel('Energy Consumption (Joules)')
    plt.title(f"Energy Consumption Comparison - {title}")
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()

    os.makedirs(output_dir, exist_ok=True)
    plt.savefig(f'{output_dir}/{title}_energy_consumption.png')
    plt.close()

def plot_runtime(data, output_dir, title):
    if not data:
        print(f"No data found for {title}")
        return

    # Filtrar dados para otimizações O0 e O2
    non_optimized_data = [row for row in data if '_O0_' in row['Program']]
    optimized_data = [row for row in data if '_O2_' in row['Program']]

    if not non_optimized_data or not optimized_data:
        print(f"Not enough data for runtime comparison in {title}")
        return

    # Calcular valores médios de tempo de execução
    avg_time_O0 = sum(float(row['Time (ms)']) for row in non_optimized_data) / len(non_optimized_data)
    avg_time_O2 = sum(float(row['Time (ms)']) for row in optimized_data) / len(optimized_data)

    # Criar gráfico
    plt.figure(figsize=(10, 6))
    bars = plt.bar(['O0', 'O2'], [avg_time_O0, avg_time_O2], color=['blue', 'green'], edgecolor='black')

    # Adicionar valores no topo das barras
    for bar, value in zip(bars, [avg_time_O0, avg_time_O2]):
        plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height(), f'{value:.2f}', ha='center', va='bottom')

    plt.xlabel('Optimization Level')
    plt.ylabel('Runtime (ms)')
    plt.title(f"Runtime Comparison - {title}")
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()

    os.makedirs(output_dir, exist_ok=True)
    plt.savefig(f'{output_dir}/{title}_runtime.png')
    plt.close()

# Exercício 2.4.
def compare_energy_consumption(rapl_file, codecarbon_files, output_dir):
    rapl_data = open_read_csv(rapl_file)
    codecarbon_data = []
    for file in codecarbon_files:
        codecarbon_data.extend(open_read_csv(file))

    if not rapl_data or not codecarbon_data:
        print("Erro: Dados insuficientes para comparação.")
        return

    programs = ['fibonacci_linear', 'fibonacci_recursive']
    for program in programs:
        # Filtrar dados do RAPL
        rapl_filtered = [
            row for row in rapl_data
            if program in row['Program'].lower()
        ]

        # Filtrar dados do CodeCarbon
        codecarbon_filtered = [
            row for row in codecarbon_data
            if row['Program'].lower() == program
        ]

        if not rapl_filtered:
            print(f"Erro: Dados insuficientes para {program} no RAPL. Pulando...")
            continue

        if not codecarbon_filtered:
            print(f"Erro: Dados insuficientes para {program} no CodeCarbon. Pulando...")
            continue

        # Calcular médias para RAPL
        rapl_O0 = [float(row['Package']) for row in rapl_filtered if '_O0_' in row['Program']]
        rapl_O2 = [float(row['Package']) for row in rapl_filtered if '_O2_' in row['Program']]
        avg_rapl_O0 = sum(rapl_O0) / len(rapl_O0) if rapl_O0 else 0
        avg_rapl_O2 = sum(rapl_O2) / len(rapl_O2) if rapl_O2 else 0

        # Converter energy_consumed de kWh para Joules no CodeCarbon
        codecarbon_O0 = [
            float(row['energy_consumed']) * 3.6e6
            for row in codecarbon_filtered
            if row['Optimization'] == 'O0'
        ]
        codecarbon_O2 = [
            float(row['energy_consumed']) * 3.6e6
            for row in codecarbon_filtered
            if row['Optimization'] == 'O2'
        ]
        avg_codecarbon_O0 = sum(codecarbon_O0) / len(codecarbon_O0) if codecarbon_O0 else 0
        avg_codecarbon_O2 = sum(codecarbon_O2) / len(codecarbon_O2) if codecarbon_O2 else 0

        # Criar gráfico comparativo
        plt.figure(figsize=(10, 6))
        labels = ['O0', 'O2']
        rapl_values = [avg_rapl_O0, avg_rapl_O2]
        codecarbon_values = [avg_codecarbon_O0, avg_codecarbon_O2]

        x = np.arange(len(labels))
        width = 0.35

        bars_rapl = plt.bar(x - width/2, rapl_values, width, label='RAPL', color='blue', edgecolor='black')
        bars_codecarbon = plt.bar(x + width/2, codecarbon_values, width, label='CodeCarbon', color='green', edgecolor='black')

        # Adicionar valores no topo das barras
        for bar in bars_rapl:
            plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height(), f'{bar.get_height():.2f}', ha='center', va='bottom')
        for bar in bars_codecarbon:
            plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height(), f'{bar.get_height():.2f}', ha='center', va='bottom')

        plt.xlabel('Optimization Level')
        plt.ylabel('Energy Consumption (Joules)')
        plt.title(f"Energy Consumption Comparison - {program}")
        plt.xticks(x, labels)
        plt.legend()
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.tight_layout()

        os.makedirs(output_dir, exist_ok=True)
        plt.savefig(f"{output_dir}/{program}_energy_comparison.png")
        plt.close()

def compare_runtime(rapl_file, codecarbon_files, output_dir):
    rapl_data = open_read_csv(rapl_file)
    codecarbon_data = []
    for file in codecarbon_files:
        codecarbon_data.extend(open_read_csv(file))

    if not rapl_data or not codecarbon_data:
        print("Erro: Dados insuficientes para comparação.")
        return

    programs = ['fibonacci_linear', 'fibonacci_recursive']
    for program in programs:
        # Filtrar dados do RAPL
        rapl_filtered = [
            row for row in rapl_data
            if program in row['Program'].lower()
        ]

        # Filtrar dados do CodeCarbon
        codecarbon_filtered = [
            row for row in codecarbon_data
            if row['Program'].lower() == program
        ]

        if not rapl_filtered:
            print(f"Erro: Dados insuficientes para {program} no RAPL. Pulando...")
            continue

        if not codecarbon_filtered:
            print(f"Erro: Dados insuficientes para {program} no CodeCarbon. Pulando...")
            continue

        # Calcular médias para RAPL
        rapl_O0 = [float(row['Time (ms)']) for row in rapl_filtered if '_O0_' in row['Program']]
        rapl_O2 = [float(row['Time (ms)']) for row in rapl_filtered if '_O2_' in row['Program']]
        avg_rapl_O0 = sum(rapl_O0) / len(rapl_O0) if rapl_O0 else 0
        avg_rapl_O2 = sum(rapl_O2) / len(rapl_O2) if rapl_O2 else 0

        # Converter duration de segundos para milissegundos no CodeCarbon
        codecarbon_O0 = [float(row['duration']) * 1000 for row in codecarbon_filtered if row['Optimization'] == 'O0']
        codecarbon_O2 = [float(row['duration']) * 1000 for row in codecarbon_filtered if row['Optimization'] == 'O2']
        avg_codecarbon_O0 = sum(codecarbon_O0) / len(codecarbon_O0) if codecarbon_O0 else 0
        avg_codecarbon_O2 = sum(codecarbon_O2) / len(codecarbon_O2) if codecarbon_O2 else 0

        # Criar gráfico comparativo
        plt.figure(figsize=(10, 6))
        labels = ['O0', 'O2']
        rapl_values = [avg_rapl_O0, avg_rapl_O2]
        codecarbon_values = [avg_codecarbon_O0, avg_codecarbon_O2]

        x = np.arange(len(labels))
        width = 0.35

        bars_rapl = plt.bar(x - width/2, rapl_values, width, label='RAPL', color='blue', edgecolor='black')
        bars_codecarbon = plt.bar(x + width/2, codecarbon_values, width, label='CodeCarbon', color='green', edgecolor='black')

        # Adicionar valores no topo das barras
        for bar in bars_rapl:
            plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height(), f'{bar.get_height():.2f}', ha='center', va='bottom')
        for bar in bars_codecarbon:
            plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height(), f'{bar.get_height():.2f}', ha='center', va='bottom')

        plt.xlabel('Optimization Level')
        plt.ylabel('Runtime (ms)')
        plt.title(f"Runtime Comparison - {program}")
        plt.xticks(x, labels)
        plt.legend()
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.tight_layout()

        os.makedirs(output_dir, exist_ok=True)
        plt.savefig(f"{output_dir}/{program}_runtime_comparison.png")
        plt.close()

if __name__ == "__main__":
    output_dir = os.path.join(os.getcwd(), 'Plots')
    rapl_files = "./CSV/measurements.csv"
    codecarbon_files = ["./CSV/emissions_Fibonacci_Linear.csv", "./CSV/emissions_Fibonacci_Recursive.csv"]
    # all_data = open_read_csv("./CSV/measurements_ex6.csv")
    #all_data = open_read_csv("./CSV/measurements_compare.csv")
    #all_data = open_read_csv("./CSV/measurements_PowerCap.csv"F
    #all_data = collect_data_from_directories("measurements.csv")
    
    variables = {
        'Package': 'Energy Consumption (Joules)',
        'Core(s)': 'Energy Consumption (Joules)',
        'Time (ms)': 'Time (ms)',
        'Temperature': 'Temperature (Celsius)',
        'Memory': 'Memory (KBytes)'
    }
    
    #for title, data in all_data.items():
    #for variable, ylabel in variables.items():
        #plot_multiple_metrics(all_data, output_dir, "measurements", [variable], ylabel)
    
    #plot_comparative_metrics(all_data, output_dir)
    
    # Exercício de PowerCap
    #result = subprocess.run(["python3", "powercap.py"], check=True, capture_output=True, text=True)
    #output = result.stdout
    #powercap = re.search(r'Optimal Power Cap: (\d+)W', output).group(1)
    #print(f"Power Cap: {powercap}")

    #powercaps = [int(powercap), -1]
    #plot_comparative_metrics_powercaps({"measurements": all_data}, output_dir, powercaps)
    
    #plot_gps_up_powercaps(all_data, output_dir, powercaps)

    #plot_gps_up(all_data['measurements'], output_dir)

    # Exercício 1.7.
    #plot_energy_consumption(all_data, output_dir, "measurements")
    #plot_runtime(all_data, output_dir, "measurements")

    # Exercício 2.4.
    compare_energy_consumption(rapl_files, codecarbon_files, output_dir)
    compare_runtime(rapl_files, codecarbon_files, output_dir)