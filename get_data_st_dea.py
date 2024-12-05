def get_data_st_dea(df, dmu_col, dmus=None, colunas_inputs=None, colunas_outputs=None):
    """
    Filtra e organiza os dados para análise DEA de maneira geral.
    Verifica também se a regra básica de DMUs, inputs e outputs é atendida.
    
    :param df: DataFrame contendo os dados completos.
    :param dmu_col: Nome da coluna que contém os identificadores das DMUs.
    :param dmus: Lista de DMUs de interesse (None para ignorar filtro por DMUs).
    :param colunas_inputs: Lista de colunas que serão usadas como inputs.
    :param colunas_outputs: Lista de colunas que serão usadas como outputs.
    :return: DataFrame filtrado e organizado com DMUs, inputs e outputs.
    """
    try:
        df_filtrado = df.copy()
        
        # Validar se o nome da coluna de DMUs é uma string
        if not isinstance(dmu_col, str):
            raise ValueError("O parâmetro 'dmu_col' deve ser uma string representando o nome da coluna das DMUs.")
        
        # Filtro pelas DMUs, se especificadas
        if dmus is not None:
            df_filtrado = df_filtrado[df_filtrado[dmu_col].isin(dmus)]
            
        # Seleção das colunas: dmu, inputs e outputs
        if colunas_inputs is None or colunas_outputs is None:
            raise ValueError("As listas de colunas de inputs e outputs devem ser fornecidas.")
            
        colunas_selecionadas = [dmu_col] + colunas_inputs + colunas_outputs
        data_dea = df_filtrado[colunas_selecionadas]
        
        # Verificar a regra básica de DEA
        num_dmus = len(data_dea[dmu_col].unique())
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
            
        print("Dados do DEA organizados com sucesso!")
        return data_dea
        
    except KeyError as e:
        print(f"Erro: Coluna não encontrada - {e}")
    except ValueError as e:
        print(f"Erro: {e}")
    except Exception as e:
        print(f"Erro ao preparar os dados: {e}")

