#!/usr/bin/env python
# coding: utf-8

# # ¡Hola  !🙋🏻‍♂️
# 
# Te escribe Lisandro Saez, soy revisor de código en Tripleten y tengo el agrado de revisar el proyecto que entregaste.
# 
# Para simular la dinámica de un ambiente de trabajo, si veo algún error, en primer instancia solo los señalaré, dándote la oportunidad de encontrarlos y corregirlos por tu cuenta. En un trabajo real, el líder de tu equipo hará una dinámica similar. En caso de que no puedas resolver la tarea, te daré una información más precisa en la próxima revisión.
# 
# Encontrarás mis comentarios más abajo - **por favor, no los muevas, no los modifiques ni los borres**.
# 
# ¿Cómo lo voy a hacer? Voy a leer detenidamente cada una de las implementaciones que has llevado a cabo para cumplir con lo solicitado. Verás los comentarios de esta forma:
# 
# <div class="alert alert-block alert-success">
# <b>Comentario del revisor</b> <a class="tocSkip"></a>
# 
# Si todo está perfecto.
# </div>
# 
# 
# <div class="alert alert-block alert-warning">
# <b>Comentario del revisor</b> <a class="tocSkip"></a>
# 
# Si tu código está bien pero se puede mejorar o hay algún detalle que le hace falta. Se aceptan uno o dos comentarios de este tipo en el borrador, pero si hay más, deberías hacer las correcciones. Es como una tarea de prueba al solicitar un trabajo: muchos pequeños errores pueden hacer que un candidato sea rechazado.
# </div>
# 
# <div class="alert alert-block alert-danger">
# 
# <b>Comentario del revisor</b> <a class="tocSkip"></a>
# 
# Si de pronto hace falta algo o existe algún problema con tu código o conclusiones.
# </div>
# 
# Puedes responderme de esta forma (no te preocupes, no es obligatorio):
# 
# <div class="alert alert-block alert-info">
# <b>Respuesta del estudiante</b> <a class="tocSkip"></a>
# 
# Hola, muchas gracias por tus comentarios y la revisión.
# </div>
# 
# ¡Empecemos!

# # Ice videogames seller
# 
# La tienda online Ice vende videojuegos por todo el mundo. Las reseñas de usuarios y expertos, los géneros, las plataformas y los datos históricos sobre las ventas de juegos están disponibles en fuentes abiertas. A la empresa le gustaría que identificar patrones que determinen si un juego tiene éxito o no. Esto le permitirá detectar proyectos prometedores y planificar campañas publicitarias a futuro.

# Plan de trabajo
# 1. Previsualización de la información
# 2. Preparación de datos
# 3. Análisis de datos
# 4. Análisis por región
# 5. Prueba de hipotesis 
# 6. Conclusiones Generales

# ## TOC:
# * [Previsualización de la información](#Inicializacion)
# * [Preparacion de datos](#Preprocesamiento)
# * [Analisis de datos](#Analisis)
# * [Analisis por región NA EU JP](#Perfiles)
# * [Prueba las siguientes hipótesis](#Hipotesis)
# * [Conclusiones finales](#Conclusiones)

# #  Inicializacion

# In[1]:


# Cargar todas las librerías
import pandas as pd
import numpy as np
import math
import seaborn as sns
from matplotlib import pyplot as plt
from scipy import stats as st


# 1.1  Cargar datos

# In[2]:


df_datagames=pd.read_csv("/datasets/games.csv")
print(df_datagames.info())


# 
# 
# <div class="alert alert-block alert-success">
# <b>Comentario del revisor</b> <a class="tocSkip"></a>
# 
# Bien hecho! Siempre es importante que pasemos el set de datos que estamos usando a `DataFrame`!</div>
# 
# 

# In[3]:


print(df_datagames.head())


# # Preprocesamiento

# 2.1 Encabezados en minusculas

# In[4]:


df_datagames.columns=df_datagames.columns.str.lower()

#Comprobación de títulos en minúsculas
print(df_datagames.info())


# 2.2 Convertir tipo de datos al necesario

# In[5]:


#Solo se visualiza que year of release necesita modificarse a un número entero
df_datagames['year_of_release']=pd.to_numeric(df_datagames['year_of_release'], errors='coerce').astype('Int64')
print(df_datagames.info())


# 2.3 Valores Duplicados

# In[6]:


duplicados=df_datagames[df_datagames.duplicated()]
print(duplicados)


# Comentarios:
# No se encuentran valores duplicados

# 2.3 Valores Ausentes

# 2.3.1 Valores Ausentes Columna "name"

# In[7]:


df_datagames['name']=df_datagames['name'].fillna('NoData')

#Comprobamos que se hayan hecho las modificaciones
print(df_datagames[df_datagames['name']=='NoData'])


# 2.3.2 Valores Ausentes Columna "platform"

# In[8]:


print(df_datagames['platform'].isna().sum())


# Comentarios:
# No se encuentran valores ausentes en plataforma

# 2.3.3 Valores Ausentes Columna "year_of_release"

# In[9]:


#Reviso mediana y mediana de la columna year of release para elegir cual se utilizará para rellenar los datos
print('Mean of data year of release:',df_datagames['year_of_release'].mean())
print()
print('Median of data year of release:',df_datagames['year_of_release'].median())


# In[10]:


df_datagames['year_of_release']=df_datagames['year_of_release'].fillna(df_datagames['year_of_release'].median())

#Comprobación que los valores fueron rellenados
print(df_datagames.info())


# Comentarios: 
# De los 16,715 datos que debería tener la columna, se encontraron 16,446. 269 faltantesel 1.6% faltante. Los cuales fueron rellenados con la mediana. Entre la media y mediana no había una diferencia signifcativa. Se opta rellenar con la mediana.  

# 2.3.4 Valores Ausentes Columna "genre"

# In[11]:


df_datagames['genre']=df_datagames['genre'].fillna('NoData')

#Comprobamos que se hayan hecho las modificaciones
print(df_datagames[df_datagames['name']=='NoData'])


# 
# <div class="alert alert-block alert-success">
# <b>Comentario del revisor</b> <a class="tocSkip"></a>
# 
# Te felicito por haber eliminado los NaNs! Es una parte fundamental del análisis de datos!
# </div>

# 2.3.5 Valores Ausentes Columna "na_sales"

# In[12]:


print(df_datagames['na_sales'].isna().sum())


# 2.3.6 Valores Ausentes Columna "eu_sales"

# In[13]:


print(df_datagames['eu_sales'].isna().sum())


# 2.3.7 Valores Ausentes Columna "jp_sales"

# In[14]:


print(df_datagames['jp_sales'].isna().sum())


# 2.3.8 Valores Ausentes Columna "other_sales"

# In[15]:


print(df_datagames['other_sales'].isna().sum())


# Comentarios: Se encuentran todos los valores de ventas de Norte America, Europa, Japón y Otras ventas.

# 2.3.9 Valores Ausentes Columna "critic_score"

# In[16]:


df_datagames['critic_score']=df_datagames['critic_score'].fillna('NaN')
df_datagames['critic_score'] = pd.to_numeric(df_datagames['critic_score'], errors='coerce')


# 2.3.10 Valores Ausentes Columna "user_score"

# In[17]:


df_datagames['user_score']=df_datagames['user_score'].fillna('NaN')
df_datagames['user_score'] = pd.to_numeric(df_datagames['user_score'], errors='coerce')


# Se convierten los datos de las columnas critic ans user score a número e ignorando los datos TBD Y NaN. Si más adelante se condigue la información se podría agregar a la tabla.

# 2.3.11 Valores Ausentes Columna "rating"

# In[18]:


df_datagames['rating']=df_datagames['rating'].fillna('NaN')


# Revisamos la información del data frame completo

# In[19]:


print(df_datagames.info())


# 2.4 Agregamos columna de ventas totales

# In[20]:


df_datagames['total_sales_region']=df_datagames['na_sales']+df_datagames['eu_sales']+df_datagames['jp_sales']

df_datagames['total']=df_datagames['na_sales']+df_datagames['eu_sales']+df_datagames['jp_sales']+df_datagames['other_sales']

print(df_datagames.info())
print()
print(df_datagames.head())


# # Analisis

# 3.1 Juegos Lanzados por año

# In[21]:


df_datagames_byyear=df_datagames.groupby(['year_of_release']).count().reset_index()
#Se comprobo que la agrupación estuviera de forma correcta
#print(df_datagames_byyear)

plt.bar(df_datagames['year_of_release'],df_datagames['total'], align='center',alpha=0.7)
plt.title('Videogames sold by year')
plt.legend(['Year', 'Videogames sold'])
plt.show()


# 
# 
# <div class="alert alert-block alert-success">
# <b>Comentario del revisor</b> <a class="tocSkip"></a>
# 
# Gran trabajo utilizando `groupby()`!</div>
# 
# 

# Comentarios:
# Se observan ciclos constantes aproximadamente 5 años donde el lanzamiento de videojuegos repunta. En 2005 hubo un incremento altamente mayor en comparación con otros años. Del 2005 al 2010 se observan una cantidad mayor de lanzamientos en ese periodo de 5 años a comparación de otros lustros.

# 

# 3.2 Juegos Lanzados por plataforma y año

# In[22]:


df_datagames_byplatform=df_datagames.groupby(['platform'])['total'].sum().sort_values(ascending=False)
print("Top 5",df_datagames_byplatform.head(5))
print()
print("Least sold",df_datagames_byplatform.tail(5))


# Comentarios: El Top 5 de ventas de las plataformas de los juegos más vendidos versus los 5 menos vendidos

# 3.2.1 Ventas del Top 5 atraves de los años

# In[23]:


data_ps2=df_datagames.groupby(['platform','year_of_release']).sum().reset_index()
data_ps2=data_ps2[data_ps2['platform']=='PS2']
#print(data_ps2)

data_X360=df_datagames.groupby(['platform','year_of_release']).sum().reset_index()
data_X360=data_X360[data_X360['platform']=='X360']
#print(data_X360)

data_ps3=df_datagames.groupby(['platform','year_of_release']).sum().reset_index()
data_ps3=data_ps3[data_ps3['platform']=='PS3']
#print(data_ps3)

data_Wii=df_datagames.groupby(['platform','year_of_release']).sum().reset_index()
data_Wii=data_Wii[data_Wii['platform']=='Wii']
#print(data_Wii)

data_DS=df_datagames.groupby(['platform','year_of_release']).sum().reset_index()
data_DS=data_DS[data_DS['platform']=='DS']
#print(data_DS)

plt.bar(data_ps2['year_of_release'],data_ps2['total'], align='center',alpha=0.5)
plt.bar(data_X360['year_of_release'],data_X360['total'], align='center',alpha=0.5)
plt.bar(data_ps3['yebmar_of_release'],data_ps3['total'], align='center',alpha=0.5)
plt.bar(data_Wii['year_of_release'],data_Wii['total'], align='center',alpha=0.5)
plt.bar(data_DS['year_of_release'],data_DS['total'], align='center',alpha=0.5)

plt.title('Top 5 Platforms of Videogames Sold by Year')
plt.legend(['ps2','X360','ps3','Wii','DS'])
plt.xlim(1995,2020)
plt.show()


# 
# 
# <div class="alert alert-block alert-success">
# <b>Comentario del revisor</b> <a class="tocSkip"></a>
# 
# Te felicito por haber recordado resetear el índice después de modificar la tabla!</div>
# 
# 

# Comentarios:
# Se observan periodos de 10 años de ventas aproxidamente desde el lanzamiento de una nueva plataforma hasta que lo descontinuan. En los años intermedios (3 años - 6 años) se observan los picos de ventas a exception de la plataforma Wii. Apartir del 2000 se obtiene mayor información para crear un modelo para el 2017. Del 2000 para atras son juegos de otro estilo.

# 3.2.2 Juegos Clásicos

# Se analizaran los juegos que antes estaban de moda, antes del año 2000. Identificando cuales se siguen generando ventas.

# In[24]:


df_clasicgames=df_datagames[df_datagames['year_of_release']<2000]
df_clasicplatforms=df_clasicgames.groupby('platform')['total'].sum()

print(df_clasicplatforms.sort_values(ascending=False))


# Las plataformas más vendidas antes del 2000, PS, NES, GB,SNES, N64. Estos juegos evolucionaron a otras plataformas que se venden hasta el 2016. LA PC sigue siendo la plataforma que se sigue vendiendo hasta la actualidad.

# 3.3 Ventas globales por plataforma

# In[25]:


df_globalsales=df_datagames.groupby(['platform','year_of_release'])['total'].sum().sort_values(ascending=False).reset_index()
print('Global sales by platform')
print(df_globalsales)
plt.figure(figsize=(10, 10))
plt.title('Global sales by platform')
sns.boxplot(data=df_globalsales, x='platform', y='total')


# 
# 
# <div class="alert alert-block alert-success">
# <b>Comentario del revisor</b> <a class="tocSkip"></a>
# 
# Tus gráficos se ven increíbles y se nota el trabajo que has invertido en ellos. Felicitaciones!</div>
# 
# 
# 

# Comentarios: Al ser bastantes plataformas y las diferencias son significativamente grandes por lo que no se alcanza a visualizar las cajas, se hara un boxplot del top 4 con más ventas.

# In[26]:


df_top5globalsales=df_globalsales[df_globalsales['platform'].isin(['PS2', 'Wii', 'X360', 'PS', 'PS3'])]
#print(df_top5globalsales)

plt.figure(figsize=(6, 6))
sns.boxplot(data=df_top5globalsales, x='platform', y='total')


# Comentarios: Las 3 primeras plataformas son diferentes entre si, y las que siguen en ventas son el desarrollo de una plataforma.

# 3.4 Las Reseñas de los Usuarios y Profesionales Afectan las ventas de PC

# Comentarios: Se toman datos del 2005 en adelante para el análisis de la correlación. Se eligió la plataforma PC, debido a que estaban el 73% de sus datos, en comparación a otras plataformas que se encontraban más datos faltantes. Se eliminarán los valores con TBD y NaN para que la correlación se realice de forma correcta.No se agregan datos extra debido a que hay más del 10% de la población faltante y eso afectaría el análisis de datos. 

# In[27]:


df_datagames_pc = df_datagames[(df_datagames['platform'] == 'PC') & (df_datagames['year_of_release'] > 2004)]

#Para Usuarios
df_datagames_pc_u = df_datagames_pc[~df_datagames_pc['user_score'].isin(['tbd']) & ~df_datagames_pc['user_score'].isin(['NaN'])]
#Se comprobó que los data frames estuvieran correctamente filtrados
#print(df_datagames_pc)

correlation_u = df_datagames_pc_u['user_score'].corr(df_datagames_pc_u['total'])
print('Correlación de Ventas vs Score por los Usuarios')
print(correlation_u)
print()

#Graficos
plt.scatter( df_datagames_pc_u['user_score'],  df_datagames_pc_u['total'])
plt.title('Gráfico de Dispersión de User Score vs Total')
plt.xlabel('User Score')
plt.ylabel('Total')
plt.grid()
plt.show()


#Para Criticos
df_datagames_pc_c = df_datagames_pc[~df_datagames_pc['critic_score'].isin(['tbd']) & ~df_datagames_pc['critic_score'].isin(['NaN'])]
correlation_c = df_datagames_pc_c['critic_score'].corr(df_datagames_pc_c['total'])
print()
print('Correlación de Ventas vs Score por los Criticos')
print(correlation_c)
print()

#Gráficos
plt.scatter( df_datagames_pc_c['critic_score'],  df_datagames_pc_c['total'])
plt.title('Gráfico de Dispersión de User Score vs Total')
plt.xlabel('Critic Score')
plt.ylabel('Total')
plt.grid()
plt.show()


# Comentarios: No afecta una calificación mala o buena a la venta de videojuegos, ni por expertos ni por usuarios. En ambos casos el coficiente de relación es débil

# 

# 3.4.1 Venta de Sims 3 en diferentes plataformas

# In[28]:


df_datagames_sims3=df_datagames[df_datagames['name']=='The Sims 3']
#print(df_datagames_sims3)

#Grafico
plt.bar( df_datagames_sims3['platform'],  df_datagames_sims3['total'])
plt.title('Gráfico de Ventas vs Plataforma')
plt.xlabel('Platform')
plt.ylabel('Sales')
plt.grid()
plt.show()


# Comentarios: En comparación a otras plataformas, las personas prefieren jugar Sims en PC que en algun otro dispositivo

# 3.4.2 Venta de Star Wars en diferentes plataformas

# In[29]:


df_datagames_worldwar=df_datagames[df_datagames['name'].str.contains('Star Wars', na=False)]
#print(df_datagames_worldwar)

#Grafico
plt.bar(df_datagames_worldwar['platform'],  df_datagames_worldwar['total'])
plt.title('Gráfico de Ventas vs Plataforma')
plt.xlabel('Platform')
plt.ylabel('Sales')
plt.grid()
plt.show()


# Comentarios: Al elegir otro juego que se juegue en diversas plataformas aparte de PC son muy pocos. Por lo cual decidí elegir los juegos que contentan algo relacionado con star wars para observar como se comportan en distintas plataformas. La plataforma predilecta para este tipo de juegos es el PS4.

# 3.5 Ventas de videojuegos por género

# In[30]:


df_datagames_bygenre=df_datagames[df_datagames['year_of_release']>2004]
df_datagames_bygenre=df_datagames.groupby('genre').sum().reset_index().sort_values(by='total',ascending=False)
print(df_datagames_bygenre[['genre','total']])


# In[31]:


#Grafico
plt.figure(figsize=(10, 10))
plt.bar(df_datagames_bygenre['genre'],df_datagames_bygenre['total'])
plt.xlabel('Platform')
plt.ylabel('Sales')
plt.grid()
plt.show()


# In[32]:


#Correlaciones de venta entre paises
correlation_naeu = df_datagames_bygenre['na_sales'].corr(df_datagames_bygenre['eu_sales'])
print('Correlación de Ventas de North America y Europa')
print(correlation_naeu)
print()


# In[33]:


#Correlaciones de venta entre paises
correlation_eujp = df_datagames_bygenre['eu_sales'].corr(df_datagames_bygenre['jp_sales'])
print('Correlación de Ventas de Europa y Japón')
print(correlation_eujp)
print()


# In[34]:


#Correlaciones de venta entre paises
correlation_najp = df_datagames_bygenre['na_sales'].corr(df_datagames_bygenre['jp_sales'])
print('Correlación de Ventas de Europa y Japón')
print(correlation_najp)
print()


# Comentarios: 
# Top 5 de generos más vendidos
# Action: 1744.17
# Sports: 1331.27
# Shooter: 1052.45
# Role-Playing: 934.56
# Platform: 827.77

# Comentarios: Los generos más vendidos se desarrollan en las plataformas más vendidas, de igual forma las ventas de los generos más vendidos son similares en North America y Europa a diferencia de japón. Se realizaron correlaciones para confirmar que si hay relación entre estos datos, al existir una población mayor en estos lugares las ventas son mayores.

# 
# <div class="alert alert-block alert-success">
# <b>Comentario del revisor</b> <a class="tocSkip"></a>
# 
# Te felicito por la precisión que muestras a la hora de realizar las observaciones!</div>
# 
# 

# # Perfiles

# 4.1 Perfil de North America

# 4.1.1 Análisis North America Platforms

# In[35]:


df_datagames_na=df_datagames[df_datagames['year_of_release']>2004]
#print(df_datagames_na)
df_datagames_na_platform=df_datagames_na.groupby(['platform'])['na_sales'].sum().sort_values(ascending=False).reset_index()
#print(df_datagames_na)
#Grafico de barras
plt.figure(figsize=(8, 8))
plt.bar(df_datagames_na_platform['platform'],df_datagames_na_platform['na_sales'])
plt.xlabel('Platform')
plt.ylabel('North America Sales')
plt.grid()
plt.show()


# In[36]:


print(df_datagames_na_platform.head())
print()

#Agrego el top de plataformas en una lista para hacer un análisis más adelante del top de plataformas
top_platform=[]
top_platform=df_datagames_na_platform['platform'].head()


# Comentarios: Top 5 de plataformas más vendidas en North America. Se tomaron en cuenta las ventas del 2005 en adelante para obtener un datos que se puedan proyectar al futuro.

# 4.1.2 Análisis North America Genre

# In[37]:


df_datagames_na_genre=df_datagames_na.groupby('genre')['na_sales'].sum().sort_values(ascending=False).reset_index()
print(df_datagames_na_genre)
#Grafico de barras
plt.figure(figsize=(8,8))
plt.bar(df_datagames_na_genre['genre'],df_datagames_na_genre['na_sales'])
plt.xlabel('Genre')
plt.ylabel('North America Sales')
plt.grid()
plt.show()


# In[38]:


print(df_datagames_na_genre.head())


# 4.1.3 Análisis North America Rating (ESRB)

# In[39]:


df_datagames_na_rating=df_datagames_na.groupby('rating')['na_sales'].sum().sort_values(ascending=False).reset_index()
df_datagames_na_rating=df_datagames_na_rating[df_datagames_na_rating['rating']!='NaN']


# In[40]:


#Grafico de barras
plt.figure(figsize=(8,8))
plt.bar(df_datagames_na_rating['rating'],df_datagames_na_rating['na_sales'])
plt.xlabel('Rating (ESRB)')
plt.ylabel('North America Sales')
plt.grid()
plt.show()


# In[41]:


print(df_datagames_na_rating.head(4))


# Comentarios: Top de Ventas por Rating. 

# 4.2 Perfil de Europe

# 4.2.1 Análisis Europe Platforms

# In[42]:


df_datagames_eu=df_datagames[df_datagames['year_of_release']>2004]
df_datagames_eu_platform=df_datagames_eu.groupby('platform')['eu_sales'].sum().sort_values(ascending=False).reset_index()
#Grafico de barras
plt.figure(figsize=(8,8))
plt.bar(df_datagames_eu_platform['platform'],df_datagames_eu_platform['eu_sales'])
plt.xlabel('Platform')
plt.ylabel('Europe Sales')
plt.grid()
plt.show()


# In[43]:


print(df_datagames_eu_platform.head())
top_platform=top_platform.append(df_datagames_eu_platform['platform'].head(5))


# Comentarios: Top 5 plataformas vendidas en Europa

# 4.2.2 Análisis Europe Genres

# In[44]:


df_datagames_eu_genre=df_datagames_eu.groupby('genre')['eu_sales'].sum().sort_values(ascending=False).reset_index()
#df_datagames_eu_genre

#Grafico de barras
plt.figure(figsize=(8,8))
plt.bar(df_datagames_eu_genre['genre'],df_datagames_eu_genre['eu_sales'])
plt.xlabel('Genre')
plt.ylabel('Europe Sales')
plt.grid()
plt.show()


# In[45]:


print(df_datagames_eu_genre.head())


# 4.2.3 Análisis de Rating en Europa (ESRB)

# In[46]:


df_datagames_eu_rating=df_datagames_eu.groupby('rating')['eu_sales'].sum().sort_values(ascending=False).reset_index()
df_datagames_eu_rating=df_datagames_eu_rating[df_datagames_eu_rating['rating']!='NaN']
#print(df_datagames_eu_rating)

#Grafico de barras
plt.figure(figsize=(8,8))
plt.bar(df_datagames_eu_rating['rating'],df_datagames_eu_rating['eu_sales'])
plt.xlabel('Rating')
plt.ylabel('Europe Sales')
plt.grid()
plt.show()


# 4.3 Perfil de Japón

# 4.3.1 Análisis de Plataformas en Japón

# In[47]:


df_datagames_jp=df_datagames[df_datagames['year_of_release']>2004]
df_datagames_jp_platform=df_datagames_jp.groupby('platform')['jp_sales'].sum().sort_values(ascending=False).reset_index()

#Grafico de barras
plt.figure(figsize=(8,8))
plt.bar(df_datagames_jp_platform['platform'],df_datagames_jp_platform['jp_sales'])
plt.xlabel('Platform')
plt.ylabel('Japan Sales')
plt.grid()
plt.show()


# In[48]:


print(df_datagames_jp_platform.head())


# Comentarios: Top 5 de Plataformas Vendidas

# 4.3.2 Análisis de Generos en Japón 

# In[49]:


df_datagames_jp_genres=df_datagames_jp.groupby('genre')['jp_sales'].sum().sort_values(ascending=False).reset_index()

#Grafico de barras
plt.figure(figsize=(8,8))
plt.bar(df_datagames_jp_genres['genre'],df_datagames_jp_genres['jp_sales'])
plt.xlabel('Genres')
plt.ylabel('Japan Sales')
plt.grid()
plt.show()


# In[50]:


print(df_datagames_jp_genres.head())
top_platform=top_platform.append(df_datagames_jp_platform['platform'].head(5))


# Comentarios: Top 5 de Generos Vendidos

# 4.3.3 Análisis de Rating (ESBR) en Japón

# In[51]:


df_datagames_jp_rating=df_datagames_jp.groupby('rating')['jp_sales'].sum().sort_values(ascending=False).reset_index()
df_datagames_jp_rating=df_datagames_jp_rating[df_datagames_jp_rating['rating']!='NaN']

#Grafico de barras
plt.figure(figsize=(6,6))
plt.bar(df_datagames_jp_rating['rating'],df_datagames_jp_rating['jp_sales'])
plt.xlabel('Rating')
plt.ylabel('Japan Sales')
plt.grid()
plt.show()


# Comentarios: Existen varias filas nulas. Se eliminan y se hace la gráfica de barras con los datos que si contienen el rating.

# 4.4 Comparación de ventas por Regiones (NA, EU, JP) por plataforma

# In[52]:


#Data frame filtrado con las ventas apartir del 2005 que nos interesa analizar
df_datagames_sales=df_datagames[df_datagames['year_of_release']>2004]
df_datagames_sales=df_datagames_sales.groupby(['platform','year_of_release']).sum().reset_index()
#print(df_datagames_sales)


# Top de Ventas y Plataformas en North America, Europe and Japan

# In[53]:


print("Ventas Totales por región")
sales_sum = df_datagames_sales.agg({
    'na_sales': 'sum',
    'eu_sales': 'sum',
    'jp_sales': 'sum'
})

print(sales_sum)

print()
print("Top 5 de plataformas vendidas en North America, Europe, Japan")
top_platform=top_platform.drop_duplicates().reset_index()
print(top_platform)


# Elegimos las 8 más vendidas en todas las regiones y filtramos el data frame por esas plataformas

# In[54]:


df_sales_platforms= df_datagames_sales[df_datagames_sales['platform'].isin(top_platform['platform'])]

print("Calcular la desviación estándar y estadisticos de las ventas en Norteamérica, Europa y Japón para cada plataforma")
df_sales_platform_s= df_sales_platforms.groupby('platform')[['na_sales', 'eu_sales', 'jp_sales']].describe()
print('North America Sales')
print(df_sales_platform_s['na_sales'])
print()
print('Europe Sales')
print(df_sales_platform_s['eu_sales'])
print()
print('Japan Sales')
print(df_sales_platform_s['jp_sales'])


# # Hipotesis

# 5.1 Pruebas de Hipotesis de las calificaciones promedio de los usuarios para las plataformas Xbox One y PC.

# Pruebas de Hipótesis:

# Hipotesis Nula: Los Scores son iguales para Xbox One y PC

# Hipotesis Alternativa: Los Scores son diferentes para Xbox One y PC

# Valor Alpha: 0.05

# Comentarios Valor Alpha: Se propone un valor alpha de 0.05 lo que el nivel de significación de 0.05 indica un riesgo del 5%. Un nivel de significación de 0.05 indica un riesgo del 5% de concluir que existe una diferencia cuando no hay una diferencia real. 

# In[55]:


#Datos XBOX ONE
df_ph_xone=df_datagames[df_datagames['platform']=='XOne'] 
df_ph_xone = df_ph_xone.dropna(subset=['user_score']).reset_index(drop=True)
#df_ph_xone=df_ph_xone['user_score']
#print('Data Xbox One')
#print(df_ph_xone)

#Datos PC
df_ph_pc=df_datagames[df_datagames['platform']=='PC'] 
df_ph_pc = df_ph_pc.dropna(subset=['user_score']).reset_index(drop=True)
#df_ph_pc=df_ph_pc['user_score']
#print()
#print('Data PC')
#print(df_ph_pc)


# In[56]:


#Calculo de la varianza XBOX
variance_xone=np.var(df_ph_xone['user_score'])
print('Media de users score',df_ph_xone['user_score'].mean())
print('Variance Xbox One:',variance_xone)
print()
#Calculo de la varianza PC
print('Media de users score',df_ph_pc['user_score'].mean())
variance_pc=np.var(df_ph_pc['user_score'])
print('Variance PC:',variance_pc)


# In[57]:


# Prueba de levene
# Hipótesis nula: Las varianzas de los grupos son iguales.
# Hipótesis alternativa: Al menos uno de los grupos tiene una variable diferente.

# Prueba de Levene para igualdad de varianzas
pvalue_levene_platform = st.levene(df_ph_xone['user_score'], df_ph_pc['user_score'])

# Imprimir resultados de la prueba de Levene
print('Statistic',pvalue_levene_platform.statistic)
print('P value', pvalue_levene_platform.pvalue)

if pvalue_levene_platform.pvalue < 0.05:
    print('Se rechaza la hipótesis nula: Al menos uno de los grupos tiene una variable diferente')
else:
    print('No podemos rechazar la hipótesis nula : Las varianzas de los grupos son iguales')


# Comentarios: Las varianzas son iguales. Se utilizará el metodo de muestras independientes, con el parametro de varianza igual a True

# In[58]:


alpha=0.05
resultado_ttest_xone_pc = st.ttest_ind(df_ph_xone['user_score'], df_ph_pc['user_score'], equal_var=True)

print("P value", resultado_ttest_xone_pc.pvalue)

if resultado_ttest_xone_pc.pvalue < alpha:
    print("Rechazamos la hipotesis nula")
else:
    print("No podemos rechazar la hipotesis nula")
    
print()


# Conclusiones: De acuerdo a los scores promedio otorgados por los usuarios, se ha realizado una prueba de hipotesis con una prueba de hipotesis de muestras independientes con valor alpha de 0.05, concluimos rechazando la hipotesis nula. No tenemos sustento necesario para afirmar que las muestras son iguales, por lo tanto los users score son diferentes
# 

# 5.2 Pruebas de Hipotesis de las calificaciones promedio de los usuarios para los géneros de Acción y Deportes

# Pruebas de Hipótesis:

# Hipotesis Nula: Los Scores son iguales para acción y deportes

# Hipotesis Alternativa: Los Scores son diferentes para acción y deportes

# Valor Alpha: 0.05

# Comentarios Valor Alpha: Se propone un valor alpha de 0.05 lo que el nivel de significación de 0.05 indica un riesgo del 5%. Un nivel de significación de 0.05 indica un riesgo del 5% de concluir que existe una diferencia cuando no hay una diferencia real. 

# 5.1 Data Frames de Action and Sports

# In[59]:


#Data Frames Action Y Sports
df_ph_action = df_datagames[(df_datagames['genre'] == 'Action') & (df_datagames['year_of_release'] > 2004)]
df_ph_action=df_ph_action.dropna(subset=['user_score']).reset_index(drop=True)
#print(df_ph_action[['genre','user_score']])

#Data Frame Action
df_ph_sports = df_datagames[(df_datagames['genre'] == 'Sports') & (df_datagames['year_of_release'] > 2004)]
df_ph_sports=df_ph_sports.dropna(subset=['user_score']).reset_index(drop=True)
#print(df_ph_sports[['genre','user_score']])


# 5.2 Prueba de varianzas

# In[60]:


# Prueba de levene
# Hipótesis nula: Las varianzas de los grupos son iguales.
# Hipótesis alternativa: Al menos uno de los grupos tiene una variable diferente.

# Prueba de Levene para igualdad de varianzas
pvalue_levene_genre = st.levene(df_ph_action['user_score'], df_ph_sports['user_score'])

# Imprimir resultados de la prueba de Levene
print('Statistic',pvalue_levene_genre.statistic)
print('P value', pvalue_levene_genre.pvalue)

if pvalue_levene_genre.pvalue < 0.05:
    print('Se rechaza la hipótesis nula: Al menos uno de los grupos tiene una variable diferente')
else:
    print('No podemos rechazar la hipótesis nula : Las varianzas de los grupos son iguales')


# Comentarios: Las varianzas son diferentes, se utilizara el método de muestras independientes con el parametro de variancia igual en Falso

# 5.2 Prueba de hipótesis

# In[61]:


alpha=0.05
resultado_ttest_genre = st.ttest_ind(df_ph_action['user_score'], df_ph_sports['user_score'], equal_var=False)

print("P value", resultado_ttest_genre.pvalue)

if resultado_ttest_genre.pvalue < alpha:
    print("Rechazamos la hipotesis nula")
else:
    print("No podemos rechazar la hipotesis nula")
    
print()


# Comentarios:Rechazamos la hipótesis nula. Por lo cual las calificaciones de los usuarios es diferente por género son diferentes. 

# 
# <div class="alert alert-block alert-success">
# <b>Comentario del revisor</b> <a class="tocSkip"></a>
# 
# Grandísimo trabajo con el análisis de hipótesis. Felicitaciones!</div>
# 

# # Conclusiones

# Prepocesamiento de datos: 
# A continuación se explica la forma en la que se rellenaron. 
# 
# Name se rellenó con NoData, Plataforma no tuvo valores ausentes.
# 
# Year of Release: De los 16,715 datos que debería tener la columna, se encontraron 16,446. 269 faltantes el 1.6% faltante. Los cuales fueron rellenados con la mediana. Entre la media y mediana no había una diferencia signifcativa. Se opta rellenar con la mediana. De igual forma se convirtió de un flotante a un número entero. 
# 
# Genre se rellenó con No Data. En las columnas de ventas de North America, Europe, Japan and Other no hay valores faltantes. 
# 
# En critic and user score se decide no eliminar ni rellenar con la media o mediana los datos, son más del 10% de datos faltantes. Se deciden mantener por si más adelante se proporcionaba la información. Se rellenan con 'NaN' y en el momento de realizar el análisis especifico se hace el tratamiento oportuno. De igual forma se toma esa decisión para no hacer modificaciones al data frame original que afecten a los resultados y prospecciones a futuro. Se agrega columna de datos de ventas totales.

# Analisis: Comentarios:
# Se observan ciclos constantes aproximadamente 5 años donde el lanzamiento de videojuegos repunta. En 2005 hubo un incremento altamente mayor en comparación con otros años. Del 2005 al 2010 se observan una cantidad mayor de lanzamientos en ese periodo de 5 años a comparación de otros lustros. 
# 
# El Top Top 5 platform
# PS2     1255.77
# X360     971.42
# PS3      939.65
# Wii      907.51
# DS       806.12
# 
# Se identifican que estos fueron antes del 2005
# Least sold platform
# WS      1.42
# TG16    0.16
# 3DO     0.10
# GG      0.04
# PCFX    0.03
# 
# Se observan periodos de 10 años de ventas aproxidamente desde el lanzamiento de una nueva plataforma hasta que lo descontinuan. En los años intermedios (3 años - 6 años) se observan los picos de ventas a exception de la plataforma Wii. Apartir del 2000 se obtiene mayor información para crear un modelo para el 2017. Del 2000 para atras son juegos de otro estilo. Dependiendo de la plataforma y del año de lanzamiento se podría pronosticar la cantidad de productos que se productos que se podrían vender y la cantidad de ventas que se puedan obtener.
# 
# El top de plataformas vendidas al rededor del mundo son: PS2, Wii, X360, PS, PS3
# 
# Analisis del critic_user
# Se eligió la plataforma PC, debido a que estaban el 73% de sus datos, en comparación a otras plataformas que se encontraban más datos faltantes. 
# Se toman datos del 2005 en adelante para el análisis de la correlación.
# Se eliminarán los valores con TBD y NaN para que la correlación se realice de forma correcta.No se agregan datos extra debido a que hay más del 10% de la población faltante y eso afectaría el análisis de datos.
# 
# Valor: -0.03025729153368257
# No afecta una calificación mala o buena a la venta de videojuegos, ni por expertos ni por usuarios. En ambos casos el coficiente de relación es débil
# 
# Valor: 0.27599738561336423
# No afecta una calificación mala o buena a la venta de videojuegos, ni por expertos ni por usuarios. En ambos casos el coficiente de relación es débil. 
# 
# En comparación a otras plataformas, las personas prefieren jugar Sims en PC que en algun otro dispositivo
# 
# Al elegir otro juego que se juegue en diversas plataformas aparte de PC son muy pocos. Por lo cual decidí elegir los juegos que contentan algo relacionado con star wars para observar como se comportan en distintas plataformas. La plataforma predilecta para este tipo de juegos es el PS4.
# 
# Los generos más vendidos se desarrollan en las plataformas más vendidas, de igual forma las ventas de los generos más vendidos son similares en North America y Europa a diferencia de japón. Se realizaron correlaciones para confirmar que si hay relación entre estos datos, al existir una población mayor en estos lugares las ventas son mayores.
# 
# Dados estos comentarios, es importante analizar que tipo de juego es importante solicitar en que tipo de consola prefieren los usuarios
# 
# Se hicieron correlaciones para revisar si las ventas de North America, Europe y Japan tienen relación. Encontrando que North America, Europe se pueden realizar los pronosticos para proyectar envios y preparar temas logisticos.

# Perfiles por region:
# Perfil en North America: 
# Top Plataformas: X360, Wii, PS3, DS, PS2
# Genres Favoritos: Action, Sport, Shooter, Misc, Role Playing
# Rating: E, M, T, E10
# 
# Perfil en Europa: 
# Top Plataformas: PS3. X360, Wii, DS, PS4
# Genres Favoritos: Action, Sport, Shooter, Misc, Racing
# Rating: E, M, T, E10
# 
# Perfil en Japan: 
# Top Plataformas: DS, 3DS, PS3, PSP, Wii
# Genres Favoritos: Role Playing, Action, Misc, Sport, Platform
# Rating: E, M, T, E10
# 
# A diferencia de North America y Europe en Japon en los primeros 2 lugares son plataformas portatiles en lugar de plataformas que son estaticas.
# Los géneros se parecen más entre North America y Europe
# Los ratings son similares.
# 
# Las ventas de las plataformas por región son diferentes. En North America son significativamente superiores que en las otras regiones. Sería importante hacer una estrategia de marketing especial para esta región.
# 
# 

# Pruebas de Hipotesis: 
# 
# Se realizaron 2 pruebas de hipótesis de muestras independientes.
# 
# Hipotesis 1:
# Hipotesis Nula: Las muestras de los users_score de Xbox y PC son similares.
# Hipotesis Alternativa: Las muestras de los users_score de Xbox y PC no son similares.
# Valor alpha= 0.05
# 
# Comentarios Valor Alpha: Se propone un valor alpha de 0.05 lo que el nivel de significación de 0.05 indica un riesgo del 5%. Un nivel de significación de 0.05 indica un riesgo del 5% de concluir que existe una diferencia cuando no hay una diferencia real. 
# 
# De acuerdo a los scores promedio otorgados por los usuarios, se ha realizado una prueba de hipotesis con una prueba de hipotesis de muestras independientes con valor alpha de 0.05, concluimos rechazando la hipotesis nula. Varianzas similares. No tenemos sustento necesario para afirmar que las muestras son iguales, por lo tanto los users score son diferentes
# 
# 
# Hipotesis 2: 
# Hipotesis Nula: Los ratings de Action y Score son similares
# Hipotesis Alternativa: Los ratings de Action y Score no son similares
# 
# Comentarios Valor Alpha: Se propone un valor alpha de 0.05 lo que el nivel de significación de 0.05 indica un riesgo del 5%. Un nivel de significación de 0.05 indica un riesgo del 5% de concluir que existe una diferencia cuando no hay una diferencia real. 
# 
# De acuerdo a los scores promedio otorgados por los usuarios, se ha realizado una prueba de hipotesis con una prueba de hipotesis de muestras independientes con valor alpha de 0.05, concluimos rechazando la hipotesis nula. Varianzas diferentes. No tenemos sustento necesario para afirmar que las muestras son iguales, por lo tanto los users score son diferentes.
# 
# Despues de este análisis podemos observar que cada región tiene sus caracteristicas que se pueden tomar decisiones importantes para potenciar las ventas en los siguientes años que puedan apoyar en temas operativos, financieros y logisticos.

# <div class="alert alert-block alert-success">
# <b>Comentario del revisor</b> <a class="tocSkip"></a>
# 
# Realmente tus conclusiones demuestran tu expertise en el tema, te felicito por haberte esforzado tanto en este sprint. Excelente trabajo!</div>
# 

# MP Ortiz
