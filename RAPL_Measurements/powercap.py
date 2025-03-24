import pandas as pd

# Carregar o arquivo CSV
file_path = "/home/hugomes21/Desktop/4º Ano/2º Semestre/sdvm/tds/Green-Software-Developer/RAPL_Measurements/Languages/measurements_PowerCap.csv"
data = pd.read_csv(file_path)

# Calcular a energia consumida (J)
data['Energy (J)'] = data[' Package'] * (data[' Time (ms)'] / 1000)

# Agrupar por PowerLimit e calcular a média da energia consumida
grouped = data.groupby(' PowerLimit')['Energy (J)'].mean()

# Encontrar o PowerLimit com o menor consumo de energia
optimal_power_cap = grouped.idxmin()
optimal_energy = grouped.min()

print(f"Optimal Power Cap: {optimal_power_cap}W")
print(f"Lowest Energy Consumption: {optimal_energy:.6f}J")