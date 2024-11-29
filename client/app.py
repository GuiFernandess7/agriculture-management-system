import os
import psycopg2
import streamlit as st
import geopandas as gpd
from shapely import wkt
import pandas as pd
from streamlit_folium import folium_static
import folium

if 'field_selected' not in st.session_state:
    st.session_state.field_selected = None

st.set_page_config(
    page_title="AgriTrack",
    page_icon="https://cdn-icons-png.flaticon.com/512/2516/2516640.png",
    layout="wide",
    initial_sidebar_state="expanded",
)

with st.sidebar:
    st.title("AgriTrack")
    st.image("https://cdn-icons-png.flaticon.com/512/2516/2516640.png", width=90)

POSTGRES_HOST = os.getenv('POSTGRES_HOST', 'db')
POSTGRES_DB = os.getenv('POSTGRES_DB', 'mydb')
POSTGRES_USER = os.getenv('POSTGRES_USER', 'user')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD', 'password')
TABLE_NAME = f"core_field"

def get_db_connection():
    conn = psycopg2.connect(
        host=POSTGRES_HOST,
        dbname=POSTGRES_DB,
        user=POSTGRES_USER,
        password=POSTGRES_PASSWORD
    )
    return conn

query = f"""
SELECT id, name, ST_AsText(location) AS point, lat, lon, soil_type, area
FROM {TABLE_NAME}
"""

conn = get_db_connection()

df = pd.read_sql(query, conn)

conn.close()

gdf = gpd.GeoDataFrame(df, geometry=gpd.GeoSeries.from_wkt(df['point']))

gdf.set_crs('EPSG:4326', allow_override=True, inplace=True)

gdf = gdf.to_crs(epsg=4326)

def generate_map(gdf, field_name: str):
    field = gdf[gdf['name'] == field_name].iloc[0]
    m = folium.Map(location=[field.geometry.centroid.y, field.geometry.centroid.x], zoom_start=12)

    folium.TileLayer(
        tiles='https://mt1.google.com/vt/lyrs=s&x={x}&y={y}&z={z}',
        attr='Google',
        name='Google Satellite',
        overlay=False,
        control=True
    ).add_to(m)
    folium.GeoJson(field.geometry).add_to(m)

    folium.Marker(
        location=[field.geometry.centroid.y, field.geometry.centroid.x],
        popup=f"ID: {field['id']}, Nome: {field['name']}"
    ).add_to(m)

    st.components.v1.html(m._repr_html_(), height=600)

with st.sidebar:
    form = st.form(key='main-form')
    form.markdown("## Menu")
    st.session_state.field_selected = form.selectbox(label="Terrenos", options=list(gdf["name"]))
    form.form_submit_button("Acessar")

if st.session_state.field_selected is not None:
    generate_map(gdf, st.session_state.field_selected)

""" def fetch_data():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM {TABLE_NAME} LIMIT 10;")
    rows = cur.fetchall()
    conn.close()
    return rows

st.title('Exemplo de Conexão com o Banco de Dados')
data = fetch_data()

st.write('Dados do Banco:')
st.write(data)
"""

""" SELECT table_name
FROM information_schema.tables
WHERE table_schema = 'public'
ORDER BY table_name; """

"""
docker-compose down   # Para parar e remover containers antigos
docker-compose build  # Para reconstruir as imagens
docker-compose up     # Para subir os containers novamente

"""