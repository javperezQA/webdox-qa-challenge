# Test Plan – Descuento Inteligente 2.0 (Smart Discount)

**Autor:** Javier Perez Sierra  
**Fecha:** 2026-01-14  
**Contexto:** Desafío Técnico QA Engineer – Webdox  

---

## 1. Supuestos

Para efectos de este plan de pruebas, se establecen los siguientes supuestos:

1. **Asistencia válida**: solo se considera el registro presencial de ingreso al gimnasio (check-in físico). Las reservas de clases no cuentan como asistencia.
2. **Ventana de 30 días**: el cálculo de asistencias de “últimos 30 días” utiliza la zona horaria del gimnasio. Para este desafío se asume `America/Santiago (GMT-3)`.
3. **Vencimiento < 7 días**: se interpreta como `<= 7 días`, incluyendo el día 7 exacto.
4. **Plan activo**: solo socios con suscripción en estado `ACTIVE` y no vencida al momento de la evaluación.
5. **No acumulable**: cualquier promoción o beneficio activo bloquea la aplicación del descuento inteligente.
6. **Deuda pendiente**: si el socio registra deuda al momento de ejecutar la lógica, no es elegible.
7. **Cuenta corporativa**: existe un atributo identificable (ej. `is_corporate=true`) para excluir estos usuarios.
8. **Regla de 60 días**: se valida contra el historial de ofertas del socio, independiente del tipo de plan.
9. **Plan en pareja**: ambos miembros deben cumplir la condición de inactividad (<3 asistencias) para aplicar el 30%.
10. **Plan familiar**: se asume condición por miembro (todos con <3 asistencias), dado el conflicto con la regla R4.
11. **API externa**: si falla o excede 3 segundos, se registra el error en `/api/v2/logs/errors` y no se considera oferta creada.
12. **valid_until**: proviene de la configuración de la campaña; si no existe, se asume el fin del ciclo de renovación.
13. **Promociones activas**: se asume que descuentos por campañas especiales (ej. Black Friday, Navidad) bloquean el descuento inteligente.

---

## 2. Análisis del Requerimiento

### 2.1 Objetivo de negocio
Reducir la tasa de cancelación y abandono de socios con baja actividad, incentivando la renovación mediante un descuento automático aplicado bajo reglas de negocio estrictas.

### 2.2 Alcance
- Planes: **Mensual y Trimestral**
- Rol elegible: **Socio**
- Feature flag global: `smart_discount_enabled`
- Integraciones:
  - API externa de marketing
  - API interna de beneficios
- Registro de eventos y errores

### 2.3 Fuera de alcance
- Ejecución real de pagos
- Cambios de precios o planes fuera del flag
- Modificación manual de descuentos por admin
- Canales no especificados (SMS, push)

### 2.4 Ambigüedades / inconsistencias
- **Plan familiar**: la tabla de planes indica condición por miembro, mientras que la regla R4 menciona promedio grupal.
- **Límite de 7 días**: no se especifica si incluye el día exacto.
- **Promociones activas**: no se define el origen del dato.
- **R6 vs plan familiar**: R6 indica que planes automáticos no deberían tener descuento, pero el plan familiar es automático y tiene condiciones descritas.

### 2.5 Riesgos
1. Aplicación incorrecta del descuento (impacto financiero).
2. Duplicación de ofertas (incumplimiento regla 60 días).
3. Fallas o latencia de la API externa.
4. Cálculo incorrecto de asistencias o fechas.
5. Estados o logs inconsistentes que dificulten trazabilidad.

---

## 3. Plan de Pruebas

### 3.1 Estrategia
- Pruebas funcionales (reglas de elegibilidad y cálculo).
- Pruebas negativas (exclusiones).
- Pruebas de integración (API externa, beneficios, logs).
- Pruebas de roles y permisos.
- Pruebas no funcionales básicas (timeout, manejo de errores).

### 3.2 Riesgos principales
- Descuentos aplicados fuera de regla.
- Ofertas duplicadas o sin `offer_id`.
- Dependencia de la API externa.
- Cálculo incorrecto de asistencias (reservas vs ingresos).

### 3.3 Criterios de entrada y salida

**Entrada**
- Feature flag `smart_discount_enabled` configurable.
- Datos de prueba: socios con distintos planes, asistencias, vencimientos, deuda, promociones, cuentas corporativas y ofertas previas.
- Endpoints disponibles:
  - `/api/v2/benefits/offers`
  - `/api/v2/logs/events`
  - `/api/v2/logs/errors`
  - API externa (o mock).

**Salida**
- Casos críticos y negativos principales aprobados.
- Sin defectos bloqueantes relacionados a elegibilidad, no acumulación, regla 60 días e integraciones.
- Evidencia trazable en logs y estados de ofertas.

---

## 4. Casos de Prueba

### 4.0 Flujo esperado (alto nivel)
1. Feature flag activo.
2. Socio con plan Mensual/Trimestral, estado ACTIVE y vencimiento <=7 días.
3. Menos de 3 asistencias presenciales en 30 días.
4. Cumple reglas de elegibilidad.
5. Se genera evento `SMART_DISCOUNT_TRIGGERED`.
6. POST a API externa con datos correctos.
7. Respuesta 201 + `offer_id`.
8. Registro en beneficios y logs.
9. Oferta visible como **PENDIENTE**.
10. Socio acepta y renueva → estado **ACEPTADA**.

---

### 4.1 Suite de Regresión (P0 – Smoke UI)
- TC_REG_01: Login Admin y acceso a vista de Ofertas.
- TC_REG_02: Login Socio y acceso a vista de renovación.
- TC_REG_03: Activar/Desactivar `smart_discount_enabled`.
- TC_REG_04: Listado de ofertas se renderiza correctamente.
- TC_REG_05: Filtros de ofertas funcionan.
- TC_REG_06: Acción “Generar ofertas” disponible.
- TC_REG_07: Renovación desde oferta pendiente mantiene consistencia.
- TC_REG_08: Logout redirige a login.

---

### 4.2 Casos Funcionales y Negativos (P1)

**Planes**
- TC_FUNC_01: Plan Individual elegible genera 20%.
- TC_FUNC_02: Plan Pareja (ambos inactivos) genera 30%.
- TC_NEG_01: Plan Pareja con un miembro activo no aplica.
- TC_FUNC_03: Plan Familiar (todos <3) aplica descuento (según supuesto).

**Flag y rol**
- TC_NEG_02: Flag OFF no ejecuta lógica.
- TC_SEC_01: Solo rol socio es elegible.

**Reglas excluyentes**
- TC_NEG_03: Deuda pendiente.
- TC_NEG_04: Cuenta corporativa.
- TC_NEG_05: Promoción activa.
- TC_NEG_06: Socio nuevo (<30 días).
- TC_NEG_07: Oferta en últimos 60 días.

**Alcance del plan**
- TC_NEG_08: Plan fuera de alcance.
- TC_NEG_09: Plan no ACTIVE.

**Bordes**
- TC_EDGE_01: 2 asistencias → elegible.
- TC_EDGE_02: 3 asistencias → no elegible.
- TC_EDGE_03: Vencimiento = 7 días → elegible.
- TC_EDGE_04: Vencimiento = 8 días → no elegible.
- TC_EDGE_05: Reservas sin ingreso no cuentan.

**Integración**
- TC_INT_01: API externa 201 crea oferta y logs.
- TC_NF_01: Timeout >3s registra error y no crea oferta.
- TC_INT_02: Error 4xx/5xx registra error.
- TC_INT_03: Ejecución duplicada no duplica ofertas.

---

## 5. Scripts de Prueba (UI)

El repositorio incluye tres scripts de prueba de interfaz desarrollados como ejemplo,
utilizando Playwright con Python y el patrón Page Object Model (POM).

Los scripts representan flujos críticos del negocio y están orientados a evidenciar
criterio de automatización, estructura y mantenibilidad del código.
