import streamlit as st
import pandas as pd
from get_data_dea import get_data_dea
from get_ccr_output_mult import get_ccr_output_mult

st.set_page_config(
    page_title="DEA Analysis",
    layout="wide",
    initial_sidebar_state="expanded"
)

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

# Seleção do ano com dropdown incluindo None
years = [None] + list(range(2000, 2025))
selected_year = st.sidebar.selectbox(
    "Select Year (None for all years)",
    options=years,
    format_func=lambda x: "None" if x is None else str(x)
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
    st.write("- Year:", "All" if selected_year is None else selected_year)
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
            data_dea = get_data_dea(
                df=df,
                ano=selected_year,
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


