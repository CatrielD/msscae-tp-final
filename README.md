# Archivos

- **./** raiz del proyecto, contiene la presentación con los experimentos elegidos de forma más prolija
- **data** caché de datos obtenidos
  - los datos están comprimidos, hay que correr un script par descomprimirlo si se quieren correr los experimentos
  - en caso contrario, se intentarán bajar de internet
- **img** imágenes generadas por la experimentación
- **src/** Contiene archivos de notebook con experimentación, generan los gráficos que se ven en la presentación 
- **src/lib** Carpeta con archivos python con todo el código usado. 
- **src/backups** Viejos notebooks que pueden ser interesante consultar
- **tools** una herramienta para ver diffs de los notebooks sin que sea meta en el medio los resultados; también permite ver las celdas por la terminal
  - **./config-difftool** configura el git para que al usar el comando *git difftool <archivo.ipynb>* use esta herramienta

# Notas para correr el notebook

Es conveniente entrar en la carpeta ```data/``` y descomprimir los datos, así no se fetchean de nuevo

Esto se corre desde este directorio donde se encuentra este README.

## Instalar ambiente virtual

usar virtualenv con python3.10:
```
virtualenv --python=/usr/bin/python3.10 venv
```
reemplazar el path de python por el que tengan en su máquina.
(existe también venv y varios otros para poder probar ambientes con otra versión de python [ver esta respuesta de stackoverflow](https://stackoverflow.com/a/41573588) yo lo hice andar con virtualenv y el python3.10 lo instalé con el admin de paquetes de sistema, si eso no es una opción tal vez puedan checkear pyenv)

# Activar ambiente virtual

```
source venv/bin/activate
```

comprobar que es python3.10

```
python --version
```

instalar las dependencias:
```
pip install -r requirements
```

correr jupyter notebook
```
jupyter notebook
```
