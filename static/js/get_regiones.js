fetch('https://raw.githubusercontent.com/tampueroc/cc5002-tareas/main/tarea_1/regiones_y_comunas.json')
            .then(response => response.json())
            .then(data => {
                let regionSelect = document.getElementById('region');
                let comunaSelect = document.getElementById('comuna');
                let tipoSelect = document.getElementById('tipo');
                let disableComuna = document.getElementById('disable-comuna');

                data.regiones.forEach(region => {
                    let option = document.createElement('option');
                    option.value = region.id;
                    option.text = region.nombre;
                    regionSelect.add(option);
                });

                regionSelect.addEventListener('change', function () {
                    if (this.value == "0") {
                        comunaSelect.innerHTML = '<option value="0">Seleccione una comuna</option>';
                        disableComuna.disabled = true;
                    } else {
                        disableComuna.disabled = false;
                        let selectedRegion = data.regiones.find(region => region.id == this.value);
                        selectedRegion.comunas.forEach(comuna => {
                            let option = document.createElement('option');
                            option.value = comuna.id;
                            option.text = comuna.nombre;
                            comunaSelect.add(option);
                        })
                    };
                });

                tipoSelect.innerHTML += '<option value="verdura">Verduras</option>';
                tipoSelect.innerHTML += '<option value="fruta">Frutas</option>';
                tipoSelect.innerHTML += '<option value="otro">Otro</option>';
            })
            .catch(error => console.error(error));