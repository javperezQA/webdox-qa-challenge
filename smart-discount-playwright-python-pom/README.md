# Smart Discount 2.0 - Playwright (Python) + POM

Este proyecto incluye 3 pruebas UI en Playwright (Python) usando un POM liviano (`pages/`).

## Estructura
- `app/` : demo entregado (HTML + assets)
- `pages/` : Page Objects (selectores `data-testid`)
- `tests/` : tests pytest
- `conftest.py` : fixtures de Playwright (sin plugins)

## Requisitos
- Python 3.10+
- Node.js (solo para instalar browsers de Playwright)

## Instalación
```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# Mac/Linux: source .venv/bin/activate

pip install -r requirements.txt
python -m playwright install
```

## Levantar el demo (servidor estático)
Desde la carpeta del demo:

```bash
cd app/smart-discount-2.0---gimnasio-demo
python -m http.server 5173
```

## Ejecutar tests
En otra terminal (con el venv activo):

```bash
# BASE_URL por defecto: http://127.0.0.1:5173
pytest
```

Si tu servidor está en otro puerto:
```bash
BASE_URL=http://127.0.0.1:PUERTO pytest
```
