#!/usr/bin/env python3
import os
import platform
import socket
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Optional
from urllib.parse import urlparse

import requests
from colorama import Fore, Style, init

# Inicializar colorama
init(autoreset=True)

# ============================================================
# Configuración
# ============================================================
THREADS = 40
TIMEOUT = 6.0
USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/27.0 Safari/605.1.15"
OUTPUT_FILE = "vivos.txt"

# Wordlist de calidad (se usa si sub.txt no existe o está vacío)
DEFAULT_SUBDOMAINS = [
    "www", "mail", "ftp", "localhost", "webmail", "smtp", "pop", "ns1", "webdisk",
    "ns2", "cpanel", "whm", "autodiscover", "autoconfig", "m", "imap", "test",
    "ns", "blog", "pop3", "dev", "www2", "admin", "forum", "news", "vpn", "ns3",
    "mail2", "new", "mysql", "old", "lists", "support", "mobile", "mx", "static",
    "docs", "beta", "shop", "sql", "secure", "demo", "cp", "calendar", "wiki",
    "web", "media", "email", "images", "img", "www1", "intranet", "portal",
    "video", "sip", "dns2", "api", "cdn", "stats", "dns1", "ns4", "www3", "dns",
    "search", "staging", "server", "mx1", "chat", "wap", "my", "svn", "mail1",
    "sites", "proxy", "ads", "online", "store", "app", "panel", "download",
    "remote", "db", "bbs", "ns5", "exchange", "owa", "office", "sharepoint",
    "lyncdiscover", "git", "gitlab", "jenkins", "jira", "confluence", "status",
    "monitor", "grafana", "prometheus", "dashboard", "auth", "login", "sso",
    "id", "accounts", "account", "billing", "pay", "payment", "cdn1", "cdn2",
    "static1", "static2", "assets", "img1", "img2", "media1", "files", "upload",
    "downloads", "dl", "ftp1", "sftp", "ssh", "vpn1", "vpn2", "remote1", "rdp",
    "citrix", "vdi", "desk", "helpdesk", "support1", "ticket", "tickets",
    "crm", "erp", "hr", "intranet1", "extranet", "partner", "partners",
    "client", "clients", "customer", "customers", "portal1", "myportal",
    "app1", "app2", "apps", "mobile1", "m1", "api1", "api2", "rest", "graphql",
    "ws", "websocket", "socket", "realtime", "live", "stream", "streaming",
    "video1", "vod", "tv", "radio", "podcast", "blog1", "news1", "press",
    "media2", "pr", "marketing", "ads1", "ad", "tracker", "analytics",
    "stats1", "metrics", "logs", "log", "elk", "kibana", "elasticsearch",
    "db1", "db2", "mysql1", "postgres", "mongo", "redis", "cache", "memcached",
    "queue", "rabbit", "kafka", "mq", "jenkins1", "ci", "cd", "build", "deploy",
    "staging1", "stage", "preprod", "uat", "qa", "test1", "testing", "dev1",
    "development", "sandbox", "demo1", "preview", "beta1", "alpha", "canary",
    "edge", "origin", "backend", "frontend", "web1", "web2", "www4", "www5",
    "ns6", "ns7", "dns3", "mx2", "mx3", "mail3", "smtp1", "smtp2", "relay",
    "spam", "antispam", "filter", "gateway", "fw", "firewall", "proxy1",
    "waf", "security", "sec", "ids", "ips", "siem", "soc"
]


def clear_terminal():
    """Limpia la terminal según el sistema operativo."""
    system = platform.system().lower()
    if system == "windows":
        os.system("cls")
    else:
        # Linux, macOS, Android (Termux), etc.
        os.system("clear")


def get_device_info() -> str:
    """Identifica el sistema operativo y dispositivo actual."""
    system = platform.system()
    release = platform.release()
    machine = platform.machine()

    if system == "Windows":
        return f"Windows {release} ({machine})"
    elif system == "Darwin":
        return f"macOS {release} ({machine})"
    elif system == "Linux":
        # Detectar si es Android / Termux
        if "android" in platform.platform().lower() or "com.termux" in os.environ.get("PREFIX", "").lower():
            return f"Android / Termux ({machine})"
        # Intentar obtener el nombre de la distro
        try:
            with open("/etc/os-release", "r") as f:
                for line in f:
                    if line.startswith("PRETTY_NAME="):
                        distro = line.split("=")[1].strip().strip('"')
                        return f"{distro} ({machine})"
        except Exception:
            pass
        return f"Linux {release} ({machine})"
    else:
        return f"{system} {release} ({machine})"


def print_banner():
    banner = f"""
{Fore.CYAN}
╔════════════════════════════════════════════════════════════════════════════════════════════════════════════╗
║                                                                                                            ║
║  ▄█▀▀▀█▄█           ▄██                    ▀███                                     ██                     ║
║ ▄██    ▀█            ██                      ██                                                            ║
║ ▀███▄   ▀███  ▀███   ██▄████▄           ▄█▀▀███   ▄██▀██▄▀████████▄█████▄  ▄█▀██▄ ▀███ ▀████████▄  ▄██▀███ ║
║   ▀█████▄ ██    ██   ██    ▀██        ▄██    ██  ██▀   ▀██ ██    ██    ██ ██   ██   ██   ██    ██  ██   ▀▀ ║
║ ▄     ▀██ ██    ██   ██     ██  █████ ███    ██  ██     ██ ██    ██    ██  ▄█████   ██   ██    ██  ▀█████▄ ║
║ ██     ██ ██    ██   ██▄   ▄██        ▀██    ██  ██▄   ▄██ ██    ██    ██ ██   ██   ██   ██    ██  █▄   ██ ║
║ █▀█████▀  ▀████▀███▄ █▀█████▀          ▀████▀███▄ ▀█████▀▄████  ████  ████▄████▀██▄████▄████  ████▄██████▀ ║
║                                                                                                            ║
║                                     By: VicenteRC-DEV | Versión: 2.0                                       ║
║                                                                                                            ║
╚════════════════════════════════════════════════════════════════════════════════════════════════════════════╝
{Style.RESET_ALL}"""
    print(banner)


def ensure_wordlist() -> list[str]:
    """Asegura que exista sub.txt con contenido válido."""
    path = Path("sub.txt")

    if not path.exists() or path.stat().st_size < 10:
        print(f"{Fore.YELLOW}[!] sub.txt no existe o está vacío.")
        print(f"{Fore.YELLOW}[!] Creando wordlist profesional por defecto...")
        with open(path, "w", encoding="utf-8") as f:
            f.write("# Wordlist de subdominios - un subdominio por línea\n")
            f.write("# Líneas que empiezan con # se ignoran\n\n")
            f.write("\n".join(DEFAULT_SUBDOMAINS) + "\n")
        print(f"{Fore.GREEN}[+] sub.txt creado correctamente ({len(DEFAULT_SUBDOMAINS)} subdominios).")

    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        subs = [
            line.strip().lower()
            for line in f
            if line.strip() and not line.strip().startswith("#")
        ]

    # Eliminar duplicados manteniendo orden
    seen = set()
    unique = []
    for s in subs:
        if s not in seen:
            seen.add(s)
            unique.append(s)

    return unique


def clean_domain(raw: str) -> str:
    """Limpia y normaliza el dominio ingresado por el usuario."""
    raw = raw.strip().lower()

    if not raw:
        return ""

    # Quitar protocolo si lo pega
    if "://" in raw:
        raw = urlparse(raw).netloc or raw.split("://")[-1]

    # Quitar path, query, etc.
    raw = raw.split("/")[0].split("?")[0].split("#")[0]

    # Quitar puerto
    raw = raw.split(":")[0]

    # Quitar www. inicial si lo puso
    if raw.startswith("www."):
        raw = raw[4:]

    return raw


def is_valid_domain(domain: str) -> bool:
    """Validación básica de dominio."""
    if not domain or "." not in domain:
        return False
    if " " in domain or len(domain) < 4:
        return False
    return True


def resolve_ip(hostname: str) -> Optional[str]:
    try:
        return socket.gethostbyname(hostname)
    except (socket.gaierror, socket.timeout):
        return None


def check_subdomain(sub: str, domain: str) -> dict:
    """Comprueba un subdominio de forma robusta."""
    full_host = f"{sub}.{domain}"
    result = {
        "subdomain": full_host,
        "alive": False,
        "status_code": None,
        "ip": None,
        "server": None,
        "cloudflare": False,
        "scheme": None,
    }

    # Resolver IP primero (más rápido filtrar)
    result["ip"] = resolve_ip(full_host)
    if result["ip"] is None:
        return result  # No tiene registro DNS → no tiene sentido seguir

    headers = {"User-Agent": USER_AGENT}

    # Intentar HTTPS primero
    for scheme in ("https", "http"):
        url = f"{scheme}://{full_host}"
        try:
            response = requests.get(
                url,
                timeout=TIMEOUT,
                allow_redirects=True,
                headers=headers,
                verify=True,
            )
            result["alive"] = True
            result["status_code"] = response.status_code
            result["server"] = response.headers.get("Server", "N/A")
            result["cloudflare"] = "cloudflare" in str(result["server"]).lower()
            result["scheme"] = scheme
            break
        except requests.exceptions.SSLError:
            continue
        except requests.exceptions.RequestException:
            continue
        except Exception:
            continue

    return result


def print_result(result: dict):
    """Imprime un resultado vivo de forma legible."""
    status = result["status_code"] or "???"
    status_color = Fore.GREEN if isinstance(status, int) and status < 400 else Fore.YELLOW

    ip = result["ip"] or "N/A"
    server = str(result["server"] or "N/A")[:24]
    cf = f" {Fore.CYAN}[Cloudflare]" if result["cloudflare"] else ""
    scheme = result["scheme"] or "?"

    print(
        f"{Fore.GREEN}[+] {result['subdomain']:<42} "
        f"{status_color}{status:<4} "
        f"{Fore.WHITE}{ip:<16} "
        f"{Fore.MAGENTA}{server:<24}"
        f"{Fore.BLUE}{scheme}{cf}"
    )


def main():
    # Limpiar terminal al iniciar
    clear_terminal()

    print_banner()

    # Mostrar información del dispositivo
    device = get_device_info()
    print(f"{Fore.CYAN}[*] Dispositivo detectado : {Fore.WHITE}{device}")
    print()

    print(f"{Fore.YELLOW}Ingresa el dominio a escanear (ejemplo: google.com)")
    raw_domain = input(f"{Fore.WHITE}>> ").strip()

    domain = clean_domain(raw_domain)

    if not domain:
        print(f"{Fore.RED}[!] No ingresaste ningún dominio.")
        sys.exit(1)

    if not is_valid_domain(domain):
        print(f"{Fore.RED}[!] Dominio inválido: '{domain}'")
        print(f"{Fore.RED}    Ejemplo válido: google.com / ejemplo.com.ar")
        sys.exit(1)

    print()
    subdomains = ensure_wordlist()

    print(f"{Fore.CYAN}[*] Dominio objetivo      : {Fore.WHITE}{domain}")
    print(f"{Fore.CYAN}[*] Subdominios a probar  : {Fore.WHITE}{len(subdomains)}")
    print(f"{Fore.CYAN}[*] Hilos concurrentes    : {Fore.WHITE}{THREADS}")
    print(f"{Fore.CYAN}[*] Timeout por request   : {Fore.WHITE}{TIMEOUT}s")
    print(f"{Fore.CYAN}[*] Archivo de resultados : {Fore.WHITE}{OUTPUT_FILE}")
    print()
    print(f"{Fore.YELLOW}[~] Iniciando escaneo...\n")

    alive = []
    total = len(subdomains)
    start_time = time.time()

    with ThreadPoolExecutor(max_workers=THREADS) as executor:
        futures = {
            executor.submit(check_subdomain, sub, domain): sub
            for sub in subdomains
        }

        completed = 0
        for future in as_completed(futures):
            completed += 1
            result = future.result()

            if result["alive"]:
                alive.append(result)
                print_result(result)

            # Barra de progreso
            percent = (completed / total) * 100
            bar_len = 30
            filled = int(bar_len * completed // total)
            bar = "█" * filled + "░" * (bar_len - filled)
            print(
                f"{Fore.BLUE}[{bar}] {completed}/{total} ({percent:.1f}%)",
                end="\r",
                flush=True,
            )

    elapsed = time.time() - start_time

    print("\n")
    print(f"{Fore.CYAN}{'═' * 72}")
    print(f"{Fore.GREEN}[✓] Escaneo finalizado")
    print(f"{Fore.CYAN}{'═' * 72}")
    print(f"{Fore.WHITE}    Subdominios vivos     : {Fore.GREEN}{len(alive)}")
    print(f"{Fore.WHITE}    Tiempo total          : {Fore.YELLOW}{elapsed:.2f} segundos")
    print(f"{Fore.WHITE}    Velocidad aproximada  : {Fore.YELLOW}{total / elapsed:.1f} checks/s")
    print(f"{Fore.CYAN}{'═' * 72}")

    if alive:
        alive.sort(key=lambda x: x["subdomain"])

        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            f.write(f"# Resultados vivos para: {domain}\n")
            f.write(f"# Fecha de escaneo: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("# Formato: subdomain | status | ip | server | scheme\n")
            f.write("#" + "=" * 70 + "\n")
            for r in alive:
                f.write(
                    f"{r['subdomain']} | {r['status_code']} | {r['ip']} | "
                    f"{r['server']} | {r['scheme']}\n"
                )

        print(f"{Fore.GREEN}[+] Resultados guardados en → {OUTPUT_FILE}")
    else:
        print(f"{Fore.RED}[-] No se encontraron subdominios vivos con la wordlist actual.")
        print(f"{Fore.YELLOW}    Tip: Agrega más subdominios a sub.txt y vuelve a ejecutar.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{Fore.RED}[!] Escaneo interrumpido por el usuario.")
        sys.exit(1)
    except Exception as e:
        print(f"\n{Fore.RED}[!] Error inesperado: {e}")
        sys.exit(1)
