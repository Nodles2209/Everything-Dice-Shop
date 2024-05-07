const csrf_token = "{{ csrf_token() }}";
$.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrf_token);
            }
        }
    });

function togglePaymentForm() {
    let paymentTypeSelect = document.getElementById("payment-type-select");
    let cardFormGroup = document.getElementById("card-form-group");
    let onlineFormGroup = document.getElementById("online-form-group");

    console.log(paymentTypeSelect.value);

    if (paymentTypeSelect.value === "card") {
        cardFormGroup.style.display = "block";
        onlineFormGroup.style.display = "none";
        disableValidation(onlineFormGroup);
        enableValidation(cardFormGroup);
    } else if (paymentTypeSelect.value === "online") {
        cardFormGroup.style.display = "none";
        onlineFormGroup.style.display = "block";
        disableValidation(cardFormGroup);
        enableValidation(onlineFormGroup);
    } else {
        cardFormGroup.style.display = "none";
        onlineFormGroup.style.display = "none";
        disableValidation(cardFormGroup);
        disableValidation(onlineFormGroup);
    }
}

function disableValidation(formGroup) {
    let fields = formGroup.querySelectorAll(".form-control");
    fields.forEach(function(field) {
        field.removeAttribute("required");
    });
}

function enableValidation(formGroup) {
    let fields = formGroup.querySelectorAll(".form-control");
    fields.forEach(function(field) {
        field.setAttribute("required", true);
    });
}

function validateForm() {
    let payment_type = document.getElementById("payment-type-select");
    let payment_value = payment_type.value;

    let phone_number = document.getElementById("phone-number").value;

    if (phone_number.length < 9 || phone_number.length > 12) {
        alert("Please enter a valid 9-12 digit phone number");
        return false;
    }

    if (payment_value === "none") {
        alert("Please select a payment option");
        return false;
    } else if (payment_value === "card") {
        let card_number = document.getElementById("card-number").value;
        if (card_number.length !== 16) {
            alert("Please enter a valid 16-digit card number");
            return false;
        }
    }

    return true;
}