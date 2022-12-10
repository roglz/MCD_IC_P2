import os
import urllib.request
import zipfile
import shutil
import datetime

# Diccionario con {NOMBRE}:{URL} de los datasets a descargar
files_dict={
    # Datos de georreferenciados de los territorios de Sonora.
    'geo_shp': 'https://www.inegi.org.mx/contenidos/masiva/indicadores/inv/2016/26_SCINCE_zip.zip',
    # Datos de población de Sonora [1920 - 2050]
    'pob_son': 'https://www.inegi.org.mx/contenidos/masiva/indicadores/temas/estructura/estructura_26_xlsx.zip',
    # Datos sobre las unidades económica [2015 - 2020]
    'denue15': 'https://www.inegi.org.mx/contenidos/masiva/denue/2015/denue_26_25022015_csv.zip',
    'denue16': 'https://www.inegi.org.mx/contenidos/masiva/denue/2016_10/denue_26_1016_csv.zip',
    'denue17': 'https://www.inegi.org.mx/contenidos/masiva/denue/2017_11/denue_26_1117_csv.zip',
    'denue18': 'https://www.inegi.org.mx/contenidos/masiva/denue/2018_11/denue_26_1118_csv.zip',
    'denue19': 'https://www.inegi.org.mx/contenidos/masiva/denue/2019_11/denue_26_1119_csv.zip',
    'denue20': 'https://www.inegi.org.mx/contenidos/masiva/denue/2020_11/denue_26_1120_csv.zip',
    # Datos de incidencia delictiva en todos los municipios de México [2015-2022]
    'crimen_SESNSP':'https://drive.google.com/u/0/uc?id=1wzbzND3FR_-mUUaH3crre7MlswlLcDB5&export=down\
load&confirm=t&uuid=d0d45b18-6e74-440a-8acb-a46bd9db6146&at=ALAFpqzmlIuR3TqwOes80_SLwuZh:1667361872892'
}

# Verificación de mi existencia de archivos
if not os.path.exists('raw_data'):
    # Directorio de los raw datasets
    os.makedirs('raw_data')

if not os.path.exists('raw_data/zip_files/'):
    # Directorio de las descargas en zip
    os.makedirs('raw_data/zip_files/')

if not os.path.exists('tidy_data/'):
    # Directorio de los datasets limpios
    os.makedirs('tidy_data')

if not os.path.exists('tidy_data/metadata.txt'):
    # Archivo de matadata
    with open('tidy_data/metadata.txt', 'w') as f:
        f.write('Archivos sobre poblacion, unidades economicas, incidencia delictiva, y geometria de Sonora, Mexico.\n')
        f.write('Descargado el ' + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + '\n')
        info = """
      Los datos de poblacion corresponden al Censo de Poblacion y Vivienda (2010, 2015, 2020)
    realizado por INEGI, y cuenta con informacion sobre porcentajes de viviendas de los municipios 
    de Sonora, poblacion y algunas de sus caracteristicas demograficas, socioeconomicas y culturales.

      Los datos sobre unidades economicas corresponden al Directorio Estadístico Nacional de Unidades
    Economicas (2015-20219 realizado por INEGI.
            
      Los datos de incidencia delictiva por municipio de Mexico (2015-2020) son proporcionados por
    Secretariado Ejecutivo del Sistema Nacional de Seguridad Publica (SESNSP), y cuenta con
    informacion sobre de los registros por mes de los delitos: locacion, tipo de delito, subtipo,
    modalidad y bien juridico que afecta.
            
      Los datos georreferenciados de los territorios de Sonora corresponden al Inventario Nacional
    de Vivienda (INV) realizado por INEGI.
             
      Los datos de pobreza corresponden al Consejo Nacional de Evaluacion de la Politica de Desarrollo
    Social (CONEVAL) y fueron accedidos a traves de DataMexico. Corresponden a censos de 2010, 2015 y 2020.
            """
        f.write(info + '\n')
        f.write("Descargado el " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "\n")

# Descarga de los datos
for dataset in files_dict:
    if not os.path.exists('raw_data/zip_files/'+ dataset +'.zip'):
        urllib.request.urlretrieve(files_dict[dataset], 'raw_data/zip_files/'+ dataset +'.zip')
    # Registro del archivo en metadata
    with open('tidy_data/metadata.txt', 'a') as f:
        f.write('Nombre: '+ dataset +'\n')
        f.write('Desde: '+ files_dict[dataset] +'\n\n')
    #Extracción de los zip
    with zipfile.ZipFile('raw_data/zip_files/'+ dataset +'.zip', 'r') as zip_ref:
        if dataset=='geo_shp':
            zip_ref.extract(member='26/municipal.dbf', path='raw_data')
            zip_ref.extract(member='26/municipal.shp', path='raw_data')
            zip_ref.extract(member='26/municipal.prj', path='raw_data')
            zip_ref.extract(member='26/municipal.shx', path='raw_data')
            if not os.path.exists('raw_data/geo_shp/'):
                os.makedirs('raw_data/geo_shp/')
            os.replace('raw_data/26/municipal.dbf', 'raw_data/geo_shp/municipal.dbf')
            os.replace('raw_data/26/municipal.shp', 'raw_data/geo_shp/municipal.shp')
            os.replace('raw_data/26/municipal.prj', 'raw_data/geo_shp/municipal.prj')
            os.replace('raw_data/26/municipal.shx', 'raw_data/geo_shp/municipal.shx')
            os.rmdir('raw_data/26')
        
        elif dataset=='pob_son':
            zip_ref.extract(member='estructura_26.xlsx', path='raw_data')
            os.replace('raw_data/estructura_26.xlsx', f'raw_data/{dataset}.xlsx')
        
        elif dataset=='denue15':
            zip_ref.extract(member='DENUE_INEGI_26_.csv', path='raw_data')
            if not os.path.exists('raw_data/denue/'):
                os.makedirs('raw_data/denue/')
            os.replace('raw_data/DENUE_INEGI_26_.csv', f'raw_data/denue/{dataset}.csv')
        
        elif dataset=='denue16' or dataset=='denue17':
            zip_ref.extract(member='denue_26_csv/conjunto_de_datos/denue_inegi_26_.csv', path='raw_data')
            os.replace('raw_data/denue_26_csv/conjunto_de_datos/denue_inegi_26_.csv', f'raw_data/denue/{dataset}.csv')
            shutil.rmtree('raw_data/denue_26_csv')

        elif dataset=='denue18' or dataset=='denue19' or dataset=='denue20':
            zip_ref.extract(member='conjunto_de_datos/denue_inegi_26_.csv', path='raw_data')
            os.replace('raw_data/conjunto_de_datos/denue_inegi_26_.csv', f'raw_data/denue/{dataset}.csv')
            shutil.rmtree('raw_data/conjunto_de_datos')

        elif dataset=='crimen_SESNSP':
            if not os.path.exists('raw_data/delitos/'):
                os.makedirs('raw_data/delitos/')
            zip_ref.extract(member='Municipal-Delitos-2015-2022_sep2022/2015.xlsx', path='raw_data')
            zip_ref.extract(member='Municipal-Delitos-2015-2022_sep2022/2016.xlsx', path='raw_data')
            zip_ref.extract(member='Municipal-Delitos-2015-2022_sep2022/2017.xlsx', path='raw_data')
            zip_ref.extract(member='Municipal-Delitos-2015-2022_sep2022/2018.xlsx', path='raw_data')
            zip_ref.extract(member='Municipal-Delitos-2015-2022_sep2022/2019.xlsx', path='raw_data')
            zip_ref.extract(member='Municipal-Delitos-2015-2022_sep2022/2020.xlsx', path='raw_data')
            os.replace('raw_data/Municipal-Delitos-2015-2022_sep2022/2015.xlsx', 'raw_data/delitos/delitos15.xlsx')
            os.replace('raw_data/Municipal-Delitos-2015-2022_sep2022/2016.xlsx', 'raw_data/delitos/delitos16.xlsx')
            os.replace('raw_data/Municipal-Delitos-2015-2022_sep2022/2017.xlsx', 'raw_data/delitos/delitos17.xlsx')
            os.replace('raw_data/Municipal-Delitos-2015-2022_sep2022/2018.xlsx', 'raw_data/delitos/delitos18.xlsx')
            os.replace('raw_data/Municipal-Delitos-2015-2022_sep2022/2019.xlsx', 'raw_data/delitos/delitos19.xlsx')
            os.replace('raw_data/Municipal-Delitos-2015-2022_sep2022/2020.xlsx', 'raw_data/delitos/delitos20.xlsx')
            os.rmdir('raw_data/Municipal-Delitos-2015-2022_sep2022')