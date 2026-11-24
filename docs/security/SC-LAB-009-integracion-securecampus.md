# SC-LAB-009 → SecureCampus: SAST, imágenes que construyen y Trivy en CI

El laboratorio usa un proyecto Flask del docente (pytest, Bandit, pip-audit, Trivy). Ese paquete no estaba disponible al
entregar, así que los controles se aplicaron a la aplicación real (`AppDesarrolloSeguro`, TypeScript). Lo que no se pudo
verificar está declarado en el Word y al final de este documento. Después llegó el ZIP y se ejecutó: 22 pruebas aprobadas,
Bandit y pip-audit sin hallazgos, imagen construida. El pipeline del ZIP también corrió en GitHub Actions: el trabajo
`security` pasó y el trabajo `container` quedó **rojo**, porque Trivy halló 5 vulnerabilidades HIGH (con corrección) en paquetes
Python de la imagen (msgpack, setuptools, urllib3). Evidencia en `SC-LAB-009-evidencias/zip-docente/`; el detalle, incluidos los
cambios que hubo que hacer al workflow del ZIP para que corriera, está en `github_actions_pipeline.txt`.

## Qué se aplicó

| El laboratorio pide | En SecureCampus | Dónde |
|---|---|---|
| `pytest -q` | `pnpm test` (204 unitarias) y `pnpm test:int` (120 de integración con Postgres y Redis) | ya existían; +25 pruebas nuevas |
| `bandit -r src -ll -ii` (SAST) | **Cambio:** `pnpm sast` con eslint-plugin-security, configuración aparte de `pnpm lint` | `eslint.seguridad.config.mjs` |
| `pip-audit` (SCA) | `pnpm audit --prod --audit-level=high`: documentado, sin tocar | `ci.yml` (job `dependencias`) |
| Leer el pipeline YAML | **Cambio:** workflow nuevo con los trabajos `sast` y `contenedor` | `.github/workflows/sc-lab-009-devsecops.yml` |
| `docker build` + Trivy | **Cambio:** las imágenes ahora sí construyen; Trivy fijado por digest, informe y compuerta | `apps/*/Dockerfile`, workflow |
| `USER`, `read_only`, `cap_drop`, `127.0.0.1` | Ya estaban (SC-LAB-008); se verificaron en ejecución | `docker-compose.yml`, `contenedores.spec.ts` |

## Hallazgos

1. **SAST: 20 alertas, 4 reales.** `sanear` (bitácora) perdía la clave `__proto__`; `agruparPorCampo` (API y web) lanzaba
   `TypeError` con claves como `constructor`. Las pruebas fallaban antes de corregir (`evidencias/hallazgo_pruebas_antes.txt`).
   Las otras 16 se justificaron una por una en el código; las dos regex se midieron con una entrada de 200 000 caracteres.
2. **Ninguna imagen de producción se había construido.** Salieron nueve fallos (postinstall de `contracts` y de Prisma sin
   su código, `pnpm prune` sin TTY y que deja `node_modules` vacío, API y web sin los módulos de `contracts` y de Next.js,
   la imagen de la API cargaba también la web, npm con CVE altas). Tabla completa en el Word, sección 8.
3. **Trivy.** Web limpia; API con tres CVE de dependencias (`body-parser`, `effect`, `multer`) que coinciden con `pnpm audit`.
   Hay además 38 hallazgos de Debian sin corrección publicada (uno CRITICAL, `zlib1g` CVE-2023-45853, `will_not_fix`):
   quedan en el informe y fuera de la compuerta (`--ignore-unfixed`).
4. **`pnpm audit` sigue en rojo:** 4 altas (`zod`, `body-parser`, `multer`, `effect`) y 7 moderadas. Todas tienen versión
   corregida; `zod` exige migrar a la versión 4. Decisión pendiente del equipo.

## Cómo ejecutarlo

```bash
pnpm install --frozen-lockfile
pnpm lint && pnpm typecheck && pnpm sast && pnpm test
docker build --target produccion -f apps/api/Dockerfile -t securecampus-api:lab009 .
docker build --target produccion --build-arg NEXT_PUBLIC_API_URL=https://api.campus.ejemplo.mx \
  -f apps/web/Dockerfile -t securecampus-web:lab009 .
docker run --rm -v /var/run/docker.sock:/var/run/docker.sock \
  aquasec/trivy@sha256:8f6bb947dbc528902e11f2f5be52f7b519f6a39d5d148f41166f2040499768fb \
  image --severity HIGH,CRITICAL --ignore-unfixed securecampus-api:lab009
```

## Límites

- El entorno donde se ejecutó usa un proxy con certificado propio: las imágenes se construyeron con Dockerfiles temporales
  idénticos salvo por una variable de certificado, y los contenedores con red del anfitrión. El job de GitHub construye con
  los Dockerfile tal cual están en el repositorio.
- La API no llega a escuchar en un contenedor de producción mientras haya decisiones institucionales sin firmar
  (`DECISIONES-PENDIENTES.md`); es el comportamiento previsto.
- Prisma avisa que no detecta OpenSSL en la imagen `slim`; una consulta real desde la imagen funcionó. No se pudo instalar
  OpenSSL para comparar (el entorno no alcanza los repositorios de Debian).
- Las etapas de desarrollo siguen como root y la imagen web aún lleva todo `node_modules`.
