# Run Launcher

Este proyecto es un ejecutor automático de archivos fuente basado en su extensión, similar a cómo funcionan los "launchers". Busca archivos con un nombre objetivo (`run` por defecto), detecta su tipo por extensión, y ejecuta el archivo con el binario/interprete correspondiente configurado.

---

## 🚀 Características

- Soporte multiplataforma (Linux / Windows).
- Ejecuta archivos como `.py`, `.sh`, `.rb`, `.c`, etc., según su extensión.
- Gestión automática de configuración desde `~/.config/run/config.txt` o `%APPDATA%/run/config.txt`.
- Detección de múltiples archivos `run.*` y permite elegir cuál ejecutar.
- Colores en la terminal (mediante `colorama`).
- Analizador simple de argumentos (`--help`, `--target`).

---

## 📁 Estructura de configuración

Al ejecutar el programa por primera vez, se crea un archivo de configuración que define las extensiones y sus binarios asociados:

```ini
#basic conficuration
#binary and extension
python3 = py
bash = sh
gcc = c
ruby = rb
