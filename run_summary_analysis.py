# run_summary_analysis.py
import json
import os
# Adiciona o diretório raiz ao sys.path para permitir importações relativas
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.services import summary_service

# Obtém o caminho absoluto do diretório do script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Constrói os caminhos absolutos para os arquivos de entrada e saída
api_response_path = os.path.join(script_dir, 'api_response_test.json')
output_path = os.path.join(script_dir, 'resource_summary.json')

# Carrega os dados de exemplo da fazenda
try:
    with open(api_response_path, 'r') as f:
        farm_data = json.load(f)    
except FileNotFoundError:
    print(f"Erro: Arquivo de entrada não encontrado em {api_response_path}")
    exit(1)
except json.JSONDecodeError:
    print(f"Erro: Não foi possível decodificar o JSON de {api_response_path}")
    exit(1)

# Executa a análise de sumário
summary_data = summary_service.analyze_resources_summary(farm_data)

# Escreve o resultado em um novo arquivo JSON
with open(output_path, 'w') as f:
    json.dump(summary_data, f, indent=4)

print(f"Sumário de recursos gerado com sucesso em {output_path}")
