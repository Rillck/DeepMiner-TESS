import os
import gc
import numpy as np
import pandas as pd
import lightkurve as lk
import inquirer
import shutil

print(r"""
──────────────────────────────────────────────────────────────────
                 Welcome to DeepMiner-TESS! 
──────────────────────────────────────────────────────────────────
""")

def limpar_cache_lightkurve():
    home_dir = os.path.expanduser("~")
    tess_path = os.path.join(home_dir, ".lightkurve", "cache", "mastDownload", "TESS")
    if os.path.exists(tess_path):
        for filename in os.listdir(tess_path):
            file_path = os.path.join(tess_path, filename)
            try:
                if os.path.isfile(file_path):
                    os.remove(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print(f"Erro ao apagar {file_path}: {e}")

def download_light_curves():
    def escolher_arquivo_txt():
        arquivos_txt = [f for f in os.listdir('.') if f.endswith('.txt')]
        if not arquivos_txt:
            print("No .txt files found in the current directory.")
            return None
        pergunta = [
            inquirer.List(
                'file',
                message="Choose the .txt file you want to analyze",
                choices=arquivos_txt,
            ),
        ]
        resposta = inquirer.prompt(pergunta)
        return resposta['file']

    def obter_nome_pasta_download():
        pasta = input("Enter the name of the folder that will receive the downloaded files [dat]: ")
        if not pasta.strip():
            pasta = 'dat'
        if not os.path.exists(pasta):
            os.makedirs(pasta)
        return pasta

    def read_file(file_path):
        with open(file_path, 'r') as f:
            lines = f.readlines()
        separator_index = lines.index('===\n')
        config_lines = lines[:separator_index]
        configurations = [tuple(line.strip().split(';')) for line in config_lines if line.strip()]
        configurations = [(author, int(exptime)) for author, exptime in configurations]
        tic_lines = lines[separator_index + 1:]
        tic_list = [int(line.strip()) for line in tic_lines if line.strip()]
        return configurations, tic_list

    def download_lightcurves(configurations, tic_list, pasta_de_download, block_size=250):
        total_tics = len(tic_list)
        contador_target = 1
        for start in range(0, total_tics, block_size):
            tic_block = tic_list[start:start + block_size]
            for tic in tic_block:
                for author, exptime in configurations:
                    search = lk.search_lightcurve(f'TIC {tic}', mission='TESS', author=author, exptime=exptime)
                    for j in range(len(search)):
                        if search.table['target_name'][j] == str(tic):
                            sector = search.table['mission'][j][12:]
                            sector = int(sector)
                            if limit_sector and sector > max_sector:
                                continue
                            file_name = f'{pasta_de_download}/{tic}_{sector}_{author}{exptime}.dat'
                            #if os.path.exists(file_name):
                                #continue
                            lc = search[j].download(quality_bitmask='none')
                            time = lc.time.value
                            flux = lc.flux.value
                            data = pd.DataFrame(np.column_stack([time, flux]), columns=['Time', 'Flux']).dropna()
                            data.to_csv(file_name, sep=' ', index=False, header=False)
                            del lc, time, flux, data
                            gc.collect()
                print(f'Targets analyzed: [{contador_target}/{total_tics}] ({(contador_target / total_tics) * 100:.2f}%)', end='\r')
                if contador_target % 100 == 0:
                    limpar_cache_lightkurve()
                contador_target += 1

    # Escolher o arquivo .txt para análise
    file_path = escolher_arquivo_txt()
    if not file_path:
        print("No file selected. Returning to the main menu.")
        return

    # Obter a pasta de download dos arquivos
    pasta_de_download = obter_nome_pasta_download()

    # Perguntar se deseja limitar o número de setores
    pergunta_limite = [
        inquirer.List(
            'limitar',
            message="Do you want to limit the sector number?",
            choices=['No', 'Yes'],
            default='No',
        )
    ]
    resposta = inquirer.prompt(pergunta_limite)

    limit_sector = False
    max_sector = None

    if resposta['limitar'] == 'Yes':
        max_sector = int(input("Enter the maximum sector number (e.g., 10): "))
        limit_sector = True

    # Ler o arquivo e baixar as curvas de luz
    configurations, tic_list = read_file(file_path)
    download_lightcurves(configurations, tic_list, pasta_de_download)

    print(rf"""
    ──────────────────────────────────────────────────────────────────
                        Download Completed!
    ──────────────────────────────────────────────────────────────────
    All files were saved in '{pasta_de_download}'.
    """)

# Execução direta
download_light_curves()
