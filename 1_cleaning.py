import os
import pandas as pd
import geopandas as gpd

raw_geoshapes_file='datasets/geo_shapes/26/municipal.shp'

raw_denue15_file='datasets/denue2015/DENUE_INEGI_26_.csv'
raw_denue16_file='datasets/denue2016/denue_26_csv/conjunto_de_datos/denue_inegi_26_.csv'
raw_denue17_file='datasets/denue2017/denue_26_csv/conjunto_de_datos/denue_inegi_26_.csv'
raw_denue18_file='datasets/denue2018/conjunto_de_datos/denue_inegi_26_.csv'
raw_denue19_file='datasets/denue2019/conjunto_de_datos/denue_inegi_26_.csv'
raw_denue20_file='datasets/denue2020/conjunto_de_datos/denue_inegi_26_.csv'
raw_denue21_file='datasets/denue2021/conjunto_de_datos/denue_inegi_26_.csv'

raw_crimen15_file='datasets/crimen_SESNSP/Municipal-Delitos-2015-2022_sep2022/2015.xlsx'
raw_crimen16_file='datasets/crimen_SESNSP/Municipal-Delitos-2015-2022_sep2022/2016.xlsx'
raw_crimen17_file='datasets/crimen_SESNSP/Municipal-Delitos-2015-2022_sep2022/2017.xlsx'
raw_crimen18_file='datasets/crimen_SESNSP/Municipal-Delitos-2015-2022_sep2022/2018.xlsx'
raw_crimen19_file='datasets/crimen_SESNSP/Municipal-Delitos-2015-2022_sep2022/2019.xlsx'
raw_crimen20_file='datasets/crimen_SESNSP/Municipal-Delitos-2015-2022_sep2022/2020.xlsx'
raw_crimen21_file='datasets/crimen_SESNSP/Municipal-Delitos-2015-2022_sep2022/2021.xlsx'

shapes_gdframe=gpd.read_file(raw_geoshapes_file)
shapes_gdframe=shapes_gdframe[['CVEGEO','NOMBRE','geometry']]
shapes_gdframe['CVEGEO']=shapes_gdframe['CVEGEO'].astype('int64')-26000

def cleaning_raw_denue(df,year):
    df_op=df.copy(deep=True)
    if year == '2015':
        df_op=df_op[['Código de la clase de actividad SCIAN','Clave municipio']]
        df_op.rename(columns={'Código de la clase de actividad SCIAN':'COD_ACT',
            'Clave municipio':'CVE_MUN'}, inplace=True)
    else:
        df_op=df_op[['codigo_act','cve_mun']]
        df_op.rename(columns={'codigo_act':'COD_ACT',
            'cve_mun':'CVE_MUN'}, inplace=True)
    
    df_op[year]=1
    df_op['COD_ACT']=df_op['COD_ACT'].astype(str).str.replace('^11....','11',regex=True)
    df_op['COD_ACT']=df_op['COD_ACT'].astype(str).str.replace('^21....','21',regex=True)
    df_op['COD_ACT']=df_op['COD_ACT'].astype(str).str.replace('^22....','22',regex=True)
    df_op['COD_ACT']=df_op['COD_ACT'].astype(str).str.replace('^23....','23',regex=True)
    df_op['COD_ACT']=df_op['COD_ACT'].astype(str).str.replace('^31....','31',regex=True)
    df_op['COD_ACT']=df_op['COD_ACT'].astype(str).str.replace('^3[1-3]....','31',regex=True)
    df_op['COD_ACT']=df_op['COD_ACT'].astype(str).str.replace('^43....','43',regex=True)
    df_op['COD_ACT']=df_op['COD_ACT'].astype(str).str.replace('^46....','46',regex=True)
    df_op['COD_ACT']=df_op['COD_ACT'].astype(str).str.replace('^4[8-9]....','48',regex=True)
    df_op['COD_ACT']=df_op['COD_ACT'].astype(str).str.replace('^51....','51',regex=True)
    df_op['COD_ACT']=df_op['COD_ACT'].astype(str).str.replace('^52....','52',regex=True)
    df_op['COD_ACT']=df_op['COD_ACT'].astype(str).str.replace('^53....','53',regex=True)
    df_op['COD_ACT']=df_op['COD_ACT'].astype(str).str.replace('^54....','54',regex=True)
    df_op['COD_ACT']=df_op['COD_ACT'].astype(str).str.replace('^55....','55',regex=True)
    df_op['COD_ACT']=df_op['COD_ACT'].astype(str).str.replace('^56....','56',regex=True)
    df_op['COD_ACT']=df_op['COD_ACT'].astype(str).str.replace('^61....','61',regex=True)
    df_op['COD_ACT']=df_op['COD_ACT'].astype(str).str.replace('^62....','62',regex=True)
    df_op['COD_ACT']=df_op['COD_ACT'].astype(str).str.replace('^71....','71',regex=True)
    df_op['COD_ACT']=df_op['COD_ACT'].astype(str).str.replace('^72....','72',regex=True)
    df_op['COD_ACT']=df_op['COD_ACT'].astype(str).str.replace('^81....','81',regex=True)
    df_op['COD_ACT']=df_op['COD_ACT'].astype(str).str.replace('^93....','93',regex=True)

    df_op=df_op.groupby(by=['CVE_MUN','COD_ACT']).sum().rename_axis(columns = None).reset_index()
    
    return df_op

def cleaning_raw_crimen(df,year):
    df_op=df.copy(deep=True)
    df_op=df_op[df_op['Entidad']=='Sonora']
    df_op=df_op[df_op['Municipio']!='No Especificado']
    df_op=df_op[df_op['Municipio']!='Otros Municipios']
    df_op[year]=df_op[['Enero','Febrero','Marzo','Abril','Mayo','Junio','Julio','Agosto','Septiembre',
        'Octubre','Noviembre','Diciembre']].sum(axis=1)
    df_op=df_op[['Cve. Municipio','Tipo de delito',year]]
    df_op['Cve. Municipio']=df_op['Cve. Municipio']-26000
    df_op.rename(columns={'Cve. Municipio':'CVE_MUN',
                            'Tipo de delito':'DELITO'}, inplace=True)
    df_op=df_op.groupby(by=['CVE_MUN','DELITO']).sum().rename_axis(columns = None).reset_index()
    return df_op

def joining_dframes(df_15,df_16,df_17,df_18,df_19,df_20,df_21,tema):
    if tema == 'denue':
        tidy_df=df_15.merge(df_16, how='outer',on=['CVE_MUN','COD_ACT'])
        tidy_df=tidy_df.merge(df_17, how='outer',on=['CVE_MUN','COD_ACT'])
        tidy_df=tidy_df.merge(df_18, how='outer',on=['CVE_MUN','COD_ACT'])
        tidy_df=tidy_df.merge(df_19, how='outer',on=['CVE_MUN','COD_ACT'])
        tidy_df=tidy_df.merge(df_20, how='outer',on=['CVE_MUN','COD_ACT'])
        tidy_df=tidy_df.merge(df_21, how='outer',on=['CVE_MUN','COD_ACT'])
    else:
        tidy_df=df_15.merge(df_16, how='outer',on=['CVE_MUN','DELITO'])
        tidy_df=tidy_df.merge(df_17, how='outer',on=['CVE_MUN','DELITO'])
        tidy_df=tidy_df.merge(df_18, how='outer',on=['CVE_MUN','DELITO'])
        tidy_df=tidy_df.merge(df_19, how='outer',on=['CVE_MUN','DELITO'])
        tidy_df=tidy_df.merge(df_20, how='outer',on=['CVE_MUN','DELITO'])
        tidy_df=tidy_df.merge(df_21, how='outer',on=['CVE_MUN','DELITO'])
    tidy_df.fillna(value=0,inplace=True)
    tidy_df[['2015','2016','2017','2018','2019','2020','2021']]=tidy_df[['2015','2016','2017','2018','2019','2020','2021']].astype('int64')
    return tidy_df

def tidier(df,tema):
    if tema == 'crimen':
        df_op=df.pivot(index='CVE_MUN',columns='DELITO',values=['2015','2016','2017','2018','2019','2020','2021'])
        df_op=df_op.sort_index(axis=1, level=1)
        df_op.columns=[f'{delito}_{anio}' for anio,delito in df_op.columns]
    elif tema == 'denue':
        df_op=df.pivot(index='CVE_MUN',columns='COD_ACT',values=['2015','2016','2017','2018','2019','2020','2021'])
        df_op=df_op.sort_index(axis=1, level=1)
        df_op.columns=[f'{cod_act}_{anio}' for anio,cod_act in df_op.columns]
    df_op = df_op.reset_index()
    return df_op

denue15_dframe=cleaning_raw_denue(pd.read_csv(raw_denue15_file),'2015')
denue16_dframe=cleaning_raw_denue(pd.read_csv(raw_denue16_file),'2016')
denue17_dframe=cleaning_raw_denue(pd.read_csv(raw_denue17_file),'2017')
denue18_dframe=cleaning_raw_denue(pd.read_csv(raw_denue18_file),'2018')
denue19_dframe=cleaning_raw_denue(pd.read_csv(raw_denue19_file,encoding='latin-1'),'2019')
denue20_dframe=cleaning_raw_denue(pd.read_csv(raw_denue20_file,encoding='latin-1'),'2020')
denue21_dframe=cleaning_raw_denue(pd.read_csv(raw_denue21_file,encoding='latin-1'),'2021')

crimen15_dframe=cleaning_raw_crimen(pd.read_excel(raw_crimen15_file),'2015')
crimen16_dframe=cleaning_raw_crimen(pd.read_excel(raw_crimen16_file),'2016')
crimen17_dframe=cleaning_raw_crimen(pd.read_excel(raw_crimen17_file),'2017')
crimen18_dframe=cleaning_raw_crimen(pd.read_excel(raw_crimen18_file),'2018')
crimen19_dframe=cleaning_raw_crimen(pd.read_excel(raw_crimen19_file),'2019')
crimen20_dframe=cleaning_raw_crimen(pd.read_excel(raw_crimen20_file),'2020')
crimen21_dframe=cleaning_raw_crimen(pd.read_excel(raw_crimen21_file),'2021')

denue_dframe=joining_dframes(denue15_dframe,denue16_dframe,denue17_dframe,
    denue18_dframe,denue19_dframe,denue20_dframe,denue21_dframe,'denue')
crimen_dframe=joining_dframes(crimen15_dframe,crimen16_dframe,crimen17_dframe,
    crimen18_dframe,crimen19_dframe,crimen20_dframe,crimen21_dframe,'crimen')

tidy_denue_dframe=tidier(denue_dframe,'denue')
tidy_crimen_dframe=tidier(crimen_dframe,'crimen')

if not os.path.exists('tidy_datasets/'):
    os.makedirs('tidy_datasets/')
shapes_gdframe.to_parquet('tidy_datasets/shapes_gdframe.parquet',index=False)
tidy_denue_dframe.to_parquet('tidy_datasets/denue_dframe.parquet',index=False)
tidy_crimen_dframe.to_parquet('tidy_datasets/crimen_dframe.parquet',index=False)