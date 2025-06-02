# HardInfoBack
Back de HardInfo con FastAPI y SQlite

Por el momento solo registro y login.

La bd, como es sqlite, es un archivo local.

Para levantarlo tiren "python -m uvicorn main:app --reload"
Acuerdense de instalar todas las librerias del requirements.txt

http://localhost:8000/auth/register
body:
{
    "nombre": "Ian",
    "apellido": "Campo",
    "usuario": "Oniloco",
    "email": "Oniloco@example.com",
    "password": "Bananon"
}

http://localhost:8000/auth/token
form con
username=Oniloco
password=Bananon

Te genera un token, dura 30 minutos, se puede cambiar en auth.py
