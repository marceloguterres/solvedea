import numpy as np
from scipy.optimize import linprog
import pandas as pd

def get_ccr_output_mult(data_dea, inputs, outputs):
    """
    DEA CCR multiplicadores orientado a outputs, com impressão do PPL completo
    """
    n_dmus = len(data_dea)
    n_inputs = len(inputs)
    n_outputs = len(outputs)
    resultados = []
    
    for idx, dmu_alvo in data_dea.iterrows():
        print("\n" + "="*80)
        print(f"PROBLEMA DE PROGRAMAÇÃO LINEAR - DMU {dmu_alvo['dmu']}")
        print("="*80)
        
        # Matriz de restrições para todas as DMUs
        A_ub = []
        b_ub = []
        
        # Construir e mostrar a função objetivo
        print("\nFUNÇÃO OBJETIVO:")
        fo_termos = []
        for out in outputs:
            fo_termos.append(f"u_{out}*{dmu_alvo[out]:.4f}")
        print(f"max θ = {' + '.join(fo_termos)}")
        
        print("\nSUJEITO A:")
        
        # Mostrar restrição de normalização
        norm_termos = []
        for inp in inputs:
            norm_termos.append(f"v_{inp}*{dmu_alvo[inp]:.4f}")
        print(f"\n1. {' + '.join(norm_termos)} = 1")
        
        print("\n2. Restrições de eficiência para cada DMU:")
        # Construir restrições para cada DMU
        for _, dmu in data_dea.iterrows():
            # Coeficientes dos inputs e outputs
            input_terms = []
            output_terms = []
            
            # Termos dos outputs
            for out in outputs:
                output_terms.append(f"u_{out}*{dmu[out]:.4f}")
                
            # Termos dos inputs
            for inp in inputs:
                input_terms.append(f"v_{inp}*{dmu[inp]:.4f}")
            
            # Mostrar restrição completa
            print(f"   DMU {dmu['dmu']}: {' + '.join(output_terms)} - ({' + '.join(input_terms)}) ≤ 0")
            
            # Adicionar à matriz de restrições
            input_coef = [-dmu[inp] for inp in inputs]
            output_coef = [dmu[out] for out in outputs]
            A_ub.append(input_coef + output_coef)
            b_ub.append(0)
            
        # Restrição de normalização dos inputs
        A_eq = [[dmu_alvo[inp] for inp in inputs] + [0]*n_outputs]
        b_eq = [1]
        
        # Função objetivo
        c = [0]*n_inputs + [-dmu_alvo[out] for out in outputs]
        
        print("\n3. Restrições de não-negatividade:")
        for inp in inputs:
            print(f"   v_{inp} ≥ 0.000001")
        for out in outputs:
            print(f"   u_{out} ≥ 0.000001")
        
        print("\nMATRIZES DO PROBLEMA:")
        print(f"A_ub shape: {np.array(A_ub).shape}")
        print(f"b_ub shape: {np.array(b_ub).shape}")
        print(f"A_eq shape: {np.array(A_eq).shape}")
        print(f"b_eq shape: {np.array(b_eq).shape}")
        print(f"c shape: {np.array(c).shape}")
        
        # Resolver
        res = linprog(
            c=c,
            A_ub=np.array(A_ub),
            b_ub=np.array(b_ub),
            A_eq=np.array(A_eq),
            b_eq=np.array(b_eq),
            bounds=[(0.000001, None)]*(n_inputs + n_outputs),
            method='highs'
        )
        
        if res.success:
            # Separar multiplicadores
            v = res.x[:n_inputs]
            u = res.x[n_inputs:]
            
            eficiencia = -res.fun
            
            resultado = {
                'DMU': dmu_alvo['dmu'],
                'Eficiência': eficiencia
            }
            
            # Adicionar multiplicadores
            for i, inp in enumerate(inputs):
                resultado[f'v_{inp}'] = v[i]
            for i, out in enumerate(outputs):
                resultado[f'u_{out}'] = u[i]
            
            print("\nSOLUÇÃO ÓTIMA:")
            print(f"Eficiência: {eficiencia:.6f}")
            print("Multiplicadores dos inputs:", {inp: f"{v[i]:.6f}" for i, inp in enumerate(inputs)})
            print("Multiplicadores dos outputs:", {out: f"{u[i]:.6f}" for i, out in enumerate(outputs)})
                
        else:
            resultado = {
                'DMU': dmu_alvo['dmu'],
                'Eficiência': None
            }
            print(f"\nERRO: Não foi possível encontrar solução ótima para DMU {dmu_alvo['dmu']}!")
            
        resultados.append(resultado)
        print("="*80 + "\n")
    
    return pd.DataFrame(resultados)
