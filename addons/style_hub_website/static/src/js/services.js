/* StyleHub - Services Page JavaScript */

console.log('[StyleHub Services] Script loaded');

document.addEventListener('DOMContentLoaded', function() {
    console.log('[StyleHub Services] DOM loaded, initializing...');
    
    // Hacer las cards clickeables
    var cards = document.querySelectorAll('.service-product-card');
    console.log('[StyleHub Services] Found ' + cards.length + ' service cards');
    
    cards.forEach(function(card) {
        card.addEventListener('click', function(e) {
            console.log('[StyleHub Services] Card clicked:', this);
            
            // Si el click no fue en el botón, redirigir
            if (!e.target.closest('.btn-book-service')) {
                var serviceId = this.getAttribute('data-service-id');
                console.log('[StyleHub Services] Redirecting to booking with service ID:', serviceId);
                window.location.href = '/appointment/book?service_id=' + serviceId;
            } else {
                console.log('[StyleHub Services] Button clicked directly, default link will handle');
            }
        });
    });
    
    console.log('[StyleHub Services] Initialization complete');
});
