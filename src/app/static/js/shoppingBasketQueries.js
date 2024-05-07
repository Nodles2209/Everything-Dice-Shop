const csrf_token = "{{ csrf_token() }}";
$.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrf_token);
            }
        }
    });

axios.defaults.headers.common["X-CSRFToken"] = "{{ csrf_token() }}";

function updateIndividualPrice(optionId, newPrice) {
    // Select the individual price display using the optionId
    let individualPriceDisplay = document.getElementById(optionId);

    // Update the individual price display
    individualPriceDisplay.textContent = '£' + newPrice.toFixed(2);
}

function updatePriceOnChange(quantityField) {
    let itemContainer = quantityField.closest('.basket-item');
    let priceField = itemContainer.querySelector('.price-field');
    let optionId = itemContainer.querySelector('.hidden-field input').value;
    let newQuantity = parseInt(quantityField.value);

    // Make a request to get the price based on the option ID
    fetch('/get_price/' + optionId)
    .then(response => response.text())
    .then(price => {
        let newPrice = parseFloat(price) * newQuantity;
        priceField.value = '£' + newPrice.toFixed(2);


        updateIndividualPrice(optionId, newPrice);
        updateTotalPrice();
    })
    .catch(error => {
        console.error('Error fetching price:', error);
    });
}

// Listen for changes in quantity fields
let quantityFields = document.querySelectorAll('.quantity-field');
quantityFields.forEach(function(quantityField) {
    quantityField.addEventListener('change', function() {
        updatePriceOnChange(quantityField);
    });
});

function updateBasketItem(optionId, quantity) {
    let formData = new FormData();
    formData.append('quantity', quantity);

    console.log(csrf_token);


    axios.post('/basket/update/' + optionId, formData, {
            headers: {
                'Content-Type': 'multipart/form-data',
                'X-CSRFToken': csrf_token
            }
        })
    .then(response => {
        if (response.ok) {
            // Success, update total price and any other UI elements
            updateTotalPrice();
            // Additional UI updates if needed
        } else {
            // Handle error
            console.error('Failed to update basket item');
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

    // Function to update total price
function updateTotalPrice() {
    let totalPrice = 0;
    let priceFields = document.querySelectorAll('.price-field');

    for (const element of priceFields) {
        const priceText = element.value.replace('£', '').replace(',', '');
        const price = parseFloat(priceText);
        totalPrice += price;
}

document.querySelector('.total-price .formatted-total-price').textContent = '£' + totalPrice.toFixed(2);
}

    // Listen for changes in quantity or price fields
const itemForms = document.querySelectorAll('.change-item-form');
for (const element of itemForms) {
    element.addEventListener('change', function(event) {
        let optionId = event.target.closest('.change-item-form').querySelector('.hidden-field input').value;
        let quantity = event.target.value;
        updateBasketItem(optionId, quantity);
    });
}
