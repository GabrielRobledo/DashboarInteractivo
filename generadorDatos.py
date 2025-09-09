import pandas as pd
import numpy as np
from faker import Faker
import random
from datetime import datetime, timedelta

fake = Faker('es_ES')  # Configuro Faker para español

# Configuraciones
cantidad_expedientes = 100
tipos_expedientes = ["Permiso", "Reclamo", "Consulta", "Denuncia"]
sectores = ["Administración", "Legales", "Finanzas", "Operaciones", "Atención al Cliente"]
etiquetas_posibles = ["Urgente", "Revisión", "Prioritario", "Normal", "Demorado"]
estados_importancia = ["Abierto - Alta", "Abierto - Media", "Abierto - Baja", "Cerrado - Alta", "Cerrado - Baja"]

# Rango de fechas: últimos 2 años
hoy = datetime.today()
fecha_inicio_minima = hoy - timedelta(days=365*2)

def fecha_aleatoria(inicio, fin):
    return inicio + timedelta(seconds=random.randint(0, int((fin - inicio).total_seconds())))

# Generar expedientes
lista_expedientes = []

for nro in range(1, cantidad_expedientes + 1):
    fecha_inicio = fecha_aleatoria(fecha_inicio_minima, hoy)
    etiquetas = random.sample(etiquetas_posibles, k=random.randint(1, 3))
    estado = random.choice(estados_importancia)
    
    expediente = {
        "Nro. Expediente": nro,
        "Extracto": fake.sentence(nb_words=5),
        "Fecha inicio": fecha_inicio.strftime("%Y-%m-%d"),
        "Tipo Expediente": random.choice(tipos_expedientes),
        "Sector Actual": random.choice(sectores),
        "Etiquetas": ", ".join(etiquetas),
        "Mes Inicio": fecha_inicio.month,
        "Estado - Importancia": estado
    }
    lista_expedientes.append(expediente)

df_expedientes = pd.DataFrame(lista_expedientes)
print(df_expedientes.head())

# Guardar en CSV
df_expedientes.to_csv("expedientes_generados.csv", index=False)

# Parámetros
cantidad_pases = 200  # Puede ser mayor que la cantidad de expedientes

sectores_pases = sectores  # Usamos la misma lista de sectores
personas_pasado_por = [fake.name() for _ in range(20)]  # 20 nombres ficticios para "Pasado por"

# Generar pases
lista_pases = []

for nro in range(1, cantidad_pases + 1):
    fecha_ingreso = fecha_aleatoria(fecha_inicio_minima, hoy)
    tiempo_sector = random.randint(1, 30)  # Días que pasó en ese sector
    
    pase = {
        "Nro. Expediente": random.randint(1, cantidad_expedientes),  # Link con expediente random
        "Sector": random.choice(sectores_pases),
        "Fecha ingreso": fecha_ingreso.strftime("%Y-%m-%d"),
        "Pasado por": random.choice(personas_pasado_por),
        "Tiempo en el sector (días)": tiempo_sector
    }
    
    lista_pases.append(pase)

df_pases = pd.DataFrame(lista_pases)
print(df_pases.head())
# Guardar en CSV
df_pases.to_csv("pases_generados.csv", index=False)