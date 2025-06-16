#IMPORTS DO STREAMLIT E AGREGADOS
import streamlit as st
from streamlit_option_menu import option_menu
import streamlit_antd_components as sac
from streamlit_lightweight_charts import renderLightweightCharts
import streamlit.components.v1 as components
from streamlit_extras.metric_cards import style_metric_cards

#IMPORTS DO PYTHON
import pymongo
import csv
import io
import json
import pandas as pd
import numpy as np
from pprint import pprint
from datetime import datetime

SOCIAL_MEDIA_JSON = {
    "rede": "",
    "mes": 0,
    "seguidores": {},
    "visualizacoes": {},
    "visitas": {},
    "alcance": {},
    "toques": {},
    "interacoes": {}
}

TRILHAS_OFERTADAS = ["Design para quem não é designer",
                     "Criação de personagens para games",
                     "Fundamentos de programação",
                     "Prototipação para quem tem pressa",
                     "Versionamento de código",
                     "Fundamentos de orientação a objetos",
                     "Storytelling",
                     "Entendendo Linux"]

TRILHAS_DICT = {
                    "DND":"Design para quem não é designer",
                    "CPG":"Criação de personagens para games",
                    "FP":"Fundamentos de programação",
                    "PQTP":"Prototipação para quem tem pressa",
                    "VS":"Versionamento de código",
                    "FOO":"Fundamentos de orientação a objetos",
                    "STY":"Storytelling",
                    "ELX": "Entendendo Linux"}

class App:

    st.set_page_config(page_title="Análise Certificados", layout="wide")

    if 'client' not in st.session_state:
        print("Initializing MongoDB client variable in session state.")
        st.session_state.client = None
    
    if 'db' not in st.session_state:
        print("Initializing MongoDB database variable in session state.")
        st.session_state.db = None

    if 'collection' not in st.session_state:
        print("Initializing MongoDB collection variable in session state.")
        st.session_state.collection = None
    
    if 'collection_auth' not in st.session_state:
        print("Initializing MongoDB collection_auth variable in session state.")
        st.session_state.collection_auth = None

    if 'collection_social' not in st.session_state:
        print("Initializing MongoDB collection_social variable in session state.")
        st.session_state.collection_social = None

    if 'user' not in st.session_state:
        print("Initializing user variable in session state.")
        st.session_state.user = None

    if 'authenticated' not in st.session_state:
        print("Initializing authenticated variable in session state.")
        st.session_state.authenticated = False

    if 'selected_page' not in st.session_state:
        print("Initializing selected_page variable in session state.")
        st.session_state.selected_page = "Login"
    
    if 'flag_login_bt' not in st.session_state:
        print("Initializing flag_login_bt variable in session state.")
        st.session_state.flag_login_bt = False

    if 'login_bt' not in st.session_state:
        print("Initializing login_bt variable in session state.")
        st.session_state.login_bt = False

    if 'upload_button' not in st.session_state:
        print("Initializing upload_button variable in session state.")
        st.session_state.upload_button = False

    if 'plot_data' not in st.session_state:
        print("Initializing plot_data variable in session state.")
        st.session_state.plot_data = None
    
    if 'upload_data' not in st.session_state:
        print("Initializing upload_data variable in session state.")
        st.session_state.upload_data = False

    if 'mongo_connection' not in st.session_state:
        MONGO_URI = st.secrets["database"]["mongo_uri"]
        MONGO_DB = st.secrets["database"]["mongo_db"]
        MONGO_COLLECTION = st.secrets["database"]["mongo_collection"]
        MONGO_COLLECTION_AUTH = st.secrets["database"]["mongo_collection_auth"]
        MONGO_COLLECTION_SOCIAL = st.secrets["database"]["mongo_collection_social"]

        try:
            # Connect to MongoDB
            st.session_state.client = pymongo.MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
            st.session_state.db = st.session_state.client[MONGO_DB]
            st.session_state.collection = st.session_state.db[MONGO_COLLECTION]
            st.session_state.collection_social = st.session_state.db[MONGO_COLLECTION_SOCIAL]
            st.session_state.collection_auth = st.session_state.db[MONGO_COLLECTION_AUTH]

            st.session_state.mongo_connection = True
            st.success("MongoDB connection successful.")
        except pymongo.errors.ConnectionError as e:
            st.session_state.mongo_connection = False

    if 'total_inscritos_canvas' not in st.session_state:
        print("Initializing total_inscritos_canvas variable in session state.")
        st.session_state.total_inscritos_canvas = 0

    if 'flag_files_social_media' not in st.session_state:
        print("Initializing flag_files_social_media variable in session state.")
        st.session_state.flag_files_social_media = False

    if 'social_media_data' not in st.session_state:
        print("Initializing social_media_data variable in session state.")
        st.session_state.social_media_data = {
            "rede": "",
            "mes": 0,
            "ano": 0,
            "seguidores": {},
            "visualizacoes": {},
            "visitas": {},
            "alcance": {},
            "toques": {},
            "interacoes": {}
        }

    if 'social_media_mongo' not in st.session_state:
        print("Initializing social_media_mongo variable in session state.")
        st.session_state.social_media_mongo = {}

    if 'flag_social_media_mongo' not in st.session_state:
        print("Initializing flag_social_media_mongo variable in session state.")
        st.session_state.flag_social_media_mongo = False

    if 'ano_op' not in st.session_state:
        print("Initializing ano_op variable in session state.")
        st.session_state.ano_op = []
    
    if 'mes_op' not in st.session_state:
        print("Initializing mes_op variable in session state.")
        st.session_state.mes_op = []

    if 'upload_button_moodlefiles' not in st.session_state:
        print("Initializing upload_button_moodlefiles variable in session state.")
        st.session_state.upload_button_moodlefiles = False

    if 'role_flag' not in st.session_state:
        print("Initializing role_flag variable in session state.")
        st.session_state.role_flag = False

    def __init__(self):
        self.title = "My Streamlit App"
        self.description = "This is a simple Streamlit app."
        self.version = "1.0.0"
        self.author = "Alleff Dymytry"

    def authentication(self, username, password):
        '''Função com a lógica de autenticação'''
        mongo_user = st.session_state.collection_auth.find_one({"username": username, "password": password})
        if mongo_user.get("username") == username and mongo_user.get("password") == password:
            st.session_state.user = mongo_user
            if mongo_user.get("role") == "admin":
                st.session_state.role_flag = False
            else:
                st.session_state.role_flag = True
            
            st.session_state.authenticated = True
            return True
        else:
            st.session_state.authenticated = False
            return False
    
    def render_chart_with_tooltip(self, series_data):
        components.html(f"""
        <div id="chart-container" style="position: relative; height: 400px; width: 100%;">
            <div id="chart" style="height: 100%;"></div>
            <div id="tooltip" style="
                width: 120px;
                height: auto;
                position: absolute;
                display: none;
                padding: 8px;
                box-sizing: border-box;
                font-size: 12px;
                text-align: left;
                z-index: 1000;
                top: 12px;
                left: 12px;
                pointer-events: none;
                border: 1px solid rgba(38, 166, 154, 1);
                border-radius: 2px;
                font-family: -apple-system, BlinkMacSystemFont, 'Trebuchet MS', Roboto, Ubuntu, sans-serif;
                background: white;
                color: black;
            "></div>
        </div>
        <script src="https://cdn.jsdelivr.net/npm/lightweight-charts@4.0.0/dist/lightweight-charts.standalone.production.js"></script>
        <script>
            const chart = LightweightCharts.createChart(document.getElementById('chart'), {{
                layout: {{
                    background: {{ type: 'solid', color: '#000000' }},
                    textColor: '#ffffff',
                }},
                grid: {{
                    vertLines: {{ color: 'rgba(197, 203, 206, 0.5)' }},
                    horzLines: {{ color: 'rgba(197, 203, 206, 0.5)' }},
                }},
                crosshair: {{
                    mode: LightweightCharts.CrosshairMode.Normal,
                }},
            }});

            const tooltip = document.getElementById('tooltip');
            const container = document.getElementById('chart-container');

            // Adicionando múltiplas séries
            const seriesData = {series_data};
            seriesData.forEach((seriesItem) => {{
                const series = chart.addLineSeries({{
                    color: seriesItem.options.color,
                    lineWidth: 2,
                }});
                series.setData(seriesItem.data);
            }});

            chart.subscribeCrosshairMove((param) => {{
                if (!param.time || param.point.x < 0 || param.point.x > container.clientWidth || param.point.y < 0 || param.point.y > container.clientHeight) {{
                    tooltip.style.display = 'none';
                    return;
                }}

                const price = param.seriesData.values().next().value?.value || 'N/A';
                tooltip.style.display = 'block';
                tooltip.innerHTML = `
                    <div style="color: rgba(38, 166, 154, 1);">Certificados</div>
                    <div style="font-size: 24px; margin: 4px 0px; color: black;">${{price}}</div>
                    <div style="color: black;">${{param.time}}</div>
                `;

                const toolTipWidth = 120;
                const toolTipHeight = 80;
                const toolTipMargin = 15;

                let left = param.point.x + toolTipMargin;
                if (left > container.clientWidth - toolTipWidth) {{
                    left = param.point.x - toolTipMargin - toolTipWidth;
                }}

                let top = param.point.y + toolTipMargin;
                if (top > container.clientHeight - toolTipHeight) {{
                    top = param.point.y - toolTipHeight - toolTipMargin;
                }}

                tooltip.style.left = left + 'px';
                tooltip.style.top = top + 'px';
            }});

            chart.timeScale().fitContent();
        </script>
        """, height=400)

    def update_data_plot(self):
        '''Função para atualizar os dados do gráfico'''
        if st.session_state.plot_data == None or st.session_state.upload_data:
            data = st.session_state.collection.find()
            st.session_state.plot_data = []
            for item in data:
                st.session_state.plot_data.append(item)
            st.session_state.upload_data = False

    def get_data(self):
        '''Função para pegar os dados do MongoDB'''

        chart_data = {}
        
        aux = sorted(st.session_state.plot_data, key=lambda x: (x["type"], datetime.strptime(x["dia"], "%d-%m-%y")))
        st.session_state.plot_data = aux
        for item in st.session_state.plot_data:
            item_type = item.get('type')
            data_aux = item.get('dia').split("-")
            data_en = f"20{data_aux[2]}-{data_aux[1]}-{data_aux[0]}"
            if item_type not in chart_data:
                chart_data[item_type] = []
            chart_data[item_type].append({
            "time": data_en,
            "value": item.get('qnt')
            })

        # Convert the chart_data into a format suitable for streamlit_lightweight_charts
        series_data = []
        for item_type, values in chart_data.items():
            series_data.append({
            "type": 'Line',
            "data": values,
            "options": {
                "color": '#26a69a' if item_type == 'T' else '#ff5722',
                "lineWidth": 2,
            }
            })

        self.render_chart_with_tooltip(series_data)

        # Render the chart
        renderLightweightCharts([
            {
            "chart": {
                "height": 400,
                "layout": {
                "background": {
                    "type": 'solid',
                    "color": '#ffffff'
                },
                "textColor": '#000000',
                },
                "grid": {
                "vertLines": {
                    "color": 'rgba(197, 203, 206, 0.5)',
                },
                "horzLines": {
                    "color": 'rgba(197, 203, 206, 0.5)',
                }
                }
            },
            "series": series_data,
            "tooltip": {
                "mode": "single",
                "position": "absolute",
                "backgroundColor": "rgba(0, 0, 0, 1)",
                "borderColor": "rgba(255, 255, 255, 1)",
                "borderWidth": 1,
                "textColor": "#ffffff",
                "fontSize": 12,
                "padding": 8,
            }
            }
        ], 'chart')

    def __insert_user_manager(self, username, password, role):
        '''Função para inserir o usuário no MongoDB'''
        if st.session_state.mongo_connection:
            st.session_state.collection_auth.insert_one({"username": username, "password": password, "role": role})
            st.success("User inserted successfully.")
        else:
            st.error("MongoDB connection failed.")

    def run(self):

        if not st.session_state.authenticated and st.session_state.selected_page == "Login" and not st.session_state.flag_login_bt:
            with st.sidebar:
                st.session_state.selected_page = option_menu("Main Menu", ["Login"], 
                            icons=['gear'], menu_icon="cast", default_index=0)
                st.markdown("#")
                st.markdown("#")
                st.markdown("#")
                st.markdown("#")
                st.markdown("#")
                st.markdown("#")
                st.markdown("#")
                st.markdown("#")
                st.markdown("#")
                st.markdown("#")
                st.write(f"Version: {self.version}")
                st.write(f"Author: {self.author}")
            
            self.username = st.text_input("Username")
            self.password = st.text_input("Password", type="password")
            st.session_state.login_button = st.button("Login")

            if st.session_state.mongo_connection:
                if st.session_state.login_button and not st.session_state.flag_login_bt:
                    if self.username != "" or self.password != "":
                        if self.authentication(self.username, self.password):
                            st.success("Login successful!")
                            st.session_state.selected_page = "Home"
                            st.session_state.flag_login_bt = True
                            st.rerun()
                        else:
                            st.error("Invalid username or password.")
                    else:
                        st.error("Please enter username and password.")
            
            # st.image("/Users/alleff/Downloads/regua.png", width=200)
        else:
            with st.sidebar:
                # st.session_state.selected_page = option_menu("Main Menu", ["Home", "Dashboard", "Inserir Dados Certificados", "Inserir Dados Redes Sociais", "Configurações", "Dashboard Redes","Inserir Posts", "---" ,"Info"], 
                #             icons=['house', 'database', 'cloud-upload','gear', 'gear', 'database', 'postage','','question-circle-fill'], menu_icon="cast", default_index=0)
                with st.container(border=True):
                    st.session_state.selected_page = sac.menu([
                        sac.MenuItem('Home', icon='house-fill'),
                        sac.MenuItem('Dashboards', icon='box-fill', children=[
                            sac.MenuItem('Certificados', icon='apple',disabled=st.session_state.role_flag),
                            sac.MenuItem('Redes Sociais', icon='apple'),
                            sac.MenuItem('Inserir Dados', icon='gear', children=[
                                sac.MenuItem('Certificados', icon='cloud-upload',disabled=st.session_state.role_flag),
                                sac.MenuItem('Redes Sociais', icon='cloud-upload'),
                                sac.MenuItem('Posts', icon='cloud-upload',disabled=st.session_state.role_flag),
                            ]),]),
                        sac.MenuItem(type='divider'),
                        sac.MenuItem('Ferramentas', icon='git', description='Análises', children=[
                                sac.MenuItem('Canvas', icon='google', children=[
                                    sac.MenuItem('Análise de Indicadores', icon='file-earmark-text',disabled=st.session_state.role_flag),
                                    sac.MenuItem('Envio de Arquivos', icon='cloud-upload',disabled=st.session_state.role_flag),
                                ]),
                                sac.MenuItem('Moodle', icon='gitlab', children=[
                                    sac.MenuItem('Análise de Indicadores', icon='file-earmark-text',disabled=st.session_state.role_flag),
                                    sac.MenuItem('Envio de Arquivos', icon='cloud-upload',disabled=st.session_state.role_flag),
                                ]),]),
                        sac.MenuItem(type='divider'),
                        sac.MenuItem('Links', type='group', children=[
                            sac.MenuItem('TICLAB', icon='heart-fill', href='https://ticlab.com.br'),
                            sac.MenuItem('TIC em Trilhas', icon='heart-fill', href='https://ticemtrilhas.org.br'),
                        ]),
                        sac.MenuItem(type='divider'),
                        sac.MenuItem('Configurações', icon='gear', children=[
                            sac.MenuItem('Configurações Gerais', icon='gear',disabled=st.session_state.role_flag),
                            sac.MenuItem('Configurações de Usuário', icon='person-circle',disabled=st.session_state.role_flag),
                        ]),
                    ], open_all=True, return_index=True, variant='filled')
                    # st.write(st.session_state.selected_page)
                if st.session_state.authenticated:
                    st.button("Logout", on_click=lambda: [setattr(st.session_state, 'authenticated', False), setattr(st.session_state, 'selected_page', "Login"), setattr(st.session_state, 'flag_login_bt', False)])
                st.markdown("#")
                st.markdown("#")
                st.markdown("#")
                st.markdown("#")
                st.markdown("#")
                st.markdown("#")
                st.markdown("#")
                st.markdown("#")
                st.markdown("#")
                st.markdown("#")
                st.write(f"Version: {self.version}")
                st.write(f"Author: {self.author}")
                
            if st.session_state.selected_page == 0: # Home
                st.markdown("# Análise de Certificados Emitidos")
                st.markdown("---")
                st.markdown("### Esse é um projeto para análise dos certificados emitidos na plataforma Canvas e Moodle.")
                st.markdown("#### No atual momento o projeto está em fase de desenvolvimento:")
                st.markdown("- ✅ Análise de certificados emitidos na plataforma Canvas")
                st.markdown("- ❌ Análise de certificados emitidos na plataforma Moodle")
                st.markdown("- ❌ Análise de certificados emitidos na capacitação presencial")
                st.markdown("- ✅ Gráfico de certificados emitidos na plataforma Canvas (totais e únicos)")
                st.markdown("- ✅ Envio de arquivos de certificados emitidos (Canvas)")
                st.markdown("- ❌ Envio de arquivos de certificados emitidos (Moodle)")
                st.markdown("- ❌ Gráfico de certificados emitidos na plataforma Moodle (totais e únicos)")
                st.markdown("- ✅ Integração dos dados com o Banco de Dados")
                st.markdown("- ✅ Sisetma de Login")
            elif st.session_state.selected_page == 2: # Dashboard Certificados
                sac.segmented(
                    items=[
                        sac.SegmentedItem(label='Linha', icon='graph-up'),
                        sac.SegmentedItem(label='Área', icon='mask'),
                        sac.SegmentedItem(label='Barras', icon='bar-chart-fill'),
                        sac.SegmentedItem(label='link', icon='share-fill', href='https://mantine.dev/core/segmented-control/'),
                    ], label='Tipos de gráficos', align='center'
                )
            
                filter_column = st.columns([1, 1, 1])

                sac.cascader(items=[
                    sac.CasItem('home', icon='house'),
                    sac.CasItem('app', icon='app', children=[
                        sac.CasItem('store', icon='bag-check'),
                        sac.CasItem('brand', icon='award', children=[
                            sac.CasItem('github', icon='github'),
                            sac.CasItem('google', icon='google'),
                            sac.CasItem('apple', icon='apple', children=[
                                sac.CasItem('admin', icon='person-circle'),
                                sac.CasItem('guest', icon='person'),
                                sac.CasItem('twitter' * 5, icon='twitter'),
                            ]),
                        ]),
                    ]),
                    sac.CasItem('disabled', icon='send', disabled=True),
                    sac.CasItem('other1'),
                    sac.CasItem('other2')
                ], label='Filtros', index=None, multiple=True, search=True, clear=True)
                st.button("Aplicar Filtros")

                self.update_data_plot()
                c1, c2 , c3 = st.columns(3)
                with c1:
                    st.metric(label="Inscritos", value=st.session_state.total_inscritos_canvas, delta=0)
                with c2:
                    aux = []
                    for item in st.session_state.plot_data:
                        if item.get('type') == 'T':
                            aux.append(item.get('qnt'))
                    aux = sorted(aux, key=lambda x: x)
                    maior = max(aux)
                    st.metric(label="Certificados Emitidos", value=maior, delta=f"{round(((maior*100)/aux[-2])-100,2)}%")
                self.get_data()  
            elif st.session_state.selected_page == "Configurações": # Configurações
                st.write("Welcome to the Settings page!")
            elif st.session_state.selected_page == 22: 
                st.write("Welcome to the Info page!")
                uploaded_files = st.file_uploader("Upload CSV", type=["csv"], accept_multiple_files=True)
                st.session_state.upload_button = st.button("JUNTA TUDO", on_click=self.junta_tudo, args=(uploaded_files,))


                header = ["Nome estudante", "CPF", "Gênero", "Data de nascimento", "Escolaridade", "Estado", "Status do estudante", "Trilha", "Nível da trilha", "Modalide", "Parceiro", "Afirmativa", "Acessível", "Área TIC", "Área ACM", "Executora"]
                siproex_files = st.file_uploader("Upload SIPROEX", type=["csv"], accept_multiple_files=True)
                st.session_state.upload_button = st.button("ANALISE", on_click=self.siproex, args=(siproex_files,))
            elif st.session_state.selected_page == 6: # Inserir Dados Redes Sociais
                st.markdown("# Inserção de dados das Redes Sociais")
                uploaded_files = st.file_uploader("Upload CSV", type=["csv"], accept_multiple_files=True)
                cl, cr = st.columns([1, 1])
                with cl:
                    mes = st.selectbox("Selecione o mês", options=["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"])
                with cr:
                    ano = st.number_input("Digite o Ano", min_value=2020, max_value=2100, value=2025, step=1)
                st.session_state.upload_button = st.button("Upload", on_click=self.upload_button_socialmedia, args=(uploaded_files,mes,ano,))
            elif st.session_state.selected_page == 7: # Inserir Dados Posts
                st.write("POSTS")
                with st.container(border=True):
                    cl, cm, cr = st.columns([1,1,1])
                    with cl:
                        st.text_input("Nome do Post")
                        st.selectbox("Tipo de Post", options=["Reel", "Carrosel"], index=None, placeholder="Escolha o tipo de post")
                    with cm:
                        st.date_input("Data de Publicação")
                        st.text_input("Intenção")
                    with cr:
                        st.selectbox("Plataforma", options=["Instagram", "Linkedin"], index=None, placeholder="Escolha a plataforma")
                        st.selectbox("Trilha Foco", options=TRILHAS_OFERTADAS, index=None, placeholder="Escolha a trilha")
                bt_align = st.columns([1,1,1])
                with bt_align[1]:
                    bt_align_sub = st.columns([1,1,1])
                    with bt_align_sub[1]:
                        st.button("Cadastrar")
            elif st.session_state.selected_page == 3: # Dashboard Redes Sociais
                if not st.session_state.flag_social_media_mongo:
                    st.session_state.ano_op, st.session_state.mes_op = self.get_data_social_media()
                    st.session_state.flag_social_media_mongo = True
                
                metric_l2, metric_m2, metric_r2 = st.columns([1, 1, 1])
                with metric_l2:
                    st.metric(label="Total de Seguidores geral", value=1000, delta=0, border=True)
                with metric_m2:
                    st.metric(label="Total de Alcance geral", value=10000, delta=0, border=True)
                with metric_r2:
                    st.metric(label="Total de Interações geral", value=50, delta=0, border=True)
                style_metric_cards(background_color="#000000", border_color="#000000")

                date_lf,date_rh = st.columns([1, 1])
                with date_lf:
                    ano_de_postagem = st.selectbox("Selecione o ano", options=st.session_state.ano_op, index=None)
                with date_rh:
                    mes_de_postagem = st.selectbox("Selecione o mês", options=st.session_state.mes_op, index=None)

                if st.session_state.flag_social_media_mongo:
                    metric_m, metric_r = st.columns([1, 1])
                    with metric_m:
                        st.metric(label="Total de Alcance mês X", value=10000, delta=0, border=True)
                    with metric_r:
                        st.metric(label="Total de Interações mês X", value=50, delta=0, border=True)
                    style_metric_cards(background_color="#000000", border_color="#000000")

                    sl, sm, sr = st.columns([1, 1, 1])
                    with sl:
                        select_ano = st.selectbox("Ano", options=st.session_state.ano_op, index=None)
                    with sm:
                        select_mes = st.selectbox("Mês", options=st.session_state.mes_op, index=None)
                    with sr:
                        select_semana = st.selectbox("Semana", options=["01 - 07", "08 - 15", "16 - 24", "25 - 31"], index=None)

                    # Transform st.session_state.social_media_mongo into a dictionary for easier access
                    social_media_dict = {}
                    for item in st.session_state.social_media_mongo:
                        year = item.get('ano')
                        month = item.get('mes')
                        if year not in social_media_dict:
                            social_media_dict[year] = {}
                        if month not in social_media_dict[year]:
                            social_media_dict[year][month] = {}
                        for key, value in item.items():
                            if key not in ['ano', 'mes', '_id', 'rede']:
                                social_media_dict[year][month][key] = value

                    if select_ano != None:
                        if select_mes != None:
                            major_c_l, major_c_m, major_c_r = st.columns([1, 1, 1])

                            indicators = ["Seguidores", "Visualizações", "Visitas", "Alcance", "Toques", "Interações"]
                            colors = ['#26a69a', '#7bb6d4', '#ad5a34', '#4a34ad', '#bfb82e', '#db4471']
                            cont = 0
                            series_data_all = []

                            for name in indicators:
                                # Convert the chart_data into a format suitable for streamlit_lightweight_charts
                                series_data = []
                                for date, value in social_media_dict[select_ano][select_mes][self.convert_name(name)].items():
                                    if select_semana != None:
                                        semana = select_semana.split(" - ")
                                        # st.write(semana)
                                        date_aux = date.split("-")
                                        # st.write(date_aux)
                                        if date_aux[2] >= semana[0] and date_aux[2] <= semana[1]:
                                                series_data.append({
                                                    "type": 'Line',
                                                    "data": [{"time": date, "value": int(value)}],
                                                    "options": {
                                                        "color": '#26a69a',
                                                        "lineWidth": 2,}})
                                    else:
                                        series_data.append({
                                            "type": 'Line',
                                            "data": [{"time": date, "value": int(value)}],
                                            "options": {
                                                "color": '#26a69a',
                                                "lineWidth": 2,
                                            }
                                        })

                                # Group data by type and create a single series for each type
                                grouped_data = {}
                                for item in series_data:
                                    print(item)
                                    for point in item["data"]:
                                        if item["type"] not in grouped_data:
                                            grouped_data[item["type"]] = []
                                        grouped_data[item["type"]].append(point)

                                # Combine grouped data into a single series for each type
                                combined_series_data = []
                                
                                for series_type, points in grouped_data.items():
                                    combined_series_data.append({
                                        "type": 'Line',
                                        "data": sorted(points, key=lambda x: x["time"]),
                                        "options": {
                                            "color": colors[cont],
                                            "lineWidth": 2,
                                        }
                                    })

                                series_data = combined_series_data
                                series_data_all.append(series_data)
                                cont += 1

                            with major_c_l:
                                # Render the chart
                                st.markdown("### Seguidores")
                                renderLightweightCharts([
                                    {
                                    "chart": {
                                        "height": 200,
                                        "layout": {
                                            "background": {
                                                "type": 'solid',
                                                "color": '#000000'
                                            },
                                            "textColor": '#ffffff',
                                        },
                                        "grid": {
                                            "vertLines": {
                                                "color": 'rgba(197, 203, 206, 0.0)',
                                            },
                                            "horzLines": {
                                                "color": 'rgba(197, 203, 206, 0.0)',
                                            }
                                        },
                                        "rightPriceScale": {
                                            "scaleMargins": {"top": 0.4, "bottom": 0.15},
                                            "priceFormat": {
                                                "type": "price",
                                                "precision": 0,
                                                "minMove": 1
                                            }
                                        }
                                    },
                                    "series": series_data_all[0],
                                    "tooltip": {
                                        "mode": "single",
                                        "position": "absolute",
                                        "backgroundColor": "rgba(0, 0, 0, 1)",
                                        "borderColor": "rgba(255, 255, 255, 1)",
                                        "borderWidth": 1,
                                        "textColor": "#ffffff",
                                        "fontSize": 12,
                                        "padding": 8,
                                    }
                                }
                                ], 'chart1')

                                # Render the chart
                                st.markdown("### Visualizações")
                                renderLightweightCharts([
                                    {
                                    "chart": {
                                        "height": 200,
                                        "layout": {
                                            "background": {
                                                "type": 'solid',
                                                "color": '#000000'
                                            },
                                            "textColor": '#ffffff',
                                        },
                                        "grid": {
                                            "vertLines": {
                                                "color": 'rgba(197, 203, 206, 0.0)',
                                            },
                                            "horzLines": {
                                                "color": 'rgba(197, 203, 206, 0.0)',
                                            }
                                        }
                                    },
                                    "series": series_data_all[1],
                                    "tooltip": {
                                        "mode": "single",
                                        "position": "absolute",
                                        "backgroundColor": "rgba(0, 0, 0, 1)",
                                        "borderColor": "rgba(255, 255, 255, 1)",
                                        "borderWidth": 1,
                                        "textColor": "#ffffff",
                                        "fontSize": 12,
                                        "padding": 8,
                                    }
                                    }
                                ], 'chart2')
                            with major_c_m:
                                # Render the chart
                                st.markdown("### Visitas")
                                renderLightweightCharts([
                                    {
                                    "chart": {
                                        "height": 200,
                                        "layout": {
                                            "background": {
                                                "type": 'solid',
                                                "color": '#000000'
                                            },
                                            "textColor": '#ffffff',
                                        },
                                        "grid": {
                                            "vertLines": {
                                                "color": 'rgba(197, 203, 206, 0.0)',
                                            },
                                            "horzLines": {
                                                "color": 'rgba(197, 203, 206, 0.0)',
                                            }
                                        }
                                    },
                                    "series": series_data_all[2],
                                    "tooltip": {
                                        "mode": "single",
                                        "position": "absolute",
                                        "backgroundColor": "rgba(0, 0, 0, 1)",
                                        "borderColor": "rgba(255, 255, 255, 1)",
                                        "borderWidth": 1,
                                        "textColor": "#ffffff",
                                        "fontSize": 12,
                                        "padding": 8,
                                    }
                                    }
                                ], 'chart3')

                                # Render the chart
                                st.markdown("### Alcance")
                                renderLightweightCharts([
                                    {
                                    "chart": {
                                        "height": 200,
                                        "layout": {
                                            "background": {
                                                "type": 'solid',
                                                "color": '#000000'
                                            },
                                            "textColor": '#ffffff',
                                        },
                                        "grid": {
                                            "vertLines": {
                                                "color": 'rgba(197, 203, 206, 0.0)',
                                            },
                                            "horzLines": {
                                                "color": 'rgba(197, 203, 206, 0.0)',
                                            }
                                        }
                                    },
                                    "series": series_data_all[3],
                                    "tooltip": {
                                        "mode": "single",
                                        "position": "absolute",
                                        "backgroundColor": "rgba(0, 0, 0, 1)",
                                        "borderColor": "rgba(255, 255, 255, 1)",
                                        "borderWidth": 1,
                                        "textColor": "#ffffff",
                                        "fontSize": 12,
                                        "padding": 8,
                                    }
                                    }
                                ], 'chart4')
                            with major_c_r:
                            # Render the chart
                                st.markdown("### Toques")
                                renderLightweightCharts([
                                    {
                                    "chart": {
                                        "height": 200,
                                        "layout": {
                                            "background": {
                                                "type": 'solid',
                                                "color": '#000000'
                                            },
                                            "textColor": '#ffffff',
                                        },
                                        "grid": {
                                            "vertLines": {
                                                "color": 'rgba(197, 203, 206, 0.0)',
                                            },
                                            "horzLines": {
                                                "color": 'rgba(197, 203, 206, 0.0)',
                                            }
                                        }
                                    },
                                    "series": series_data_all[4],
                                    "tooltip": {
                                        "mode": "single",
                                        "position": "absolute",
                                        "backgroundColor": "rgba(0, 0, 0, 1)",
                                        "borderColor": "rgba(255, 255, 255, 1)",
                                        "borderWidth": 1,
                                        "textColor": "#ffffff",
                                        "fontSize": 12,
                                        "padding": 8,
                                    }
                                    }
                                ], 'chart5')

                                # Render the chart
                                st.markdown("### Interações")
                                renderLightweightCharts([
                                    {
                                    "chart": {
                                        "height": 200,
                                        "layout": {
                                            "background": {
                                                "type": 'solid',
                                                "color": '#000000'
                                            },
                                            "textColor": '#ffffff',
                                        },
                                        "grid": {
                                            "vertLines": {
                                                "color": 'rgba(197, 203, 206, 0.0)',
                                            },
                                            "horzLines": {
                                                "color": 'rgba(197, 203, 206, 0.0)',
                                            }
                                        }
                                    },
                                    "series": series_data_all[5],
                                    "tooltip": {
                                        "mode": "single",
                                        "position": "absolute",
                                        "backgroundColor": "rgba(0, 0, 0, 1)",
                                        "borderColor": "rgba(255, 255, 255, 1)",
                                        "borderWidth": 1,
                                        "textColor": "#ffffff",
                                        "fontSize": 12,
                                        "padding": 8,
                                    }
                                    }
                                ], 'chart6')

                            data_json = json.dumps(series_data_all[5][0]["data"])

                            # Insere o código HTML+JS diretamente via componente
                            components.html(f"""
                            <div id="container" style="width: 100%; height: 300px; position: relative;"></div>

                            <script src="https://unpkg.com/lightweight-charts@4.0.0/dist/lightweight-charts.standalone.production.js"></script>
                            <script>
                                const chartOptions = {{
                                    layout: {{
                                        textColor: 'black',
                                        background: {{ type: 'solid', color: 'white' }},
                                    }},
                                    rightPriceScale: {{
                                        scaleMargins: {{
                                            top: 0.4,
                                            bottom: 0.15,
                                        }},
                                    }},
                                    crosshair: {{
                                        horzLine: {{
                                            visible: false,
                                            labelVisible: false,
                                        }},
                                    }},
                                    grid: {{
                                        vertLines: {{ visible: false }},
                                        horzLines: {{ visible: false }},
                                    }},
                                }};

                                const chart = LightweightCharts.createChart(document.getElementById('container'), chartOptions);

                                const areaSeries = chart.addAreaSeries({{
                                    topColor: '#2962FF',
                                    bottomColor: 'rgba(41, 98, 255, 0.28)',
                                    lineColor: '#2962FF',
                                    lineWidth: 2,
                                    crossHairMarkerVisible: false,
                                }});

                                const data = {data_json};
                                areaSeries.setData(data);

                                const symbolName = 'Interações';
                                const container = document.getElementById('container');

                                const legend = document.createElement('div');
                                legend.style = `
                                    position: absolute;
                                    left: 12px;
                                    top: 12px;
                                    z-index: 1;
                                    font-size: 14px;
                                    font-family: sans-serif;
                                    line-height: 18px;
                                    font-weight: 300;
                                    color: black;
                                `;
                                container.appendChild(legend);

                                const getLastBar = series => {{
                                    const bars = data;
                                    return bars[bars.length - 1];
                                }};

                                const formatPrice = price => (Math.round(price * 100) / 100).toFixed(2);

                                const setTooltipHtml = (name, date, price) => {{
                                    legend.innerHTML = `
                                        <div style="font-size: 24px; margin: 4px 0px;">${{name}}</div>
                                        <div style="font-size: 22px; margin: 4px 0px;">${{price}}</div>
                                        <div>${{date}}</div>
                                    `;
                                }};

                                const updateLegend = param => {{
                                    const valid = param && param.time !== undefined && param.point && param.point.x >= 0 && param.point.y >= 0;
                                    const bar = valid ? param.seriesData.get(areaSeries) : getLastBar(areaSeries);
                                    const time = bar.time;
                                    const price = bar.value !== undefined ? bar.value : bar.close;
                                    const formattedPrice = formatPrice(price);
                                    setTooltipHtml(symbolName, time, formattedPrice);
                                }};

                                chart.subscribeCrosshairMove(updateLegend);
                                updateLegend(undefined);

                                chart.timeScale().fitContent();
                            </script>
                            """, height=520)

                            st.json(st.session_state.social_media_data)
                        else:
                            major_c_l, major_c_m, major_c_r = st.columns([1, 1, 1])

                            indicators = ["Seguidores", "Visualizações", "Visitas", "Alcance", "Toques", "Interações"]
                            colors = ['#26a69a', '#7bb6d4', '#ad5a34', '#4a34ad', '#bfb82e', '#db4471']
                            cont = 0
                            series_data_all = []
                            

                            for name in indicators:
                                # Convert the chart_data into a format suitable for streamlit_lightweight_charts
                                series_data = []
                                
                                for year, year_data in social_media_dict.items():
                                    for month, month_data in year_data.items():
                                        for key, value in month_data.items():
                                            for date, val in value.items():
                                                if self.convert_name(name) == key:
                                                    series_data.append({
                                                        "type": 'Line',
                                                        "data": sorted([{"time": date, "value": int(val)}]),
                                                        "options": {
                                                            "color": colors[cont],
                                                            "lineWidth": 2,
                                                        }
                                                    })
                                
                                # # Group data by type and create a single series for each type
                                grouped_data_aux = {}
                                
                                for item in series_data:
                                    print(item) #{'type': 'Line', 'data': [{'time': '2025-03-02', 'value': 2}], 'options': {'color': '#db4471', 'lineWidth': 2}}
                                    for point in item["data"]:
                                        if item["type"] not in grouped_data_aux:
                                            grouped_data_aux[item["type"]] = []
                                        grouped_data_aux[item["type"]].append(point)

                                # Combine grouped data into a single series for each type
                                combined_series_data = []
                                # print(grouped_data_aux.items())
                                for series_type, points in grouped_data_aux.items():
                                    # print(points)
                                    combined_series_data.append({
                                        "type": 'Line',
                                        "data": sorted(points, key=lambda x: x["time"]),
                                        "options": {
                                            "color": colors[cont],
                                            "lineWidth": 2,
                                        }
                                    })

                                series_data = combined_series_data
                                series_data_all.append(series_data)
                                cont += 1

                            with major_c_l:
                                # Render the chart
                                st.markdown("##### Seguidores")
                                renderLightweightCharts([
                                    {
                                    "chart": {
                                        "height": 200,
                                        "layout": {
                                            "background": {
                                                "type": 'solid',
                                                "color": '#000000'
                                            },
                                            "textColor": '#ffffff',
                                        },
                                        "grid": {
                                            "vertLines": {
                                                "color": 'rgba(197, 203, 206, 0.0)',
                                            },
                                            "horzLines": {
                                                "color": 'rgba(197, 203, 206, 0.0)',
                                            }
                                        },
                                        "rightPriceScale": {
                                            "scaleMargins": {"top": 0.4, "bottom": 0.15},
                                            "priceFormat": {
                                                "type": "price",
                                                "precision": 0,
                                                "minMove": 1
                                            }
                                        }
                                    },
                                    "series": series_data_all[0],
                                    "tooltip": {
                                        "mode": "single",
                                        "position": "absolute",
                                        "backgroundColor": "rgba(0, 0, 0, 1)",
                                        "borderColor": "rgba(255, 255, 255, 1)",
                                        "borderWidth": 1,
                                        "textColor": "#ffffff",
                                        "fontSize": 12,
                                        "padding": 8,
                                    }
                                }
                                ], 'chart1')

                                # Render the chart
                                st.markdown("##### Visualizações")
                                renderLightweightCharts([
                                    {
                                    "chart": {
                                        "height": 200,
                                        "layout": {
                                            "background": {
                                                "type": 'solid',
                                                "color": '#000000'
                                            },
                                            "textColor": '#ffffff',
                                        },
                                        "grid": {
                                            "vertLines": {
                                                "color": 'rgba(197, 203, 206, 0.0)',
                                            },
                                            "horzLines": {
                                                "color": 'rgba(197, 203, 206, 0.0)',
                                            }
                                        }
                                    },
                                    "series": series_data_all[1],
                                    "tooltip": {
                                        "mode": "single",
                                        "position": "absolute",
                                        "backgroundColor": "rgba(0, 0, 0, 1)",
                                        "borderColor": "rgba(255, 255, 255, 1)",
                                        "borderWidth": 1,
                                        "textColor": "#ffffff",
                                        "fontSize": 12,
                                        "padding": 8,
                                    }
                                    }
                                ], 'chart2')
                            with major_c_m:
                                # Render the chart
                                st.markdown("##### Visitas")
                                renderLightweightCharts([
                                    {
                                    "chart": {
                                        "height": 200,
                                        "layout": {
                                            "background": {
                                                "type": 'solid',
                                                "color": '#000000'
                                            },
                                            "textColor": '#ffffff',
                                        },
                                        "grid": {
                                            "vertLines": {
                                                "color": 'rgba(197, 203, 206, 0.0)',
                                            },
                                            "horzLines": {
                                                "color": 'rgba(197, 203, 206, 0.0)',
                                            }
                                        }
                                    },
                                    "series": series_data_all[2],
                                    "tooltip": {
                                        "mode": "single",
                                        "position": "absolute",
                                        "backgroundColor": "rgba(0, 0, 0, 1)",
                                        "borderColor": "rgba(255, 255, 255, 1)",
                                        "borderWidth": 1,
                                        "textColor": "#ffffff",
                                        "fontSize": 12,
                                        "padding": 8,
                                    }
                                    }
                                ], 'chart3')

                                # Render the chart
                                st.markdown("##### Alcance")
                                renderLightweightCharts([
                                    {
                                    "chart": {
                                        "height": 200,
                                        "layout": {
                                            "background": {
                                                "type": 'solid',
                                                "color": '#000000'
                                            },
                                            "textColor": '#ffffff',
                                        },
                                        "grid": {
                                            "vertLines": {
                                                "color": 'rgba(197, 203, 206, 0.0)',
                                            },
                                            "horzLines": {
                                                "color": 'rgba(197, 203, 206, 0.0)',
                                            }
                                        }
                                    },
                                    "series": series_data_all[3],
                                    "tooltip": {
                                        "mode": "single",
                                        "position": "absolute",
                                        "backgroundColor": "rgba(0, 0, 0, 1)",
                                        "borderColor": "rgba(255, 255, 255, 1)",
                                        "borderWidth": 1,
                                        "textColor": "#ffffff",
                                        "fontSize": 12,
                                        "padding": 8,
                                    }
                                    }
                                ], 'chart4')
                            with major_c_r:
                            # Render the chart
                                st.markdown("##### Toques")
                                renderLightweightCharts([
                                    {
                                    "chart": {
                                        "height": 200,
                                        "layout": {
                                            "background": {
                                                "type": 'solid',
                                                "color": '#000000'
                                            },
                                            "textColor": '#ffffff',
                                        },
                                        "grid": {
                                            "vertLines": {
                                                "color": 'rgba(197, 203, 206, 0.0)',
                                            },
                                            "horzLines": {
                                                "color": 'rgba(197, 203, 206, 0.0)',
                                            }
                                        }
                                    },
                                    "series": series_data_all[4],
                                    "tooltip": {
                                        "mode": "single",
                                        "position": "absolute",
                                        "backgroundColor": "rgba(0, 0, 0, 1)",
                                        "borderColor": "rgba(255, 255, 255, 1)",
                                        "borderWidth": 1,
                                        "textColor": "#ffffff",
                                        "fontSize": 12,
                                        "padding": 8,
                                    }
                                    }
                                ], 'chart5')

                                # Render the chart
                                st.markdown("##### Interações")
                                renderLightweightCharts([
                                    {
                                    "chart": {
                                        "height": 200,
                                        "layout": {
                                            "background": {
                                                "type": 'solid',
                                                "color": '#000000'
                                            },
                                            "textColor": '#ffffff',
                                        },
                                        "grid": {
                                            "vertLines": {
                                                "color": 'rgba(197, 203, 206, 0.0)',
                                            },
                                            "horzLines": {
                                                "color": 'rgba(197, 203, 206, 0.0)',
                                            }
                                        }
                                    },
                                    "series": series_data_all[5],
                                    "tooltip": {
                                        "mode": "single",
                                        "position": "absolute",
                                        "backgroundColor": "rgba(0, 0, 0, 1)",
                                        "borderColor": "rgba(255, 255, 255, 1)",
                                        "borderWidth": 1,
                                        "textColor": "#ffffff",
                                        "fontSize": 12,
                                        "padding": 8,
                                    }
                                    }
                                ], 'chart6')
            elif st.session_state.selected_page == 5: # Inserir Dados
                st.write("Welcome to the Inserir Dados page!")
                uploaded_files = st.file_uploader("Upload CSV", type=["csv"], accept_multiple_files=True)
                st.session_state.upload_button = st.button("Upload", on_click=self.upload_button, args=(uploaded_files,))
            elif st.session_state.selected_page == 15:

                st.button("INSERIR USER DATABASE", on_click=self.__insert_user_manager, args=("vitoria_tlab","souza12345","user",))


                st.markdown("### TESTE DE INSERÇÃO DE DADOS MOODLE")
                uploaded_files = st.file_uploader("Upload CSV", type=["csv"], accept_multiple_files=True)
                st.session_state.upload_button_moodlefiles = st.button("Upload", on_click=self.upload_button_moodle, args=(uploaded_files,))

            # footer_html = """<div style='text-align: center; background-color: #ffffff; position: fixed; bottom: 0px; left: 338px; right: 0px; margin-bottom: 0px;'>
            # <img src='https://raw.githubusercontent.com/alleff-pucrs/images_site/refs/heads/main/regua.png?token=GHSAT0AAAAAADDLGE5GCW73UOFBZFKIGDWY2AY626A' alt='Logo' style='width: auto; height: auto;'>
            # </div>"""
            # st.markdown(footer_html, unsafe_allow_html=True)

    def junta_tudo(self, uploaded_files):
        '''Função que junta tudo'''
        head = ["ID da Trilha", "Trilha", "Turma", "ID do Aluno", "Nome", "Email", "CPF", "Escolaridade", "Data de nascimento", "Gênero", "Status", "Estado", "Cidade", "Data de conclusão", "Link certificado"]

    def certificate_file_analisys(self, filename):
        '''Função que vai fazer análise do arquivo CSV'''
        '''
            Informações do arquivo:
            Trilha [2]
            ID da Trilha [3]
            ID do Aluno [5]
            Nome do Aluno [6]
            Email do Aluno [7]
            CPF [8]
            Nível de educação [9]
            Data de nascimento [10]
            Gênero [12]
            Progresso [21]
            Link certificado [23]
        '''
        clean_info = []
        
        for row in filename[1:]:
            aux = row[4].split(" ")
            edicao = aux[1]
            clean_info.append([row[2], row[3], row[5], row[6], row[7], row[8], row[9], row[10], row[12], row[21], row[23], row[4], edicao])

        count_completion_certificate = 0

        count_total = 0

        certificate_only = []

        for info in clean_info:
            count_total += 1
            if info[10] != "":
                certificate_only.append(info)
                count_completion_certificate += 1
        print(f"Quantidade de certificados emitidos: {count_completion_certificate}")
        unique_cpf = []
        for info in certificate_only:
            if info[5] not in [cpf[5] for cpf in unique_cpf]:
                unique_cpf.append(info)
        print(f"Unicidade baseada no CPF")
        print(f"Quantidade de pessoas únicas certificadas na plataforma Canvas: {len(unique_cpf)}")
        print(f"Porcentagem de pessoas que fizeram outras trilhas: {round(100-(len(unique_cpf)/len(certificate_only))*100, 2)}%")
        print("###############################################################################################")
        st.session_state.total_inscritos_canvas = count_total
        return len(certificate_only), len(unique_cpf)

    def send_data_certificate(self, total, unico):
        '''Função que envia os dados dos certificados para o banco de dados'''
        print(f"O QUE TEM NAS LISTAS: {total} | {unico}")
        if st.session_state.db != None:
            try:
                st.session_state.db.certificados.insert_many(total["data"])
                st.session_state.db.certificados.insert_many(unico["data"])
                st.session_state.upload_data = True
                st.success("Data inserted successfully.")
            except pymongo.errors.BulkWriteError as e:
                st.error(f"Error inserting data into MongoDB: {e}")

    def convert_name(self, name):
        '''Função para ajustar o nome dos indicadores das Redes Sociais em Keys do JSON'''
        if name == "Seguidores":
            return "seguidores"
        elif name == "Visualizações":
            return "visualizacoes"
        elif name == "Visitas":
            return "visitas"
        elif name == "Alcance":
            return "alcance"
        elif name == "Toques":
            return "toques"
        elif name == "Interações":
            return "interacoes"

    def upload_button_socialmedia(self, uploaded_files, mes, ano):
        '''Função de tratamento dos arquivos CSV após upload'''

        if uploaded_files != []:
            st.session_state.social_media_data["rede"] = "Instagram"
            st.session_state.social_media_data["mes"] = mes
            st.session_state.social_media_data["ano"] = ano
            for uploaded_file in uploaded_files:
                content = io.StringIO(uploaded_file.read().decode('utf-16'))
                _redaer = csv.reader(content)
                #Tratamento de cada um dos 6 arquivos CSV que o Instagram disponibiliza
                if uploaded_file.name == "Alcance.csv":
                    # 1 - Alcance
                    next(_redaer)
                    next(_redaer)
                    next(_redaer)
                    for row in _redaer:
                        if row != []:
                            st.session_state.social_media_data["alcance"][row[0].split("T")[0]] = row[1]
                elif uploaded_file.name == "Interações.csv":
                    # 2 - Interações
                    next(_redaer)
                    next(_redaer)
                    next(_redaer)
                    for row in _redaer:
                        if row != []:
                            st.session_state.social_media_data["interacoes"][row[0].split("T")[0]] = row[1]
                elif uploaded_file.name == "Seguidores.csv":
                    # 3 - Seguidores
                    next(_redaer)
                    next(_redaer)
                    next(_redaer)
                    for row in _redaer:
                        if row != []:
                            st.session_state.social_media_data["seguidores"][row[0].split("T")[0]] = row[1]
                elif uploaded_file.name == "Visualizações.csv":
                    # 4 - Visualizações
                    next(_redaer)
                    next(_redaer)
                    next(_redaer)
                    for row in _redaer:
                        if row != []:
                            st.session_state.social_media_data["visualizacoes"][row[0].split("T")[0]] = row[1]
                elif uploaded_file.name == "Visitas.csv":
                    # 5 - Visitas
                    next(_redaer)
                    next(_redaer)
                    next(_redaer)
                    for row in _redaer:
                        if row != []:
                            st.session_state.social_media_data["visitas"][row[0].split("T")[0]] = row[1]
                elif uploaded_file.name == "Cliques no link.csv":
                    # 6 - Toques
                    next(_redaer)
                    next(_redaer)
                    next(_redaer)
                    for row in _redaer:
                        if row != []:
                            st.session_state.social_media_data["toques"][row[0].split("T")[0]] = row[1]
            st.session_state.flag_files_social_media = True
            # st.json(social, expanded=True)
            if st.session_state.db != None:
                try:
                    st.session_state.db.redes.insert_one(st.session_state.social_media_data)
                    st.success("Data inserted successfully.")
                    st.session_state.social_media_data = {
                        "rede": "",
                        "mes": 0,
                        "ano": 0,
                        "seguidores": {},
                        "visualizacoes": {},
                        "visitas": {},
                        "alcance": {},
                        "toques": {},
                        "interacoes": {}
                    }
                except pymongo.errors.BulkWriteError as e:
                    st.error(f"Error inserting data into MongoDB: {e}")

    def siproex(self, uploaded_files):
        '''Função que vai fazer a análise do SIPROEX'''
        teste_total = {"dados": []}
        base_dados = {"dados": []}
        base_interna = {'Está na aba No ar': '',
                        'Ano de nascimento': '',
                        'ID_PROJETO': '',
                        'NM_PROJETO': '',
                        'NM_STATUS': '',
                        'TX_UNIDADES': '',
                        'ESCOLA': '',
                        'ID_INSCRICAO': '',
                        'ID_ALUNO': '',
                        'NM_ALUNO': '',
                        'CPF_PASSAPORTE': '',
                        'DT_NASCIMENTO': '',
                        'TP_SEXO': '',
                        'ESTADO': '',
                        'TX_TP_STATUS': '',
                        'DT_PROJETO_INICIO': '',
                        'DT_PROJETO_FIM': ''}
        status_alunos_dados = {"dados": []}
        dados_internos = {"edicao": "", "trilha": "", "alunos": []}
        dados_aluno = {'Número da Inscrição': '',
                       'Matrícula da Extensão': '',
                       'Nome do Aluno': '',
                       'Grau': '',
                       'Freqüência Total': '',
                       'Avaliação Final': '',
                       'Situação': '',
                       'Data de Solicitação de Certificado': '',
                       'Situação do Certificado': ''}
        base_total = {"dados": []}
        total_interno = {"Nome estudante": '',
                  "CPF": '',
                  "Gênero": '',
                  "Data de nascimento": '',
                  "Escolaridade": '',
                  "Estado": '',
                  "Status do estudante": '',
                  "Número/Edição": '',
                  "Trilha": '',
                  "Nível da trilha": '',
                  "Modalide": '',
                  "Parceiro": '',
                  "Afirmativa": '',
                  "Acessível": '',
                  "Área TIC": '',
                  "Área ACM": '',
                  "Executora": ''}
        if uploaded_files != []:
            for uploaded_file in uploaded_files:
                if uploaded_file.name == "TRILHAS_DICT.csv":
                    # st.write(uploaded_file.name)
                    df = pd.read_csv(uploaded_file)
                    # st.write(df.columns.tolist())
                    col = df.columns.tolist()
                    cols = col[0].split(';')
                    for item in df.values.tolist():
                        teste = {}
                        items = item[0].split(';')
                        for keys,_items in zip(cols,items):
                            teste[keys] = _items
                        teste_total["dados"].append(teste)
                    # st.write(teste_total)
                elif uploaded_file.name == "BASE_SIPROEX_MOODLE.csv":
                    # st.write(uploaded_file.name)
                    df = pd.read_csv(uploaded_file, delimiter=';')
                    for item in df.values.tolist():
                        aux_base = base_interna.copy()
                        for keys, items in zip(base_interna, item):
                            if pd.isna(items):
                                aux_base[keys] = "Não Informado"
                            else:
                                aux_base[keys] = items
                        base_dados["dados"].append(aux_base)
                    # st.write(base_dados)
                else:
                    # st.write(uploaded_file.name)
                    df = pd.read_csv(uploaded_file, delimiter=';')
                    aux_dados_internos = dados_internos.copy()
                    aux_dados_internos["edicao"] = uploaded_file.name.split("_")[1].replace(".csv", "")
                    # st.write([x for x in teste_total["dados"] if x["Turma"] == aux_dados_internos["edicao"]])
                    # st.markdown("---")
                    # st.write(teste_total["dados"])
                    aux_dados_internos["trilha"] = [x for x in teste_total["dados"] if x["Turma"] == aux_dados_internos["edicao"]][0]["Nome da Trilha"]
                    for item in df.values.tolist():
                        aux_aluno = dados_aluno.copy()
                        for keys, items in zip(dados_aluno.keys(),item):                            
                            if pd.isna(items):
                                aux_aluno[keys] = "Não Informado"
                            else:
                                aux_aluno[keys] = items
                        aux_dados_internos['alunos'].append(aux_aluno)
                    status_alunos_dados["dados"].append(aux_dados_internos)
                    # st.write(aux_dados_internos)
                # bytes_data = uploaded_file.read()
                # st.write("filename:", uploaded_file.name)
                # content = io.StringIO(bytes_data.decode('utf-8'))
                # csv_reader = csv.reader(content)
                # data_list = list(csv_reader)
                # # Aqui você pode processar os dados conforme necessário
                # st.write("Data from uploaded file:", data_list)
            # aux_dados_internos['alunos'][0]["Matrícula da Extensão"]
            # for item in base_dados["dados"]:
            for items in base_dados["dados"]:
                aux_aluno = total_interno.copy()
                for status_item in status_alunos_dados["dados"]:
                    for aluno in status_item['alunos']:
                        if aluno["Matrícula da Extensão"] == items["ID_ALUNO"]:
                            trilha = [x for x in teste_total["dados"] if int(items["ID_PROJETO"]) == int(x["Turma"])][0]
                            aux_aluno["Nome estudante"] = aluno["Nome do Aluno"]
                            aux_aluno["CPF"] = items["CPF_PASSAPORTE"]
                            aux_aluno["Gênero"] = items["TP_SEXO"]
                            aux_aluno["Data de nascimento"] = items["DT_NASCIMENTO"]
                            aux_aluno["Escolaridade"] = aluno["Grau"]
                            aux_aluno["Estado"] = items["ESTADO"]
                            aux_aluno["Status do estudante"] = aluno["Avaliação Final"] if aluno["Avaliação Final"] != "Não Informado" else "Em andamento"
                            aux_aluno["Nível da trilha"] = trilha["Nível"]
                            aux_aluno["Modalide"] = trilha["Modalidade"]
                            if trilha != []:
                                aux_aluno["Trilha"] = trilha["Nome da Trilha"]
                                aux_aluno["Parceiro"] = trilha["Parceiro"]
                                aux_aluno["Número/Edição"] = trilha["Turma"]
                            aux_aluno["Afirmativa"] = trilha["Afirmativa"]
                            aux_aluno["Acessível"] = trilha["Acessível"]
                            aux_aluno["Área TIC"] = trilha["Área TIC"]
                            aux_aluno["Área ACM"] = trilha["Área ACM"]
                            aux_aluno["Executora"] = trilha["Executora"]
                            break
                if aux_aluno["Nome estudante"] != "":
                    base_total["dados"].append(aux_aluno)
            # for status_item in status_alunos_dados["dados"]:
            #     for aluno in status_item['alunos']:
            #         # st.write([item for item in base_dados["dados"] if item["ID_ALUNO"] == aluno["Matrícula da Extensão"]])
            #         item_da_base = [item for item in base_dados["dados"] if item["ID_ALUNO"] == aluno["Matrícula da Extensão"]]
            #         # st.write(item_da_base)
            #         for items in item_da_base:
            #             if aluno["Matrícula da Extensão"] == items["ID_ALUNO"]:
            #                 aux_aluno = total_interno.copy()
            #                 # print(aluno["Nome do Aluno"])
            #                 trilha = [x for x in teste_total["dados"] if int(items["ID_PROJETO"]) == int(x["Turma"])][0]
            #                 aux_aluno["Nome estudante"] = aluno["Nome do Aluno"]
            #                 aux_aluno["CPF"] = items["CPF_PASSAPORTE"]
            #                 aux_aluno["Gênero"] = items["TP_SEXO"]
            #                 aux_aluno["Data de nascimento"] = items["DT_NASCIMENTO"]
            #                 aux_aluno["Escolaridade"] = aluno["Grau"]
            #                 aux_aluno["Estado"] = items["ESTADO"]
            #                 aux_aluno["Status do estudante"] = aluno["Avaliação Final"] if aluno["Avaliação Final"] != "Não Informado" else "Em andamento"
            #                 aux_aluno["Nível da trilha"] = trilha["Nível"]
            #                 aux_aluno["Modalide"] = trilha["Modalidade"]
            #                 if trilha != []:
            #                     aux_aluno["Trilha"] = trilha["Nome da Trilha"]
            #                     aux_aluno["Parceiro"] = trilha["Parceiro"]
            #                     aux_aluno["Número/Edição"] = trilha["Turma"]
            #                 aux_aluno["Afirmativa"] = trilha["Afirmativa"]
            #                 aux_aluno["Acessível"] = trilha["Acessível"]
            #                 aux_aluno["Área TIC"] = trilha["Área TIC"]
            #                 aux_aluno["Área ACM"] = trilha["Área ACM"]
            #                 aux_aluno["Executora"] = trilha["Executora"]
            #                 base_total["dados"].append(aux_aluno)
                            # st.write(f"Aluno encontrado: {item['NM_ALUNO']} - {item['ID_ALUNO']} - {item['NM_PROJETO']}")
                # print(e)
            # st.write(base_total)
            df_t = pd.DataFrame(base_total["dados"])
            csv_buffer = io.StringIO()
            df_t.to_csv(csv_buffer, index=False)
            teste_csv_data_download = csv_buffer.getvalue()
            st.download_button('TESTE', teste_csv_data_download, file_name='base_total.csv', mime='text/csv')
        else:
            st.warning("Please upload a CSV file.")

    def upload_button_moodle(self, uploaded_files):
        '''Função de tratamento dos arquivos CSV após upload'''
        file_datas_flag = False
        file_notas_flag = False

        teste = TRILHAS_DICT.copy()
        for key,value in teste.items():
            value = {'nome': value, 'file_datas_flag': file_datas_flag, 'file_notas_flag': file_notas_flag}
            teste[key] = value

        if uploaded_files != []:
            for uploaded_file in uploaded_files:
                aux = [x for x in teste.keys() if x in uploaded_file.name]
                if aux != []:
                    if len(uploaded_file.name.split("_")) > 3:
                        teste[aux[0]]["file_notas_flag"] = True
                    elif len(uploaded_file.name.split("_")) == 3:
                        teste[aux[0]]["file_datas_flag"] = True
                    st.success("Arquivo correto! " + uploaded_file.name.split("_")[0])
                    st.write(teste)
                else:
                    st.error("Arquivo incorreto! Por favor, verifique o nome do arquivo.")
                # bytes_data = uploaded_file.read()
                # st.write("filename:", uploaded_file.name)
                # content = io.StringIO(bytes_data.decode('utf-8'))
                # csv_reader = csv.reader(content)
                # data_list = list(csv_reader) 
        else:
            st.warning("Please upload a CSV file.")
             
    def upload_button(self, uploaded_files):
        '''Função de tratamento dos arquivos CSV após upload'''
        total_type = {"data": []}
        unico_type = {"data": []}
        
        if uploaded_files != []:
            for uploaded_file in uploaded_files:
                bytes_data = uploaded_file.read()
                st.write("filename:", uploaded_file.name)
                content = io.StringIO(bytes_data.decode('utf-8'))
                csv_reader = csv.reader(content)
                data_list = list(csv_reader)
                # st.write("Data from uploaded file:", data_list)
                # print(uploaded_file._file_urls.upload_url)
                certificate_only, unique_cpf = self.certificate_file_analisys(data_list)
                # st.write(f"Quantidade de certificados emitidos: {certificate_only}")
                # st.write(f"Quantidade de pessoas únicas certificadas na plataforma Canvas: {unique_cpf}")
                
                total_type["data"].append({"dia": uploaded_file.name.split("_")[0], "qnt": certificate_only, "type": "T"})
                unico_type["data"].append({"dia": uploaded_file.name.split("_")[0], "qnt": unique_cpf, "type": "U"})

            self.send_data_certificate(total_type, unico_type)
        else:
            st.warning("Please upload a CSV file.")

    def get_data_social_media(self):
        '''Função para pegar os dados do MongoDB da Rede Social'''
        data = st.session_state.collection_social.find()
        print(data)
        ano = []
        mes = []
        dados = []
        for item in data:
            if item.get('ano') not in ano:
                ano.append(item.get('ano'))
            if item.get('mes') not in mes:
                mes.append(item.get('mes'))
            dados.append(item)
        st.session_state.social_media_mongo = dados
        return ano, mes

if __name__ == "__main__":

    app = App()
    app.run()