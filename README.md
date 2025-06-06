# Run Executor Tool

Una herramienta flexible para ejecutar scripts automáticamente según su extensión, configurada por el usuario.

## 🧩 Características

- Detecta archivos con nombre `run` (u otro definido por el usuario).
- Ejecuta los archivos según su extensión (`.py`, `.sh`, `.rb`, `.c`, etc.).
- Soporta configuración personalizada de binarios en un archivo `config.txt`.
- Soporta múltiples archivos objetivo.
- Parser de argumentos con soporte para alias (`--path`, `-p`, etc.).

---

## 📦 Instalación

1. Clona el repositorio:

```bash
git clone https://github.com/usuario/run.git
cd run
./run.sh
```

2. La primera vez que ejecutes el script, se creará automáticamente un archivo de configuración en:

- Linux/macOS: `~/.config/run/config.txt`
- Windows: `%APPDATA%/run/config.txt`

Edita este archivo para agregar tus propias asociaciones de binarios/extensiones si lo deseas:

```txt
#binary and extension
python3 = py
bash = sh
gcc = c
ruby = rb
```

---

## 🚀 Uso

```bash
./run [--help] [--target <nombre_archivo>] [--path <ruta>] [--execute-all]
```

### Opciones

| Opción                  | Descripción                                              |
|-------------------------|----------------------------------------------------------|
| `--help`, `-h`          | Muestra este mensaje de ayuda.                          |
| `--target`, `-T`        | Define el nombre base del archivo a ejecutar (sin extensión). Por defecto es `run`. |
| `--path`, `-p`          | Directorio donde buscar el archivo. Por defecto es el actual. |
| `--execute-all`, `-EA`  | Ejecuta todos los archivos coincidentes automáticamente. |

---

### 🧪 Ejemplos

#### Ejecutar `run.*` en el directorio actual:
```bash
./run
```

#### Ejecutar archivo llamado `deploy.*`:
```bash
./run --target deploy
```

#### Buscar archivos `setup.*` en una ruta específica:
```bash
./run --target setup --path ~/proyectos/scripts
```

#### Ejecutar todos los archivos `run` encontrados:
```bash
./run --execute-all
```

---

## 📁 Estructura del Proyecto

```
run                      # Archivo principal ejecutable
src/
└── main.py              # Lógica principal
~/.config/run/config.txt # Archivo de configuración generado
```

---

## 🛠 Dependencias

- Python 3.x
- [colorama](https://pypi.org/project/colorama/)

## 🧑‍💻 Autor

Desarrollado por [m0opha](https://github.com/m0opha)
