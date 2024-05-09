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
    let optionId = document.getElementById("option").value;
    let quantity = document.getElementById("quantity").value;

    const xhr = new XMLHttpRequest();
    xhr.open("GET", "/get_price/" + optionId, true);
    xhr.onreadystatechange = function() {
        if (xhr.readyState === 4 && xhr.status === 200) {
            let price = parseFloat(xhr.responseText);
            let totalPrice = price * quantity;
            document.getElementById("price").value = "£" + totalPrice.toFixed(2);
        }
    };
    xhr.send();
}


document.querySelectorAll('.option-img img').forEach(function(optionImg) {
    optionImg.addEventListener('click', function() {

        const newImgSrc = optionImg.getAttribute('src');


        document.querySelector('.main-img img').setAttribute('src', newImgSrc);
    });
});

