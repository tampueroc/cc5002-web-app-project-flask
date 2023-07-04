fetch('https://raw.githubusercontent.com/tampueroc/cc5002-tareas-resources/main/tarea_1/comunas_chile_coords.json')
            .then(response => response.json())
            .catch(error => console.error(error));