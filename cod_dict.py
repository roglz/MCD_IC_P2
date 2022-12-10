# Diccionario de sectores de unidades económicas y su código
ue_dict={
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
    'Gubernamental':'UE_GUB'}

# Diccionario de bien jurídico afectado por delito y su código
del_dict={
    'La vida y la Integridad corporal':'DE_VI',
    'Libertad personal':'DE_LP',
    'La libertad y la seguridad sexual':'DE_LS',
    'El patrimonio':'DE_PA',
    'La familia':'DE_FA',
    'La sociedad':'DE_SO',
    'Otros bienes jurídicos afectados (del fuero común)':'DE_BJ'}

# Función para consultar el valor de los códigos
def get_cod(ref):
    if ref in ue_dict.values():
        return [key for key, value in ue_dict.items() if value==ref]
    elif ref in del_dict.values():
        return [key for key, value in del_dict.items() if value==ref]
    return None
