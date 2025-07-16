# Proyecto No. 2 de Inteligencia Artificial
Todo esto se hace en la ruta dónde se guarda el proyecto
## Instalación de librerías
```
pip install -r requirements.txt
```
## Ejecución de proyecto
```
py app.py
```
## Modificar CSS
### Instalar depedencias
```
npm install
```
### Ejecutar TailwindCSS
Crear en la ruta `static/css/` un archivo con el nombre `input.css`, con la línea.
```
@import "tailwindcss";
```
En hoja de formulario.html
```
npx @tailwindcss/cli -i ./static/css/input.css -o ./static/css/formulario.css --watch
```
En hoja de resultado.html
```
npx @tailwindcss/cli -i ./static/css/input.css -o ./static/css/resultado.css --watch
```