# Notas para correr el notebook

Es conveniente entrar en la carpeta ```data/``` y descomprimir los datos, así no se fetchean de nuevo

# Notas para correr el Ambiente

usar virtualenv con python3.10:
```
virtualenv --python=/usr/bin/python3.10 venv
```

reemplazar el path de python por el que tengan en su máquina.
(existe también venv y varios otros para poder probar ambientes con otra versión de python [ver esta respuesta de stackoverflow](https://stackoverflow.com/a/41573588) yo lo hice andar con virtualenv y el python3.10 lo instalé con el admin de paquetes de sistema, si eso no es una opción tal vez puedan checkear pyenv)

activar el ambiente:
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

