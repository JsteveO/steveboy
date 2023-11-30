import csv

def read_csv(ubi):
  with open(ubi,'r') as filas:
    leer = csv.reader(filas,delimiter=',')
    encabezado = next(leer)
    datos = []
    
    for i in leer:
      unir = zip(encabezado,i,)
      dict = {key: value for key, value in unir}
      datos.append(dict)
      
    return datos
      
if __name__ == '__main__':
  data = read_csv('./Proyecto_csv.csv')
  print(data)
