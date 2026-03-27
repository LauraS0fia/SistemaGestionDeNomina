//fetch eventos
const tabla = document.getElementById('TablaEmpleados');
const formulario = document.getElementById('formulario-empleado');
const submit = document.getElementById('submit');
const formMode = document.getElementById('form-mode');
const totalEmpleados = document.getElementById('total-empleados');
const totalNomina = document.getElementById('total-nomina');
const promedioNeto = document.getElementById('promedio-neto');

let editingId = null;

function formatCOP(value) {
    const number = Number(value) || 0;
    return number.toLocaleString('es-CO', {
        style: 'currency',
        currency: 'COP',
        maximumFractionDigits: 0
    });
}

function updateSummary(users) {
    const count = users.length;
    const total = users.reduce((acc, user) => acc + (Number(user.neto) || 0), 0);
    const average = count > 0 ? total / count : 0;

    totalEmpleados.textContent = String(count);
    totalNomina.textContent = formatCOP(total);
    promedioNeto.textContent = formatCOP(average);
}

//cargar empleados cuando carga la pagina
async function loadUsers() {
    const res = await fetch("/api/users");
    const users = await res.json();
    
    tabla.innerHTML = "";
    updateSummary(users);

    users.forEach(u => {
        const safeName = String(u.nombre).replace(/'/g, "\\'");

        tabla.innerHTML += `
            <tr>
                <td>${u.nombre}</td>
                <td>${formatCOP(u.sueldo)}</td>
                <td>${formatCOP(u.auxilio)}</td>
                <td>${formatCOP(u.horas_extra)}</td>
                <td>${formatCOP(u.devengado)}</td>
                <td>${formatCOP(u.salud)}</td>
                <td>${formatCOP(u.pension)}</td>
                <td>${formatCOP(u.deducciones)}</td>
                <td>${formatCOP(u.neto)}</td>
                <td>
                    <button class="btn-edit" onclick="editUser('${u.id}', '${safeName}', ${u.Sbasico}, ${u.Dias}, ${u.nivel_arl}, ${u.HED}, ${u.HEN}, ${u.HEDF}, ${u.HENF})">Editar</button>
                    <button class="btn-delete" onclick="deleteUser('${u.id}')">Eliminar</button>
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
    formMode.textContent = "Editando";
    
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
            formMode.textContent = "Nuevo";
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
        formMode.textContent = "Nuevo";
        loadUsers();
    } catch (error) {
        alert('Error al guardar el empleado');
        console.error(error);
    }
});

//inicializar cargar empleados al abrir la pagina
loadUsers();