# Ficha de Sistematización — Espiral 1
## ERP Django · Espiral E1: Infraestructura y Configuración Base
## UTEC Celaya · Técnico en Programación (SEP 3061300006-23)

| Campo | Contenido |
|---|---|
| **Número de espiral** | 1 |
| **Nombre del ciclo** | Infraestructura y Configuración Base |
| **Semanas** | W01 – W03 |
| **Fecha de inicio** | ___/___/_____ |
| **Fecha de cierre** | ___/___/_____ |
| **Responsable** | [Nombre del estudiante] |
| **Asesor** | MC. Román Fernando López González |

---

## 1. Objetivo del ciclo

Establecer el entorno de desarrollo portable en USB y desplegar el
proyecto Django base en Render.com, de modo que cualquier avance
posterior tenga una URL pública verificable desde el inicio del proyecto.

---

## 2. Tareas realizadas

| # | Tarea | Estado | Tiempo invertido |
|---|---|---|---|
| 1 | Configurar Python 3.11 embeddable en USB | ✅ | h:mm |
| 2 | Instalar pip y virtualenv | ✅ | h:mm |
| 3 | Configurar Git Portable | ✅ | h:mm |
| 4 | Crear scripts iniciar/finalizar sesión | ✅ | h:mm |
| 5 | Crear proyecto Django con 5 apps | ✅ | h:mm |
| 6 | Sistema de templates Fable 5 AzulERP | ✅ | h:mm |
| 7 | Configurar WhiteNoise y estáticos | ✅ | h:mm |
| 8 | Completar settings_prod.py con PostgreSQL | ✅ | h:mm |
| 9 | Crear Procfile, Dockerfile, docker-compose.yml | ✅ | h:mm |
| 10 | Crear render.yaml | ✅ | h:mm |
| 11 | Desplegar en Render.com → URL pública | ✅ | h:mm |
| 12 | Ejecutar Sprint 0 Review y Retrospectiva | ✅ | h:mm |

---

## 3. Evidencias generadas

- [ ] Repositorio GitHub: https://github.com/sjaguilary2528-beep/erp-django-utec.git
- [ ] URL pública Render: https://erp-django-utec-samara.onrender.com
- [ ] Captura de pantalla: `evidencias/espiral_01/render_url.png`
- [ ] Captura de pantalla: `evidencias/espiral_01/manage_check.png`
- [ ] Resultado de tests: Ran 35 tests in 1.296s OK
- [ ] Commit de cierre: [main 0f3428f] Sprint 0 CIERRE [M1]: Render.com desplegado + 33 tests OK + Ficha Schmelkes E1
 14 files changed, 1010 insertions(+), 121 deletions(-)
 delete mode 100644 Fichas/espiral_01_infra.md
 create mode 100644 evidencias/Captura de pantalla 2026-10-17 225545.png
 create mode 100644 evidencias/Captura de pantalla 2026-10-17 225654.png
 create mode 100644 evidencias/Captura de pantalla 2026-10-17 225738.png
 create mode 100644 "evidencias/Inicio \302\267 UTEC Celaya.html"
 create mode 100644 "evidencias/Inicio \302\267 UTEC Celaya_files/bootstrap.bundle.min.js.descarga"
 create mode 100644 "evidencias/Inicio \302\267 UTEC Celaya_files/bootstrap.min.css"
 create mode 100644 "evidencias/Inicio \302\267 UTEC Celaya_files/css2"
 create mode 100644 evidencias/espiral_01
 create mode 100644 sprint0_retrospective.md
 create mode 100644 tests/test_w03_deploy.py
---

## 4. Criterios de aceptación verificados

| Criterio | ¿Cumplido? | Evidencia |
|---|---|---|
| `manage.py check --deploy` sin warnings críticos | ✅ / ❌ | Captura de terminal |
| URL pública `https://…onrender.com/` → HTTP 200 | ✅ / ❌ | Captura del navegador |
| Repositorio con ≥ 6 commits en rama `main` | ✅ / ❌ | `git log --oneline` |
| 33 tests pasando (W01 + W02 + W03) | ✅ / ❌ | Resultado pytest |
| Ficha Schmelkes E1 completa | ✅ / ❌ | Este documento |

---

## 5. Problemas encontrados y soluciones

| Problema | Causa | Solución aplicada |
|---|---|---|
| | | |
| | | |
b7afaf9 (HEAD -> main, origin/main) Corregir variables del superusuario
48ea360 Actualizar configuracion para produccion
7bcbc0c Crear superusuario para produccion
b094e23 Merge con remoto, conservar versiones locales
806bdea Fix settings_prod y render.yaml para Render
---

## 6. Lecciones aprendidas

1.
2.
3.

---

## 7. Tiempo total invertido

| Categoría | Horas |
|---|---|
| Diseño / planeación | |
| Implementación | |
| Pruebas | |
| Despliegue | |
| Documentación | |
| **Total Espiral 1** | |

---

## 8. Conexión con el trabajo recepcional

> Esta espiral aporta evidencia para el **Capítulo 4** (Desarrollo),
> sección 4.1 "Espiral 1: Infraestructura", y para el
> **Capítulo 3** (Metodología), subsección "Ciclos del modelo espiral".
