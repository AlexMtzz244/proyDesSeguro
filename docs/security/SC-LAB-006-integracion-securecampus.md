# SC-LAB-006 → SecureCampus: validadores, permisos y pruebas en la app real

El laboratorio (`docs/security/SC-LAB-006-securecampus/`, Flask + pytest) deja
tres piezas. Este documento registra cómo se trasladaron a la aplicación real
(`AppDesarrolloSeguro`, NestJS + Zod + Prisma) y qué hallazgos salieron en el
camino.

## Equivalencias

| Laboratorio (Python) | Aplicación (TypeScript) | Pruebas |
|---|---|---|
| `src/validators.py` → `validar_calificacion` | `packages/contracts/src/validadores.ts` (`tieneMaximoDosDecimales`, `parsearCalificacionTexto`) y `esquemaValorCalificacion` en `calificaciones.ts` | `packages/contracts/src/validadores.spec.ts` |
| `src/permissions.py` → `puede_modificar`, `puede_consultar` | `apps/api/src/autorizacion/permisos-calificacion.ts` (`puedeModificarCalificacion`, `puedeConsultarCalificacion`, `puedeCorregirCalificacion`, `asignacionEsVigente`) | `apps/api/src/autorizacion/permisos-calificacion.spec.ts` |
| `tests/test_security.py` | las dos specs anteriores (reglas puras) + integración contra Postgres real | `apps/api/test/calificaciones.int.spec.ts` |

Como en el laboratorio, las reglas de permiso son **funciones puras**: reciben
hechos ya resueltos (asignación vigente, periodo abierto, inscripción) y
devuelven la decisión. Los resolvedores de `relaciones.ts` hacen la consulta a
Prisma y delegan en ellas, de modo que cada regla se prueba con una tabla de
verdad sin base de datos. El comportamiento externo no cambió.

## Hallazgos del diagnóstico

1. **El esquema compartido dejaba pasar `1e-7` y `5e-324`.** Se usaba
   `z.number().min(0).max(100).multipleOf(0.01)`; el `multipleOf` de Zod 3 usa
   aritmética de flotantes. La columna es `Decimal(5,2)`, así que Postgres
   habría redondeado a `0.00` en silencio: una nota guardada que nadie
   capturó. Comprobado antes de corregir:
   `1e-7 → true`, `5e-324 → true`. Ahora se valida sobre la representación
   textual (`/^\d+(\.\d{1,2})?$/`) y se **rechaza**, nunca se redondea.
2. **El validador del navegador rechazaba notas válidas y aceptaba formatos
   raros.** `Math.round(n*100) === n*100` da falso para `0.07` y `1.1`, y
   `Number('0x10')` / `Number('1e1')` pasaban. Ahora el formulario de captura y
   el de corrección usan `parsearCalificacionTexto`, la misma regla que el
   servidor, con un mensaje distinto por causa.
3. **Las reglas de permiso de calificaciones solo se podían probar con base de
   datos.** Estaban mezcladas con las consultas. Ahora tienen pruebas
   unitarias, incluidos los límites de vigencia (`hastaEl === ahora` ya no es
   vigente; una asignación futura aún no cuenta).

## Cómo ejecutarlo

```bash
pnpm install --frozen-lockfile
pnpm typecheck && pnpm lint && pnpm test      # contracts 79 · api 51
pnpm test:int                                 # 7 archivos · 105 pruebas (requiere Postgres y Redis)
```

Resultado de la última ejecución: unitarias, `typecheck` y `lint` en verde en
los tres paquetes; integración 105/105.

## Alcance

La API del laboratorio no incluía MFA ni rate limiting; la aplicación sí los
tiene y no se tocaron. No se cambió la regla de negocio de la escala 0–100
(decisión D-03, pendiente de la dirección académica).
