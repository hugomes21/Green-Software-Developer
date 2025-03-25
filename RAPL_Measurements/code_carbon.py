import os
import pandas as pd
from codecarbon import OfflineEmissionsTracker
import subprocess

# Caminhos para os diretórios dos programas
program_paths = ["./Languages/C/Fibonacci_Linear", "./Languages/C/Fibonacci_Recursive"]
sizes = [10, 30, 40]  # Valores de entrada para o tamanho
n_times = 10  # Número de execuções por programa
optimizations = ["O0", "O2"]  # Otimizações a serem usadas

# Loop pelos diretórios dos programas
for program_path in program_paths:
    # Nome do arquivo CSV consolidado para o programa atual
    program_name = program_path.split('/')[-1]
    output_file = f"emissions_{program_name}.csv"
    consolidated_data = []  # Lista para armazenar os dados de todas as execuções

    for size in sizes:
        for optimization in optimizations:
            # Compilar o programa com a otimização especificada
            compile_command = f'make -C "{program_path}" compile_{optimization} size={size}'
            print(f"Compilando: {compile_command}")
            subprocess.run(compile_command, shell=True, check=True)

            # Loop para executar o programa 10 vezes
            for i in range(1, n_times + 1):
                print(f"\nExecução {i}/{n_times} no programa {program_path} com otimização {optimization} e tamanho {size}:")

                # Iniciar o rastreador do CodeCarbon
                tracker = OfflineEmissionsTracker(country_iso_code="PRT")
                tracker.start()

                # Executar o programa com a otimização especificada
                exec_command = f'make -C "{program_path}" exec_{optimization} size={size}'
                print(f"Executando: {exec_command}")
                subprocess.run(exec_command, shell=True, check=True)

                # Parar o rastreador e obter as emissões
                tracker.stop()

                # Verificar se o arquivo emissions.csv foi gerado
                if os.path.exists("emissions.csv"):
                    # Ler o arquivo emissions.csv
                    df = pd.read_csv("emissions.csv")
                    
                    # Verificar se o DataFrame contém dados antes de processar
                    if not df.empty:
                        # Selecionar colunas específicas (substitua pelos nomes reais das colunas)
                        selected_columns = ['duration', 'emissions', 'cpu_power', 'ram_power', 'cpu_energy', 'ram_energy', 'energy_consumed', 'ram_total_size']  # Exemplo
                        filtered_df = df[selected_columns]

                        # Adicionar informações adicionais (programa, otimização, execução e tamanho)
                        filtered_df['Program'] = program_name
                        filtered_df['Optimization'] = optimization
                        filtered_df['Execution'] = i
                        filtered_df['Size'] = size

                        # Adicionar os dados ao consolidado
                        consolidated_data.append(filtered_df)
                    else:
                        print(f"O arquivo emissions.csv está vazio na execução {i}.")
                else:
                    print(f"emissions.csv não encontrado na execução {i}.")

    # Salvar os dados consolidados no arquivo CSV do programa
    if consolidated_data:
        final_df = pd.concat(consolidated_data, ignore_index=True)
        final_df.to_csv(output_file, index=False)
        print(f"Resultados consolidados salvos em {output_file}")
    else:
        print(f"Nenhum dado foi coletado para o programa {program_name}.")