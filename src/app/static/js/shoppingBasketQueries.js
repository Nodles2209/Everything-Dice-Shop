const csrf_token = "{{ csrf_token() }}";
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrf_token);
        }
    }
});

axios.defaults.headers.common["X-CSRFToken"] = "{{ csrf_token() }}";

function updateIndividualPrice(basketItemNum, newPrice) {
    let individualPriceDisplay = document.getElementById(basketItemNum);
    if (individualPriceDisplay) {
        individualPriceDisplay.textContent = '£' + newPrice.toFixed(2);
    }
}

function updatePriceOnChange(quantityField) {
    let itemContainer = quantityField.closest('.basket-item');
    let priceField = itemContainer.querySelector('.price-field');
    let optionId = itemContainer.querySelector('.hidden-field input[name="hidden-option-id"]').value;
    let basketItemNum = itemContainer.querySelector('.hidden-field input[name="hidden-basket-id"]').value;
    let newQuantity = parseInt(quantityField.value);

    fetch('/get_price/' + optionId)
    .then(response => response.text())
    .then(price => {
        let newPrice = parseFloat(price) * newQuantity;
        priceField.value = '£' + newPrice.toFixed(2);

        updateIndividualPrice(basketItemNum, newPrice);
        updateTotalPrice();
        updateBasketItem(optionId, newQuantity, basketItemNum);
    })
    .catch(error => {
        console.error('Error fetching price:', error);
    });
}

let quantityFields = document.querySelectorAll('.quantity-field');
quantityFields.forEach(function(quantityField) {
    quantityField.addEventListener('change', function() {
        updatePriceOnChange(quantityField);
    });
});

function updateBasketItem(optionId, quantity, basketItemNum) {
    let formData = new FormData();
    formData.append('quantity', quantity);
    formData.append('basket_item_num', basketItemNum);

    axios.post('/basket/update/' + optionId, formData, {
        headers: {
            'Content-Type': 'multipart/form-data',
            'X-CSRFToken': csrf_token
        }
    })
    .then(response => {
        if (response.ok) {
            updateTotalPrice();
        } else {
            console.error('Failed to update basket item');
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

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

const itemForms = document.querySelectorAll('.change-item-form');
for (const element of itemForms) {
    element.addEventListener('change', function(event) {
        let optionId = event.target.closest('.change-item-form').querySelector('.hidden-field input[name="hidden-option-id"]').value;
        let quantity = event.target.value;
        let basketItemNum = event.target.closest('.change-item-form').querySelector('.hidden-field input[name="hidden-basket-id"]').value;
        updateBasketItem(optionId, quantity, basketItemNum);
    });
}
