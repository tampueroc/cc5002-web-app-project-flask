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

function validateFormDonacion() {

  let region_id = document.getElementById("region").value;
  let comuna_id = document.getElementById("comuna").value;
  let street = document.getElementById("calle-numero").value;
  let type = document.getElementById("tipo").value;
  let cantidad = document.getElementById("cantidad").value;
  let fecha = document.getElementById("fecha-disponibilidad").value;
  let desc = document.getElementById("descripcion").value;
  let cond = document.getElementById("condiciones").value;
  let nombre = document.getElementById("nombre").value;
  let email = document.getElementById("email").value;
  let phone = document.getElementById("telefono").value;
  let fotos = document.getElementById("fotos");

  let invalidInputs = [];
  let isValid = true;
  const setInvalidInput = (inputName) => {
    invalidInputs.push(inputName);
    isValid &&= false;
  };

  const validateFotos = (fotos) => {
    if (fotos.files.length < 1) {
      setInvalidInput("debe subir al menos una foto");
    }
    if (fotos.files.length > 3) {
      setInvalidInput("debe subir como máximo 3 fotos");
    }
  }

  if (region_id == "" || region_id == "0") {
    setInvalidInput("region requerida");
  }

  if (comuna_id == "" || comuna_id == "0") {
    setInvalidInput("comuna requirida");
  }

  if (street == "") {
    setInvalidInput("calle y numero requerido");
  }

  if (type == "") {
    setInvalidInput("tipo requerido");
  }

  if (cantidad == "") {
    setInvalidInput("cantidad requerida");
  }

  if (fecha == "") {
    setInvalidInput("fecha requerida");
  } else {
    if (validateDate(fecha) == false) {
      setInvalidInput("fecha debe tener formato correcto (YYYY-MM-DD)");
    } else {
      const today = Date.now();
      const fecha_parsed = Date.parse(fecha);
      if (fecha_parsed <= today) {
        console.log("fecha invalida");
        setInvalidInput("fecha debe ser mayor o igual a la fecha actual");
      }
    }
  }

  validateFotos(fotos);

  if (nombre == "") {
    setInvalidInput("nombre requerido");
  }

  if (nombre.length > 80 && isValid) {
    setInvalidInput("nombre debe ser menor a 80 caracteres");
  }


  if (nombre.length < 3 && isValid) {
    setInvalidInput("nombre debe ser mayor a 3 caracteres");
  }


  if (email == "") {
    setInvalidInput("email requerido");
  } else {
    if (validateEmail(email) == false) {
      setInvalidInput("email debe tener formato correcto");
    }
  }

  if (phone == "") {
    setInvalidInput("telefono requerido");
  } else {
    if (validatePhone(phone) == false) {
      setInvalidInput("telefono debe tener formato correcto");
    }
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
    validationLabel.innerText = "¿Confirma que desea agregar esta donación?";
    validationText.innerHTML = `<button type="button" class="btn btn-primary" id="modal-confirm">Sí, confirmo</button> <button type="button" class="btn btn-primary" data-dismiss="modal">No, quiero volver al formulario</button>`;
    let validationConfirm = document.getElementById("modal-confirm");
    validationConfirm.addEventListener("click", async function () {
      let url = "http://localhost:5000/api/agregar-donacion";
      try {
        let data = new FormData()
        data.append('region_id', region_id);
        data.append('comuna_id', comuna_id);
        data.append('calle_numero', street);
        data.append('tipo', type);
        data.append('cantidad', cantidad);
        data.append('descripcion', desc);
        data.append('condiciones_retirar', cond);
        data.append('fecha_disponibilidad', fecha);
        data.append('nombre', nombre);
        data.append('email', email);
        data.append('celular', phone);
        for (let i = 0; i < fotos.files.length; i++) {
          data.append('fotos', fotos.files[i]);
        }
        const response = await fetch(url, {
          "method": "POST",
          "body": data,
          "headers": { "Access-Control-Allow-Origin": "*" }
        });
        const result = await response.status;
        console.log(result);
      } catch (error) {
        console.error("Error:", error);
      }
      validationText.innerHTML = `<p>Hemos recibido la información de su donación. Muchas gracias.</p> <button type="button" class="btn btn-primary" onclick="window.location.href='./'" data-dismiss="modal" >Inicio</button>`;
    });
  }
}