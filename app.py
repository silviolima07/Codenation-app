import streamlit as st
import altair as alt


import pandas as pd
import numpy as np
import seaborn as sns
from PIL import Image

pd.set_option('precision',2)

# Emoji
import emoji

from bokeh.models.widgets import Div

def get_value( my_key, my_dicts):
    for key, value in my_dicts.items():
        if my_key == key:
            return value

def get_key( my_value, my_dicts):
    for key, value in my_dicts.items():
        if my_value == value:
            return key


def create_bars(column_num, column_cat,df_sorted):
    bars = alt.Chart(df_sorted,width = 700).mark_bar().encode(x= alt.X(column_cat, sort=None), y = alt.Y(column_num), tooltip = [column_cat, column_num]).interactive()
    return bars

def create_boxplot(column_num, column_cat,df):
    boxplot = alt.Chart(df, width = 700).mark_boxplot().encode(x= column_num, y = column_cat)
    return boxplot

def criar_boxplot(coluna_num, coluna_cat, df):
    boxplot = alt.Chart(df, width=600).mark_boxplot().encode(
        x=coluna_num,
        y=coluna_cat
    )
    return boxplot

def cria_correlationplot(df, col_num):
    cor_data = (df[col_num]).corr().stack().reset_index().rename(columns={0: 'correlation', 'level_0': 'variable', 'level_1': 'variable2'})
    #cor_data['correlation_label'] = cor_data['correlation'].map('{:.2f}'.format)  # Round to 2 decimal
    #base = alt.Chart(cor_data, width=500, height=500).encode( x = 'variable2:O', y = 'variable:O')
    #text = base.mark_text().encode(text = 'correlation_label',color = alt.condition(alt.datum.correlation > 0.5,alt.value('white'),
    #alt.value('black')))

# The correlation heatmap itself
    #cor_plot = base.mark_rect().encode(
    #color = 'correlation:Q')

    return cor_data #+ text


def main():
    """Exploratory Data Analysis App """

    #logo = Image.open("logo.png")
    #st.sidebar.image(logo,caption="", width=200)
   

    html_page = """
    <div style="background-color:tomato;padding=50px">
        <p style='text-align:center;font-size:50px;font-weight:bold'>World Happiness Rank</p>
    </div>
              """
    st.markdown(html_page, unsafe_allow_html=True)

    html2_page = """
    <div style="padding=10px">
        <p style='text-align:center;font-size:20px;font-weight:bold'>EDA - Exploratory Data Analysis</p>
    </div>
              """
    st.markdown(html2_page, unsafe_allow_html=True)
    
    
     
    image = Image.open("logo2.png")
    st.sidebar.image(image,caption="", use_column_width=True)

    activities1 = ["Home","Questions","Answers","About"]
    choice1 = st.sidebar.selectbox("Home",activities1)

    # Read dataset
    df = pd.read_csv('happiness.csv',encoding='latin-1', decimal = ',')

    # Converter para númerico
    #df['% Habitações sem banheiro / esgoto'] = df['% Habitações sem banheiro / esgoto'].astype(np.float16)
    
    # Filtra colunas numéricas e colunas categóricas
    col_num = df.select_dtypes(include=[np.number])
    col_cat = df.select_dtypes(include=[object])
     
    if choice1 == 'Home':
        st.subheader("Better Life Index by OECD")
        st.write("There is more to life than the cold numbers of GDP and economic statistics.This dataset contains the 2017 data of the Better Life Index which allows you to compare well-being across countries as well as measuring well-being, based on some topics the OECD has identified as essential, in the areas of material living conditions and quality of life.")
        if st.button("visit page"):
            js = "window.open('https://www.oecd-ilibrary.org/social-issues-migration-health/data/oecd-social-and-welfare-statistics/better-life-index-edition-2017_678d7570-en')"
            html = '<img src onerror="{}">'.format(js)
            div = Div(text=html)
            st.bokeh_chart(div)
    
    elif choice1 == "Questions":
        st.subheader("Questions")
        st.error("01 - Which are the 3 most relevant factors considered essential to have quality of life ?")
        st.error("02 - Which are the 3 countries show the best life satisfation level ?")

    elif choice1 == "Answers":
        st.subheader("Answers")
        st.subheader("Question 01:")
        st.error("Which are the 3 most relevant factors considered essential to have quality of life ?")
        st.success(" 01 - Number of rooms divided by the number of people living in the house")
        st.success(" 02 - Feeling safe walking alone at night")
        st.success("03 - Life expectancy")
        st.text("")
        st.subheader("Question 02:")
        st.error("Which are the 3 countries show the best life satisfation level ?")
        st.success("First place: Iceland")
        st.success("Second     : Finland")
        st.success("Third      : Norway")

    elif choice1 == 'About':
        st.subheader("Built with Streamlit")
        st.subheader("by Silvio Lima")
        
        if st.button("Linkedin"):
            js = "window.open('https://www.linkedin.com/in/silviocesarlima/')"
            html = '<img src onerror="{}">'.format(js)
            div = Div(text=html)
            st.bokeh_chart(div)
   

    activities2 = ["Dataset Shape", "Colum & Type", "Select & Show Columns", 'Bar Chart', 'Correlation Coef']
    choice2 = st.sidebar.radio("EDA",activities2)

    if choice2 == 'Dataset Shape':
        st.subheader("Dataset Shape")
        observations = df.shape[0]
        columns = df.shape[1]
        st.markdown(str(observations)+" observations")
        st.markdown(str(columns)+" columns")
         
    elif choice2 == "Colum & Type":
        st.subheader("Column and type:")
        df2 = pd.DataFrame()
        df2[''] = df.dtypes
        st.text(df2)
    
    elif choice2 == "Select & Show Columns":
        st.subheader("Select & Show Columns")
        options = st.multiselect("Columns", df.columns)
        st.table(df[options])

    elif choice2 == "Bar Chart":
        st.subheader("Bar Chart")
        num = len(col_num.columns)
        for i in range(num):
            st.subheader('Chart --> '+col_num.columns[i]+' x Country')
            st.text("")
            df_sorted = df.sort_values(by=col_num.columns[i], ascending= False)
            st.write(create_bars(col_num.columns[i], 'Country', df_sorted))
    
    #elif choice2 == "Box Plot":
        #st.subheader("Box Plot")
        #col_num_box = st.selectbox("Choose a column", list(col_num), key = 'unique')
        #simple_boxplot = alt.Chart(df).mark_boxplot().encode(
        #x = 'Country', y = 'Anos de Estudo')
        #st.write(simple_boxplot)
        #st.pyplot()
        #st.write(create_boxplot('Anos de Estudo', 'Country', df))
        #col_num_box = st.selectbox('Selecione a Coluna Numerica:', list(col_num) )
        #col_cat_box = st.selectbox('Selecione uma coluna categorica : ', colunas_object, key = 'unique')
        #st.markdown('Boxplot ' + 'Country' + ' pela coluna ' + col_num_box)
        #st.write(criar_boxplot('Anos de Estudo', 'Country', df))
        #st.markdown('Gráfico de correlação das colunas númericas')
        #st.write(cria_correlationplot(df, col_num))
        #col_num_box = st.selectbox('Selecione a Coluna Numerica:', col_num,key = 'unique' )
        #col_cat_box = st.selectbox('Selecione uma coluna categorica : ', col_cat, key = 'unique')
        #st.markdown('Boxplot ' + str(col_cat_box) + ' pela coluna ' + col_num_box)
        #st.write(criar_boxplot(col_num_box, col_cat_box, df))
        #st.write(cria_correlationplot(df, col_num))
       
    elif choice2 == "Correlation Coef":
        st.subheader("Correlation Coef")
        corr = df.corrwith(df['Life satisfaction'])
        corr = corr.sort_values(ascending=False)[-11:]

        #ax = sns.heatmap(corr, vmin=-1, vmax=1, center=0, cmap =sns.diverging_palette(20,220, n=200), square = True, annot = True)
        #corr_plot = sns.heatmap(df.corr(), annot= True)
        #ax.set_xticklabels( ax.get_xticklabels(), rotation=45, horizontalalignment = 'right')
        #st.pyplot()
        #teste = list(corr)

        df4 = pd.DataFrame(corr,columns=['Correlation Coefficients'])
        st.table(df4)

       
     

    
   
    
    
if __name__ == '__main__':
    main()
