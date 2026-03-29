const API = "/api/vehicles";

const TYPE_LABELS = { CAR: "Avtomobil", VAN: "Kombi", MOTORCYCLE: "Motor" };

async function loadVehicles() {
  const type = document.getElementById("filter-type").value;
  const availableOnly = document.getElementById("filter-available").value === "true";

  let url = API + "?";
  if (type) url += `type=${type}&`;
  if (availableOnly) url += "available_only=true";

  try {
    const res = await fetch(url);
    const vehicles = await res.json();
    renderTable(vehicles);
  } catch {
    document.getElementById("vehicles-body").innerHTML =
      '<tr><td colspan="10" class="empty-row">Napaka pri nalaganju.</td></tr>';
  }
}

function renderTable(vehicles) {
  const tbody = document.getElementById("vehicles-body");
  if (!vehicles.length) {
    tbody.innerHTML = '<tr><td colspan="10" class="empty-row">Ni vozil.</td></tr>';
    return;
  }
  tbody.innerHTML = vehicles
    .map(
      (v) => `
    <tr>
      <td>${v.id}</td>
      <td>${v.make}</td>
      <td>${v.model}</td>
      <td>${TYPE_LABELS[v.type] || v.type}</td>
      <td>${v.year}</td>
      <td>${v.price_per_day.toFixed(2)}</td>
      <td class="${v.available ? "available" : "unavailable"}">${v.available ? "Da" : "Ne"}</td>
      <td>${v.branch}</td>
      <td>${v.license_plate}</td>
      <td>
        <button class="btn-edit" onclick='openEditModal(${JSON.stringify(v)})'>Uredi</button>
        <button class="btn-delete" onclick="deleteVehicle(${v.id})">Izbriši</button>
      </td>
    </tr>`
    )
    .join("");
}

function openAddModal() {
  document.getElementById("modal-title").textContent = "Dodaj vozilo";
  document.getElementById("vehicle-form").reset();
  document.getElementById("vehicle-id").value = "";
  document.getElementById("form-error").textContent = "";
  document.getElementById("modal").classList.remove("hidden");
}

function openEditModal(v) {
  document.getElementById("modal-title").textContent = "Uredi vozilo";
  document.getElementById("vehicle-id").value = v.id;
  document.getElementById("make").value = v.make;
  document.getElementById("model").value = v.model;
  document.getElementById("type").value = v.type;
  document.getElementById("year").value = v.year;
  document.getElementById("price_per_day").value = v.price_per_day;
  document.getElementById("license_plate").value = v.license_plate;
  document.getElementById("branch").value = v.branch;
  document.getElementById("available").value = String(v.available);
  document.getElementById("form-error").textContent = "";
  document.getElementById("modal").classList.remove("hidden");
}

function closeModal() {
  document.getElementById("modal").classList.add("hidden");
}

async function submitForm(event) {
  event.preventDefault();
  const id = document.getElementById("vehicle-id").value;

  const payload = {
    make: document.getElementById("make").value,
    model: document.getElementById("model").value,
    type: document.getElementById("type").value,
    year: parseInt(document.getElementById("year").value),
    price_per_day: parseFloat(document.getElementById("price_per_day").value),
    available: document.getElementById("available").value === "true",
    branch: document.getElementById("branch").value,
    license_plate: document.getElementById("license_plate").value,
  };

  const url = id ? `${API}/${id}` : API;
  const method = id ? "PUT" : "POST";

  const res = await fetch(url, {
    method,
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });

  if (res.ok) {
    closeModal();
    loadVehicles();
  } else {
    const err = await res.json();
    document.getElementById("form-error").textContent = err.detail || "Napaka pri shranjevanju.";
  }
}

async function deleteVehicle(id) {
  if (!confirm("Res želite izbrisati to vozilo?")) return;
  const res = await fetch(`${API}/${id}`, { method: "DELETE" });
  if (res.ok) {
    loadVehicles();
  } else {
    alert("Napaka pri brisanju.");
  }
}

// close modal on backdrop click
document.getElementById("modal").addEventListener("click", (e) => {
  if (e.target === document.getElementById("modal")) closeModal();
});

loadVehicles();
