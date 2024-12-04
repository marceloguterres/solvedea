import streamlit as st
import pandas as pd


st.set_page_config(
    page_title="DEA Analysis",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("Data Envelopment Analysis")

# Model selection
st.sidebar.header("Select Parameters")

selectbox_model = st.sidebar.selectbox(
    "Select the DEA model of your choice?",
    ("Model 1", "Model 2", "Model 3")
)


input_vars_text = st.sidebar.text_input(
    "Enter input variables (comma-separated)",
    "x1, x2, x3"
)

# Converter a string em lista
input_vars = [x.strip() for x in input_vars_text.split(',')]

# Sidebar - Upload de arquivo
st.sidebar.header("Upload Data")
uploaded_file = st.sidebar.file_uploader(
    "Choose your input file",
    type=['csv', 'xlsx', 'xls']
)



# Área principal - Sumário das seleções
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
       
        
    except Exception as e:
        st.error(f"Error: {e}")
else:
    st.info("Please upload a file to begin the analysis.")




st.subheader("Selections")
st.write("**Selected Model:**", selectbox_model)
st.write("**Input Variables Configuration:**")
st.write(f"- Number of inputs: {len(input_vars)}")
st.write("- Variables:", ", ".join(input_vars))


