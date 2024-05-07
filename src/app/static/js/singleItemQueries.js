const csrf_token = "{{ csrf_token() }}";
$.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrf_token);
            }
        }
    });

window.onload = function() {
    updatePrice();
};

document.getElementById("option").addEventListener("change", updatePrice);
document.getElementById("quantity").addEventListener("input", updatePrice);

function updatePrice() {
    let optionId = document.getElementById("option").value; // Get the selected option's ID
    let quantity = document.getElementById("quantity").value; // Get the quantity

    // Make AJAX request to fetch the price based on optionId
    const xhr = new XMLHttpRequest();
    xhr.open("GET", "/get_price/" + optionId, true); // Replace "/get_price" with your server route
    xhr.onreadystatechange = function() {
        if (xhr.readyState === 4 && xhr.status === 200) {
            let price = parseFloat(xhr.responseText); // Parse the response
            let totalPrice = price * quantity;
            document.getElementById("price").value = "£" + totalPrice.toFixed(2); // Update the price field
        }
    };
    xhr.send();
}
