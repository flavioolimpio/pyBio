import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu
st.set_page_config(page_title="pyBio")

def calculate_total(df):
    df['Preço da venda * Qntd'] = df['Preço da Venda'] * df['Qntd']
    return df

def main():
    st.title("Interface de Compra e Revenda de Produtos")

    with st.sidebar:
        option = option_menu('Navegação:', ['Revenda', 'Compra'], 
        icons=['cart-arrow-down', 'cart-plus'], menu_icon="cast", default_index=0)


    if option == 'Revenda':
        df = pd.read_excel('Tabela_sistema_BioInstitnto.xlsx')
        df['Qntd'] = [0]*len(df)
        df['Preço da Venda'] = [0.0]*len(df)
        df['Preço da venda * Qntd'] = [0.0]*len(df)

        for i in range(len(df)):
            st.subheader(f'Produto: {df.iloc[i, 0]}')
            quantity = st.number_input(f'Insira a quantidade do produto {df.iloc[i, 0]}', min_value=0, value=0, key=str(i))
            price = st.number_input(f'Insira o preço de venda do produto {df.iloc[i, 0]}', min_value=0.0, value=0.0, key=str(i)+'price')
            df.loc[i, 'Qntd'] = quantity
            df.loc[i, 'Preço da Venda'] = price
            df.loc[i, 'Preço da venda * Qntd'] = quantity * price

        if st.button('Processar Planilha de Revenda'):
            df = df[df['Preço da venda * Qntd'] > 0]  # Exclui produtos com valor zero
            result = calculate_total(df)
            st.write(result)
            total_value = result['Preço da venda * Qntd'].sum()
            st.write('O valor total a ser repassado para o cliente é: ', total_value)

            result.to_excel('nova_planilha_revenda.xlsx', index=False)
            st.success('Nova planilha de Excel de revenda criada com sucesso!')

    elif option == 'Compra':
        df = pd.read_excel('Tabela_sistema_BioInstitnto.xlsx')
        df['Qntd'] = [0]*len(df)

        for i in range(len(df)):
            st.subheader(f'Produto: {df.iloc[i, 0]}')
            quantity = st.number_input(f'Insira a quantidade do produto {df.iloc[i, 0]}', min_value=0, value=0, key=str(i))
            df.loc[i, 'Qntd'] = quantity

        if st.button('Processar Planilha de Compra'):
            df = df[df['Qntd'] > 0]  # Exclui produtos com quantidade zero
            st.write(df)

            df.to_excel('nova_planilha_compra.xlsx', index=False)
            st.success('Nova planilha de Excel de compra criada com sucesso!')

if __name__ == '__main__':
    main()
