def get_data_dea(df, ano=None, dmus=None, colunas_inputs=None, colunas_outputs=None):
    """
    Filtra e organiza os dados para análise DEA de maneira geral, com variáveis em português.
    Verifica também se a regra básica de DMUs, inputs e outputs é atendida.

    :param df: DataFrame contendo os dados completos.
    :param ano: Ano desejado para análise (None para ignorar filtro por ano).
    :param dmus: Lista de DMUs de interesse (None para ignorar filtro por DMUs).
    :param colunas_inputs: Lista de colunas que serão usadas como inputs.
    :param colunas_outputs: Lista de colunas que serão usadas como outputs.
    :return: DataFrame filtrado e organizado com DMUs, inputs e outputs.
    """
    try:
        # Filtro pelo ano, se for especificado
        if ano is not None:
            df_filtrado = df[df['ano'] == ano]
        else:
            df_filtrado = df.copy()  # Ignora o filtro por ano

        # Filtro pelas DMUs, se especificadas
        if dmus is not None:
            df_filtrado = df_filtrado[df_filtrado['dmu'].isin(dmus)]

        # Seleção das colunas: dmu, inputs e outputs
        if colunas_inputs is None or colunas_outputs is None:
            raise ValueError("As listas de colunas de inputs e outputs devem ser fornecidas.")

        colunas_selecionadas = ['dmu'] + colunas_inputs + colunas_outputs
        data_dea = df_filtrado[colunas_selecionadas]

        # Verificar a regra básica de DEA
        num_dmus = len(data_dea['dmu'].unique())
        num_inputs = len(colunas_inputs)
        num_outputs = len(colunas_outputs)
        min_dmus = 3 * (num_inputs + num_outputs)

        if num_dmus < min_dmus:
            print("\n")
            print("************************************************************")
            print(f"AVISO: Número de DMUs ({num_dmus}) é insuficiente!")
            print(f"Número mínimo de DMUs necessário: {min_dmus}.")
            print(f"Inputs fornecidos: {num_inputs}. Outputs fornecidos: {num_outputs}.")
            print("SUGESTÃO: Adicione mais DMUs ou reduza inputs/outputs.")
            print("************************************************************")
            print("\n")

        print("Dados do DEA organizadoss com sucesso!")
        #print(data_dea.info())  # Mostra informações gerais do DataFrame
        #print(data_dea.head())
        return data_dea

    except KeyError as e:
        print(f"Erro: Coluna não encontrada - {e}")
    except ValueError as e:
        print(f"Erro: {e}")
    except Exception as e:
        print(f"Erro ao preparar os dados: {e}")

