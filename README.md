# SecureCampus — Documentación

Documentación del proyecto **SecureCampus**, sistema web académico desarrollado
para el curso **Desarrollo Seguro**.

Este repositorio contiene únicamente la documentación: los manuales de las
prácticas, los análisis de seguridad, las decisiones de arquitectura y el
material de operación.

> **El código de la aplicación está en
> [AppDesarrolloSeguro](https://github.com/AlexMtzz244/AppDesarrolloSeguro).**

## Equipo

| Integrante | Matrícula |
|---|---|
| Cesar Adan De La Cruz Moctezuma | _(completar)_ |
| Diego Salazar Reyes | _(completar)_ |
| Juan Pablo Castillo Angeles | _(completar)_ |
| Alejandro Martínez | _(completar)_ |

| | |
|---|---|
| **Curso** | Desarrollo Seguro |
| **Docente** | Isc. Marelis Carrillo Lara |
| **Ciclo** | Septiembre 2026 |

---

## Los dos repositorios

| Repositorio | Contiene |
|---|---|
| **proyDesSeguro** (este) | Manuales Word de las prácticas, análisis SC-LAB / SC-SRS, ADR, decisiones pendientes y manual de operación. |
| [**AppDesarrolloSeguro**](https://github.com/AlexMtzz244/AppDesarrolloSeguro) | El código: API (NestJS · Prisma), web (Next.js), contratos compartidos, infraestructura y CI. |

---

## La idea que atraviesa todo el proyecto

De [SC-LAB-001 §1](docs/security/SC-LAB-001-analisis-inicial.md):

> En los cuatro roles el alcance no está definido por el rol solamente, sino
> por la **relación entre el usuario y el recurso concreto** (mi perfil, mi
> grupo, mi documento). Un sistema que verifique únicamente el rol y no esa
> relación quedará expuesto, aunque la autenticación funcione perfectamente.

Todo el diseño del servidor sale de ahí. Y su corolario, descubierto al
analizar al jefe de carrera: **si un control se apoya en un dato, ese dato
hereda la criticidad del control**.

---

## Contenido

```
proyDesSeguro/
└── docs/
    ├── security/          SC-LAB-001..003 y SC-SRS-001
    ├── adr/               ADR-001..008
    ├── DECISIONES-PENDIENTES.md
    ├── OPERACION.md
    └── *.docx             Manuales de alumno de cada práctica
```

### Análisis previo a la implementación

| Práctica | Pregunta que responde | Documento | Manual |
|---|---|---|---|
| **SC-LAB-001** | ¿Qué puede salir mal? | [Análisis inicial](docs/security/SC-LAB-001-analisis-inicial.md) | [Word](docs/SC_LAB_001_Manual_Alumno_Analisis_Inicial_Seguridad_v1.0.docx) |
| **SC-LAB-002** | ¿En qué fase se actúa? | [Mapa Secure SDLC](docs/security/SC-LAB-002-secure-sdlc-map.md) | [Word](docs/SC_LAB_002_Manual_Alumno_Secure_SDLC.docx) |
| **SC-LAB-003** | ¿Qué cuesta descubrirlo tarde? | [Costo y Shift Left](docs/security/SC-LAB-003-shift-left-analysis.md) | [Word](docs/SC_LAB_003_Manual_Alumno_Shift_Left_v1.0.docx) |
| **SC-SRS-001** | ¿Qué debe hacer, y qué no debe permitir? | [Requisitos](docs/security/SC-SRS-001-requisitos-aplicacion.md) | — |

### Decisiones de arquitectura

| ADR | Tema |
|---|---|
| [001](docs/adr/ADR-001-autorizacion-por-relacion.md) | Autorización por relación y *deny by default* |
| [002](docs/adr/ADR-002-sesion-opaca.md) | Sesión opaca en cookie, no JWT |
| [003](docs/adr/ADR-003-auditoria-append-only.md) | Auditoría append-only y atómica |
| [004](docs/adr/ADR-004-argon2-y-cifrado-totp.md) | Argon2id y cifrado del secreto TOTP |
| [005](docs/adr/ADR-005-monorepo-y-frontera.md) | Monorepo y frontera web↔api |
| [006](docs/adr/ADR-006-asignacion-docente-versionada.md) | Asignación docente versionada |
| [007](docs/adr/ADR-007-entrega-privada-documentos.md) | Entrega privada de documentos |
| [008](docs/adr/ADR-008-alertas-y-umbrales.md) | Alertas y umbrales |

### Operación

- [**Decisiones pendientes**](docs/DECISIONES-PENDIENTES.md) — once decisiones
  que corresponden a la institución, no al equipo. El sistema propone un valor
  para cada una y funciona con él, pero la propuesta es **visible** en
  `/panel/decisiones`, **atribuible** al firmarse, y **exigible**: el arranque
  en producción falla mientras D-06, D-07 o D-10 sigan sin firma.
- [**Operación e incidentes**](docs/OPERACION.md) — SLA, respuesta, respaldos,
  endurecimiento.

---

## Convenciones

- Documentación en español, en `docs/`. Los análisis de seguridad en
  `docs/security/` con el identificador de la práctica en el nombre.
- Antes de cada commit: `git status`, `git diff`, `git add`, `git diff --staged`.
- Mensajes con prefijo de tipo: `docs: agregar analisis inicial SC-LAB-001`.
- Los cambios de código van en
  [AppDesarrolloSeguro](https://github.com/AlexMtzz244/AppDesarrolloSeguro), no aquí.
