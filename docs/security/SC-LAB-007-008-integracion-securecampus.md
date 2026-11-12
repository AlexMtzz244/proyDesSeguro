# SC-LAB-007 y SC-LAB-008 → SecureCampus: matriz HTTP, CSRF, sesión y contenedores

Los dos laboratorios usan una aplicación Flask del docente (REST, GraphQL, simulador móvil, Docker). Ese paquete
no estuvo disponible para el equipo, así que las experiencias se ejecutaron contra la aplicación real
(`AppDesarrolloSeguro`, NestJS + PostgreSQL + Redis). Lo que no se ejecutó está declarado en cada Word.

## Qué se aplicó

| Laboratorio | Qué pide la guía | En SecureCampus | Dónde |
|---|---|---|---|
| 007 A–C | 200 / 403 / 401 / 400 según el recurso, no solo la sesión | Ya cumplía; se fijó con una matriz de pruebas y un script contra la API real | `apps/api/test/sc-lab-007-008.int.spec.ts`, `apps/api/scripts/casos-http-lab007.ts` |
| 007 §11 | El PUT exige token CSRF | **Cambio:** verificación de `Origin` / `Sec-Fetch-Site` en toda petición que cambia estado | `apps/api/src/autorizacion/origen.guard.ts` |
| 007 D | GraphQL con autorización | No aplica: la app no expone GraphQL | — |
| 008 paso 4 | Nada de secretos en `localStorage` | Ya cumplía (cookie HttpOnly); se fijó con una prueba | `apps/web/src/lib/almacenamiento.spec.ts` |
| 008 paso 6 | HTTP solo en local, HTTPS en producción | Ya cumplía; se fijó con una prueba | `apps/api/src/config/entorno.spec.ts` |
| 008 pasos 7–8, 12 | USER no root, `read_only`, `cap_drop`, `no-new-privileges`, tmpfs, puerto en 127.0.0.1, sin BD/secretos en la imagen | **Cambio:** perfil `endurecido` en el compose y `.dockerignore` | `docker-compose.yml`, `.dockerignore`, `apps/api/src/config/contenedores.spec.ts` |

## Hallazgos

1. **CSRF sin defensa del servidor.** Solo existía `SameSite=Lax`. Antes del cambio, una petición con sesión válida y
   `Origin` ajeno modificó una calificación (201, valor 91), inició sesión (200) y cerró la sesión de otra persona
   (204). Ahora las tres responden 403 y no cambian nada (`evidencias/casos_http_antes.txt` y `casos_http_despues.txt`).
2. **Sin `.dockerignore`.** Los Dockerfile hacen `COPY . .`; el `.env` con secretos entraba al contexto de build.
3. **Sin controles de contenedor en tiempo de ejecución** (`read_only`, `cap_drop`, `no-new-privileges`, tmpfs).
4. **Pendiente:** las etapas de desarrollo de `api` y `web` siguen corriendo como root (montan el código del host).

## Cómo ejecutarlo

```bash
pnpm install --frozen-lockfile
pnpm typecheck && pnpm lint && pnpm test      # contracts 79 · api 96 · web 4
pnpm test:int                                 # 8 archivos · 120 pruebas (Postgres y Redis)
pnpm db:seed && pnpm --filter api lab:casos-http   # con la API en marcha y SESION_COOKIE_SECURE=false
```

## Límites

- El perfil `endurecido` está verificado con `docker compose config` y pruebas de configuración. **No se arrancó ningún
  contenedor**: el entorno de trabajo no tenía motor Docker. Debe probarse con Docker Desktop.
- La imagen de producción exige HTTPS y un CAPTCHA real, por lo que no se levanta por HTTP en localhost.
- `pnpm audit --prod` sigue en rojo en `main` por `zod < 4.6.6` y otras dependencias; no se tocó en este cambio.
