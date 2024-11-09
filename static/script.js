document.addEventListener("DOMContentLoaded", function() {
    const totalGastoInput = document.querySelector('input[name="total_gasto"]');
    
    totalGastoInput.addEventListener("input", function(event) {
        let value = event.target.value.replace(/\D/g, '');
        event.target.value = new Intl.NumberFormat().format(value);
    });
});
