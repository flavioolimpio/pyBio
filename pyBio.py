import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu
st.set_page_config(page_title="pyBio")


def main():
    with st.sidebar:
        option = option_menu('Navegação:', ['Catalogo', 'Revenda', 'Compra'], 
        icons=['list', 'cart-arrow-down', 'cart-plus'], menu_icon="cast", default_index=0)

    df = pd.read_excel('Tabela_sistema_BioInstitnto.xlsx')

    
    if option == 'Catalogo':
        st.title("Produtos e Preços de Revenda")
        st.markdown("Clique aqui para acessar o catálogo de produtos")

        # Calcula o preço de revenda para cada produto
        df['Preço de Revenda'] = df.iloc[:, 1] + df.iloc[:, 1] * 0.51

        # Seleciona apenas as colunas 'Produto' e 'Preço de Revenda'
        products_df = df[['Produto', 'Preço de Revenda']]

        # Exibe a tabela de produtos e preços de revenda
        st.dataframe(products_df)
    
    elif option == 'Revenda':
        st.title("Interface de Revenda de Produtos")
        df['Qntd'] = [0]*len(df)
        df['Preço Final'] = [0.0]*len(df)

        for i in range(len(df)):
            st.subheader(f'Produto: {df.iloc[i, 0]}')
            quantity = st.number_input(f'Insira a quantidade do produto {df.iloc[i, 0]}', min_value=0, value=0, key=str(i))
            price = (df.iloc[i, 1] + df.iloc[i, 1] * 0.51) * quantity  # Calcula o preço de revenda
            df.loc[i, 'Qntd'] = quantity
            df.loc[i, 'Preço Final'] = price

            # Exibe o valor de revenda calculado
            st.text(f'Preço de revenda do produto {df.iloc[i, 0]}: R$ {price:.2f}')

        if st.button('Processar Planilha de Revenda'):
            df = df[df['Preço Final'] > 0]  # Exclui produtos com valor zero
            total_value = df['Preço Final'].sum()
            st.write('O valor total a ser repassado para o cliente é: ', total_value)

            # Seleciona apenas as colunas 'Qntd' e 'Preço Final'
            final_df = df[['Produto', 'Qntd', 'Preço Final']]

            # Exibe a tabela final
            st.dataframe(final_df)

            df.to_excel('nova_planilha_revenda.xlsx', index=False)
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
