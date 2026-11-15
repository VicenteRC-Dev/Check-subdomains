<div align="center">

# Check Subdomains

**Herramienta para escanear subdominios hecha en python.**

</div>

---

## Características

- Interfaz interactiva (usa `input()`)
- Wordlist desde `sub.txt` (se crea automáticamente si no existe)
- Escaneo concurrente (40 hilos por defecto)
- Timeouts configurados
- Resolución de IP + detección de HTTP/HTTPS
- Detección de Cloudflare, Server header y Status Code
- Barra de progreso en tiempo real
- Guardado automático de resultados en `vivos.txt`
- Código limpio, robusto y mantenible
- Validación y limpieza del dominio ingresado

---

## Requisitos

- Python 3.8+
- `requests`
- `colorama`

---

## Instalación

```bash
git clone https://github.com/VicenteRC-Dev/Check-subdomains
cd Check-subdomains
pip install -r requirements.txt
```

---

## Uso

```bash
python3 Check.py
```

El programa te pedirá el dominio:

```
Ingresa el dominio a escanear (ejemplo: google.com)
>> ejemplo.com
```

---

## Archivos

| Archivo            | Descripción                                      |
|--------------------|--------------------------------------------------|
| `Check.py`         | Script principal                                 |
| `sub.txt`          | Wordlist de subdominios (uno por línea)          |
| `requirements.txt` | Dependencias                                     |
| `vivos.txt`        | Se genera automáticamente con los resultados     |
| `README.md`        | Este archivo                                     |

---

## Personalizar la wordlist

Edita el archivo `sub.txt` y agrega o quita subdominios (uno por línea).

Las líneas que empiezan con `#` se ignoran.

```
www
mail
api
admin
dev
staging
# esto es un comentario
cdn
```

---

## Ejemplo de salida

Los resultados son de ejemplo, para saberlo utiliza la herramienta usando un dominio!

```
[+] api.prueba.com                           200  142.250.xx.xx     cloudflare              https [Cloudflare]
[+] mail.prueba.com                          301  142.250.xx.xx     nginx                   https
[+] admin.prueba.com                         200  142.250.xx.xx     Apache                  http
...
[✓] Escaneo finalizado
    Subdominios vivos     : 12
    Tiempo total          : 8.43 segundos
    Velocidad aproximada  : 28.5 checks/s
[+] Resultados guardados en → vivos.txt
```
## Captura

<img width="789" height="651" alt="image" src="https://github.com/user-attachments/assets/21d4debd-0acb-46a8-bb0b-540cd662a77d" />

## Notas

- El script prioriza HTTPS y hace fallback a HTTP si es necesario.
- Solo muestra los subdominios que responden (vivos).
- Los resultados se guardan automáticamente en `vivos.txt`.

---

<div align="center">

**Creado para mejorar la versión anterior.**

## Contacto

**Discord:** `kid.kidd`
</div>
