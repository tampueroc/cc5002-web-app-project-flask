function validateEmail(email) {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(String(email).toLowerCase());
}
function validatePhone(phone) {
    const re = /^\+56(?:9)[1-9]\d{7}$/;
    return re.test(String(phone).toLowerCase());
}
function validateDate(date) {
    const re = /^\d{4}-(?:0[1-9]|1[0-2])-(?:0[1-9]|[1-2][0-9]|3[0-1])$/;
    return re.test(String(date).toLowerCase());
}

function validateFormPedido() {

    let region_id = document.getElementById("region").value;
    let comuna_id = document.getElementById("comuna").value;
    let type = document.getElementById("tipo").value;
    let cantidad = document.getElementById("cantidad").value;
    let desc = document.getElementById("descripcion").value;
    let nombre = document.getElementById("nombre").value;
    let email = document.getElementById("email").value;
    let phone = document.getElementById("telefono").value;

    let invalidInputs = [];
    let isValid = true;
    const setInvalidInput = (inputName) => {
        invalidInputs.push(inputName);
        isValid &&= false;
    };

    if (region_id == "" || region_id == "0") {
        setInvalidInput("region requerida");
    }

    if (comuna == "" || comuna == "0") {
        setInvalidInput("comuna requirida");
    }

    if (type == "") {
        setInvalidInput("tipo requerido");
    }

    if (desc == "") {
        setInvalidInput("descripcion requerida");
    } else {
        if (desc.length > 250) {
            setInvalidInput("descripcion debe ser menor a 250 caracteres");
        }
    }

    if (cantidad == "") {
        setInvalidInput("cantidad requerida");
    }

    // TODO picture validation

    if (nombre == "") {
        setInvalidInput("nombre requerido");
    } else {
        if (nombre.length > 80) {
            setInvalidInput("nombre debe ser menor a 80 caracteres");
        }
        if (nombre.length < 3) {
            setInvalidInput("nombre debe ser mayor a 3 caracteres");
        }
    }

    if (email == "") {
        setInvalidInput("email requerido");
    } else {
        if (validateEmail(email) == false) {
            setInvalidInput("email debe tener formato correcto");
        }
    }

    if (phone != "" && validatePhone(phone) == false) {
        setInvalidInput("telefono debe tener formato correcto");
    }



    // finally display validation
    let validationModal = document.getElementById("validation-box");
    let validationText = document.getElementById("validation-text");
    let validationLabel = document.getElementById("validation-label");


    $(document).ready(function () {
        $("#validation-box").on('hidden.bs.modal', function () {
            validationText.innerHTML = ``;
            invalidInputs = [];
        });
    });

    if (!isValid) {
        validationLabel.innerText = "Los siguientes campos son inválidos:";
        console.log(invalidInputs);
        for (input of invalidInputs) {
            validationText.innerHTML += `<li>${input}</li>`;
        }
        validationText.innerHTML += "</ul>";
        validationModal.hidden = false;
    } else {
        validationLabel.innerText = "¿Confirma que desea agregar este pedido?";
        validationText.innerHTML = `<button type="button" class="btn btn-primary" id="modal-confirm">Sí, confirmo</button> <button type="button" class="btn btn-primary" data-dismiss="modal">No, quiero volver al formulario</button>`;
        let validationConfirm = document.getElementById("modal-confirm");
        validationConfirm.addEventListener("click", async function () {
            let validate_pedido_url = "http://localhost:5000/api/agregar-pedido"
            try {
                let data = new FormData()
                data.append('region_id', region_id);
                data.append('comuna_id', comuna_id);
                data.append('tipo', type);
                data.append('cantidad', cantidad);
                data.append('descripcion', desc);
                data.append('nombre_solicitante', nombre);
                data.append('email_solicitante', email);
                data.append('celular_solicitante', phone);
                const response = await fetch(validate_pedido_url, {
                    "method": "POST",
                    "body": data,
                    "headers": { "Access-Control-Allow-Origin": "*" }
                });
                const result = await response.status;
                console.log(result);
            } catch (error) {
                console.error("Error:", error);
            }
            validationText.innerHTML = `<p>Hemos recibido la información de su pedido. Muchas gracias.</p> <button type="button" class="btn btn-primary" onclick="window.location.href='./'" data-dismiss="modal" >Inicio</button>`;
        });
    }
}
