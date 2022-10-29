# Instrucciones para ejecutar este proyecto

### 1. Abrir Git Bash para `Windows` o una terminal para `Linux/Unix`.

- Clonar el proyecto
```bash
git clone https://github.com/SabriBon/Entrega_Intermedia_Bonanno.git

### 3. Crear y activar entorno virtual
(Windows)
```bash
python -m venv venv
.\venv\Scripts\activate
```

(Linux)
```bash
python3 -m venv venv
source venv/bin/activate
```

### 4. Instalar las dependencias del proyecto
```bash
pip install -r requirements.txt
```

### 5. Navegamos hacia la carpeta del proyecto `my_blog`
```bash
cd Entrega_Intermedia_Bonanno
```

### 6. Se crean las migraciones que son una "plantilla" para crear la base de datos con la que trabajará nuestro proyecto de Django
```bash
python manage.py makemigrations
```

### 7. Se ejecuta la migración para crear la base de datos con la que trabajará nuestro proyecto de Django
```bash
python manage.py migrate
```

### 8. Se levanta el servidor de Django que expone el servicio por el localhost en el puerto 8000 por defecto `http://127.0.0.1:8000/`
```bash
python manage.py runserver
```

- Es hora de ir al navegador y en una pestaña nueva navegar hacia para visualizar el proyecto que hicimos.

