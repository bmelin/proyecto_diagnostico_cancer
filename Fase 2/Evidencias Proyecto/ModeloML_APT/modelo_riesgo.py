import pandas as pd
import pyodbc

# Conexión con SQL Server
conn = pyodbc.connect(
    'DRIVER={ODBC Driver 17 for SQL Server};'
    'SERVER=localhost;DATABASE=ProyectoAPT;UID=sa;PWD=tu_contraseña;'
)

# Leer datos desde la base
df = pd.read_sql("SELECT * FROM pacientes_registros", conn)

def calcular_puntaje(row):
    puntos = 0

    # Edad
    if row['edad'] < 40: puntos += 0
    elif row['edad'] < 50: puntos += 5
    elif row['edad'] < 60: puntos += 12
    else: puntos += 20

    # Sexo
    if row['sexo'] == 'M': puntos += 5

    # Familiar primer grado
    if row['FamiliarPrimerGradoCC'] == 'Sí': puntos += 25

    # Familiar segundo grado
    if row['FamiliarSegundoGradoCC'] == 'Sí': puntos += 4

    # Diagnóstico previo
    if row['DiagnosticoPrevioCancer'] == 'Sí': puntos += 30

    # Menstruación
    if row['Menstruacion'] == '<12 años': puntos += 6
    elif row['Menstruacion'] == '12–13 años': puntos += 3

    # Primer hijo
    if row['PrimerHijo'] == 'Nunca tuvo hijos': puntos += 8
    elif row['PrimerHijo'] == 'Primer hijo ≥30 años': puntos += 5

    # Ejercicio
    if row['Ejercicio'] == 'Ninguna': puntos += 5
    elif row['Ejercicio'] == '<3 horas': puntos += 3
    elif row['Ejercicio'] == '3–4 horas': puntos -= 2
    elif row['Ejercicio'] == '>4 horas': puntos -= 5

    # Alcohol
    if row['Alcohol'] == 'Ocasional': puntos += 2
    elif row['Alcohol'] == 'Frecuente': puntos += 5
    elif row['Alcohol'] == 'Diario': puntos += 8

    # Mamografía
    if row['Mamografia'] == 'Sí': puntos -= 3

    return puntos

df['puntaje'] = df.apply(calcular_puntaje, axis=1)

# Clasificación del riesgo
def clasificar_riesgo(p):
    if p < 20: return 'Bajo'
    elif p < 50: return 'Moderado'
    else: return 'Alto'

df['riesgo'] = df['puntaje'].apply(clasificar_riesgo)

# Guardar resultados en otra tabla
for _, row in df.iterrows():
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO resultados_prediccion (id_paciente, probabilidad_cancer, algoritmo_usado, fecha_prediccion)
        VALUES (?, ?, ?, GETDATE())
    """, row['id_paciente'], row['puntaje'], 'ModeloPonderado')
    conn.commit()
