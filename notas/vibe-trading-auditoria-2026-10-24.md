# Auditoría de seguridad — vibe-trading (copia privada de HKUDS/Vibe-Trading)

- Fecha: 2026-10-24
- Commit auditado: `41f333b6` (3,355 commits, igual al upstream)
- Repo: https://github.com/AngelFrancoBlackteko/vibe-trading
- Herramientas: pip-audit (Python), npm audit (frontend), grep de secretos en HEAD y en historial git, lectura manual de `agent/api_server.py`, `agent/src/api/security.py`, `docker-compose.yml`, `Dockerfile`.
- Alcance: código de terceros, ANTES de cargar llaves de broker/LLM. No se ejecutó la app.

## Veredicto

Usable, con 2 ajustes antes de poner llaves reales. El proyecto tiene buena higiene de seguridad
(auth con comparación constante, CORS cerrado a loopback, docker publica solo en 127.0.0.1,
redacción de secretos en logs). Nada crítico.

## Hallazgos

### MEDIO
1. **Dependencias Python con CVEs** (`requirements-lock.txt`):
   - `pypdf 6.19.0` → 11 CVEs (fix: 6.21.2). Riesgo real solo si el agente procesa PDFs de origen no confiable.
   - `fastmcp 3.4.7` → GHSA-7xgj-8392-5q4r (fix: 3.4.10). Afecta al servidor MCP.
   - `opentelemetry-api 1.45.0` → CVE-2026-114603 (fix: 1.45.1).
   - `brotli 1.2.0` → 2 avisos (fix: 1.2.1).
   Acción: actualizar antes de usar, o esperar a que upstream lo haga y hacer `git pull upstream main`.

2. **Comando legacy `serve` escucha en todas las interfaces** (`agent/cli/_legacy.py:5573`, default `0.0.0.0`).
   El comando moderno (`agent/src/api/server_cli.py:20`) usa `127.0.0.1`. Si por error se usa el legacy sin
   `API_AUTH_KEY`, cualquiera en la red local solo recibe 403 (hay guard), pero igual expone superficie.
   Acción: definir SIEMPRE `API_AUTH_KEY` en `agent/.env`.

### LEVE
3. `katex` (frontend) — prototype pollution, severidad baja. Solo renderizado de fórmulas.
4. El Dockerfile arranca con `--host 0.0.0.0` dentro del contenedor; es correcto porque compose
   publica solo en `127.0.0.1:8899`. No cambiar el `ports:` de compose a `0.0.0.0`.

### OK (verificado)
- Sin secretos reales en HEAD ni en historial git. Los tokens encontrados son fixtures de tests (`xoxb-dummy`, `AKIAIOSFODNN7EXAMPLE`).
- Sin `.env`, `.pem`, `.key` trackeados. `.env` está en `.gitignore`.
- Auth: `hmac.compare_digest` contra `API_AUTH_KEY`; sin llave solo acepta loopback; rechaza llave en query string.
- CORS: solo orígenes loopback por default.
- Settings de credenciales requieren auth explícita (`require_settings_write_auth`).

## Antes de usar con dinero real
1. `agent/.env` con `API_AUTH_KEY` largo y aleatorio.
2. Actualizar pypdf / fastmcp / opentelemetry-api / brotli.
3. Empezar con paper trading; revisar qué proveedor LLM recibe los datos de tu cuenta de broker.
4. No cambiar los `ports:` de compose a `0.0.0.0`.
