// This file contains JavaScript functions specific to the coffee ordering page, managing coffee selection and order submission.

document.addEventListener('DOMContentLoaded', function() {
    const coffeeForm = document.getElementById('coffee-order-form');
    const coffeeSelect = document.getElementById('coffee-select');
    const orderButton = document.getElementById('order-button');
    const orderSummary = document.getElementById('order-summary');

    orderButton.addEventListener('click', function(event) {
        event.preventDefault();
        const selectedCoffee = coffeeSelect.value;
        if (selectedCoffee) {
            orderSummary.textContent = `You have ordered: ${selectedCoffee}`;
            coffeeForm.reset();
        } else {
            alert('Please select a coffee to order.');
        }
    });
});