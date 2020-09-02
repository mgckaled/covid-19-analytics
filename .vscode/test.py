# livraria

# Download do dataset 
def main(): 

    import sys 
    import requests
    import pandas as pd
    import numpy as np
    import matplotlib.pyplot as plt
    from IPython.display import clear_output 


    stdoutOrigin=sys.stdout 
    sys.stdout = open("log_cidade.txt", "w")   

    def dload_ds():
        download_url = "https://data.brasil.io/dataset/covid19/caso.csv.gz"
        target_csv_path = "caso.csv.gz"

        response = requests.get(download_url)
        response.raise_for_status()    # Check that the request was successful
        with open(target_csv_path, "wb") as f:
            f.write(response.content)

    # descomprimir arquivo 'gz'    
    df = pd.read_csv('caso.csv.gz', compression='gzip',error_bad_lines=False)

    # Input do estado e filtro do mesmo
    estado = str(input('\nDigite o estado conforme a lista acima: ')).upper()
    df_estado = df[df['state'] == estado]

    # Input da cidade e filtro da mesma
    cidade = input('\nDigite o nome da cidade a lista acima: ')
    df_cidade = df[df['city'] == cidade]

     # Filtro de quantidades por estado e município 
    tot_conf_est = df_estado[(df_estado["place_type"] == 'state')].iloc[0].values[4]
    tot_morte_est = df_estado[(df_estado["place_type"] == 'state')].iloc[0].values[5]
    tot_conf_cid = df_cidade[(df_cidade["is_last"] == True)].iloc[0].values[4]
    tot_mortes_cid = df_cidade[(df_cidade["is_last"] == True)].iloc[0].values[5]
    conf_per_100mil = df_cidade[(df_cidade["is_last"] == True)].iloc[0].values[10]
    tx_morte = df_cidade[(df_cidade["is_last"] == True)].iloc[0].values[11] * 100

    def grafico():
        fig, ax = plt.subplots(figsize=(15,5))
        fig.subplots_adjust(top=0.80)
        fig.suptitle(f'Evolução Covid-19 em {cidade} ({estado})',fontsize=14, fontweight='bold')
        ax.plot(df_cidade['order_for_place'], df_cidade['confirmed'],'b-', label="Casos Confirmados")
        ax.plot(df_cidade['order_for_place'], df_cidade['deaths'],'r-',label="Mortes",)
        ax.legend()
        ax.set(xlabel='$dias$ $após$ $o$ $primeiro$ $caso$',
        title=f'Casos confirmados:{tot_conf_cid} ** Mortes:{tot_mortes_cid} ** Casos por 100k/Hab.: {conf_per_100mil:.2f} ** Taxa de Mortalidade:{tx_morte:.2f}%')
        plt.grid(axis='y')
        fig.savefig('evol_c19_cid.png')

    def output_dados():

        print('Dados Covid-19 por Estado:\n ')

        for x in df.state.unique().astype(str):
            a = df[(df["state"] == x) & df['is_last'] == True].iloc[0].values[4]
            b = df[(df["state"] == x) & df['is_last'] == True].iloc[0].values[5]
            c = df[(df["state"] == x) & df['is_last'] == True].iloc[0].values[10]
            d = df[(df["state"] == x) & df['is_last'] == True].iloc[0].values[11] * 100
        print(f'''********* {x} **********
        Casos Confirmados: {a}
        Mortes: {b}
        Casos por 100k/Hab.: {c:.2f}
        Taxa de Mortalidade: {d:.2f}%
        ''')

        print('Dados Covid-19 por cidade:\n ')

        # Eliminar todas as linhas da coluna da cidade cujo valor seja Nan ou nulo.
        df1 = df.dropna(subset = ['city'])

        #Loop de exibição dos valores e dados de cada cidade: 
        for y in df1.city.unique():
            e = df1[(df1["city"] == y) & df1['is_last'] == True].iloc[0].values[4]
            f = df1[(df1["city"] == y) & df1['is_last'] == True].iloc[0].values[5]
            g = df1[(df1["city"] == y) & df1['is_last'] == True].iloc[0].values[10]
            h = df1[(df1["city"] == y) & df1['is_last'] == True].iloc[0].values[11] * 100
            j = df1[(df1["city"] == y) & df1['is_last'] == True].iloc[0].values[2]
        print(f'''*** {y} ({j}) ***
        Casos Confirmados: {e}
        Mortes: {f}
        Casos por 100k/Hab.: {g:.2f}
        Taxa de Mortalidade: {h:.2f}%
        ''')

    dload_ds()
    grafico()
    output_dados()

    sys.stdout.close()
    sys.stdout=stdoutOrigin

if __name__ == '__main__':
    main()
