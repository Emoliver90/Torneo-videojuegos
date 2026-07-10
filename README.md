# 🎮 Torneo de Videojuegos

Aplicación web desarrollada con **Django** para gestionar un torneo de videojuegos: registro de usuarios, perfiles con estadísticas por juego (kills, victorias, goles) y un ranking general con gráfica interactiva.

## Tecnologías

- Python 3 / Django 6.0
- SQLite (base de datos de desarrollo)
- Bootstrap (Bootswatch "Lux") + CSS personalizado
- Chart.js para las gráficas del ranking
- python-decouple para gestión de variables de entorno

## Estructura del proyecto

```
torneo/
├── manage.py
├── requirements.txt
├── .env.example          # plantilla de variables de entorno
├── torneo/                # configuración del proyecto (settings, urls)
└── usuarios/               # app principal
    ├── models.py            # Usuario, Juego, Estadistica
    ├── views.py
    ├── forms.py
    ├── admin.py
    ├── templates/
    └── static/
```

## Instalación y ejecución local

1. Clona el repositorio y entra en la carpeta:
   ```bash
   git clone <url-del-repositorio>
   cd torneo
   ```

2. Crea y activa un entorno virtual:
   ```bash
   python -m venv venv
   source venv/bin/activate      # Windows: venv\Scripts\activate
   ```

3. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```

4. Copia el archivo de variables de entorno y genera tu propia clave secreta:
   ```bash
   cp .env.example .env
   python -c "import secrets; print(secrets.token_urlsafe(50))"
   ```
   Pega el valor generado en `SECRET_KEY` dentro de `.env`.

5. Aplica las migraciones:
   ```bash
   python manage.py migrate
   ```

6. (Opcional) Crea un superusuario para acceder al admin:
   ```bash
   python manage.py createsuperuser
   ```

7. Levanta el servidor:
   ```bash
   python manage.py runserver
   ```
   La aplicación estará disponible en `http://127.0.0.1:8000/`.

## Buenas prácticas aplicadas en esta revisión

Este proyecto fue revisado y ajustado respecto a la versión original. Resumen de los cambios:

### Seguridad
- **`SECRET_KEY`, `DEBUG` y `ALLOWED_HOSTS`** desde variables de entorno (`.env`) usando `python-decouple`. Esto evita exponer la clave secreta en el repositorio y permite tener configuraciones distintas para desarrollo y producción.
- Se añadió `.env.example` como plantilla (sin datos sensibles) y `.env` quedó excluido en `.gitignore`.


### Corrección de errores
- **Bug en `perfil.html`**: la plantilla comparaba el objeto `estadistica` directamente contra el texto `'kills'` (`{% if estadistica == 'kills' %}`), lo cual nunca era verdadero. Como resultado, el número de *kills* nunca se mostraba en el perfil de los jugadores de juegos tipo *shooter*. Se corrigió comparando el tipo de ranking real del juego (`user.juego.tipo_ranking == 'kills'`) y se añadió un mensaje para cuando el usuario todavía no tiene estadísticas registradas.
- **HTML inválido en `estadisticas.html`**: la etiqueta `<html>` tenía un atributo `xmlns:juego.id` que no correspondía a nada (residuo de una prueba) y el `<div class="ranking-container">` se abría y cerraba vacío, dejando la tabla y la gráfica fuera de su contenedor. Se corrigió la estructura para que el contenedor envuelva correctamente la tabla y la gráfica.
- Se añadieron `<!DOCTYPE html>` y `<meta charset="UTF-8">` en las plantillas que no los tenían (`login.html`, `registro.html`, `perfil.html`), para mantener HTML válido en todas las páginas.

### Rendimiento
- Las vistas `estadisticas` y `obtener_ranking` ahora usan `select_related('jugador', 'juego')`, evitando el problema de **N+1 queries** al recorrer la lista de estadísticas en las plantillas.
- `obtener_ranking` usa `get_object_or_404` en lugar de `Juego.objects.get(id=...)`, así que un `id` de juego inexistente en la URL devuelve un 404 en vez de un error 500.

### Organización del código
- Se reordenaron las funciones de `views.py` en un orden más lógico de lectura (páginas públicas → autenticación → utilidades internas).
- Se corrigió la indentación inconsistente de `usuarios/urls.py`.
- Se añadió el método `__str__` al modelo `Estadistica` para que se muestre de forma legible en el panel de administración.

### Archivos estáticos
- Se eliminaron 8 imágenes de fondo que no estaban referenciadas en ningún CSS ni plantilla, reduciendo el peso del repositorio.
- Se renombró la imagen `fondo 3.jpg` a `fondo3.jpg` (los nombres de archivo con espacios son una mala práctica: pueden romper URLs y dar problemas en distintos sistemas operativos/servidores).

### Dependencias
- Se corrigió el nombre del archivo de dependencias (antes `requeriments.txt`, con un error de tipeo) a `requirements.txt`.
- El archivo estaba guardado en codificación UTF-16 (probablemente generado con PowerShell en Windows); se regeneró en UTF-8 estándar.
- Se añadió `python-decouple` como dependencia, necesaria para la gestión de variables de entorno.

## Mejoras a futuro

- [ ] **Tests automatizados**: el archivo `tests.py` está vacío. Añadir pruebas unitarias para los modelos (por ejemplo, el método `puntaje()`), las vistas (`estadisticas`, `perfil`, `registro`) y el formulario de registro.
- [ ] **Paginación** en la vista de `estadisticas`, para que el ranking no cargue todos los registros de golpe si el torneo crece.
- [ ] **Editar estadísticas desde una interfaz propia**: actualmente las estadísticas (`kills`, `goles`, `partidos_ganados`) solo se pueden cargar desde el panel de administración de Django. Sería útil un formulario o un rol de "organizador" para cargarlas desde el frontend.
- [ ] **Manejo de errores más claro en los formularios**: mostrar los mensajes de validación con estilos propios (actualmente se apoya en el render por defecto de Django, `{{ form.as_p }}`).
- [ ] **Migrar a PostgreSQL** para un entorno de producción real (SQLite es adecuado solo para desarrollo).
- [ ] **Despliegue**: preparar `settings.py` para producción (`django-environ` + `whitenoise` para servir estáticos, configuración de `SECURE_*`, HTTPS, etc.) y documentar el despliegue en un servicio como Railway, Render o PythonAnywhere.
- [ ] **Optimizar imágenes**: las imágenes de fondo pesan varios MB cada una; comprimirlas o convertirlas a formatos modernos (WebP) reduciría el tiempo de carga.
- [ ] **Internacionalización**: aunque `LANGUAGE_CODE = 'es'` ya está configurado, los textos están escritos directamente en las plantillas. Usar el sistema de traducciones de Django (`{% trans %}`) si en el futuro se quiere soportar más de un idioma.
- [ ] **API REST** (opcional): exponer el ranking y las estadísticas vía Django REST Framework para poder consumirlas desde otras aplicaciones (por ejemplo, una app móvil).
- [ ] **CI básico**: agregar un workflow de GitHub Actions que corra `python manage.py check` y los tests en cada push/PR.

## Licencia

Proyecto académico, de uso libre para fines educativos.
