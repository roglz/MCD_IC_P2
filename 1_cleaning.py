import os
import pandas as pd
import geopandas as gpd

raw_geoshapes_file='datasets/geo_shapes/26/municipal.shp'

raw_pobl_file='datasets/poblacion/estructura_26.xlsx'

raw_denue15_file='datasets/denue2015/DENUE_INEGI_26_.csv'
raw_denue16_file='datasets/denue2016/denue_26_csv/conjunto_de_datos/denue_inegi_26_.csv'
raw_denue17_file='datasets/denue2017/denue_26_csv/conjunto_de_datos/denue_inegi_26_.csv'
raw_denue18_file='datasets/denue2018/conjunto_de_datos/denue_inegi_26_.csv'
raw_denue19_file='datasets/denue2019/conjunto_de_datos/denue_inegi_26_.csv'
raw_denue20_file='datasets/denue2020/conjunto_de_datos/denue_inegi_26_.csv'

raw_crimen15_file='datasets/crimen_SESNSP/Municipal-Delitos-2015-2022_sep2022/2015.xlsx'
raw_crimen16_file='datasets/crimen_SESNSP/Municipal-Delitos-2015-2022_sep2022/2016.xlsx'
raw_crimen17_file='datasets/crimen_SESNSP/Municipal-Delitos-2015-2022_sep2022/2017.xlsx'
raw_crimen18_file='datasets/crimen_SESNSP/Municipal-Delitos-2015-2022_sep2022/2018.xlsx'
raw_crimen19_file='datasets/crimen_SESNSP/Municipal-Delitos-2015-2022_sep2022/2019.xlsx'
raw_crimen20_file='datasets/crimen_SESNSP/Municipal-Delitos-2015-2022_sep2022/2020.xlsx'

cod_UE_dict={
    'Agropecuaria':'UE_AGRO',
    'Minería':'UE_MIN',
    'Enectricidad, agua y gas':'UE_ENE',
    'Construcción':'UE_CON',
    'Industrias manufactureras':'UE_MAN',
    'Comercio al por mayor':'UE_CMA',
    'Comercio al por menor':'UE_CME',
    'Transportes, correos y almacenamiento':'UE_TRA',
    'Medios masivos':'UE_MM',
    'Banca y seguros':'UE_BAN',
    'Servicios inmobiliarios':'UE_INM',
    'Servicios profesionales, científicos y técnicos':'UE_PCT',
    'Corporativos':'UE_COR',
    'Servicios de manejo de residuos y remediación':'UE_MRR',
    'Servicios educativos':'UE_EDU',
    'Servicios de salud':'UE_SAL',
    'Servicios recreativos':'UE_REC',
    'Servicios de alojamiento temporal y de preparación de alimentos':'UE_ATA',
    'Otros servicios':'UE_OSE',
    'Gubernamental':'UE_GUB'
}

cod_DE_dict={
    'La vida y la Integridad corporal':'DE_VI',
    'Libertad personal':'DE_LP',
    'La libertad y la seguridad sexual':'DE_LS',
    'El patrimonio':'DE_PA',
    'La familia':'DE_FA',
    'La sociedad':'DE_SO',
    'Otros bienes jurídicos afectados (del fuero común)':'DE_BJ'
}

shapes_gdframe=gpd.read_file(raw_geoshapes_file)
shapes_gdframe=shapes_gdframe[['CVEGEO','NOMBRE','geometry']]
shapes_gdframe.rename(columns={'CVEGEO':'ID'},inplace=True)

def raw_denue_cleaner(df,agno):
    df_op=df.copy(deep=True)
    if agno == '2015':
        df_op=df_op[['Código de la clase de actividad SCIAN','Clave municipio']]
        df_op.rename(columns={'Código de la clase de actividad SCIAN':'COD_ACT',
            'Clave municipio':'CVE_MUN'}, inplace=True)
    else:
        df_op=df_op[['codigo_act','cve_mun']]
        df_op.rename(columns={'codigo_act':'COD_ACT',
            'cve_mun':'CVE_MUN'}, inplace=True)

    df_op[agno]=1
    df_op['COD_ACT']=df_op['COD_ACT'].astype(str).str.replace('^11....','UE_AGRO',regex=True)
    df_op['COD_ACT']=df_op['COD_ACT'].astype(str).str.replace('^21....','UE_MIN',regex=True)
    df_op['COD_ACT']=df_op['COD_ACT'].astype(str).str.replace('^22....','UE_ENE',regex=True)
    df_op['COD_ACT']=df_op['COD_ACT'].astype(str).str.replace('^23....','UE_CON',regex=True)
    df_op['COD_ACT']=df_op['COD_ACT'].astype(str).str.replace('^3[1-3]....','UE_MAN',regex=True)
    df_op['COD_ACT']=df_op['COD_ACT'].astype(str).str.replace('^43....','UE_CMA',regex=True)
    df_op['COD_ACT']=df_op['COD_ACT'].astype(str).str.replace('^46....','UE_CME',regex=True)
    df_op['COD_ACT']=df_op['COD_ACT'].astype(str).str.replace('^4[8-9]....','UE_TRA',regex=True)
    df_op['COD_ACT']=df_op['COD_ACT'].astype(str).str.replace('^51....','UE_MM',regex=True)
    df_op['COD_ACT']=df_op['COD_ACT'].astype(str).str.replace('^52....','UE_BAN',regex=True)
    df_op['COD_ACT']=df_op['COD_ACT'].astype(str).str.replace('^53....','UE_INM',regex=True)
    df_op['COD_ACT']=df_op['COD_ACT'].astype(str).str.replace('^54....','UE_PCT',regex=True)
    df_op['COD_ACT']=df_op['COD_ACT'].astype(str).str.replace('^55....','UE_COR',regex=True)
    df_op['COD_ACT']=df_op['COD_ACT'].astype(str).str.replace('^56....','UE_MRR',regex=True)
    df_op['COD_ACT']=df_op['COD_ACT'].astype(str).str.replace('^61....','UE_EDU',regex=True)
    df_op['COD_ACT']=df_op['COD_ACT'].astype(str).str.replace('^62....','UE_SAL',regex=True)
    df_op['COD_ACT']=df_op['COD_ACT'].astype(str).str.replace('^71....','UE_REC',regex=True)
    df_op['COD_ACT']=df_op['COD_ACT'].astype(str).str.replace('^72....','UE_ATA',regex=True)
    df_op['COD_ACT']=df_op['COD_ACT'].astype(str).str.replace('^81....','UE_OSE',regex=True)
    df_op['COD_ACT']=df_op['COD_ACT'].astype(str).str.replace('^93....','UE_GUB',regex=True)

    df_op=df_op.groupby(by=['CVE_MUN','COD_ACT']).sum().rename_axis(columns = None).reset_index()
    df_op=df_op.pivot(index='CVE_MUN',columns='COD_ACT',values=agno).rename_axis(columns = None).reset_index()
    df_op.fillna(value=0,inplace=True)
    df_op.iloc[:,-20:]=df_op.iloc[:,-20:].astype('int64')
    df_op['AGNO']=agno
    df_op['CVE_MUN']=df_op['CVE_MUN']+26000
    df_op['CVE_MUN']=df_op['CVE_MUN'].astype(str)
    df_op.rename(columns={'CVE_MUN':'ID'},inplace=True)
    return df_op

def raw_crimen_cleaner(df,agno):
    df_op=df.copy(deep=True)
    df_op=df_op[df_op['Entidad']=='Sonora']
    df_op=df_op[df_op['Municipio']!='No Especificado']
    df_op=df_op[df_op['Municipio']!='Otros Municipios']
    df_op[agno]=df_op[['Enero','Febrero','Marzo','Abril','Mayo','Junio','Julio','Agosto','Septiembre',
        'Octubre','Noviembre','Diciembre']].sum(axis=1)
    df_op=df_op[['Cve. Municipio','Bien jurídico afectado',agno]]
    df_op.rename(columns={'Cve. Municipio':'CVE_MUN',
                            'Bien jurídico afectado':'DELITO'}, inplace=True)
    df_op=df_op.groupby(by=['CVE_MUN','DELITO']).sum().rename_axis(columns = None).reset_index()
    df_op=df_op.pivot(index='CVE_MUN',columns='DELITO',values=agno).rename_axis(columns = None).reset_index()
    df_op.fillna(value=0,inplace=True)
    df_op['AGNO']=agno
    df_op['CVE_MUN']=df_op['CVE_MUN'].astype(str)
    df_op.rename(columns=cod_DE_dict,inplace=True)
    df_op.rename(columns={'CVE_MUN':'ID'},inplace=True)
    return df_op

def raw_pobl_cleaner(df):
    df_op=df.copy(deep=True)
    df_op=df_op[df_op['indicador'].isin(['Población total','Población total hombres','Población total mujeres'])]
    
    df_op=df_op[df_op['cve_municipio']!=0]
    df_op['2015']=df_op['2010']+(df_op['2020']-df_op['2010'])*(5/10)
    df_op['2016']=df_op['2010']+(df_op['2020']-df_op['2010'])*(6/10)
    df_op['2017']=df_op['2010']+(df_op['2020']-df_op['2010'])*(7/10)
    df_op['2018']=df_op['2010']+(df_op['2020']-df_op['2010'])*(8/10)
    df_op['2019']=df_op['2010']+(df_op['2020']-df_op['2010'])*(9/10)
    df_op=df_op[['cve_municipio','indicador','2015','2016','2017','2018','2019','2020']]

    df_op=pd.melt(df_op, id_vars=['cve_municipio','indicador'], value_vars=['2015','2016','2017','2018','2019','2020'], var_name='AGNO', value_name='VALOR')
    df_op=df_op.pivot(index=['cve_municipio','AGNO'],columns='indicador',values='VALOR').rename_axis(columns = None).reset_index()
    df_op['cve_municipio']=df_op['cve_municipio']+26000
    df_op['cve_municipio']=df_op['cve_municipio'].astype(str)
    df_op.rename(columns={'cve_municipio':'ID',
        'Población total':'POB_T',
        'Población total hombres':'POB_H',
        'Población total mujeres':'POB_M'},inplace=True)
    return df_op

def dframe_concater(df_15,df_16,df_17,df_18,df_19,df_20):
    df_op=pd.concat([df_15,df_16,df_17,df_18,df_19,df_20])
    return df_op

pobl_dframe=raw_pobl_cleaner(pd.read_excel(raw_pobl_file))

denue15_dframe=raw_denue_cleaner(pd.read_csv(raw_denue15_file),'2015')
denue16_dframe=raw_denue_cleaner(pd.read_csv(raw_denue16_file),'2016')
denue17_dframe=raw_denue_cleaner(pd.read_csv(raw_denue17_file),'2017')
denue18_dframe=raw_denue_cleaner(pd.read_csv(raw_denue18_file),'2018')
denue19_dframe=raw_denue_cleaner(pd.read_csv(raw_denue19_file,encoding='latin-1'),'2019')
denue20_dframe=raw_denue_cleaner(pd.read_csv(raw_denue20_file,encoding='latin-1'),'2020')

crimen15_dframe=raw_crimen_cleaner(pd.read_excel(raw_crimen15_file),'2015')
crimen16_dframe=raw_crimen_cleaner(pd.read_excel(raw_crimen16_file),'2016')
crimen17_dframe=raw_crimen_cleaner(pd.read_excel(raw_crimen17_file),'2017')
crimen18_dframe=raw_crimen_cleaner(pd.read_excel(raw_crimen18_file),'2018')
crimen19_dframe=raw_crimen_cleaner(pd.read_excel(raw_crimen19_file),'2019')
crimen20_dframe=raw_crimen_cleaner(pd.read_excel(raw_crimen20_file),'2020')

denue_dframe=dframe_concater(denue15_dframe,denue16_dframe,denue17_dframe,
    denue18_dframe,denue19_dframe,denue20_dframe)
crimen_dframe=dframe_concater(crimen15_dframe,crimen16_dframe,crimen17_dframe,
    crimen18_dframe,crimen19_dframe,crimen20_dframe)

denue_pobl_dframe=pobl_dframe.merge(denue_dframe,how='outer',on=['ID','AGNO'])
denue_pobl_dframe['UE_AGRO_PT']=(100*denue_pobl_dframe['UE_AGRO'])/denue_pobl_dframe['POB_T']
denue_pobl_dframe['UE_MIN_PT']=(100*denue_pobl_dframe['UE_MIN'])/denue_pobl_dframe['POB_T']
denue_pobl_dframe['UE_ENE_PT']=(100*denue_pobl_dframe['UE_ENE'])/denue_pobl_dframe['POB_T']
denue_pobl_dframe['UE_CON_PT']=(100*denue_pobl_dframe['UE_CON'])/denue_pobl_dframe['POB_T']
denue_pobl_dframe['UE_MAN_PT']=(100*denue_pobl_dframe['UE_MAN'])/denue_pobl_dframe['POB_T']
denue_pobl_dframe['UE_CMA_PT']=(100*denue_pobl_dframe['UE_CMA'])/denue_pobl_dframe['POB_T']
denue_pobl_dframe['UE_CME_PT']=(100*denue_pobl_dframe['UE_CME'])/denue_pobl_dframe['POB_T']
denue_pobl_dframe['UE_TRA_PT']=(100*denue_pobl_dframe['UE_TRA'])/denue_pobl_dframe['POB_T']
denue_pobl_dframe['UE_MM_PT']=(100*denue_pobl_dframe['UE_MM'])/denue_pobl_dframe['POB_T']
denue_pobl_dframe['UE_BAN_PT']=(100*denue_pobl_dframe['UE_BAN'])/denue_pobl_dframe['POB_T']
denue_pobl_dframe['UE_INM_PT']=(100*denue_pobl_dframe['UE_INM'])/denue_pobl_dframe['POB_T']
denue_pobl_dframe['UE_PCT_PT']=(100*denue_pobl_dframe['UE_PCT'])/denue_pobl_dframe['POB_T']
denue_pobl_dframe['UE_COR_PT']=(100*denue_pobl_dframe['UE_COR'])/denue_pobl_dframe['POB_T']
denue_pobl_dframe['UE_MRR_PT']=(100*denue_pobl_dframe['UE_MRR'])/denue_pobl_dframe['POB_T']
denue_pobl_dframe['UE_EDU_PT']=(100*denue_pobl_dframe['UE_EDU'])/denue_pobl_dframe['POB_T']
denue_pobl_dframe['UE_SAL_PT']=(100*denue_pobl_dframe['UE_SAL'])/denue_pobl_dframe['POB_T']
denue_pobl_dframe['UE_REC_PT']=(100*denue_pobl_dframe['UE_REC'])/denue_pobl_dframe['POB_T']
denue_pobl_dframe['UE_ATA_PT']=(100*denue_pobl_dframe['UE_ATA'])/denue_pobl_dframe['POB_T']
denue_pobl_dframe['UE_OSE_PT']=(100*denue_pobl_dframe['UE_OSE'])/denue_pobl_dframe['POB_T']
denue_pobl_dframe['UE_GUB_PT']=(100*denue_pobl_dframe['UE_GUB'])/denue_pobl_dframe['POB_T']
denue_pobl_dframe=denue_pobl_dframe[['ID','AGNO','UE_AGRO_PT','UE_MIN_PT','UE_ENE_PT',
    'UE_CON_PT','UE_MAN_PT','UE_CMA_PT','UE_CME_PT','UE_TRA_PT','UE_MM_PT','UE_BAN_PT',
    'UE_INM_PT','UE_PCT_PT','UE_COR_PT','UE_MRR_PT','UE_EDU_PT','UE_SAL_PT','UE_REC_PT',
    'UE_ATA_PT','UE_OSE_PT','UE_GUB_PT']]

crimen_pobl_dframe=pobl_dframe.merge(crimen_dframe,how='outer',on=['ID','AGNO'])
crimen_pobl_dframe['DE_PA_PT']=(100*crimen_pobl_dframe['DE_PA'])/crimen_pobl_dframe['POB_T']
crimen_pobl_dframe['DE_FA_PT']=(100*crimen_pobl_dframe['DE_FA'])/crimen_pobl_dframe['POB_T']
crimen_pobl_dframe['DE_LS_PT']=(100*crimen_pobl_dframe['DE_LS'])/crimen_pobl_dframe['POB_T']
crimen_pobl_dframe['DE_SO_PT']=(100*crimen_pobl_dframe['DE_SO'])/crimen_pobl_dframe['POB_T']
crimen_pobl_dframe['DE_VI_PT']=(100*crimen_pobl_dframe['DE_VI'])/crimen_pobl_dframe['POB_T']
crimen_pobl_dframe['DE_LP_PT']=(100*crimen_pobl_dframe['DE_LP'])/crimen_pobl_dframe['POB_T']
crimen_pobl_dframe['DE_BJ_PT']=(100*crimen_pobl_dframe['DE_BJ'])/crimen_pobl_dframe['POB_T']
crimen_pobl_dframe=crimen_pobl_dframe[['ID','AGNO','DE_PA_PT','DE_FA_PT','DE_LS_PT',
    'DE_SO_PT','DE_VI_PT','DE_LP_PT','DE_BJ_PT']]

sonora_pobl_dframe=denue_pobl_dframe.merge(crimen_pobl_dframe,on=['ID','AGNO'])
sonora_dframe=denue_dframe.merge(crimen_dframe,on=['ID','AGNO'])

if not os.path.exists('tidy_datasets/'):
    os.makedirs('tidy_datasets/')
shapes_gdframe.to_parquet('tidy_datasets/shapes_gdframe.parquet',index=False)
pobl_dframe.to_parquet('tidy_datasets/pobl_dframe.parquet',index=False)
denue_pobl_dframe.to_parquet('tidy_datasets/denue_pobl_dframe.parquet',index=False)
crimen_pobl_dframe.to_parquet('tidy_datasets/crimen_pobl_dframe.parquet',index=False)
sonora_dframe.to_parquet('tidy_datasets/sonora_dframe.parquet',index=False)
sonora_pobl_dframe.to_parquet('tidy_datasets/sonora_pobl_dframe.parquet',index=False)