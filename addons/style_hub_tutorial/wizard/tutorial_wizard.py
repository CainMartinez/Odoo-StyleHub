# -*- coding: utf-8 -*-

from odoo import models, fields, api


class TutorialWizard(models.TransientModel):
    _name = 'stylehub.tutorial.wizard'
    _description = 'StyleHub Tutorial para Empleados'

    step = fields.Integer(
        string='Paso Actual',
        default=1,
        help='Paso actual del tutorial'
    )
    
    total_steps = fields.Integer(
        string='Total de Pasos',
        default=6,
        readonly=True
    )
    
    step_title = fields.Char(
        string='Título del Paso',
        compute='_compute_step_content',
        store=False
    )
    
    step_content = fields.Html(
        string='Contenido',
        compute='_compute_step_content',
        store=False
    )
    
    progress = fields.Float(
        string='Progreso',
        compute='_compute_progress',
        store=False
    )
    
    @api.depends('step', 'total_steps')
    def _compute_progress(self):
        """Calcular el progreso del tutorial"""
        for record in self:
            record.progress = (record.step / record.total_steps) * 100
    
    @api.depends('step')
    def _compute_step_content(self):
        """Contenido para cada paso del tutorial"""
        for record in self:
            content_map = {
                1: {
                    'title': '🎉 Bienvenido a StyleHub',
                    'content': '''
                        <div class="tutorial-intro">
                            <h2>¡Bienvenido al Sistema de Gestión de StyleHub!</h2>
                            <p class="lead">Este tutorial te guiará paso a paso para que aprendas a utilizar todas las funcionalidades del sistema.</p>
                            
                            <div class="feature-list">
                                <h4>¿Qué aprenderás?</h4>
                                <ul>
                                    <li><i class="fa fa-check-circle text-success"></i> Gestionar servicios del salón</li>
                                    <li><i class="fa fa-check-circle text-success"></i> Administrar estilistas y empleados</li>
                                    <li><i class="fa fa-check-circle text-success"></i> Crear y gestionar citas</li>
                                    <li><i class="fa fa-check-circle text-success"></i> Identificar clientes VIP</li>
                                    <li><i class="fa fa-check-circle text-success"></i> Usar el calendario de citas</li>
                                    <li><i class="fa fa-check-circle text-success"></i> Consejos y mejores prácticas</li>
                                </ul>
                            </div>
                            
                            <div class="alert alert-info mt-3">
                                <i class="fa fa-info-circle"></i>
                                <strong>Consejo:</strong> Puedes volver a este tutorial en cualquier momento desde el menú principal.
                            </div>
                        </div>
                    '''
                },
                2: {
                    'title': '💇 Gestión de Servicios',
                    'content': '''
                        <div class="tutorial-step">
                            <h3>1. Catálogo de Servicios</h3>
                            <p>Los servicios son la base de tu negocio. Aquí defines qué ofreces a tus clientes.</p>
                            
                            <div class="step-instructions">
                                <h4><i class="fa fa-arrow-right text-primary"></i> Cómo crear un servicio:</h4>
                                <div style="padding-left: 20px;">
                                    <p><strong>1.</strong> Ve a <strong>Configuración → Servicios</strong></p>
                                    <p><strong>2.</strong> Haz clic en <strong>Crear</strong></p>
                                    <p><strong>3.</strong> Completa los campos:</p>
                                    <ul style="list-style-type: disc; margin-left: 30px;">
                                        <li><strong>Nombre:</strong> Ej. "Corte de Caballero", "Tinte Completo"</li>
                                        <li><strong>Duración:</strong> En horas (0.5 = 30 min, 1.5 = 1h 30min)</li>
                                        <li><strong>Precio Base:</strong> Precio estándar del servicio</li>
                                        <li><strong>Descripción:</strong> Detalles adicionales (opcional)</li>
                                    </ul>
                                    <p><strong>4.</strong> Guarda el servicio</p>
                                </div>
                            </div>
                            
                            <div class="alert alert-warning">
                                <i class="fa fa-lightbulb-o"></i>
                                <strong>Tip Profesional:</strong> Define duraciones realistas. El sistema calculará automáticamente la hora de fin de cada cita.
                            </div>
                            
                            <div class="example-box">
                                <h5>Ejemplos de servicios comunes:</h5>
                                <table class="table table-sm">
                                    <thead>
                                        <tr>
                                            <th>Servicio</th>
                                            <th>Duración</th>
                                            <th>Precio Sugerido</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        <tr>
                                            <td>Corte Caballero</td>
                                            <td>0.5h (30 min)</td>
                                            <td>15€ - 25€</td>
                                        </tr>
                                        <tr>
                                            <td>Corte + Barba</td>
                                            <td>1h</td>
                                            <td>25€ - 35€</td>
                                        </tr>
                                        <tr>
                                            <td>Tinte Completo</td>
                                            <td>2h</td>
                                            <td>60€ - 100€</td>
                                        </tr>
                                        <tr>
                                            <td>Mechas Balayage</td>
                                            <td>3h</td>
                                            <td>100€ - 150€</td>
                                        </tr>
                                    </tbody>
                                </table>
                            </div>
                        </div>
                    '''
                },
                3: {
                    'title': '👥 Gestión de Estilistas',
                    'content': '''
                        <div class="tutorial-step">
                            <h3>2. Administración de Estilistas</h3>
                            <p>Registra a todos los empleados que atenderán citas en el salón.</p>
                            
                            <div class="step-instructions">
                                <h4><i class="fa fa-arrow-right text-primary"></i> Cómo registrar un estilista:</h4>
                                <div style="padding-left: 20px;">
                                    <p><strong>1.</strong> Navega a <strong>Configuración → Estilistas</strong></p>
                                    <p><strong>2.</strong> Pulsa <strong>Crear</strong></p>
                                    <p><strong>3.</strong> Rellena la información:</p>
                                    <ul style="list-style-type: disc; margin-left: 30px;">
                                        <li><strong>Nombre:</strong> Nombre completo del estilista</li>
                                        <li><strong>Email:</strong> Para contacto interno</li>
                                        <li><strong>Teléfono:</strong> Número de contacto</li>
                                        <li><strong>Activo:</strong> Marcado por defecto (desmarca si ya no trabaja)</li>
                                    </ul>
                                    <p><strong>4.</strong> Guarda el registro</p>
                                </div>
                            </div>
                            
                            <div class="info-box bg-light p-3 rounded">
                                <h5><i class="fa fa-star text-warning"></i> Funcionalidades automáticas:</h5>
                                <ul class="mb-0">
                                    <li><strong>Vista Kanban:</strong> Visualiza el estado de cada estilista</li>
                                    <li><strong>Contador de citas:</strong> Ve cuántas citas tiene asignadas</li>
                                    <li><strong>Prevención de solapamientos:</strong> El sistema evita que se asignen citas que se solapen</li>
                                    <li><strong>Filtrado rápido:</strong> Busca estilistas disponibles fácilmente</li>
                                </ul>
                            </div>
                            
                            <div class="alert alert-info mt-3">
                                <i class="fa fa-info-circle"></i>
                                <strong>Importante:</strong> Puedes desactivar un estilista en lugar de eliminarlo. Así conservas el historial de sus citas pasadas.
                            </div>
                        </div>
                    '''
                },
                4: {
                    'title': '📅 Creación de Citas',
                    'content': '''
                        <div class="tutorial-step">
                            <h3>3. Gestión de Citas (Appointments)</h3>
                            <p>El corazón del sistema: aquí gestionas todas las reservas de tus clientes.</p>
                            
                            <div class="step-instructions">
                                <h4><i class="fa fa-arrow-right text-primary"></i> Proceso para crear una cita:</h4>
                                <div style="padding-left: 20px;">
                                    <p><strong>1.</strong> Ve a <strong>Citas → Citas</strong></p>
                                    <p><strong>2.</strong> Haz clic en <strong>Crear</strong></p>
                                    <p><strong>3.</strong> Completa el formulario:</p>
                                    <div style="margin-left: 30px;">
                                        <div class="field-group mt-2">
                                            <h5>Información Básica:</h5>
                                            <ul style="list-style-type: disc;">
                                                <li><strong>Cliente:</strong> Selecciona o crea un nuevo cliente</li>
                                                <li><strong>Estilista:</strong> Asigna el profesional que atenderá</li>
                                                <li><strong>Fecha y Hora de Inicio:</strong> Cuándo comienza la cita</li>
                                            </ul>
                                        </div>
                                        <div class="field-group mt-2">
                                            <h5>Servicios:</h5>
                                            <ul style="list-style-type: disc;">
                                                <li>Añade uno o varios servicios desde la pestaña "Servicios"</li>
                                                <li>El precio se copia automáticamente pero puedes ajustarlo</li>
                                                <li><strong>La hora de fin se calcula automáticamente</strong> según las duraciones</li>
                                            </ul>
                                        </div>
                                        <div class="field-group mt-2">
                                            <h5>Notas (Opcional):</h5>
                                            <ul style="list-style-type: disc;">
                                                <li>Preferencias del cliente</li>
                                                <li>Alergias o consideraciones especiales</li>
                                                <li>Peticiones específicas</li>
                                            </ul>
                                        </div>
                                    </div>
                                    <p><strong>4.</strong> Guarda como borrador o confirma directamente</p>
                                </div>
                            </div>
                            
                            <div class="workflow-box bg-primary text-white p-3 rounded mt-3">
                                <h5><i class="fa fa-exchange"></i> Flujo de Estados de una Cita:</h5>
                                <div class="d-flex justify-content-around align-items-center mt-2">
                                    <div class="text-center">
                                        <i class="fa fa-file-o fa-2x"></i>
                                        <div>Borrador</div>
                                    </div>
                                    <i class="fa fa-arrow-right fa-2x"></i>
                                    <div class="text-center">
                                        <i class="fa fa-check-circle fa-2x"></i>
                                        <div>Confirmada</div>
                                    </div>
                                    <i class="fa fa-arrow-right fa-2x"></i>
                                    <div class="text-center">
                                        <i class="fa fa-check-square fa-2x"></i>
                                        <div>Completada</div>
                                    </div>
                                </div>
                                <p class="mt-3 mb-0 small">También puedes cancelar una cita en cualquier momento.</p>
                            </div>
                            
                            <div class="alert alert-danger mt-3">
                                <i class="fa fa-exclamation-triangle"></i>
                                <strong>Sistema de Prevención:</strong> Si intentas crear una cita que solapa con otra del mismo estilista, recibirás un error. ¡Esto evita problemas de agenda!
                            </div>
                        </div>
                    '''
                },
                5: {
                    'title': '⭐ Clientes VIP y Calendario',
                    'content': '''
                        <div class="tutorial-step">
                            <h3>4. Sistema VIP y Visualización</h3>
                            
                            <div class="vip-section">
                                <h4><i class="fa fa-star text-warning"></i> Detección Automática de Clientes VIP</h4>
                                <p>El sistema identifica automáticamente a tus mejores clientes:</p>
                                <ul>
                                    <li><strong>Criterio:</strong> Clientes con más de 5 citas completadas</li>
                                    <li><strong>Indicador visual:</strong> Insignia "⭐ VIP FREQUENT CLIENT ⭐" en su ficha</li>
                                    <li><strong>Beneficios:</strong> Identificación rápida para dar prioridad o ventajas especiales</li>
                                </ul>
                                
                                <div class="alert alert-success">
                                    <i class="fa fa-magic"></i>
                                    <strong>Automático:</strong> No necesitas hacer nada, el sistema actualiza el estado VIP cada vez que una cita se marca como completada.
                                </div>
                            </div>
                            
                            <div class="calendar-section mt-4">
                                <h4><i class="fa fa-calendar text-primary"></i> Vista de Calendario</h4>
                                <p>Visualiza todas las citas de forma organizada:</p>
                                
                                <div class="row">
                                    <div class="col-md-6">
                                        <div class="view-option">
                                            <h5><i class="fa fa-list"></i> Vista Lista</h5>
                                            <ul>
                                                <li>Todas las citas en formato tabla</li>
                                                <li>Filtros por estado, estilista, fecha</li>
                                                <li>Ideal para búsquedas específicas</li>
                                            </ul>
                                        </div>
                                    </div>
                                    <div class="col-md-6">
                                        <div class="view-option">
                                            <h5><i class="fa fa-calendar"></i> Vista Calendario</h5>
                                            <ul>
                                                <li>Visualización por día/semana/mes</li>
                                                <li>Código de colores por estado</li>
                                                <li>Drag & drop para reprogramar</li>
                                            </ul>
                                        </div>
                                    </div>
                                </div>
                                
                                <div class="row mt-3">
                                    <div class="col-md-12">
                                        <div class="view-option">
                                            <h5><i class="fa fa-th"></i> Vista Kanban</h5>
                                            <ul>
                                                <li>Citas agrupadas por estado (Borrador, Confirmada, Completada, Cancelada)</li>
                                                <li>Mueve tarjetas entre columnas para cambiar estados</li>
                                                <li>Vista rápida de toda la información</li>
                                            </ul>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    '''
                },
                6: {
                    'title': '🎯 Mejores Prácticas y Consejos',
                    'content': '''
                        <div class="tutorial-step">
                            <h3>5. Consejos Profesionales</h3>
                            
                            <div class="best-practices">
                                <div class="practice-item">
                                    <h4><i class="fa fa-clock-o text-success"></i> Gestión del Tiempo</h4>
                                    <ul>
                                        <li>Establece duraciones realistas para cada servicio</li>
                                        <li>Añade 10-15 minutos extra para limpieza entre citas</li>
                                        <li>Revisa el calendario diariamente por las mañanas</li>
                                        <li>Confirma citas con 24h de antelación (llamada/SMS)</li>
                                    </ul>
                                </div>
                                
                                <div class="practice-item mt-3">
                                    <h4><i class="fa fa-users text-primary"></i> Atención al Cliente</h4>
                                    <ul>
                                        <li>Registra las preferencias en las notas de cada cita</li>
                                        <li>Identifica rápidamente a clientes VIP para atención prioritaria</li>
                                        <li>Usa el historial de citas para recordar servicios anteriores</li>
                                        <li>Marca citas como completadas apenas terminen</li>
                                    </ul>
                                </div>
                                
                                <div class="practice-item mt-3">
                                    <h4><i class="fa fa-line-chart text-warning"></i> Optimización del Negocio</h4>
                                    <ul>
                                        <li>Revisa qué servicios son más populares</li>
                                        <li>Identifica horas pico y ajusta personal</li>
                                        <li>Usa filtros para ver citas por estilista y optimizar cargas</li>
                                        <li>Exporta datos para análisis de ingresos</li>
                                    </ul>
                                </div>
                                
                                <div class="practice-item mt-3">
                                    <h4><i class="fa fa-shield text-danger"></i> Prevención de Errores</h4>
                                    <ul>
                                        <li><strong>Solapamientos:</strong> El sistema los evita automáticamente</li>
                                        <li><strong>Confirmación:</strong> Siempre confirma citas antes de marcar como completadas</li>
                                        <li><strong>Cancelaciones:</strong> Usa el botón "Cancelar" en lugar de eliminar</li>
                                        <li><strong>Backup:</strong> Los datos se guardan automáticamente</li>
                                    </ul>
                                </div>
                            </div>
                            
                            <div class="final-tips bg-gradient-primary text-white p-4 rounded mt-4">
                                <h4><i class="fa fa-graduation-cap"></i> ¡Felicidades!</h4>
                                <p>Has completado el tutorial de StyleHub. Ahora estás listo para:</p>
                                <ul class="mb-0">
                                    <li>✅ Gestionar servicios y precios</li>
                                    <li>✅ Administrar tu equipo de estilistas</li>
                                    <li>✅ Crear y gestionar citas eficientemente</li>
                                    <li>✅ Identificar y atender clientes VIP</li>
                                    <li>✅ Usar todas las vistas del sistema</li>
                                </ul>
                            </div>
                            
                            <div class="alert alert-info mt-3">
                                <i class="fa fa-question-circle"></i>
                                <strong>¿Necesitas ayuda?</strong> Puedes volver a este tutorial desde el menú <strong>? Ayuda → Tutorial para Empleados</strong>
                            </div>
                        </div>
                    '''
                }
            }
            
            step_data = content_map.get(record.step, content_map[1])
            record.step_title = step_data['title']
            record.step_content = step_data['content']
    
    def action_next(self):
        """Ir al siguiente paso"""
        if self.step < self.total_steps:
            self.step += 1
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'stylehub.tutorial.wizard',
            'res_id': self.id,
            'view_mode': 'form',
            'target': 'new',
        }
    
    def action_previous(self):
        """Volver al paso anterior"""
        if self.step > 1:
            self.step -= 1
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'stylehub.tutorial.wizard',
            'res_id': self.id,
            'view_mode': 'form',
            'target': 'new',
        }
    
    def action_restart(self):
        """Reiniciar tutorial"""
        self.step = 1
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'stylehub.tutorial.wizard',
            'res_id': self.id,
            'view_mode': 'form',
            'target': 'new',
        }
    
    def action_finish(self):
        """Finalizar tutorial"""
        return {'type': 'ir.actions.act_window_close'}
