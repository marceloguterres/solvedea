import streamlit as st
import pandas as pd
from get_data_st_dea import get_data_st_dea
from get_ccr_output_mult import get_ccr_output_mult

st.set_page_config(
    page_title="DEA Analysis",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Criando a seção dos desenvolvedores com estilo
st.markdown("""
    <div style='background-color: #f0f2f6; padding: 2rem; border-radius: 10px; margin-bottom: 2rem'>
        <h2 style='text-align: center; color: #1f77b4; margin-bottom: 1.5rem'>Developed by</h2>
        <div style='display: flex; justify-content: center; gap: 2rem; flex-wrap: wrap'>
            <div style='text-align: center; flex: 1; min-width: 200px; background-color: white; padding: 1.5rem; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1)'>
                <h3 style='color: #2c3e50; margin-bottom: 0.5rem'>Prof. Marcelo Xavier Guterres</h3>
                <p style='margin-bottom: 1rem'>Professor</p>
                <a href='https://www.linkedin.com/in/profguterres/' target='_blank' style='background-color: #0077b5; color: white; padding: 0.5rem 1rem; text-decoration: none; border-radius: 5px'>LinkedIn Profile</a>
            </div>
            <div style='text-align: center; flex: 1; min-width: 200px; background-color: white; padding: 1.5rem; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1)'>
                <h3 style='color: #2c3e50; margin-bottom: 0.5rem'>Profa. Viviane Falcão</h3>
                <p style='margin-bottom: 1rem'>Professor</p>
                <a href='https://www.linkedin.com/in/viviane-falc%C3%A3o-4b481633/' target='_blank' style='background-color: #0077b5; color: white; padding: 0.5rem 1rem; text-decoration: none; border-radius: 5px'>LinkedIn Profile</a>
            </div>
            <div style='text-align: center; flex: 1; min-width: 200px; background-color: white; padding: 1.5rem; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1)'>
                <h3 style='color: #2c3e50; margin-bottom: 0.5rem'>Maria Clara Seffrin</h3>
                <p style='margin-bottom: 1rem'>Master's Student</p>
                <a href='https://www.linkedin.com/in/mariaclaraseffrin/' target='_blank' style='background-color: #0077b5; color: white; padding: 0.5rem 1rem; text-decoration: none; border-radius: 5px'>LinkedIn Profile</a>
            </div>
        </div>
    </div>
""", unsafe_allow_html=True)

st.title("Data Envelopment Analysis")

# Upload de arquivo
st.sidebar.header("Upload Data")
uploaded_file = st.sidebar.file_uploader(
    "Choose your input file",
    type=['csv', 'xlsx', 'xls']
)

# Model selection
st.sidebar.header("Select Parameters")
selectbox_model = st.sidebar.selectbox(
    "Select the DEA model?",
    ("Model 1", "Model 2", "Model 3")
)

# Adicionar a descrição técnica do modelo
if selectbox_model == "Model 1":
    st.markdown("""
    <div style='background-color: #f8f9fa; padding: 20px; border-radius: 10px; border-left: 5px solid #0077b5; margin: 20px 0;'>
        <h3 style='color: #0077b5; margin-bottom: 10px'>Model 1: CCR-O (Charnes, Cooper, and Rhodes - Output Oriented)</h3>
        <p style='margin-bottom: 10px'><strong>Technical Specification:</strong></p>
        <ul style='list-style-type: none; padding-left: 0;'>
            <li>• <strong>Returns to Scale:</strong> Constant Returns to Scale (CRS)</li>
            <li>• <strong>Orientation:</strong> Output-oriented Multiplier Model</li>
            <li>• <strong>Mathematical Framework:</strong> Linear Programming Problem that maximizes the ratio of weighted outputs to weighted inputs</li>
        </ul>
        <p style='margin-top: 10px; font-style: italic'>This model assumes constant returns to scale and focuses on maximizing outputs while maintaining the current level of inputs. It's particularly suitable for operations where proportional changes in inputs result in proportional changes in outputs.</p>
        <p style='font-size: 0.9em; margin-top: 15px;'>Reference: Charnes, A.; Cooper, W.W.; Rhodes, E. (1978). "Measuring the efficiency of decision making units". European Journal of Operational Research. 2 (6): 429–444.</p>
    </div>
    """, unsafe_allow_html=True)

# Input e Output variables
input_vars_text = st.sidebar.text_input(
    "Enter input variables (comma-separated)",
    help="Example: x1, x2, x3"
)
output_vars_text = st.sidebar.text_input(
    "Enter output variables (comma-separated)",
    help="Example: y1, y2, y3"
)

# Campo de DMUs com valor padrão vazio (None)
dmus_vars_text = st.sidebar.text_input(
    "Enter DMUs (comma-separated, leave empty for all)", 
    value=""
)

# Converter strings em listas (apenas se não estiverem vazias)
input_vars = [x.strip() for x in input_vars_text.split(',')] if input_vars_text else []
output_vars = [y.strip() for y in output_vars_text.split(',')] if output_vars_text else []
selected_dmus = None if not dmus_vars_text else [x.strip() for x in dmus_vars_text.split(',')]

# Mostrar seleções em duas colunas
st.subheader("Selected Parameters:")
col1, col2 = st.columns(2)

with col1:
    st.write("Model Configuration:")
    st.write("- Model:", selectbox_model)
    st.write("- DMUs:", "All" if selected_dmus is None else ", ".join(map(str, selected_dmus)))

with col2:
    st.write("Variables:")
    st.write("- Inputs:", ", ".join(input_vars) if input_vars else "None")
    st.write("- Outputs:", ", ".join(output_vars) if output_vars else "None")

# Se um arquivo foi carregado
if uploaded_file is not None:
    try:
        # Verificar a extensão do arquivo
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)
            
        # Mostrar os dados carregados
        st.write("### Data Preview:")
        st.dataframe(df.head())
        
        # Verificar se as variáveis necessárias foram fornecidas
        if not input_vars or not output_vars:
            st.warning("Please enter input and output variables before processing.")
        else:
            # Processar dados DEA
            data_dea = get_data_st_dea(
                df=df,
                dmus=selected_dmus,
                colunas_inputs=input_vars,
                colunas_outputs=output_vars
            )
            
            if data_dea is not None:
                st.write("### Processed DEA Data:")
                st.dataframe(data_dea)
                
                # Processar CCR
                try:
                    resultados_dea = get_ccr_output_mult(data_dea, input_vars, output_vars)
                    if resultados_dea is not None:
                        st.write("### DEA Results:")
                        st.dataframe(resultados_dea)
                except Exception as e:
                    st.error(f"Error in DEA calculation: {e}")
    
    except Exception as e:
        st.error(f"Error: {e}")
else:
    st.info("Please upload a file to begin the analysis.")
