# Flow Clean

Flow Clean es una utilidad de escritorio desarrollada en Python + PySide6 para limpiar referencias problemáticas dentro de paquetes legacy `.zip` exportados desde Power Automate.

Su objetivo principal es corregir conflictos comunes relacionados con:

- referencias de conexión dañadas
- `shared_sharepointonline-1`
- `InvokerConnectionOverrideFailed`
- `PackageFlowMissingConnectionMap`
- bloques `authentication` heredados en acciones OpenApiConnection y otras babosadas

---

## Funcionalidades

- Cargar paquetes `.zip` legacy de Power Automate
- Limpiar referencias antiguas o corruptas
- Reemplazar referencias de SharePoint heredadas
- Remover bloques de autenticación conflictivos
- Generar un nuevo `.zip` limpio
- Interfaz gráfica simple con estilo oscuro/neón

---

## Estructura del proyecto

```text
flow-clean/
├── assets/
├── Scripts/
│   ├── build_exe.bat
│   ├── freeze_requirements.bat
│   ├── install_deps.bat
│   └── run_dev.bat
├── src/
│   ├── core/
│   │   └── limpiador.py
│   ├── ui/
│   │   └── main_ui.py
│   └── main.py
├── venv/
├── .gitignore
├── requirements.txt
└── README.md
```

---

## Requisitos

- Python 3.10 o superior
- Windows
- Entorno virtual recomendado

---

## Instalación

### 1. Crear y activar entorno virtual

```bash
python -m venv venv
venv\Scripts\activate
```

### 2. Instalar dependencias

```bash
pip install -r requirements.txt / scripts\install_deps.bat
```

O usando el script:

```bash
Scripts\install_deps.bat
```

---

## Ejecutar en desarrollo

```bash
python src/main.py
```

O usando el script:

```bash
Scripts\run_dev.bat
```

---

## Generar ejecutable `.exe`

```bash
Scripts\build_exe.bat
```

El ejecutable se genera en:

```text
dist/FlowClean.exe
```

---

## Dependencias principales

- PySide6
- PyInstaller

---

## Flujo de uso

1. Abrir Flow Clean
2. Cargar un archivo `.zip` exportado desde Power Automate
3. Presionar **LIMPIAR FLOW**
4. Revisar el log de cambios
5. Obtener el nuevo paquete limpio generado en la misma carpeta del zip original

---

## Notas técnicas

El motor de limpieza actualmente realiza acciones como:

- reemplazo de `shared_sharepointonline-1` por `shared_sharepointonline`
- ajuste de `connectionReferences`
- cambio de `source: "Invoker"` a `source: "Embedded"` cuando aplica
- eliminación de bloques `authentication` en acciones `OpenApiConnection`
- regeneración del paquete `.zip`

---

## Scripts incluidos

### `scripts\install_deps.bat`
Instala dependencias desde `requirements.txt`.

### `scripts\run_dev.bat`
Ejecuta la app en modo desarrollo.

### `scripts\build_exe.bat`
Limpia compilaciones anteriores y genera el `.exe`.

### `scripts\freeze_requirements.bat`
Actualiza el archivo `requirements.txt`.

---

## Recomendaciones

- Si añaden algo más, usen el `cripts\freeze_requirements.bat` para mantener actualizado el `requirements.txt`


