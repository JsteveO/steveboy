import time
import readcsv as datos
import pandas as pd
import sett
#from reportlab.lib.pagesizes import letter
#from reportlab.platypus import SimpleDocTemplate, Table, TableStyle

def format_to_pesos(value):
    return f"${int(value):,}"


datos = datos.read_csv('./Proyecto_csv.csv')

datos2 = pd.read_csv('./Proyecto_csv.csv', dtype={' SALDO CORTE ': str, 'FECHA_CASTIGO': str}, low_memory=False)


datos2[' SALDO_CORTE '] = datos2[' SALDO_CORTE '].replace(' -   ', 0)
datos2[' SALDO_CORTE '] = datos2[' SALDO_CORTE '].astype(int)


#df = pd.read_csv('./Proyecto_csv.csv')

columnas = ['Asesor','Nombre', 'Municipio','Barrio', 'Saldo']
#Asesor = None

'''la siguiente funcion devuelve ARCHIVO DE PROSPECTOS para asesores detallado por MUNICIPIOS'''

def asesor2(data2):
    #filtro = list(filter(lambda i: i['ASESOR_CIERRE'] == 'ASESOR VILLAMIZAR ', data2))
    filtro2 = list(filter(lambda i: i['PEOR_CALIFICACION'] in ['A', 'B', 'C'] 
    and (int(i['MONTO_DESEMBOLSADO']) * 0.10) > int(i[' SALDO_CORTE ']), data2))

    resultados = []
    #fila_str = ''



    for i in filtro2:
        resultado = [
        i['ASESOR_CIERRE'],
        i['APELLIDOS_NOMBRES'],
        i['MUNICIPIO_NEGOCIO'],
        i['BARRIO_NEGOCIO'],
        i[' SALDO_CORTE ']
        ]
        resultados.append(resultado)


    df = pd.DataFrame(resultados, columns=columnas)
    df['Saldo'] = df['Saldo'].apply(lambda x: f"${int(x):,}")


    return df

  
clientes = asesor2(datos)
#print(clientes)




'''la siguiente funcion devuelve el ICV para asesores por MUNICIPIO y BARRIO'''

def asesor3_optimizado(data3):
    df_stiven = data3

    # Reemplazar ' -   ' con 0 y convertir a tipo int
    #df_stiven[' SALDO_CORTE '] = pd.to_numeric(df_stiven[' SALDO_CORTE '].replace(' -   ', 0), errors='coerce')

    # Calcular ICV e ICC utilizando funciones de agregación de Pandas
    grouped = df_stiven.groupby(['ASESOR_CIERRE', 'MUNICIPIO_NEGOCIO', 'BARRIO_NEGOCIO'])

    saldo_corte_sum = grouped[' SALDO_CORTE '].sum()

    icv = (grouped['VENCIDO'].sum() / saldo_corte_sum) * 100
    icc = (grouped['CASTIGO_CON_RECUPERACIÓN'].sum() / (grouped['CASTIGO_SIN_RECUPERACIÓN'].sum() + saldo_corte_sum)) * 100

    dat2 = pd.DataFrame({
        'Saldo Corte': saldo_corte_sum,
        'Créditos': grouped['ASESOR_CIERRE'].count(),
        'ICV': icv.where(saldo_corte_sum != 0, 0),
        'ICC': icc.where(saldo_corte_sum != 0, 0),
        'ICV+ICC': icv.where(saldo_corte_sum != 0, 0) + icc.where(saldo_corte_sum != 0, 0)
    }).reset_index()

    # Ordenar el DataFrame
    dat3 = dat2.sort_values(by='Créditos', ascending=False)

    # Convertir columnas a tipos int y aplicar formato a las columnas relevantes
    #dat3['Saldo Corte'] = dat3['Saldo Corte'].astype(int)
    dat3['Saldo Corte'] = dat3['Saldo Corte'].apply(lambda x: f"${int(x):,}")
    dat3['Créditos'] = dat3['Créditos'].astype(int)
    dat3['ICV'] = dat3['ICV'].round(2).astype(str) + '%'
    dat3['ICC'] = dat3['ICC'].round(2).astype(str) + '%'
    dat3['ICV+ICC'] = dat3['ICV+ICC'].round(2).astype(str) + '%'

    return dat3

resultados = asesor3_optimizado(datos2)
#print(resultados)


'''la siguiente funcion devuelve el ICV para zonas por asesor'''

def lider_zona(data3):
    df_stiven = data3

    # Reemplazar ' -   ' con 0 y convertir a tipo int
    #df_stiven[' SALDO_CORTE '] = pd.to_numeric(df_stiven[' SALDO_CORTE '].replace(' -   ', 0), errors='coerce')

    # Calcular ICV e ICC utilizando funciones de agregación de Pandas
    grouped = df_stiven.groupby(['OFICINA_CIERRE','ASESOR_CIERRE'])

    saldo_corte_sum = grouped[' SALDO_CORTE '].sum()

    icv = (grouped['VENCIDO'].sum() / saldo_corte_sum) * 100
    icc = (grouped['CASTIGO_CON_RECUPERACIÓN'].sum() / (grouped['CASTIGO_SIN_RECUPERACIÓN'].sum() + saldo_corte_sum)) * 100

    dat2 = pd.DataFrame({
        'Saldo Corte': saldo_corte_sum,
        'Créditos': grouped['ASESOR_CIERRE'].count(),
        'ICV': icv.where(saldo_corte_sum != 0, 0),
        'ICC': icc.where(saldo_corte_sum != 0, 0),
        'ICV+ICC': icv.where(saldo_corte_sum != 0, 0) + icc.where(saldo_corte_sum != 0, 0)
    }).reset_index()

    # Ordenar el DataFrame
    dat3 = dat2.sort_values(by=['OFICINA_CIERRE', 'Créditos'], ascending=[True,False])

    # Convertir columnas a tipos int y aplicar formato a las columnas relevantes
    dat3['Saldo Corte'] = dat3['Saldo Corte'].apply(lambda x: f"${int(x):,}")
    dat3['Créditos'] = dat3['Créditos'].astype(int)
    dat3['ICV'] = dat3['ICV'].round(2).astype(str) + '%'
    dat3['ICC'] = dat3['ICC'].round(2).astype(str) + '%'
    dat3['ICV+ICC'] = dat3['ICV+ICC'].round(2).astype(str) + '%'

    return dat3

resultados_zona = lider_zona(datos2)




'''la siguiente funcion devuelve el ICV para lider comercial por ZONAS'''

def lider_comercial(data3):
    df_stiven = data3

    # Reemplazar ' -   ' con 0 y convertir a tipo int
    #df_stiven[' SALDO_CORTE '] = pd.to_numeric(df_stiven[' SALDO_CORTE '].replace(' -   ', 0), errors='coerce')

    # Calcular ICV e ICC utilizando funciones de agregación de Pandas
    grouped = df_stiven.groupby(['OFICINA_CIERRE'])

    saldo_corte_sum = grouped[' SALDO_CORTE '].sum()

    icv = (grouped['VENCIDO'].sum() / saldo_corte_sum) * 100
    icc = (grouped['CASTIGO_CON_RECUPERACIÓN'].sum() / (grouped['CASTIGO_SIN_RECUPERACIÓN'].sum() + saldo_corte_sum)) * 100

    dat2 = pd.DataFrame({
        'Saldo Corte': saldo_corte_sum,
        'Créditos': grouped['ASESOR_CIERRE'].count(),
        'ICV': icv.where(saldo_corte_sum != 0, 0),
        'ICC': icc.where(saldo_corte_sum != 0, 0),
        'ICV+ICC': icv.where(saldo_corte_sum != 0, 0) + icc.where(saldo_corte_sum != 0, 0)
    }).reset_index()

    # Ordenar el DataFrame
    dat3 = dat2.sort_values(by='Créditos', ascending=False)

    # Convertir columnas a tipos int y aplicar formato a las columnas relevantes
    dat3['Saldo Corte'] = dat3['Saldo Corte'].apply(lambda x: f"${int(x):,}")
    dat3['Créditos'] = dat3['Créditos'].astype(int)
    dat3['ICV'] = dat3['ICV'].round(2).astype(str) + '%'
    dat3['ICC'] = dat3['ICC'].round(2).astype(str) + '%'
    dat3['ICV+ICC'] = dat3['ICV+ICC'].round(2).astype(str) + '%'

    return dat3

resultados_lider = lider_comercial(datos2)


'''la siguiente funcion devuelve el ICV para lider comercial detallado por MUNICIPIOS'''

def lider_detallado(data3):
    df_stiven = data3

    # Reemplazar ' -   ' con 0 y convertir a tipo int
    #df_stiven[' SALDO_CORTE '] = pd.to_numeric(df_stiven[' SALDO_CORTE '].replace(' -   ', 0), errors='coerce')

    # Calcular ICV e ICC utilizando funciones de agregación de Pandas
    grouped = df_stiven.groupby(['OFICINA_CIERRE','MUNICIPIO_NEGOCIO'])

    saldo_corte_sum = grouped[' SALDO_CORTE '].sum()

    icv = (grouped['VENCIDO'].sum() / saldo_corte_sum) * 100
    icc = (grouped['CASTIGO_CON_RECUPERACIÓN'].sum() / (grouped['CASTIGO_SIN_RECUPERACIÓN'].sum() + saldo_corte_sum)) * 100

    dat2 = pd.DataFrame({
        'Saldo Corte': saldo_corte_sum,
        'Créditos': grouped['ASESOR_CIERRE'].count(),
        'ICV': icv.where(saldo_corte_sum != 0, 0),
        'ICC': icc.where(saldo_corte_sum != 0, 0),
        'ICV+ICC': icv.where(saldo_corte_sum != 0, 0) + icc.where(saldo_corte_sum != 0, 0)
    }).reset_index()

    # Ordenar el DataFrame
    dat3 = dat2.sort_values(by=['OFICINA_CIERRE', 'Créditos'], ascending=[True,False])

    # Convertir columnas a tipos int y aplicar formato a las columnas relevantes
    dat3['Saldo Corte'] = dat3['Saldo Corte'].apply(lambda x: f"${int(x):,}")
    dat3['Créditos'] = dat3['Créditos'].astype(int)
    dat3['ICV'] = dat3['ICV'].round(2).astype(str) + '%'
    dat3['ICC'] = dat3['ICC'].round(2).astype(str) + '%'
    dat3['ICV+ICC'] = dat3['ICV+ICC'].round(2).astype(str) + '%'

    return dat3

resultados_detallado = lider_detallado(datos2)


