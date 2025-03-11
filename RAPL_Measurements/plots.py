import matplotlib.pyplot as plt
import csv
import os
import numpy as np

def open_read_csv(file_path):
    with open(file_path, 'r') as file:
        reader = csv.DictReader(file)
        data = [{key.strip(): value.strip() for key, value in row.items()} for row in reader]
    return data

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

def collect_data_from_directories():
    all_data = {}
    file_path = os.path.join(os.path.dirname(__file__), 'measurements.csv')
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

if __name__ == "__main__":
    output_dir = os.path.join(os.getcwd(), 'Plots')
    all_data = collect_data_from_directories()
    
    variables = {
        'Package': 'Energy Consumption (Joules)',
        'Core(s)': 'Energy Consumption (Joules)',
        'Time (ms)': 'Time (ms)',
        'Temperature': 'Temperature (Celsius)',
        'Memory': 'Memory (KBytes)'
    }
    
    for title, data in all_data.items():
        for variable, ylabel in variables.items():
            plot_multiple_metrics(data, output_dir, title, [variable], ylabel)
    
    plot_comparative_metrics(all_data, output_dir)
    plot_gps_up(all_data['measurements'], output_dir)