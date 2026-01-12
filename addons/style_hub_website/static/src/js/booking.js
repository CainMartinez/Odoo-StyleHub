/* StyleHub - Booking Wizard JavaScript */

console.log('[StyleHub Booking] Script loaded');

(function() {
    'use strict';
    
    // Esperar a que jQuery esté disponible
    function initBooking() {
        console.log('[StyleHub Booking] Checking jQuery availability...');
        
        if (typeof $ === 'undefined' || typeof jQuery === 'undefined') {
            console.log('[StyleHub Booking] jQuery not ready, waiting...');
            setTimeout(initBooking, 100);
            return;
        }
        
        console.log('[StyleHub Booking] jQuery ready, initializing booking wizard...');
        
        var bookingData = {
            services: [],
            date: null,
            time: null,
            timeSlot: null
        };
        
        var currentStep = 1;
        
        // Pre-seleccionar servicio si viene de URL
        var urlParams = new URLSearchParams(window.location.search);
        var preselectedServiceId = urlParams.get('service_id');
        
        console.log('[StyleHub Booking] URL params:', urlParams.toString());
        console.log('[StyleHub Booking] Preselected service ID:', preselectedServiceId);
        
        if (preselectedServiceId) {
            console.log('[StyleHub Booking] Will preselect service:', preselectedServiceId);
            
            // Esperar un poco para asegurar que todos los elementos estén renderizados
            setTimeout(function() {
                var serviceCard = $('.service-card[data-service-id="' + preselectedServiceId + '"]');
                console.log('[StyleHub Booking] Found service card:', serviceCard.length > 0);
                
                if (serviceCard.length > 0) {
                    // Trigger click para seleccionar el servicio
                    serviceCard.trigger('click');
                    console.log('[StyleHub Booking] Service card clicked');
                    
                    // Scroll al servicio pre-seleccionado
                    setTimeout(function() {
                        var offset = serviceCard.offset();
                        if (offset) {
                            console.log('[StyleHub Booking] Scrolling to service card');
                            $('html, body').animate({
                                scrollTop: offset.top - 150
                            }, 500);
                        }
                    }, 300);
                }
            }, 500);
        }
        
        // Service selection
        $('.service-card').click(function() {
            var serviceId = parseInt($(this).data('service-id'));
            var duration = parseFloat($(this).data('duration'));
            var price = parseFloat($(this).data('price'));
            
            console.log('[StyleHub Booking] Service card clicked:', {
                id: serviceId,
                duration: duration,
                price: price
            });
            
            $(this).toggleClass('selected');
            
            var index = bookingData.services.findIndex(s => s.id === serviceId);
            if (index > -1) {
                bookingData.services.splice(index, 1);
                console.log('[StyleHub Booking] Service removed from selection');
            } else {
                bookingData.services.push({
                    id: serviceId,
                    name: $(this).find('h4').text(),
                    duration: duration,
                    price: price
                });
                console.log('[StyleHub Booking] Service added to selection');
            }
            
            console.log('[StyleHub Booking] Current services:', bookingData.services);
            updateServicesSummary();
        });
        
        function updateServicesSummary() {
            var count = bookingData.services.length;
            var total = bookingData.services.reduce((sum, s) => sum + s.price, 0);
            
            console.log('[StyleHub Booking] Updating summary:', {
                count: count,
                total: total
            });
            
            $('#selected-services-count').text(count);
            $('#total-price').text(total.toFixed(2) + ' €');
            
            $('#btn-next-1').prop('disabled', count === 0);
        }
        
        // Date selection
        var today = new Date().toISOString().split('T')[0];
        console.log('[StyleHub Booking] Setting minimum date:', today);
        
        $('#appointment_date').attr('min', today).change(function() {
            bookingData.date = $(this).val();
            console.log('[StyleHub Booking] Date selected:', bookingData.date);
            $('#btn-next-2').prop('disabled', !bookingData.date);
        });
        
        // Navigation
        $('#btn-next-1').click(function() { 
            console.log('[StyleHub Booking] Moving to step 2 (Date)');
            goToStep(2); 
        });
        $('#btn-back-2').click(function() { 
            console.log('[StyleHub Booking] Back to step 1 (Services)');
            goToStep(1); 
        });
        $('#btn-next-2').click(function() { 
            console.log('[StyleHub Booking] Moving to step 3 (Time), loading slots...');
            goToStep(3); 
            loadTimeSlots(); 
        });
        $('#btn-back-3').click(function() { 
            console.log('[StyleHub Booking] Back to step 2 (Date)');
            goToStep(2); 
        });
        $('#btn-next-3').click(function() { 
            console.log('[StyleHub Booking] Moving to step 4 (Confirmation)');
            goToStep(4); 
            showSummary(); 
        });
        $('#btn-back-4').click(function() { 
            console.log('[StyleHub Booking] Back to step 3 (Time)');
            goToStep(3); 
        });
        
        function goToStep(step) {
            console.log('[StyleHub Booking] Navigating to step:', step);
            
            $('.step-content').addClass('d-none');
            $('#step-' + step).removeClass('d-none').addClass('fade-in');
            
            $('.step-item').removeClass('active');
            for (var i = 1; i < step; i++) {
                $('#step-indicator-' + i).addClass('completed');
            }
            $('#step-indicator-' + step).addClass('active');
            
            currentStep = step;
            $('html, body').animate({ scrollTop: 0 }, 300);
        }
        
        function loadTimeSlots() {
            var serviceIds = bookingData.services.map(s => s.id);
            
            console.log('[StyleHub Booking] Loading time slots for:', {
                date: bookingData.date,
                serviceIds: serviceIds
            });
            
            $('#loading-slots').removeClass('d-none');
            $('#time-slots-container').empty();
            $('#no-slots-message').addClass('d-none');
            $('#btn-next-3').prop('disabled', true);
            
            $.ajax({
                url: '/appointment/get_available_slots',
                type: 'POST',
                contentType: 'application/json',
                data: JSON.stringify({
                    jsonrpc: '2.0',
                    method: 'call',
                    params: {
                        date: bookingData.date,
                        service_ids: serviceIds
                    }
                }),
                success: function(response) {
                    console.log('[StyleHub Booking] Slots response:', response);
                    
                    $('#loading-slots').addClass('d-none');
                    var result = response.result || {};
                    
                    if (result.error) {
                        console.error('[StyleHub Booking] Error loading slots:', result.error);
                        $('#no-slots-message').text(result.error).removeClass('d-none');
                        return;
                    }
                    
                    var slots = result.slots || [];
                    console.log('[StyleHub Booking] Available slots:', slots.length);
                    
                    if (slots.length === 0) {
                        $('#no-slots-message').removeClass('d-none');
                        return;
                    }
                    
                    slots.forEach(function(slot) {
                        var btn = $('<div class="col-md-4 col-lg-3 mb-3"><button type="button" class="btn btn-block time-slot-btn" data-datetime="' + 
                            slot.datetime + '">' + slot.time + '</button></div>');
                        $('#time-slots-container').append(btn);
                    });
                    
                    $('.time-slot-btn').click(function() {
                        $('.time-slot-btn').removeClass('active');
                        $(this).addClass('active');
                        bookingData.timeSlot = $(this).data('datetime');
                        bookingData.time = $(this).text();
                        console.log('[StyleHub Booking] Time slot selected:', {
                            datetime: bookingData.timeSlot,
                            time: bookingData.time
                        });
                        $('#btn-next-3').prop('disabled', false);
                    });
                },
                error: function(xhr, status, error) {
                    console.error('[StyleHub Booking] AJAX error:', {
                        status: status,
                        error: error,
                        response: xhr.responseText
                    });
                    $('#loading-slots').addClass('d-none');
                    $('#no-slots-message').text('Error al cargar horarios disponibles').removeClass('d-none');
                }
            });
        }
        
        function showSummary() {
            console.log('[StyleHub Booking] Showing summary');
            
            var servicesList = bookingData.services.map(s => {
                var durationText = s.duration < 1 ? (s.duration * 60) + ' min' : s.duration + ' h';
                return '<li class="mb-2"><i class="fa fa-check text-success mr-2"></i>' + s.name + ' - ' + durationText + ' - ' + s.price.toFixed(2) + ' €</li>';
            }).join('');
            $('#summary-services').html(servicesList);
            
            var totalDuration = bookingData.services.reduce((sum, s) => sum + s.duration, 0);
            var totalPrice = bookingData.services.reduce((sum, s) => sum + s.price, 0);
            
            var dateObj = new Date(bookingData.date);
            var formattedDate = dateObj.toLocaleDateString('es-ES', { 
                weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' 
            });
            
            var totalDurationText = totalDuration < 1 ? (totalDuration * 60) + ' min' : totalDuration.toFixed(1) + ' horas';
            
            console.log('[StyleHub Booking] Summary data:', {
                services: bookingData.services.length,
                duration: totalDurationText,
                price: totalPrice,
                date: formattedDate,
                time: bookingData.time
            });
            
            $('#summary-date').text(formattedDate);
            $('#summary-time').text(bookingData.time);
            $('#summary-duration').text(totalDurationText);
            $('#summary-total').text(totalPrice.toFixed(2) + ' €');
        }
        
        $('#btn-confirm').click(function() {
            console.log('[StyleHub Booking] Confirming appointment...');
            
            var btn = $(this);
            var serviceIds = bookingData.services.map(s => s.id);
            
            console.log('[StyleHub Booking] Sending data:', {
                start_datetime: bookingData.timeSlot,
                service_ids: serviceIds,
                notes: $('#appointment_notes').val()
            });
            
            btn.prop('disabled', true).html('<span class="spinner-border spinner-border-sm mr-2"></span>Procesando...');
            
            $.ajax({
                url: '/appointment/create',
                type: 'POST',
                contentType: 'application/json',
                data: JSON.stringify({
                    jsonrpc: '2.0',
                    method: 'call',
                    params: {
                        start_datetime: bookingData.timeSlot,
                        service_ids: serviceIds,
                        notes: $('#appointment_notes').val()
                    }
                }),
                success: function(response) {
                    console.log('[StyleHub Booking] Appointment creation response:', response);
                    
                    var result = response.result || {};
                    
                    if (result.error) {
                        console.error('[StyleHub Booking] Error creating appointment:', result.error);
                        $('#booking-result')
                            .removeClass('alert-success d-none')
                            .addClass('alert alert-danger')
                            .html('<i class="fa fa-times-circle fa-2x mb-3"></i><p>' + result.error + '</p>');
                        btn.prop('disabled', false).html('<i class="fa fa-check-circle mr-2"></i>Confirmar Reserva');
                    } else {
                        console.log('[StyleHub Booking] Appointment created successfully!');
                        $('#booking-result')
                            .removeClass('alert-danger d-none')
                            .addClass('alert alert-success text-center')
                            .html('<i class="fa fa-check-circle fa-3x mb-3 d-block"></i>' +
                                  '<h3>¡Reserva Confirmada!</h3>' +
                                  '<p class="lead">' + result.message + '</p>' +
                                  '<a href="/my/appointments" class="btn btn-primary btn-lg mt-3"><i class="fa fa-calendar"></i> Ver Mis Citas</a>');
                        
                        // Ocultar elementos del wizard
                        $('#step-1, #step-2, #step-3').remove();
                        $('.step-indicator, #btn-confirm').hide();
                        $('#appointment_notes').parent().hide();
                        $('.summary-box').hide();
                        
                        // Cambiar el botón Volver por Volver a Inicio
                        $('#btn-back-4')
                            .removeClass('btn-outline-secondary')
                            .addClass('btn-outline-primary')
                            .html('<i class="fa fa-home mr-2"></i>Volver a Inicio')
                            .off('click')
                            .click(function() {
                                window.location.href = '/';
                            });
                    }
                },
                error: function(xhr, status, error) {
                    console.error('[StyleHub Booking] AJAX error creating appointment:', {
                        status: status,
                        error: error,
                        response: xhr.responseText
                    });
                    $('#booking-result')
                        .removeClass('alert-success d-none')
                        .addClass('alert alert-danger')
                        .html('<i class="fa fa-times-circle fa-2x mb-3"></i><p>Error al procesar la reserva. Por favor, inténtelo de nuevo.</p>');
                    btn.prop('disabled', false).html('<i class="fa fa-check-circle mr-2"></i>Confirmar Reserva');
                }
            });
        });
    }
    
    // Iniciar cuando el documento esté listo
    console.log('[StyleHub Booking] Setting up initialization...');
    if (document.readyState === 'loading') {
        console.log('[StyleHub Booking] Document still loading, waiting for DOMContentLoaded');
        document.addEventListener('DOMContentLoaded', initBooking);
    } else {
        console.log('[StyleHub Booking] Document already loaded, initializing immediately');
        initBooking();
    }
    
    console.log('[StyleHub Booking] Script setup complete');
})();
