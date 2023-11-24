import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
st.set_page_config(page_title="Dashboard", layout='wide',
                   initial_sidebar_state='auto')
background_image = "basurero.jpg"  # Reemplaza con la ruta de tu imagen
# Estilos para el título
title_style = """
    <style>
     @keyframes slideIn {
            from {
                transform: translateX(-100%);
            }
            to {
                transform: translateX(0);
            }
        }
        .title-text {
            font-size: 30px;
            font-weight: bold;
            color: #3366cc; /* Cambia el color a tu elección */
            text-align: center;
            margin-bottom: 20px;
            animation: slideIn 1s ease-out;
        }
    </style>
"""
# Estilos con animación para el subtítulo
subtitle_style = """
    <style>
        @keyframes typing {
            from {
                width: 0;
            }
            to {
                width: 100%;
            }
        }

        .sidebar-content {
            display: flex;
            align-items: center;
        }

        .subtitle {
            font-size: 24px;
            font-weight: bold;
            color: black;
            overflow: hidden;
            white-space: nowrap;
            animation: typing 2s steps(50) infinite;
        }
    </style>
"""

# Aplicar estilos al título
st.markdown(title_style, unsafe_allow_html=True)
st.markdown("<p class='title-text'>Composición anual de residuos domiciliarios (2019-2022)</p>", unsafe_allow_html=True)
# Breve descripción
st.write("Este es un análisis de la composición anual de residuos domiciliarios entre 2019 y 2022.")

col1, col2, col3 = st.sidebar.columns([1,8,1])
with col1:
    st.write("")
with col2:
    st.image('heroguy_cropped.png',  use_column_width=True)
with col3:
    st.write("")

# Aplicar estilos animados al subtítulo y al contenido del sidebar
st.sidebar.markdown(subtitle_style, unsafe_allow_html=True)
st.sidebar.markdown("<div class='sidebar-content'><p class='subtitle'>F<span>i</span>ltrar 🔄</p></div>", unsafe_allow_html=True)

# Cargar el archivo CSV en un DataFrame
file_path = "D. Composición Anual de residuos domiciliarios_Distrital_2019_2022.csv"

# Carga de datos sin validar
# df = pd.read_csv(file_path)
# st.dataframe(df)
#Se visualiza en una sola columna
# df = pd.read_csv(file_path, encoding="ISO-8859-1")
# st.dataframe(df)

df = pd.read_csv(file_path, encoding="ISO-8859-1", delimiter=";", index_col=0, usecols=lambda x: 'Unnamed' not in x)
# Exclude the last two rows
df = df.iloc[:-2]
# st.dataframe(df)

# Imagen
st.image("basurero.jpg", caption="Descripción de la imagen", use_column_width=True)
# Convert the "PERIODO" column to integers (removing decimal parts)
df["PERIODO"] = df["PERIODO"].astype(int)

# Filter the DataFrame to include only rows where "PERIODO" is not null
df = df[df["PERIODO"].notna()]

# Contar los valores de la columna "QRESIDUOS_DOM" por "PERIODO"
count_by_periodo = df.groupby("PERIODO")["QRESIDUOS_DOM"].count().reset_index()

# Mostrar los resultados en un gráfico de pastel (donut chart) utilizando plotly.express con colores diferentes y características avanzadas
fig = px.pie(count_by_periodo, values="QRESIDUOS_DOM", names="PERIODO",
             title="Residuos",
             color_discrete_sequence=px.colors.qualitative.Set3,
             labels={"QRESIDUOS_DOM": "Conteo de QRESIDUOS_DOM"},
             hover_data=["QRESIDUOS_DOM"],
             hole=0.6,  # Specify the size of the center hole in the donut chart
             )
fig.update_traces(textinfo='percent+label', pull=[0.1] * len(count_by_periodo))  # Display percentage labels

# Add a title in the center of the donut chart
fig.add_annotation(
    text="RESIDUOS DOMICILIARIOS X AÑO",
    x=0.5,
    y=0.5,
    showarrow=False,
    font=dict(size=20)
)
st.plotly_chart(fig)

st.info('This is a purely informational message', icon="🧐")

# Agrupar por departamento y sumar los valores de la columna "QRESIDUOS_DOM"
sum_residuos_urbanos = df.groupby("DEPARTAMENTO")["QRESIDUOS_DOM"].sum().reset_index()

# Renombrar la columna para reflejar que son "residuos domiciliarios urbanos"
sum_residuos_urbanos.rename(columns={"QRESIDUOS_DOM": "Residuos Domiciliarios Urbanos"}, inplace=True)
st.dataframe(sum_residuos_urbanos)

# Crear el Bubble Chart con la suma de los residuos urbanos
fig = px.scatter(sum_residuos_urbanos, x="DEPARTAMENTO", y="Residuos Domiciliarios Urbanos",
                 size="Residuos Domiciliarios Urbanos", color="DEPARTAMENTO",
                 hover_name="DEPARTAMENTO", title="Bubble Chart de Residuos Domiciliarios Urbanos por Departamento",
                 labels={"Residuos Domiciliarios Urbanos": "Residuos Domiciliarios Urbanos", "DEPARTAMENTO": "Leyenda"},
                 size_max=60,
                 color_discrete_sequence=px.colors.qualitative.Set3)  # Utilizar la paleta Set3

# Establecer el título del eje y
fig.update_yaxes(title_text="Residuos Domiciliarios Urbanos")

# Rotar las etiquetas del eje X para mostrar todos los departamentos
fig.update_layout(xaxis_tickangle=-45)

# Estilo adicional
fig.update_layout(
    xaxis=dict(title='Departamento'),
    yaxis=dict(title='Residuos Domiciliarios Urbanos'),
    template="plotly_dark",  # Utilizar un fondo oscuro
    font=dict(family="Arial", size=12, color="white"),  # Ajustar la fuente
)

# Mostrar el gráfico
st.plotly_chart(fig)

st.warning('This is a warning', icon="⚠️")
# Agregar un selectbox para filtrar por el año en el cuerpo principal
selected_year = st.sidebar.selectbox("Seleccione año:", sorted(df["PERIODO"].unique()))

# Filtrar el DataFrame basado en la selección del usuario por "PERIODO"
filtered_year = df[df["PERIODO"] == selected_year]

# Agregar un radio button para filtrar por la columna "REG_NAT" en la barra lateral
reg_nat_values = filtered_year["REG_NAT"].unique()
reg_nat_values = reg_nat_values[~pd.isna(reg_nat_values)]  # Exclude NaN values

# Use st.sidebar to place elements in the sidebar
selected_reg_nat = st.sidebar.radio("Seleccione región natural:", reg_nat_values)

# Filtrar el DataFrame basado en la selección del usuario (excluyendo NaN)
filtered_reg = filtered_year[filtered_year["REG_NAT"] == selected_reg_nat]
st.toast('Seleccionaste '+selected_reg_nat, icon='😍')
# Contar los valores de la columna "QRESIDUOS_DOM" por "DEPARTAMENTO"
count_by_departamento = filtered_reg.groupby("DEPARTAMENTO")["QRESIDUOS_DOM"].count().reset_index()

# Mostrar los resultados en una gráfica de barras utilizando plotly.express con colores diferentes
fig = px.bar(count_by_departamento, x="DEPARTAMENTO", y="QRESIDUOS_DOM", color="DEPARTAMENTO",
             title=f"Residuos domiciliarios por departamento ({selected_year})",
             labels={"QRESIDUOS_DOM": "Conteo de QRESIDUOS_DOM"})
st.plotly_chart(fig)

st.error('This is an error', icon="🚨")

# Definir las categorías de residuos
categorias_organicos = ["QRESIDUOS_ALIMENTOS", "QRESIDUOS_MALEZA", "QRESIDUOS_OTROS_ORGANICOS"]
categorias_inorganicos = ["QRESIDUOS_PAPEL_BLANCO", "QRESIDUOS_PAPEL_PERIODICO", "QRESIDUOS_PAPEL_MIXTO",
                           "QRESIDUOS_CARTON_BLANCO", "QRESIDUOS_CARTON_MARRON", "QRESIDUOS_CARTON_MIXTO",
                           "QRESIDUOS_VIDRIO_TRANSPARENTE", "QRESIDUOS_VIDRIO_OTROS_COLORES", "QRESIDUOS_VIDRIOS_OTROS",
                           "QRESIDUOS_TEREFLATO_POLIETILENO", "QRESIDUOS_POLIETILENO_ALTA_DENSIDAD",
                           "QRESIDUOS_POLIETILENO_BAJA_DENSIDAD", "QRESIDUOS_POLIPROPILENO", "QRESIDUOS_POLIESTIRENO",
                           "QRESIDUOS_POLICLORURO_VINILO", "QRESIDUOS_TETRABRICK", "QRESIDUOS_LATA", "QRESIDUOS_METALES_FERROSOS",
                           "QRESIDUOS_ALUMINIO", "QRESIDUOS_OTROS_METALES"]
categorias_no_aprovechables = ["QRESIDUOS_BOLSAS_PLASTICAS", "QRESIDUOS_TECNOPOR", "QRESIDUOS_INERTES",
                                 "QRESIDUOS_TEXTILES", "QRESIDUOS_CAUCHO_CUERO", "QRESIDUOS_MEDICAMENTOS",
                                 "QRESIDUOS_ENVOLTURAS_SNAKCS_OTROS", "QRESIDUOS_OTROS_NO_CATEGORIZADOS"]
categorias_peligrosos = ["QRESIDUOS_SANITARIOS", "QRESIDUOS_PILAS"]

# Calcular las sumas consolidadas para cada categoría
filtered_reg["ORGANICOS"] = filtered_reg[categorias_organicos].sum(axis=1)
filtered_reg["INORGANICOS"] = filtered_reg[categorias_inorganicos].sum(axis=1)
filtered_reg["NO_APROVECHABLES"] = filtered_reg[categorias_no_aprovechables].sum(axis=1)
filtered_reg["PELIGROSOS"] = filtered_reg[categorias_peligrosos].sum(axis=1)

# st.write("Resultados Consolidados:")
# st.dataframe(filtered_reg[["DEPARTAMENTO", "ORGANICOS", "INORGANICOS", "NO_APROVECHABLES", "PELIGROSOS"]].set_index("DEPARTAMENTO"))
# Realizar la sumatoria por categoría y departamento
sum_by_department = filtered_reg.groupby("DEPARTAMENTO")["ORGANICOS", "INORGANICOS", "NO_APROVECHABLES", "PELIGROSOS"].sum()

# Mostrar los resultados en una tabla
# st.write("Suma de Residuos por Categoría y Departamento:")
# st.dataframe(sum_by_department)

# Reorganizar los datos para el gráfico de barras
sum_by_department_melted = sum_by_department.reset_index().melt(id_vars=["DEPARTAMENTO"],
                                                                value_vars=["ORGANICOS", "INORGANICOS", "NO_APROVECHABLES", "PELIGROSOS"],
                                                                var_name="Categoría", value_name="Suma de Residuos")

# Crear el gráfico de barras vertical
fig = px.bar(sum_by_department_melted, x="DEPARTAMENTO", y="Suma de Residuos", color="Categoría",
             title="Residuos en Ton/Año (Toneladas por año) por Categoría y Departamento",
             labels={"Suma de Residuos": "Suma de Residuos", "DEPARTAMENTO": "Departamento"},
             color_discrete_map={"ORGANICOS": "lightgreen", "INORGANICOS": "black", "NO_APROVECHABLES": "purple", "PELIGROSOS": "red"},
             )

# Agregar etiquetas de texto con el conteo total abreviado
for i, departamento in enumerate(sum_by_department_melted["DEPARTAMENTO"].unique()):
    total_count = sum_by_department_melted[sum_by_department_melted["DEPARTAMENTO"] == departamento]["Suma de Residuos"].sum()
    total_count_abbr = '{:,.0f}K'.format(total_count / 1000)  # Formato abreviado en K
    fig.add_annotation(
        go.layout.Annotation(
            x=departamento,
            y=total_count,
            text=total_count_abbr,
            showarrow=True,
            arrowhead=4,
            arrowcolor="teal",
            arrowsize=1,
            arrowwidth=2,
            ax=0,
            ay=-40,
            bgcolor="rgba(255, 255, 255, 0.6)",
        )
    )

# Estilo adicional
fig.update_layout(
    xaxis=dict(title='Departamento'),
    yaxis=dict(title='Suma de Residuos'),
    legend=dict(title="Categoría"),
)
# Mostrar el gráfico
st.plotly_chart(fig)

# Mostrar el DataFrame filtrado en el cuerpo principal
# st.dataframe(filtered_reg)
# Multiplicar las columnas para obtener "RESIDUOS URBANA" y "RESIDUOS RURAL"
filtered_reg["RESIDUOS URBANA"] = filtered_reg["POB_URBANA"] * filtered_reg["GPC_DOM"]
filtered_reg["RESIDUOS RURAL"] = filtered_reg["POB_RURAL"] * filtered_reg["GPC_DOM"]

# Mostrar el DataFrame actualizado
# st.dataframe(filtered_reg)

# Agrupar por departamento y sumar las columnas
count_residuos = filtered_reg.groupby("DEPARTAMENTO")["RESIDUOS URBANA", "RESIDUOS RURAL"].sum().reset_index()

# Mostrar el resultado
# st.dataframe(count_residuos)

# Reorganizar los datos para el gráfico de barras multivariable
count_residuos_melted = count_residuos.melt(id_vars=["DEPARTAMENTO"],
                                            value_vars=["RESIDUOS URBANA", "RESIDUOS RURAL"],
                                            var_name="Tipo de Residuos", value_name="Cantidad")

# Crear el gráfico de barras multivariable con texto personalizado
fig = px.bar(count_residuos_melted, x="DEPARTAMENTO", y="Cantidad", color="Tipo de Residuos",
             title="Residuos Urbanos y Rurales por Departamento en Kg/Hab./Día: Kilogramo por habitante día",
             labels={"Cantidad": "Cantidad de Residuos", "DEPARTAMENTO": "Departamento"},
             color_discrete_map={"RESIDUOS URBANA": "darkslategray", "RESIDUOS RURAL": "lime"},
             text="Cantidad",
             )

# Establecer el formato de texto personalizado con abreviación K
fig.update_traces(texttemplate='%{text:.2s}', textposition='outside')

# Estilo adicional
fig.update_layout(
    xaxis=dict(title='Departamento'),
    yaxis=dict(title='Cantidad de Residuos'),
    legend=dict(title="Tipo de Residuos"),
)

# Mostrar el gráfico
st.plotly_chart(fig)

# Add a motivational phrase
motivational_phrase = "Stay positive, work hard, and make it happen."

# Style the paragraph
st.success(
    """
    **Analisis**

    Stay positive, work hard, and make it happen.
    """, icon='🔎')

# También puedes mostrar estadísticas básicas del DataFrame filtrado
st.write(f"Estadísticas básicas del DataFrame filtrado para REG_NAT={selected_reg_nat}:")
st.write(filtered_reg.describe())
st.balloons()
# st.snow()