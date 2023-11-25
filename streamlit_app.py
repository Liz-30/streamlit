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
st.markdown("**Composición anual de residuos domiciliarios (2019-2022)**")
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

def do_view_tasks():
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
        title="Pie Chart de Residuos domiciliarios Ton/Año | 2019 - 2022",
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
    st.info('This is a purely informational message', icon="🧐")

def do_manage_tasks():
    # st.markdown('### Ticking tasks')
    sum_residuos_urbanos = df.groupby("DEPARTAMENTO")["QRESIDUOS_DOM"].sum().reset_index()
    # Renombrar la columna para reflejar que son "residuos domiciliarios urbanos"
    sum_residuos_urbanos.rename(columns={"QRESIDUOS_DOM": "Residuos Domiciliarios Urbanos"}, inplace=True)
    # st.dataframe(sum_residuos_urbanos)
    # Crear el Bubble Chart con la suma de los residuos urbanos
    fig = px.scatter(sum_residuos_urbanos, x="DEPARTAMENTO", y="Residuos Domiciliarios Urbanos",
                    size="Residuos Domiciliarios Urbanos", color="DEPARTAMENTO",
                    hover_name="DEPARTAMENTO", title="Bubble Chart de Residuos Domiciliarios Urbanos Ton/Año por Departamento",
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
    st.warning('This is a warning', icon="⚠️")

def do_chart3():
    saved_df = st.session_state['df_guardado']  
    selected_year = st.session_state['anio_seleccionado']  
    count_by_departamento = saved_df.groupby("DEPARTAMENTO")["QRESIDUOS_DOM"].count().reset_index()
    # Mostrar los resultados en una gráfica de barras utilizando plotly.express con colores diferentes
    fig = px.bar(count_by_departamento, x="DEPARTAMENTO", y="QRESIDUOS_DOM", color="DEPARTAMENTO",
             title=f"Residuos domiciliarios por departamento según región natural Ton/Año ({selected_year})",
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
    st.error('This is an error', icon="🚨")

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
                title="Residuos en Ton/Año por Categoría y Departamento",
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
    st.error('This is an error', icon="🚨")
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
                title="Residuos Urbanos y Rurales por Departamento en Kg/Hab./Día",
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
    st.success(
    """
    **Analisis**

    Stay positive, work hard, and make it happen.
    """, icon='🔎')

def do_credentials():
    st.markdown('### Security rules')
def do_logs():
    st.markdown('### Blah, blah, blah, ....')
def do_acerca():
    st.image('basurero.jpg', caption="Basura en la playa", use_column_width=True)
    st.link_button("Ir a código del proyecto", "https://github.com/summermp/streamlit", type='primary')
    st.markdown("""
La gestión de residuos sólidos domiciliarios es un desafío importante en el Perú, ya que su inadecuada disposición final genera problemas ambientales y de salud pública. La composición de los residuos sólidos domiciliarios es un factor clave para el diseño e implementación de estrategias efectivas de gestión de residuos.

En Perú, la generación de residuos sólidos domiciliarios ha aumentado significativamente en los últimos años, alcanzando aproximadamente 22,000 toneladas por día en 2022. La composición de estos residuos varía según la región, el nivel socioeconómico y otros factores. Sin embargo, en general, los residuos orgánicos constituyen la mayor parte de los residuos sólidos domiciliarios en Perú, seguidos de los residuos inorgánicos reciclables y los residuos inorgánicos no reciclables.

**Composición de los residuos sólidos domiciliarios en Perú (2019-2022)**

| Componente | Porcentaje (%) |
|---|---|
| Residuos orgánicos | 45-55% |
| Residuos inorgánicos reciclables | 25-35% |
| Residuos inorgánicos no reciclables | 15-25% |

**Impacto ambiental de la inadecuada gestión de residuos sólidos domiciliarios**

La inadecuada disposición final de los residuos sólidos domiciliarios genera una serie de problemas ambientales, incluyendo:

* Contaminación del suelo y el agua
* Emisión de gases de efecto invernadero
* Propagación de enfermedades
* Afectación de la biodiversidad

**Estrategias para la gestión efectiva de residuos sólidos domiciliarios**

Para hacer frente al desafío de la gestión de residuos sólidos domiciliarios, es necesario implementar una serie de estrategias efectivas, incluyendo:

* Reducción de la generación de residuos
* Recolección y transporte eficientes
* Recuperación y reciclaje de residuos
* Disposición final adecuada de los residuos no aprovechables

La gestión efectiva de residuos sólidos domiciliarios es esencial para proteger el medio ambiente y la salud pública.

**Conclusión**

La composición de los residuos sólidos domiciliarios en Perú es un factor importante para el diseño e implementación de estrategias efectivas de gestión de residuos. La reducción de la generación de residuos, la recuperación y reciclaje de residuos, y la disposición final adecuada de los residuos no aprovechables son estrategias clave para hacer frente al desafío de la gestión de residuos sólidos domiciliarios.
""")
def do_contact():
    st.image('agradecimiento.png', caption="Agradecimiento al equipo", use_column_width=True)
    st.markdown('### Email: streamlit@gmail.com')
    st.markdown('### Cel: 962 925 573')

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
                    'Gráfico 1' : {'action': do_view_tasks, 'item_icon': 'pie-chart-fill', 'submenu': None},
                    'Gráfico 2' : {'action': do_manage_tasks, 'item_icon': 'bar-chart-fill', 'submenu': None},
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
                    'Descripción' : {'action': None, 'item_icon': '-', 'submenu': None},
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
