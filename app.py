from dash import Dash, html, dcc
from dash.dependencies import Input, Output
import dash_leaflet as dl  
import dash_leaflet.express as dlx  
import pandas as pd
import geopandas as gpd
import json
from dash_iconify import DashIconify
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

tile_url='https://stamen-tiles-{s}.a.ssl.fastly.net/toner-background/{z}/{x}/{y}{r}.png'
tile_attr='Map tiles by <a href="http://stamen.com">Stamen Design</a>, <a href="http://creativecommons.org/licenses/by/3.0">CC BY 3.0</a> &mdash; Map data &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'

shapes_file='tidy_data/son_shapes.parquet'
son_EDU_file='tidy_data/son_EDU.parquet'
son_EDU_tasa_file='tidy_data/son_EDU_tasa.parquet'
shapes_gdf=gpd.read_parquet(shapes_file)
edu_df=pd.read_parquet(son_EDU_file)
eduT_df=pd.read_parquet(son_EDU_tasa_file)

# DASH CORE COMPONENTS #
map_tab=dcc.Tab(
                label='Mapa',
                value='map_tab',
                style={'color':'#DCD7C9', 'background-color':'#3F4E4F','border-color':'#3F4E4F','font-size':'120%'},
                selected_style={'color':'#DCD7C9', 'background-color':'#2C3639','border-color':'#2C3639','margin-top':'0', 'font-size':'120%'}
)

plot_tab=dcc.Tab(
                label='Gráfica',
                value='plot_tab',
                style={'color':'#DCD7C9', 'background-color':'#3F4E4F','border-color':'#3F4E4F', 'font-size':'120%'},
                selected_style={'color':'#DCD7C9', 'background-color':'#2C3639','border-color':'#2C3639','margin-top':'0', 'font-size':'120%'}
)

info_tab=dcc.Tab(
                label='Información',
                value='info_tab',
                style={'color':'#DCD7C9', 'background-color':'#3F4E4F','border-color':'#3F4E4F', 'font-size':'120%'},
                selected_style={'color':'#DCD7C9', 'background-color':'#2C3639','border-color':'#2C3639','margin-top':'0', 'font-size':'120%'}
)

son_ddown=dcc.Dropdown(id='son_dropdown', className='dropdown',
    options=np.append(['Todos los municipios'],shapes_gdf.NOMBRE.unique()),
    value='Todos los municipios',
    searchable=False, clearable=False,

)

del_ddown=dcc.Dropdown(id='del_dropdown', className='dropdown',
    options=[
        {'label': 'Todos los delitos', 'value': 'TOT'},
        {'label': 'La vida y la Integridad corporal', 'value': 'DE_VI'},
        {'label': 'Libertad personal', 'value': 'DE_LP'},
        {'label': 'La libertad y la seguridad sexual', 'value': 'DE_LS'},
        {'label': 'El patrimonio', 'value': 'DE_PA'},
        {'label': 'La familia', 'value': 'DE_FA'},
        {'label': 'La sociedad', 'value': 'DE_SO'},
        {'label': 'Otros bienes jurídicos afectados', 'value': 'DE_BJ'}],
    searchable=False,
    placeholder='Seleccione un delito'
)

son_radio=dcc.Checklist(id='son_check',   className='son_check',
   options=[{'label': 'Unidades Económicas Educativas', 'value': 'EDU'},
        {'label': 'Crimenes', 'value': 'DE'}],
   value=['EDU'],
   labelStyle={'display': 'block'},
   inline=False,
)

agno_slider=dcc.Slider(id='agno_slider', className='slider',
    min=2015, max=2020, step=1,
    marks={
        2015: {'label': '2015','style': {'color': '#DCD7C9', 'font-size': '120%', 'font-weight': 'bold'}},
        2016: {'label': '2016','style': {'color': '#DCD7C9', 'font-size': '120%', 'font-weight': 'bold'}},
        2017: {'label': '2017','style': {'color': '#DCD7C9', 'font-size': '120%', 'font-weight': 'bold'}},
        2018: {'label': '2018','style': {'color': '#DCD7C9', 'font-size': '120%', 'font-weight': 'bold'}},
        2019: {'label': '2019','style': {'color': '#DCD7C9', 'font-size': '120%', 'font-weight': 'bold'}},
        2020: {'label': '2020','style': {'color': '#DCD7C9', 'font-size': '120%', 'font-weight': 'bold'}},
    },
    value=2015
)

plot=html.Div([
            html.H2('Tab content 2')
])

info=html.Div([
            html.H2('Tab content 3')
])

# DASH LEAFLET COMPONENTS #

ue_grad={273.57:'#2887A1', 244.90:'#4694A8', 216.22:'#64A2AE', 187.55:'#82AFB5',
    158.88:'#A0BCBC', 130.21:'#BECAC2', 101.53:'#DCD7C9'}

del_grad={764.74:'#A14228', 655.49:'#AB5B43', 546.24:'#B5745E', 436.99:'#BE8D78',
    327.75:'#C8A593', 218.5:'#D2BEAE', 109.25:'#DCD7C9'}

map=dl.Map([],
    #center=[29.68770,-110.80995],
    zoomSnap=0.1, zoom=6.3,
    zoomControl=False, doubleClickZoom=False,
    dragging=False, scrollWheelZoom=False,
    attributionControl=False
)

edu_colorbar = dl.Colorbar(classes=(5,10,15,20,25,30,35,40),
                       colorscale=('#DCD7C9','#BECAC2','#A0BCBC','#82AFB5','#64A2AE','#4694A8','#2887A1'),
                       tickValues=(10,15,20,25,30,35),
                       tickText=('101.53', '130.21', '158.88', '187.55', '216.22', '244.90', '273.57'),
                       width=400, height=30, position='topright', min=5, max=40,
                       className='colorbar')

del_colorbar = dl.Colorbar(classes=(5,10,15,20,25,30,35,40),
                       colorscale=('#DCD7C9','#D2BEAE','#C8A593','#BE8D78','#B5745E','#AB5B43','#A14228'),
                       tickValues=(10,15,20,25,30,35),
                       tickText=('109.25', '218.50', '327.75', '436.99', '546.24', '655.49', '764.74'),
                       width=400, height=30, position='topright', min=5, max=40,
                       className='colorbar')

app=Dash(__name__)

app.layout = html.Div([

    html.Div([
        DashIconify(icon='emojione-monotone:desert', inline=False, width=80, className='icon'),
        html.H1(children='EDUCACIÓN EN SONORA')
    ], className='top_bar'),
    
    html.Div([
        dcc.Tabs(
            id='tabs_container',
            value='map_tab',
            parent_className='tabs_div',
            className='tabs_container',
            children=[
                map_tab,
                plot_tab,
                info_tab,
            ],
        ),
        ]),
 
    html.Div([],id='tabs_content', className='map_div'),

    html.Div([
        agno_slider,
    ], className='slider_div'),

    html.Div([
    ], id='son_info_div', className='son_info_div'),

    html.Div([
        html.H3(children='SONORA')
    ], className='footer'),

    html.Div([
        DashIconify(icon='mdi:police-badge', width=40, className='dd_icon'),
        html.P('Delitos por bien juridico afectado', className='dd_label'),
        del_ddown
    ], className='del_ddown_div'),

    html.Div([
        DashIconify(icon='mdi:map-marker', width=40, className='dd_icon'),
        html.P('Municipios de Sonora', className='dd_label'),
        son_ddown
    ], className='son_ddown_div'),

])

@app.callback(Output('tabs_content', 'children'),
              Input('tabs_container', 'value'),
              Input('agno_slider', 'value'),
              Input('son_dropdown', 'value'),
              Input('del_dropdown', 'value'),
              )

def render_content(tab, agno, son, dels):
    if tab == 'map_tab':
        df=shapes_gdf.merge(eduT_df[eduT_df['FECHA']==str(agno)], on='ID', how='outer')
        df['TOT']=df.loc[:,'DE_PA':'DE_BJ'].sum(axis=1)
        if dels==None:
            map.children=[dl.TileLayer(url=tile_url), edu_colorbar]
            grad=ue_grad
            feat='UE_EDU'
        else:
            map.children=[dl.TileLayer(url=tile_url), del_colorbar]
            grad=del_grad
            feat=dels
        for idx, row in df.iterrows():
            for key in grad:
                if row[feat] < key:
                    fill_color=grad[key]
            style={'fill': True,
                    'fillColor': fill_color,
                    'fillOpacity':1.0,
                    'color':'#3F4E4F',
                    'weight':2}
            map.children.append(dl.GeoJSON(data=json.loads(shapes_gdf[shapes_gdf['ID']==row.ID].to_json()),
                        options=dict(style=style)))        
        if son=='Todos los municipios':
            map.zoom=6.3
            map.center=[29.68770,-110.80995]
        else:
            polgn=df[df['NOMBRE']==son].reset_index().loc[0,'geometry']
            map.center=polgn.centroid.y, polgn.centroid.x,
            map.zoom=8          
        return map, 
    
    elif tab == 'plot_tab':
        df=edu_df.merge(shapes_gdf[['ID','NOMBRE']], on='ID', how='outer')
        df['TOT']=df.loc[:,'DE_PA':'DE_BJ'].sum(axis=1)
        if son=='Todos los municipios':
            df=df.groupby(by=['FECHA']).sum().reset_index()
        else:
            df=df[df['NOMBRE']==son]
        fig = px.area(df, x='FECHA', y='UE_EDU')#, marker=dict(color='black'))#, color='#A14228'
        if dels != None:
            fig.add_trace(go.Scatter(x=df['FECHA'], y=df[dels], mode='lines'))
        return dcc.Graph(figure=fig)
    elif tab == 'info_tab':
        return info

@app.callback(Output('son_info_div', 'children'),
              Input('agno_slider', 'value'),
              Input('son_dropdown', 'value'),
              Input('del_dropdown', 'value'))
def render_info(agno, son, delito):
    title=f'{son} - {agno}'
    #ue=0
    #por cada 100 000 habitantes \nDelito \ndelitos por cada 100 000 habitantes'
    return html.P(title)

if __name__ == '__main__':
    app.run_server(debug=True)