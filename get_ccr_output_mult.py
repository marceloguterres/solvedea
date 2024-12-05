from scipy.optimize import linprog
import pandas as pd

def get_ccr_output_mult(data, dmu_col, inputs, outputs):
    """
    Implementa o modelo CCR DEA orientado a output com retorno de DataFrame formatado.
    
    Parâmetros:
    data (DataFrame): DataFrame contendo os dados das DMUs
    inputs (list): Lista com os nomes das colunas dos inputs
    outputs (list): Lista com os nomes das colunas dos outputs
    dmu_col (str): Nome da coluna que contém os identificadores das DMUs
    
    Implementa o modelo CCR DEA orientado a output conforme a formulação:
    max z = Σ u_jm * y_jm
    sujeito a:
    Σ v_im * x_im = 1 (normalização)
    Σ u_jm * y_jn - Σ v_im * x_in ≤ 0 (para cada DMU n)
    u_jm, v_im ≥ ε
    
    Retorna os resultados incluindo:
    - Nome da DMU (identificador original da DMU)
    - phi (medida de eficiência - quanto maior, menos eficiente)
    - Et (eficiência técnica = 1/phi - quanto mais próximo de 1, mais eficiente)
    - Multiplicadores u (outputs) e v (inputs)
    """
    num_dmus = len(data)
    num_inputs = len(inputs)
    num_outputs = len(outputs)
    
    results = []
    
    for m in range(num_dmus):
        dmu_atual = data.iloc[m]
        
        # Configuração do problema permanece a mesma
        num_vars = num_outputs + num_inputs
        
        # Função objetivo: maximizar Σ u_jm * y_jm (multiplicadores u para outputs)
        c = []
        for output_col in outputs:
            c.append(-dmu_atual[output_col])
        c.extend([0] * num_inputs)
        
        # Restrições
        A_eq = []
        b_eq = []
        A_ub = []
        b_ub = []
        
        # Restrição de normalização (usando multiplicadores v para inputs)
        norm_constraint = [0] * num_outputs
        for input_col in inputs:
            norm_constraint.append(dmu_atual[input_col])
        A_eq.append(norm_constraint)
        b_eq.append(1)
        
        # Restrições de eficiência
        for n in range(num_dmus):
            dmu_n = data.iloc[n]
            efficiency_constraint = []
            
            for output_col in outputs:
                efficiency_constraint.append(dmu_n[output_col])
            for input_col in inputs:
                efficiency_constraint.append(-dmu_n[input_col])
                
            A_ub.append(efficiency_constraint)
            b_ub.append(0)
        
        # Restrições de não-negatividade
        epsilon = 1e-6
        bounds = [(epsilon, None)] * num_vars
        
        # Resolvendo o problema
        result = linprog(c, A_ub=A_ub, b_ub=b_ub, A_eq=A_eq, b_eq=b_eq, 
                        bounds=bounds, method='highs')
        
        if result.success:
            # Calculando phi e Et
            z_m = -result.fun
            phi = 1/z_m if z_m != 0 else float('inf')
            et = z_m if z_m != 0 else 0  # Et = 1/phi
            
            # Extraindo os multiplicadores (u para outputs, v para inputs)
            u_values = result.x[:num_outputs]  # Multiplicadores u (outputs)
            v_values = result.x[num_outputs:]  # Multiplicadores v (inputs)
            
            dmu_result = {
                'DMU': dmu_atual[dmu_col],
                'Phi': phi,
                'Et (1/Phi)': et,
                'Status': 'Eficiente' if abs(et - 1) < 1e-5 else 'Ineficiente'
            }
            
            # Salvando os multiplicadores dos outputs (u)
            for j, output_col in enumerate(outputs):
                dmu_result[f'u_{output_col}'] = u_values[j]
            
            # Salvando os multiplicadores dos inputs (v)
            for i, input_col in enumerate(inputs):
                dmu_result[f'v_{input_col}'] = v_values[i]
            
            results.append(dmu_result)
        else:
            print(f"Erro ao resolver para DMU {dmu_atual[dmu_col]}: {result.message}")
    
    return pd.DataFrame(results)
