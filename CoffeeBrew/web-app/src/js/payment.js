// This file contains JavaScript functions specific to the payment page, managing payment processing and validation.

document.addEventListener('DOMContentLoaded', function() {
    const paymentForm = document.getElementById('payment-form');
    
    paymentForm.addEventListener('submit', function(event) {
        event.preventDefault();
        validatePayment();
    });
});

function validatePayment() {
    const cardNumber = document.getElementById('card-number').value;
    const expiryDate = document.getElementById('expiry-date').value;
    const cvv = document.getElementById('cvv').value;

    if (!isValidCardNumber(cardNumber)) {
        alert('Invalid card number');
        return;
    }
    if (!isValidExpiryDate(expiryDate)) {
        alert('Invalid expiry date');
        return;
    }
    if (!isValidCVV(cvv)) {
        alert('Invalid CVV');
        return;
    }

    processPayment(cardNumber, expiryDate, cvv);
}

function isValidCardNumber(cardNumber) {
    return /^\d{16}$/.test(cardNumber);
}

function isValidExpiryDate(expiryDate) {
    const [month, year] = expiryDate.split('/');
    const currentDate = new Date();
    const expiry = new Date(`20${year}`, month - 1);
    return expiry > currentDate;
}

function isValidCVV(cvv) {
    return /^\d{3}$/.test(cvv);
}

function processPayment(cardNumber, expiryDate, cvv) {
    // Simulate payment processing
    alert('Payment processed successfully!');
    // Redirect or update UI as needed
}