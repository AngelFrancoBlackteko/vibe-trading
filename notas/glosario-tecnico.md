# Glosario técnico

| Término | Técnico | Simple | Fecha |
|---|---|---|---|
| Fork | Copia de un repositorio enlazada al original, en tu cuenta; GitHub conserva la relación para traer cambios y proponer PRs al origen. | Una copia que "recuerda" de dónde salió. Si el original es público, el fork también. | 2026-10-24 |
| Upstream | Remoto git que apunta al repositorio original del que se copió el código. | El enlace al repo de donde viene tu copia, para jalar sus actualizaciones. | 2026-10-24 |
| Licencia MIT | Licencia permisiva: permite usar, modificar, vender y redistribuir el código si conservas el aviso de copyright y la licencia. | Puedes hacer lo que quieras con el código mientras dejes el archivo LICENSE y el crédito. | 2026-10-24 |
| CVE | Common Vulnerabilities and Exposures: identificador público único de una vulnerabilidad conocida (ej. CVE-2026-113792). | Un "número de expediente" de un hueco de seguridad ya reportado. Si una dependencia tiene CVE, hay versión corregida. | 2026-10-24 |
| Loopback | Interfaz de red que apunta a la misma máquina (127.0.0.1 / localhost / ::1); el tráfico nunca sale del equipo. | Solo tú, desde tu propia computadora, puedes conectarte. Nadie en la red o en internet. | 2026-10-24 |
| 0.0.0.0 (bind all) | Escuchar en todas las interfaces de red del host, no solo loopback. | El servicio queda accesible desde la red local o internet, no solo desde tu máquina. Requiere auth. | 2026-10-24 |
| Paper trading | Modo de operación simulado: el sistema ejecuta la estrategia contra precios reales sin enviar órdenes a un broker. | Practicar con dinero de mentira pero mercado de verdad. Primer paso obligatorio antes de dinero real. | 2026-10-24 |
| Auditoría estática | Revisar código, dependencias y configuración sin ejecutar la aplicación (grep de secretos, pip-audit, npm audit, lectura de código). | Leer el código con lupa antes de usarlo, sin encenderlo. | 2026-10-24 |
| Lockfile (requirements-lock.txt / package-lock.json) | Archivo que fija versión exacta (y hash) de cada dependencia para instalaciones reproducibles. | La lista exacta de piezas con las que se probó el proyecto, para que no cambie sola. | 2026-10-24 |
| CI (Integración Continua) | Pipeline automático (GitHub Actions) que instala dependencias y corre tests/lint en cada push o PR. | Un robot que prueba todo el código cada vez que subes un cambio y te avisa si algo se rompió. | 2026-10-29 |
| Fast-forward / sync con upstream | Avanzar `main` al último commit del repo original cuando tu rama no tiene commits propios: no hay merge ni conflicto. | Ponerte al día con el original de un salto, sin mezclar ni reescribir nada. | 2026-10-29 |
