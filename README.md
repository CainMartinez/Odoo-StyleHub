# 💈 StyleHub - Sistema de Gestión para Peluquerías

<div align="center">

![Odoo Version](https://img.shields.io/badge/Odoo-18.0-purple?style=for-the-badge&logo=odoo)
![License](https://img.shields.io/badge/License-LGPL--3-blue?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.10+-green?style=for-the-badge&logo=python)
![Docker](https://img.shields.io/badge/Docker-Ready-blue?style=for-the-badge&logo=docker)

**Sistema integral de gestión para salones de peluquería y centros de estética**

</div>

---

## 📋 Descripción General

**StyleHub** es una solución completa desarrollada en Odoo 18.0 para la gestión integral de salones de peluquería y centros de estética. El sistema automatiza y optimiza todos los aspectos del negocio, desde la reserva de citas hasta la gestión de ventas y reportes analíticos.

### 🎯 Problema que Resuelve

Los salones de peluquería enfrentan desafíos diarios:
- ⏰ **Doble reserva de estilistas** por gestión manual
- 📊 **Falta de visibilidad** sobre citas y rendimiento
- 🔄 **Cálculo manual** de horarios y duraciones
- 📱 **Ausencia de presencia online** para reservas 24/7
- 💰 **Gestión desconectada** de servicios y ventas

**StyleHub resuelve estos problemas con:**
- ✅ Validación automática de disponibilidad
- ✅ Cálculo inteligente de horarios
- ✅ Portal web para reservas online
- ✅ Integración completa con ventas
- ✅ Sistema de fidelización VIP automático

---

## ✨ Características Principales

### 🎨 Gestión de Servicios
- Catálogo completo de servicios con precios y duraciones
- Iconos Font Awesome profesionales para cada tipo de servicio
- Categorización automática (cortes, tintes, mechas, tratamientos, etc.)
- Gestión de precios base con posibilidad de ajuste por cita

### 📅 Sistema de Citas Inteligente
- **Cálculo automático de hora de finalización** basado en servicios seleccionados
- **Prevención de conflictos**: Validación en tiempo real de disponibilidad de estilistas
- Vista de calendario con código de colores por estilista
- Vista Kanban organizada por estados (Borrador, Confirmada, Realizada, Cancelada)
- Múltiples servicios por cita con cálculo automático de totales
- Workflow completo: Borrador → Confirmada → Realizada → Cancelada

### 👥 Gestión de Estilistas
- Registro completo de empleados con datos de contacto
- Contador de citas asignadas por estilista
- Control de estilistas activos/inactivos
- Vista Kanban para gestión visual del equipo

### ⭐ Sistema VIP Automático
- **Detección automática de clientes frecuentes** (>5 citas completadas)
- Ribbon VIP visual en ficha de cliente
- Estadísticas de citas totales y completadas
- Badge destacado para identificación rápida

### 📊 Reportes y Análisis
- **Reporte de Citas Diarias** con selección de fecha
- Formato PDF profesional con datos completos:
  - Horarios, clientes, estilistas
  - Servicios realizados
  - Duraciones y precios
  - Total de citas y facturación del día
- Nomenclatura automática: `Citas-DD-MM-YYYY.pdf`
- Traducido completamente al español

### 💰 Integración con Ventas
- **Sincronización automática** servicio ↔ producto
- Creación automática de productos al crear servicios
- Actualización bidireccional de precios y descripciones
- Generación de presupuestos y pedidos de venta desde citas
- Facturación directa de servicios
- Historial de ventas preservado

### 🌐 Portal Web Público
- **Página de inicio** moderna y atractiva
- **Catálogo de servicios** con iconos y precios
- **Galería del equipo** con perfiles de estilistas
- **Sistema de reserva online** disponible 24/7
- Portal del cliente para ver historial de citas
- Diseño responsive optimizado para móviles

### 🎓 Tutorial Interactivo
- Wizard educativo de 6 pasos
- Barra de progreso visual
- Explicaciones detalladas de cada funcionalidad
- Navegación fluida entre pasos
- Diseño responsive y moderno

---

## 🏗️ Arquitectura Modular

El sistema está diseñado con arquitectura modular para máxima flexibilidad:

### 📦 **style_hub_base** - Módulo Base
**Dependencias**: `base`, `contacts`, `website`, `portal`

Funcionalidad principal del sistema:
- ✅ Modelos: Servicios, Citas, Líneas de Cita, Estilistas
- ✅ Vistas: Formularios, listas, calendario, kanban
- ✅ Lógica de negocio: Validaciones, cálculos automáticos
- ✅ Workflow de estados de citas
- ✅ Sistema VIP automático
- ✅ Interfaz completa en español

**Instalación**: Requerido (núcleo del sistema)

---

### 📊 **report_style_hub** - Módulo de Reportes
**Dependencias**: `style_hub_base`

Generación de informes y análisis:
- ✅ Wizard de selección de fecha
- ✅ Reporte PDF de citas diarias
- ✅ Filtros por fecha (pasado, presente, futuro)
- ✅ Formato profesional con totales
- ✅ Nomenclatura automática de archivos
- ✅ Traducción completa al español

**Instalación**: Opcional (recomendado para análisis)

---

### 💵 **style_hub_sales** - Integración con Ventas
**Dependencias**: `style_hub_base`, `sale_management`, `product`, `account`

Conexión con el sistema comercial de Odoo:
- ✅ Creación automática de productos desde servicios
- ✅ Sincronización bidireccional de datos
- ✅ Generación de presupuestos desde citas
- ✅ Conversión de citas a pedidos de venta
- ✅ Facturación de servicios
- ✅ Botón inteligente "Crear Presupuesto"

**Instalación**: Opcional (requerido para facturación)

---

### 🌐 **style_hub_website** - Portal Web
**Dependencias**: `style_hub_base`, `website`, `portal`

Presencia online y reservas públicas:
- ✅ Página de inicio con diseño moderno
- ✅ Catálogo de servicios público
- ✅ Galería del equipo de estilistas
- ✅ Sistema de reserva online
- ✅ Portal del cliente (historial de citas)
- ✅ CSS personalizado para branding
- ✅ JavaScript para interactividad

**Instalación**: Opcional (requerido para web pública)

---

### 🎓 **style_hub_tutorial** - Tutorial Interactivo
**Dependencias**: `style_hub_base`

Sistema educativo para usuarios:
- ✅ Wizard de 6 pasos educativos
- ✅ Barra de progreso visual
- ✅ Navegación fluida bilateral
- ✅ Diseño responsive
- ✅ Accesible desde menú principal
- ✅ CSS personalizado incluido

**Instalación**: Opcional (recomendado para nuevos usuarios)

---

## 🚀 Instalación

### Prerrequisitos
- Docker y Docker Compose instalados
- PostgreSQL 17 (incluido en docker-compose)
- Odoo 18.0 (incluido en docker-compose)

### Instalación Rápida

1. **Clonar el repositorio**
```bash
git clone <repository-url>
cd Odoo-StyleHub
```

2. **Configurar archivo de configuración**
```bash
cp config/odoo.conf.example config/odoo.conf
# Editar config/odoo.conf con tus ajustes si es necesario
```

3. **Iniciar los contenedores**
```bash
docker-compose up -d
```

4. **Acceder a Odoo**
- URL: `http://localhost:8069`
- Crear base de datos: `odoo_db`
- Instalar módulos en orden:
  1. `style_hub_base` (obligatorio)
  2. `report_style_hub` (opcional)
  3. `style_hub_sales` (opcional, si necesitas facturación)
  4. `style_hub_website` (opcional, para web pública)
  5. `style_hub_tutorial` (opcional, para tutorial)

### Actualizar Módulos

```bash
# Actualizar un módulo específico
docker-compose exec -T web odoo -d odoo_db -u style_hub_base --stop-after-init
docker-compose restart web

# Actualizar todos los módulos StyleHub
docker-compose exec -T web odoo -d odoo_db -u style_hub_base,report_style_hub,style_hub_sales,style_hub_website,style_hub_tutorial --stop-after-init
docker-compose restart web
```

---

## 🎯 Uso Básico

### 1️⃣ Configuración Inicial

#### Crear Servicios
1. Ir a **StyleHub → Configuración → Servicios**
2. Hacer clic en **CREAR**
3. Completar:
   - Nombre del servicio (ej: "Corte de Caballero")
   - Duración en horas (ej: 0.5 para 30 minutos)
   - Precio base (ej: 25 €)
   - Descripción (opcional)

#### Registrar Estilistas
1. Ir a **StyleHub → Configuración → Estilistas**
2. Hacer clic en **CREAR**
3. Completar datos del empleado:
   - Nombre
   - Email (opcional)
   - Teléfono (opcional)

### 2️⃣ Gestión de Citas

#### Crear una Cita
1. Ir a **StyleHub → Citas**
2. Hacer clic en **CREAR**
3. Seleccionar:
   - Cliente (crear nuevo o seleccionar existente)
   - Estilista disponible
   - Fecha y hora de inicio
4. En la pestaña **Servicios**:
   - Agregar servicios con el botón **+**
   - El sistema calcula automáticamente:
     - ✅ Hora de finalización
     - ✅ Duración total
     - ✅ Precio total
5. **Confirmar Cita** para bloquear el horario del estilista

#### Vista de Calendario
- Cambiar a vista **Calendario** para visualización temporal
- Código de colores por estilista
- Drag & drop para cambiar horarios (si no está confirmada)
- Prevención automática de conflictos

### 3️⃣ Generar Reportes

1. Ir a **StyleHub → Reportes → Citas Diarias**
2. Seleccionar fecha deseada
3. Hacer clic en **Imprimir Reporte**
4. Se descarga PDF: `Citas-DD-MM-YYYY.pdf`

### 4️⃣ Integración con Ventas (si está instalado)

1. Abrir una cita confirmada
2. Hacer clic en botón **Crear Presupuesto**
3. Se genera automáticamente con todos los servicios
4. Confirmar presupuesto → Pedido de venta
5. Crear factura desde el pedido

---

## 🔧 Configuración Avanzada

### Variables de Entorno (docker-compose.yml)

```yaml
environment:
  - HOST=db
  - PORT=5432
  - USER=odoo_user
  - PASSWORD=odoo_password
```

### Configuración de Odoo (config/odoo.conf)

```ini
[options]
addons_path = /mnt/extra-addons,/usr/lib/python3/dist-packages/odoo/addons
admin_passwd = admin
db_host = db
db_port = 5432
db_user = odoo_user
db_password = odoo_password
```

### Personalización de Servicios

Los servicios se categorizan automáticamente con iconos según palabras clave:

| Tipo | Palabras Clave | Icono |
|------|----------------|-------|
| Corte | corte, haircut, trim | ✂️ fa-scissors |
| Tinte | tinte, color, dye | 🎨 fa-paint-brush |
| Mechas | mechas, balayage, highlights | ✨ fa-star |
| Tratamiento | tratamiento, keratina | ❤️ fa-heart |
| Peinado | peinado, styling | 💇 fa-female |
| Barba | barba, beard | 👤 fa-user |

---

## 📚 Documentación

### Estructura del Proyecto

```
Odoo-StyleHub/
├── addons/
│   ├── style_hub_base/          # Módulo base
│   │   ├── models/               # Modelos Python
│   │   ├── views/                # Vistas XML
│   │   ├── security/             # Permisos
│   │   └── data/                 # Datos demo
│   ├── report_style_hub/         # Módulo de reportes
│   │   ├── wizard/               # Wizard de selección
│   │   ├── report/               # Templates de reporte
│   │   └── views/                # Vistas del módulo
│   ├── style_hub_sales/          # Integración ventas
│   │   ├── models/               # Extensiones de modelos
│   │   └── views/                # Vistas extendidas
│   ├── style_hub_website/        # Portal web
│   │   ├── views/                # Templates web
│   │   ├── static/src/css/       # Estilos
│   │   └── static/src/js/        # JavaScript
│   └── style_hub_tutorial/       # Tutorial
│       ├── wizard/               # Wizard tutorial
│       └── static/src/css/       # Estilos tutorial
├── config/
│   ├── odoo.conf                 # Configuración Odoo
│   └── odoo.conf.example         # Ejemplo configuración
├── docker-compose.yml            # Orquestación Docker
└── README.md                     # Esta documentación
```

### Modelos de Datos Principales

#### `stylehub.service`
- Servicios del salón (cortes, tintes, etc.)
- Campos: nombre, duración, precio base, descripción
- Sincronizado con `product.template` (si sales instalado)

#### `stylehub.appointment`
- Citas agendadas
- Campos: cliente, estilista, fecha/hora inicio/fin, estado, notas
- Estados: borrador, confirmada, realizada, cancelada
- Validación automática de conflictos

#### `stylehub.appointment.line`
- Líneas de servicio de una cita
- Campos: servicio, duración, precio
- Vinculada a cita padre

#### `stylehub.stylist`
- Empleados/estilistas del salón
- Campos: nombre, email, teléfono, activo
- Contador de citas asignadas

### API y Métodos Importantes

#### Citas

```python
# Buscar estilista disponible
appointment._find_available_stylist(start_datetime, duration_hours)

# Acciones de workflow
appointment.action_confirm()      # Confirmar cita
appointment.action_mark_done()    # Marcar como realizada
appointment.action_cancel()       # Cancelar
appointment.action_reset_to_draft()  # Volver a borrador
```

#### Servicios

```python
# Crear servicio (crea producto automáticamente si sales instalado)
service = env['stylehub.service'].create({
    'name': 'Mi Servicio',
    'duration': 1.5,  # horas
    'base_price': 50.0,
    'description': 'Descripción del servicio'
})
```

---

## 🤝 Contribución

Este proyecto fue desarrollado como parte de un sistema de gestión empresarial. Para contribuciones:

1. Fork del repositorio
2. Crear rama de feature (`git checkout -b feature/amazing-feature`)
3. Commit de cambios (`git commit -m 'Add amazing feature'`)
4. Push a la rama (`git push origin feature/amazing-feature`)
5. Abrir Pull Request

---

## 👨‍💻 Autor

**Caín Martínez**
- Website: [https://cain-dev.es](https://cain-dev.es)
- Email: contacto@cain-dev.es

---

## 🙏 Agradecimientos

- Comunidad Odoo por la plataforma
- Font Awesome por los iconos
- Bootstrap por el framework CSS
- PostgreSQL por la base de datos

---

<div align="center">

**💈 StyleHub - Transformando la gestión de salones de peluquería**

Hecho con Odoo 18.0

</div>
