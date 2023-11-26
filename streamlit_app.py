import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
# https://discuss.streamlit.io/t/streamlit-option-menu-is-a-simple-streamlit-component-that-allows-users-to-select-a-single-item-from-a-list-of-options-in-a-menu
# https://icons.getbootstrap.com/
# https://gist.github.com/asehmi/55781a5e90942fa26be87b3ba92b643c
# https://github.com/victoryhb/streamlit-option-menu
from streamlit_option_menu import option_menu
st.set_page_config(page_title='Dashboard residuos domiciliarios',page_icon="🌎",initial_sidebar_state="expanded", layout='wide')
text_style = """
    <style>
        .title_text {
            font-size: 24px; font-family: "Times New Roman", Georgia, serif;
            font-weight: bold;
        }
        .desc_text {
            font-size: 24px; font-family: "Times New Roman", Georgia, serif;
            text-align: justify;
        }

    </style>
"""
st.markdown(text_style, unsafe_allow_html=True)
st.markdown("<h3 class='title_text'>Composición anual de residuos domiciliarios (2019-2022)<h3>" , unsafe_allow_html=True)
# Cargar el archivo CSV en un DataFrame
file_path = "D. Composición Anual de residuos domiciliarios_Distrital_2019_2022.csv"
df = pd.read_csv(file_path, encoding="ISO-8859-1", delimiter=";", index_col=0, usecols=lambda x: 'Unnamed' not in x)
# Exclude the last two rows
df = df.iloc[:-2]
df["PERIODO"] = df["PERIODO"].astype(int)
# Filter the DataFrame to include only rows where "PERIODO" is not null
df = df[df["PERIODO"].notna()]
def do_upload_tasks():
    st.markdown('### Upload task file')
def do_chart1():
    global df
    # Contar los valores de la columna "QRESIDUOS_DOM" por "PERIODO"
    count_by_periodo = df.groupby("PERIODO")["QRESIDUOS_DOM"].count().reset_index()
    # Mostrar los resultados en un gráfico de pastel (donut chart) utilizando plotly.express con colores diferentes y características avanzadas
    fig = go.Figure()

    fig.add_trace(go.Pie(
        labels=count_by_periodo["PERIODO"],
        values=count_by_periodo["QRESIDUOS_DOM"],
        texttemplate="%{label}<br>"
        "%{percent:.2%}",
        hole=0.6,
        showlegend=True,
        hovertemplate="<b>Año</b>: %{label}<br>"
                      # See docs for information on d3 formatting
                      "<b>Total</b>: %{value:.0f}<br>"
                      "<b>Porcentaje</b>: %{percent:.2%}<br>"
                      "<extra></extra>",
        textinfo='percent+value',
        pull=[0.1] * len(count_by_periodo),
        marker=dict(colors=px.colors.qualitative.Set3),
    ))

    # Add a title in the center of the donut chart
    fig.add_annotation(
        text="RESIDUOS DOMICILIARIOS",
        x=0.5,
        y=0.5,
        showarrow=False,
        font=dict(size=20)
    )

    # Customize legend and layout
    fig.update_layout(
        title="Consumo de residuos domiciliarios por año Ton/Año | 2019 - 2022",
        legend=dict(
            orientation="h",  # horizontal legend
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        font=dict(family="Arial", size=12, color="black"),  # Adjust font
    )
    st.plotly_chart(fig, use_container=True)
    st.markdown("*Gráfica 1: El gráfico representa la proporción expresada en porcentajes de la cantidad de residuos sólidos domiciliarios por año*")
    st.info('En la gráfica se logra observar la comparación de la cantidad de residuos sólidos domiciliarios que fueron registrados durante el periodo 2019 al 2022 y la proporción que representan respecto al 100% del total de los datos registrados, de los cuales se puede destacar que el año 2019 y 2020 tienen un porcentaje igual de distribución y lo mismo se logra observar para los años 2021 y 2022, pero es importante destacar que los 2 últimos años del periodo fueron los que mayor porcentaje de residuos sólidos domiciliarios registraron. ', icon="🧐")
def do_chart2():
    # st.markdown('### Ticking tasks')
    sum_residuos_urbanos = df.groupby("DEPARTAMENTO")["QRESIDUOS_DOM"].sum().reset_index()
    # Renombrar la columna para reflejar que son "residuos domiciliarios urbanos"
    sum_residuos_urbanos.rename(columns={"QRESIDUOS_DOM": "Residuos Domiciliarios Urbanos"}, inplace=True)
    # st.dataframe(sum_residuos_urbanos)
    # Crear el Bubble Chart con la suma de los residuos urbanos
    fig = px.scatter(sum_residuos_urbanos, x="DEPARTAMENTO", y="Residuos Domiciliarios Urbanos",
                    size="Residuos Domiciliarios Urbanos", color="DEPARTAMENTO",
                    hover_name="DEPARTAMENTO", title="Residuos sólidos domiciliarios urbanos Ton/Año por Departamento",
                    labels={"Residuos Domiciliarios Urbanos": "Residuos Domiciliarios Urbanos", "DEPARTAMENTO": "Departamento"},
                    size_max=60,
                    # mode='markers',
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
    st.markdown("*Gráfica 2: El gráfico representa los residuos domiciliarios urbanos por departamento expresada en millones de toneladas*")
    st.warning('En el gráfico presentado podemos observar que  en  la capital del Perú Lima, es una de las ciudades más urbanizadas , de igual forma la más poblada del país y, por lo tanto, genera una gran cantidad de residuos sólidos domiciliarios. Según un informe del Ministerio del Ambiente, los habitantes de la ciudad de Lima generan un promedio de 10 M (millones)  de residuos sólidos del período tomado del 2019-2022 . Además, la cantidad de residuos sólidos generados por persona viene incrementándose debido a los patrones de consumo.', icon="⚠️")
def do_chart3():
    saved_df = st.session_state['df_guardado']  
    selected_year = st.session_state['anio_seleccionado']  
    count_by_departamento = saved_df.groupby("DEPARTAMENTO")["QRESIDUOS_DOM"].count().reset_index()
    # Mostrar los resultados en una gráfica de barras utilizando plotly.express con colores diferentes
    fig = px.bar(count_by_departamento, x="DEPARTAMENTO", y="QRESIDUOS_DOM", color="DEPARTAMENTO",
             title=f"Residuos sólidos domiciliarios Ton/Año por departamento por año y región ({selected_year})",
             labels={"QRESIDUOS_DOM": "Residuos domiciliarios"})
    # Agregar el conteo dentro de cada barra para cada departamento
    for i, row in count_by_departamento.iterrows():
        x_center = row['DEPARTAMENTO']
        y_center = row['QRESIDUOS_DOM'] / 2  # Posición en el centro de la barra
        fig.add_annotation(
            x=x_center,
            y=y_center,
            text=str(row['QRESIDUOS_DOM']),
            showarrow=False,
            font=dict(size=10),
        )
    # Agregar estilos profesionales estadísticos
    fig.update_layout(
        xaxis_title="Departamento",
        yaxis_title="Ton/Año",
        template="plotly_dark",  # Utilizar un fondo oscuro
        font=dict(family="Arial", size=12, color="black"),  # Ajustar la fuente
        showlegend=False  # Ocultar la leyenda, ya que el color se usa para departamentos
    )
    st.plotly_chart(fig)
    st.markdown("*Gráfica 3: La gráfica muestra la diferencia de consumos de residuos sólidos domiciliarios por departamento con su respectiva región.*")
    st.info('Tener en cuenta que el territorio  peruano está dividido en 3 regiones naturales: costa, sierra y selva. Esta división se basa en las características topográficas y climáticas de cada región,es por ello, que en la gráfica se puede apreciar que el mismo departamento se encuentra en diferentes regiones. Por ejemplo, el departamento de Piura que se encuentra ubicado en la zona norte del país, está distribuido geográficamente en la costa y sierra, como consecuencia se pueden apreciar playas, ríos y montañas dentro de un mismo territorio.', icon="🔎")
def do_chart4():
    # st.markdown('### chart4')
    # Access the DataFrame from session state
    saved_df = st.session_state['df_guardado']
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
    saved_df["ORGANICOS"] = saved_df[categorias_organicos].sum(axis=1)
    saved_df["INORGANICOS"] = saved_df[categorias_inorganicos].sum(axis=1)
    saved_df["NO_APROVECHABLES"] = saved_df[categorias_no_aprovechables].sum(axis=1)
    saved_df["PELIGROSOS"] = saved_df[categorias_peligrosos].sum(axis=1)
    # Realizar la sumatoria por categoría y departamento
    sum_by_department = saved_df.groupby("DEPARTAMENTO")["ORGANICOS", "INORGANICOS", "NO_APROVECHABLES", "PELIGROSOS"].sum()
    # Mostrar los resultados en una tabla
    st.write("Suma de Residuos por Categoría y Departamento:")
    st.dataframe(sum_by_department)
    # Reorganizar los datos para el gráfico de barras
    sum_by_department_melted = sum_by_department.reset_index().melt(id_vars=["DEPARTAMENTO"],
                                                                    value_vars=["ORGANICOS", "INORGANICOS", "NO_APROVECHABLES", "PELIGROSOS"],
                                                                    var_name="Categoría", value_name="Suma de Residuos")
    # Crear el gráfico de barras vertical
    fig = px.bar(sum_by_department_melted, x="DEPARTAMENTO", y="Suma de Residuos", color="Categoría",
                title="Residuos en Ton/Año (Toneladas por años) por clasificación y departamento",
                labels={"Suma de Residuos": "Suma de Residuos", "DEPARTAMENTO": "Departamento"},
                color_discrete_map={"ORGANICOS": "lime", "INORGANICOS": "black", "NO_APROVECHABLES": "purple", "PELIGROSOS": "red"},
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
    st.markdown("*La gráfica muestra la cantidad de consumo de residuos sólidos con su respectiva clasificación.*")
    st.info('''Según el Ministerio del Ambiente los residuos sólidos orgánicos se dividen en 34 tipos, en los cuales se pueden clasificar en cuatro grandes grupos: orgánicos, inorgánicos, no aprovechables y peligrosos. Dicha gráfica tiene la facilidad de identificar qué categoría prevalece más, es decir, que conjunto de residuos es más consumido en cada departamento.

**Orgánicos:** Son aquellos desechos biodegradables de origen vegetal o animal que pueden descomponerse en la naturaleza sin demasiada dificultad y transformarse en otro tipo de materia orgánica , 

**Inorgánicos:** Son aquellos desechos no biodegradables o degradables a muy largo plazo que se derivan de procesos antropogénicos (generados por el ser humano).

**No aprovechables:** Son aquellos desechos que no pueden ser reutilizados, reciclados o transformados en otros productos.

**Peligrosos:** Son aquellos residuos que, debido a sus propiedades corrosivas, explosivas, tóxicas, inflamables o radiactivas, pueden causar daños o efectos indeseados a la salud o al ambiente.
''', icon="🔎")
def do_chart5():
    # st.markdown('### chart5')
    # Multiplicar las columnas para obtener "RESIDUOS URBANA" y "RESIDUOS RURAL"
    saved_df = st.session_state['df_guardado']
    saved_df["RESIDUOS URBANA"] = saved_df["POB_URBANA"] * saved_df["GPC_DOM"]
    saved_df["RESIDUOS RURAL"] = saved_df["POB_RURAL"] * saved_df["GPC_DOM"]
    # Agrupar por departamento y sumar las columnas
    count_residuos = saved_df.groupby("DEPARTAMENTO")["RESIDUOS URBANA", "RESIDUOS RURAL"].sum().reset_index()
    # Reorganizar los datos para el gráfico de barras multivariable
    count_residuos_melted = count_residuos.melt(id_vars=["DEPARTAMENTO"],
                                                value_vars=["RESIDUOS URBANA", "RESIDUOS RURAL"],
                                                var_name="Tipo de Residuos", value_name="Cantidad")
    # Crear el gráfico de barras multivariable con texto personalizado
    fig = px.bar(count_residuos_melted, x="DEPARTAMENTO", y="Cantidad", color="Tipo de Residuos",
                title="Residuos sólidos Urbanos y rurales por departamento en Kg/Hab/día: Kilogramo por habitante día",
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
    st.markdown("*Gráfica 5:  El gráfico representa  la cantidad de consumo de residuos en la zona urbana y rural en su respectivo departamento.*")
    st.success(
    """
    En la gráfica se logra observar que la mayoría de los residuos sólidos que provienen de las zonas urbanas es en mayor cantidad con respecto a los residuos de las zonas rurales, factores como la densidad de población y estilo de vida son los responsables de dichos resultados. Por ejemplo, en las zonas urbanas las personas tienden a consumir más productos desechables envasados, generando así que la cantidad de residuos sólidos aumente, a diferencia de la población en las zonas rurales quienes tiende a consumir más productos frescos y a granel, permitiendo que la cantidad de residuos sólidos se reduzca.
    """, icon='🔎')

def do_credentials():
    st.markdown('### Security rules')
def do_logs():
    st.markdown('### Blah, blah, blah, ....')
def do_acerca():
    st.image('basurero.jpg', caption="Basura en la playa", use_column_width=True)
    st.link_button("Ir a código del proyecto", "https://github.com/summermp/streamlit", type='primary')
    
    st.markdown("""
<p class='desc_text'> La base de datos de composición de residuos sólidos domiciliarios corresponde a la información sobre la distribución de los residuos sólidos del ámbito domiciliario generados por tipo (medido en tonelada). Dicha información, fue obtenida desde los años 2019 hasta el 2022, con respecto a todos los departamentos de nuestro país.</br></br>
La información que se toma de insumo para la estimación de esta estadística es obtenida a partir de dos fuentes de información: </br></br>
Sistema de Información para la Gestión de los Residuos Sólidos – SIGERSOL el cual es administrado por el Ministerio del Ambiente (MINAM).</br></br>
Los Estudios de caracterización de residuos sólidos municipales, que se estandarizaron desde el año 2019 en adelante, aprobada mediante Resolución Ministerial N° 457-2018-MINAM.</p>
<h4 class='title_text'>¿Qué buscamos?</h4>
<p class='desc_text'>Buscamos brindar información sobre la distribución de los residuos sólidos en el ámbito domiciliario en todos los departamentos del Perú; facilitando su uso mediante gráficas y tablas para un mejor entendimiento.</p>
<h4 class='title_text'>¿Qué son los residuos sólidos domiciliarios?</h4>
<p class='desc_text'>Residuos sólidos domiciliarios son aquellos provenientes del consumo o uso de un bien o servicio, comprenden específicamente como fuente de generación a las viviendas.</p>
<h4 class='title_text'>¿Cómo influyen los residuos sólidos en los seres vivos?</h4>
<p class='desc_text'>De acuerdo a su clasificación y aprovechamiento estos residuos domiciliarios pueden influir tanto positiva como negativamente, por ejemplo, el uso irresponsable y excesivo de plástico, pilas y/o baterías podría ser muy perjudicial para los seres vivos y al ambiente, ya que estos son residuos que podrían <b>tomarse entre 100 a 1000 años en descomponerse</b>, generando así un rastro tóxico a largo plazo en nuestro ecosistema. Por otra parte, el aprovechamiento responsable y creativo de los residuos domiciliarios, tales como la materia orgánica, el papel y el cartón permiten fomentar el reciclaje y crear nuevos productos que sean en beneficio para los seres vivos y el ambiente, por ejemplo, la descomposición de la materia orgánica podría ser fuente de compostaje para las plantas.</p>
""",  unsafe_allow_html=True)
def do_contact():
    st.markdown("<h4 class='title_text'>¿Quiénes somos?</h4>", unsafe_allow_html=True)
    st.markdown("<p class='desc_text'>Somos estudiantes del cuarto semestre de la carrera de ingeniería ambiental de la Universidad Peruana Cayetano Heredia (UPCH). Nos apasiona el procesamiento y visualización de datos para mejorar y comprender la problemática ambiental y brindar información sobre los residuos sólidos generados en el Perú.</p>", unsafe_allow_html=True)
    # Crear dos columnas
    col1, col2 = st.columns(2)
    # Puedes agregar imágenes a cada columna también
    imagen1 = "greisy.png"  # Reemplaza con la URL de tu primera imagen
    imagen2 = "lizzeth.jpg"  # Reemplaza con la URL de tu segunda imagen
    col1.image(imagen1, use_column_width=True)
    col1.markdown("<p style='text-align: center;'><strong>Greisy Jhoana Delgado Gaona</strong></p>", unsafe_allow_html=True)
    col2.image(imagen2, use_column_width=True)
    col2.markdown("<p style='text-align: center;'><strong>Lizzeth Rossmery Quispe Mamani</strong></p>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    # Puedes agregar imágenes a cada columna también
    imagen1 = "amparo.jpg"  # Reemplaza con la URL de tu primera imagen
    imagen2 = "anjhy.jpg"  # Reemplaza con la URL de tu segunda imagen
    col1.image(imagen1, use_column_width=True)
    col1.markdown("<p style='text-align: center;'><strong>Amparo Marleny Vidaurre Juarez</strong></p>", unsafe_allow_html=True)
    col2.image(imagen2, use_column_width=True)
    col2.markdown("<p style='text-align: center;'><strong>Anjhy Lucero Zamora Sulca</strong></p>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    imagen1 = "liz.jpg"  # Reemplaza con la URL de tu primera imagen
    col1.image(imagen1, use_column_width=True)
    col1.markdown("<p style='text-align: center;'><strong>Liz Villarreal Zapata</strong></p>", unsafe_allow_html=True)
    # st.image('agradecimiento.png', caption="Agradecimiento al equipo", use_column_width=True)
styles = {
    "container": {"margin": "0px !important", "padding": "0!important", "align-items": "stretch", "background-color": "#fafafa"},
    "icon": {"color": "black", "font-size": "20px"}, 
    "nav-link": {"font-size": "20px", "text-align": "left", "margin":"0px", "--hover-color": "#eee"},
    "nav-link-selected": {"background-color": "#ff4b4b", "font-size": "20px", "font-weight": "normal", "color": "black", },
}

menu = {
    'title': 'Menu principal',
    'items': { 
        'Inicio' : {
            'action': None, 'item_icon': 'house', 'submenu': {
                'title': None,
                'items': { 
                    'Gráfico 1' : {'action': do_chart1, 'item_icon': 'pie-chart-fill', 'submenu': None},
                    'Gráfico 2' : {'action': do_chart2, 'item_icon': 'bar-chart-fill', 'submenu': None},
                    'Gráfico 3' : {'action': do_chart3, 'item_icon': 'bar-chart-line', 'submenu': None},
                    'Gráfico 4' : {'action': do_chart4, 'item_icon': 'bar-chart-line-fill', 'submenu': None},
                    'Gráfico 5' : {'action': do_chart5, 'item_icon': 'bar-chart-steps', 'submenu': None},
                },
                'menu_icon': None,
                'default_index': 0,
                'with_view_panel': 'main',
                'orientation': 'horizontal',
                'styles': styles
            }
        },
        'Acerca' : {
            'action': do_acerca, 'item_icon': 'people',
             'submenu': {
                'title': None,  
                'items': { 
                    'Definición' : {'action': None, 'item_icon': '-', 'submenu': None},
                },
                'menu_icon': None,
                'default_index': 0,
                'with_view_panel': 'main',
                'orientation': 'horizontal',
                'styles': styles
            }
        },
        'Contacto' : {
            'action': None, 'item_icon': 'phone', 'submenu': {
                'title': None,
                'items': { 
                    'Contactenos' : {'action': do_contact, 'item_icon': 'telephone-inbound-fill', 'submenu': None}
                },
                'menu_icon': None,
                'default_index': 0,
                'with_view_panel': 'main',
                'orientation': 'horizontal',
                'styles': styles
            }
        },
    },
    'menu_icon': 'clipboard2-check-fill',
    'default_index': 0,
    'with_view_panel': 'sidebar',
    'orientation': 'vertical',
    'styles': styles
}

def show_menu(menu):
    def _get_options(menu):
        options = list(menu['items'].keys())
        return options
    def _get_icons(menu):
        icons = [v['item_icon'] for _k, v in menu['items'].items()]
        return icons
    kwargs = {
        'menu_title': menu['title'] ,
        'options': _get_options(menu),
        'icons': _get_icons(menu),
        'menu_icon': menu['menu_icon'],
        'default_index': menu['default_index'],
        'orientation': menu['orientation'],
        'styles': menu['styles']
    }

    with_view_panel = menu['with_view_panel']
    if with_view_panel == 'sidebar':
        with st.sidebar:
            menu_selection = option_menu(**kwargs)
    elif with_view_panel == 'main':
        menu_selection = option_menu(**kwargs)
    else:
        raise ValueError(f"Unknown view panel value: {with_view_panel}. Must be 'sidebar' or 'main'.")

    selected_submenu = menu['items'][menu_selection]['submenu']
    if menu_selection == 'Inicio':
        if selected_submenu:
            # submenu_items = selected_submenu['items']
            col1, col2 = st.columns(2)
            selected_year = col1.slider("Seleccione año:", min(df["PERIODO"].unique()), max(df["PERIODO"].unique()))
            st.session_state['anio_seleccionado'] = selected_year
            # Filtrar el DataFrame basado en la selección del usuario por "PERIODO"
            filtered_year = df[df["PERIODO"] == selected_year]
            # Agregar un radio button para filtrar por la columna "REG_NAT" en la barra lateral
            reg_nat_values = filtered_year["REG_NAT"].unique()
            reg_nat_values = reg_nat_values[~pd.isna(reg_nat_values)]  # Exclude NaN values
            # Use st.sidebar to place elements in the sidebar
            selected_reg_nat = col2.radio("Seleccione región natural:", reg_nat_values, horizontal=True)
            # Filtrar el DataFrame basado en la selección del usuario (excluyendo NaN)
            st.session_state['df_guardado'] = filtered_year[filtered_year["REG_NAT"] == selected_reg_nat]
            st.toast('Seleccionaste año: '+str(selected_year)+' 📅', icon='❤')
            st.toast('Seleccionaste region: '+selected_reg_nat+' ⛰️', icon='😍')

    if menu['items'][menu_selection]['submenu']:
        show_menu(menu['items'][menu_selection]['submenu'])
    if menu['items'][menu_selection]['action']:
        menu['items'][menu_selection]['action']()
# Create two columns
# st.divider()  # 👈 Draws a horizontal rule
# Update the menu options
st.sidebar.image('https://www.precayetanovirtual.pe/moodle/pluginfile.php/1/theme_mb2nl/loadinglogo/1692369360/logo-cayetano.png', use_column_width=True)
show_menu(menu)
col1, col2, col3 = st.sidebar.columns([1,8,1])
with col1:
    st.write("")
with col2:
    st.image('heroguy.png',  use_column_width=True)
with col3:
    st.write("")
st.sidebar.text("Ing. ambiental - UPCH")
st.snow()
