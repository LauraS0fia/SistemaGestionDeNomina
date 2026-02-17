//fetch eventos
const tabla = document.getElementById('TablaEmpleados');
const formulario = document.getElementById('formulario-empleado');
const submit = document.getElementById('submit');

let editingId = null;

//cargar empleados cuando carga la pagina
async function loadUsers() {
    const res = await fetch("/api/users");
    const users = await res.json();
    
    tabla.innerHTML = "";

    users.forEach(u => {
        tabla.innerHTML += `
            <tr>
                <td>${u.nombre}</td>
                <td>${u.sueldo}</td>
                <td>${u.auxilio}</td>
                <td>${u.horas_extra}</td>
                <td>${u.devengado}</td>
                <td>${u.salud}</td>
                <td>${u.pension}</td>
                <td>${u.deducciones}</td>
                <td>${u.neto}</td>
                <td>
                    <button onclick="editUser('${u.id}', '${u.nombre}', ${u.Sbasico}, ${u.Dias}, ${u.nivel_arl}, ${u.HED}, ${u.HEN}, ${u.HEDF}, ${u.HENF})">Editar</button>
                    <button onclick="deleteUser('${u.id}')">Eliminar</button>
                </td>
            </tr>
        `;
    });
}

//editar empleado (llenar formulario )
function editUser(id, nombre, Sbasico, Dias, nivelArl, HED, HEN, HEDF, HENF) {
    document.getElementById("nombre").value = nombre;
    document.getElementById("Sbasico").value = Sbasico;
    document.getElementById("Dias").value = Dias;
    document.getElementById("nivel-arl").value = nivelArl;
    document.getElementById("HED").value = HED;
    document.getElementById("HEN").value = HEN;
    document.getElementById("HEDF").value = HEDF;
    document.getElementById("HENF").value = HENF;

    editingId = id;
    submit.textContent = "Actualizar";
    
    window.scrollTo({ top: 0, behavior: 'smooth' });
}
//eliminar empleado
async function deleteUser(id) {
    console.log("ID recibido en deleteUser:", id);

    if (!id) {
        alert("ERROR: id es undefined");
        return;
    }

    if (confirm('¿Estás seguro de eliminar este empleado?')) {
        await fetch("/api/users/" + id, { method: "DELETE" });
        loadUsers();
    }
}
//guardar o actualizar - submit del formulario
formulario.addEventListener("submit", async (e) => {
    e.preventDefault();

    const empleado = {
        nombre: document.getElementById("nombre").value,
        Sbasico: document.getElementById("Sbasico").value,
        Dias: document.getElementById("Dias").value,
        nivel_arl: document.getElementById("nivel-arl").value,
        HED: document.getElementById("HED").value,
        HEN: document.getElementById("HEN").value,
        HEDF: document.getElementById("HEDF").value,
        HENF: document.getElementById("HENF").value
    };

    try {
        // Si estamos editando → PUT
        if (editingId) {
            await fetch("/api/users/" + editingId, {
                method: "PUT",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(empleado)
            });

            editingId = null;
            submit.textContent = "Guardar";
        } 
        // Si es nuevo → POST
        else {
            await fetch("/api/users", {
                method: "POST", 
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(empleado)
            });
        }

        formulario.reset();
        loadUsers();
    } catch (error) {
        alert('Error al guardar el empleado');
        console.error(error);
    }
});

//inicializar cargar empleados al abrir la pagina 