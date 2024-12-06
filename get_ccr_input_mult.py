from scipy.optimize import linprog
import pandas as pd

def get_ccr_input_mult(data, dmu_col, inputs, outputs):
    """
    Implementa o modelo CCR DEA orientado a input na forma de multiplicadores.
    Parâmetros:
    - data (DataFrame): DataFrame contendo os dados das DMUs.
    - dmu_col (str): Nome da coluna que contém os identificadores das DMUs.
    - inputs (list): Lista com os nomes das colunas dos inputs.
    - outputs (list): Lista com os nomes das colunas dos outputs.
    Retorna:
    - DataFrame com os resultados (eficiência e status de cada DMU).
    """
    num_dmus = len(data)
    num_inputs = len(inputs)
    num_outputs = len(outputs)
    results = []

    for m in range(num_dmus):
        dmu_atual = data.iloc[m]
        num_vars = num_inputs + num_outputs

        # Função objetivo: minimizar Σ v_im * x_im
        c = [dmu_atual[input_col] for input_col in inputs]
        c += [0] * num_outputs

        # Restrição de normalização: Σ u_jm * y_jm = 1
        A_eq = []
        b_eq = []
        norm_constraint = [0] * num_inputs
        norm_constraint += [dmu_atual[output_col] for output_col in outputs]
        A_eq.append(norm_constraint)
        b_eq.append(1)

        # Restrições de eficiência: Σ u_jm * y_jn - Σ v_im * x_in ≤ 0
        A_ub = []
        b_ub = []
        for n in range(num_dmus):
            dmu_n = data.iloc[n]
            efficiency_constraint = [-dmu_n[input_col] for input_col in inputs]
            efficiency_constraint += [dmu_n[output_col] for output_col in outputs]
            A_ub.append(efficiency_constraint)
            b_ub.append(0)

        # Restrições de não-negatividade
        epsilon = 1e-6
        bounds = [(epsilon, None)] * num_vars

        # Resolvendo o problema
        result = linprog(c, A_ub=A_ub, b_ub=b_ub, A_eq=A_eq, b_eq=b_eq, 
                        bounds=bounds, method='highs')

        if result.success:
            # Theta é diretamente o valor da função objetivo
            theta = result.fun
            et = 1 / theta if theta != 0 else float('inf')  # Et = 1/Theta
            
            # Extraindo os multiplicadores
            v_values = result.x[:num_inputs]  # Multiplicadores dos inputs (v)
            u_values = result.x[num_inputs:]  # Multiplicadores dos outputs (u)
            
            dmu_result = {
                'DMU': dmu_atual[dmu_col],
                'Theta': theta,
                'Et (1/Theta)': et,
                'Status': 'Eficiente' if abs(theta - 1) < 1e-5 else 'Ineficiente'
            }
            
            # Adicionando os multiplicadores ao resultado
            for i, input_col in enumerate(inputs):
                dmu_result[f"v_{input_col}"] = v_values[i]
            for j, output_col in enumerate(outputs):
                dmu_result[f"u_{output_col}"] = u_values[j]
            
            results.append(dmu_result)
        else:
            print(f"Erro ao resolver para DMU {dmu_atual[dmu_col]}: {result.message}")

    return pd.DataFrame(results)
