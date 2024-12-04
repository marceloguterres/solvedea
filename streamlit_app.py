import streamlit as st
import pandas as pd
from get_data_dea import get_data_dea

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

input_vars_text = st.sidebar.text_input("Enter input variables (comma-separated)", )

output_vars_text = st.sidebar.text_input("Enter output variables (comma-separated)",)

# Campo de DMUs com valor padrão None
dmus_vars_text = st.sidebar.text_input("Enter DMUs (comma-separated, leave empty for all)", value="")

# Seleção do ano com dropdown incluindo None
years = [None] + list(range(2000, 2025))
selected_year = st.sidebar.selectbox(
    "Select Year (None for all years)",
    options=years,
    format_func=lambda x: "None" if x is None else str(x)
)



# Converter strings em listas
input_vars = [x.strip() for x in input_vars_text.split(',')]
output_vars = [y.strip() for y in output_vars_text.split(',')]
selected_dmus = None if not dmus_vars_text else [x.strip() for x in dmus_vars_text.split(',')]



# Mostrar seleções
st.subheader("Selections:")
st.write("- Year:", selected_year)
st.write("- Model:", selectbox_model)
st.write("- Inputs:", ", ".join(input_vars))
st.write("- Outputs:", ", ".join(output_vars))
st.write("- DMUs:", "All" if selected_dmus is None else ", ".join(selected_dmus))

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
        
    except Exception as e:
        st.error(f"Error: {e}")
else:
    st.info("Please upload a file to begin the analysis.")


