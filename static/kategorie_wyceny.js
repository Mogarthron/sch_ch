// //Edycja wiersza
// document.querySelectorAll(".edytuj").forEach(btn => {
//   btn.addEventListener("click", function () {
//     const row = this.closest("tr");
//     const id = row.dataset.id;
//     const nazwaTd = row.querySelector(".nazwa");
//     const opisTd = row.querySelector(".opis");
//     const zdjecieTd = row.querySelector(".zdjecie");

//     if (this.textContent === "Edytuj") {
//       const nazwa = nazwaTd.textContent.trim();
//       const opis = opisTd.textContent.trim();
//     //   const zdjecie = opisTd.textContent.trim();

//       nazwaTd.innerHTML = `<input type="text" name="nazwa_kategorii" class="form-control" value="${nazwa}">`;
//       opisTd.innerHTML = `<input type="text" name="opis_kategorii" class="form-control" value="${opis}">`;
//       zdjecieTd.innerHTML = `<input type="file" name="zdjecie" class="form-control mt-2" accept="image/*"></input>`;

//       this.textContent = "Zapisz";
//       this.classList.remove("btn-warning");
//       this.classList.add("btn-success");

//     } else if (this.textContent === "Zapisz") {
//       const formData = new FormData();
//       formData.append("katid", row.dataset.id);
//       formData.append("nazwa_kategorii", row.querySelector(".nazwa input").value);
//       formData.append("opis_kategorii", row.querySelector(".opis input[type=text]").value);

//       const zdjecieInput = row.querySelector(".zdjecie input[type=file]");
//       if (zdjecieInput && zdjecieInput.files.length > 0) {
//         formData.append("zdjecie", zdjecieInput.files[0]);
//       }

//       fetch("/edytuj_kategorie_wyceny", {
//         method: "POST",
//         body: formData
//       })
//       .then(res => res.json())
//         .then(data => {
//         if (data.success) {
//             nazwaTd.textContent = formData.get("nazwa_kategorii");
//             opisTd.textContent = formData.get("opis_kategorii");

//             // ← wpisujemy URL jako tekst
//             zdjecieTd.textContent = data.zdjecie_url || "brak";

//             this.textContent = "Edytuj";
//             this.classList.remove("btn-success");
//             this.classList.add("btn-warning");
//         } else {
//             alert("Błąd: " + data.error);
//         }
//         });
//     }
//   });
// });

// Edycja wiersza
document.querySelectorAll(".edytuj").forEach(btn => {
  btn.addEventListener("click", function () {
    const row = this.closest("tr");
    const id = row.dataset.id;
    const nazwaTd = row.querySelector(".nazwa");
    const opisTd = row.querySelector(".opis");
    const zdjecieTd = row.querySelector(".zdjecie");
    const widoczneTd = row.querySelector(".widoczne");

    if (this.textContent === "Edytuj") {
      const nazwa = nazwaTd.textContent.trim();
      const opis = opisTd.textContent.trim();

      // aktualny stan bool (z atrybutu lub tekstu)
      const currentBool =
        (widoczneTd.dataset.bool && widoczneTd.dataset.bool === "1") ||
        ["tak", "true", "1"].includes(widoczneTd.textContent.trim().toLowerCase());

      nazwaTd.innerHTML = `<input type="text" name="nazwa_kategorii" class="form-control" value="${nazwa}">`;
      opisTd.innerHTML = `<input type="text" name="opis_kategorii" class="form-control" value="${opis}">`;
      zdjecieTd.innerHTML = `<input type="file" name="zdjecie" class="form-control mt-2" accept="image/*">`;

      // checkbox dla "Widoczne dla klienta"
      widoczneTd.innerHTML = `
        <input type="checkbox" name="wycena_klienta" class="form-check-input" ${currentBool ? "checked" : ""}>
      `;

      this.textContent = "Zapisz";
      this.classList.remove("btn-warning");
      this.classList.add("btn-success");

    } else if (this.textContent === "Zapisz") {
      const formData = new FormData();
      formData.append("katid", row.dataset.id);
      formData.append("nazwa_kategorii", row.querySelector(".nazwa input").value);
      formData.append("opis_kategorii", row.querySelector(".opis input[type=text]").value);

      // wartość checkboxa
      const widoczneInput = row.querySelector('.widoczne input[type="checkbox"]');
      const widoczneVal = widoczneInput ? widoczneInput.checked : false;
      formData.append("wycena_klienta", widoczneVal ? "true" : "false");

      // plik (opcjonalnie)
      const zdjecieInput = row.querySelector(".zdjecie input[type=file]");
      if (zdjecieInput && zdjecieInput.files.length > 0) {
        formData.append("zdjecie", zdjecieInput.files[0]);
      }

      fetch("/edytuj_kategorie_wyceny", {
        method: "POST",
        body: formData
      })
      .then(res => res.json())
      .then(data => {
        if (data.success) {
          // odśwież widok komórek
          row.querySelector(".nazwa").textContent = formData.get("nazwa_kategorii");
          row.querySelector(".opis").textContent = formData.get("opis_kategorii");
          zdjecieTd.textContent = data.zdjecie_url || "brak";

          // „Widoczne” z powrotem jako Tak/Nie + atrybut data-bool
          widoczneTd.textContent = widoczneVal ? "Tak" : "Nie";
          widoczneTd.dataset.bool = widoczneVal ? "1" : "0";

          this.textContent = "Edytuj";
          this.classList.remove("btn-success");
          this.classList.add("btn-warning");
        } else {
          alert("Błąd: " + (data.error || "nieznany"));
        }
      })
      .catch(err => {
        console.error(err);
        alert("Wystąpił błąd połączenia.");
      });
    }
  });
});

// lista unikalych wartosci z kolumny nazwa kategorii
document.addEventListener("DOMContentLoaded", () => {
  fetch("pobierz_nazwy_kategorii")
    .then(res => res.json())
    .then(dane => {
      const datalist = document.getElementById("lista_kategorii");
      datalist.innerHTML = "";  // wyczyść

      dane.forEach(nazwa => {
        const option = document.createElement("option");
        option.value = nazwa;
        datalist.appendChild(option);
      });
    })
    .catch(err => {
      console.error("Nie udało się pobrać listy kategorii:", err);
    });
});


// obsługa formularza dodawania
document.getElementById("formularzDodajKategorie").addEventListener("submit", function (e) {
  e.preventDefault();
  const formData = new FormData(this);

//   fetch("/dodaj_kategorie_wyceny", {
//     method: "POST",
//     body: formData  
//   })
//   .then(res => res.json())
//   .then(data => {
//     if (data.success) {
//       location.reload();  
//     } else {
//       alert("Błąd: " + data.error);
//     }
//   })
//   .catch(err => {
//     console.error("Błąd sieci lub JSON:", err);
//   });

fetch("/dodaj_kategorie_wyceny", {
  method: "POST",
  body: formData
})
.then(async (res) => {
  // Sprawdź, czy odpowiedź jest OK (status 200–299)
  if (!res.ok) {
    const text = await res.text();  // odczytaj HTML/tekst błędu
    throw new Error(`HTTP ${res.status} – ${text}`);
  }

  // Spróbuj sparsować jako JSON
  return res.json();
})
.then(data => {
  if (data.success) {
    location.reload();  // lub dynamiczne dodanie do tabeli
  } else {
    alert("Błąd aplikacji: " + data.error);
  }
})
.catch(err => {
  console.error("Błąd sieci, JSON lub serwera:", err);
  alert("Wystąpił błąd:\n" + err.message);
});
});

// dodaj modal
document.addEventListener("DOMContentLoaded", function () {
  const modalEl = document.getElementById('dodajModal');
  const modal = new bootstrap.Modal(modalEl);  // działa tylko, jeśli modalEl istnieje
});


//uzuń wiersz
document.querySelectorAll(".usun").forEach(btn => {
  btn.addEventListener("click", function () {
    const row = this.closest("tr");
    const id = row.dataset.id;

    if (!confirm("Na pewno chcesz usunąć tę kategorię?")) return;

    const formData = new FormData();
    formData.append("katid", id);

    fetch("/usun_kategorie_wyceny", {
      method: "POST",
      body: formData
    })
      .then(res => res.json())
      .then(data => {
        if (data.success) {
          row.remove(); // usuń wiersz z tabeli
        } else {
          alert("Błąd: " + data.error);
        }
      })
      .catch(err => {
        console.error(err);
        alert("Wystąpił błąd połączenia.");
      });
  });
});

//filtruj tabele
function normalizeString(str) {
  return (str || "")
    .toString()
    .normalize("NFD")                
    .replace(/[\u0300-\u036f]/g, "") 
    .toLowerCase()
    .trim();
}


function debounce(fn, delay = 150) {
  let t;
  return (...args) => {
    clearTimeout(t);
    t = setTimeout(() => fn(...args), delay);
  };
}

(function initTableFilter() {
  const input = document.getElementById("filterInput");
  const clearBtn = document.getElementById("filterClear");
  const table = document.querySelector("table.table");
  if (!input || !table) return;

  const tbody = table.querySelector("tbody");
  const rows = Array.from(tbody.querySelectorAll("tr"));

  // wiersz „Brak wyników”
  let emptyRow = tbody.querySelector("tr.table-empty");
  if (!emptyRow) {
    emptyRow = document.createElement("tr");
    emptyRow.className = "table-empty";
    const td = document.createElement("td");
    td.colSpan = table.querySelectorAll("thead th").length;
    td.className = "text-center text-muted";
    td.textContent = "Brak wyników";
    emptyRow.appendChild(td);
    emptyRow.style.display = "none";
    tbody.appendChild(emptyRow);
  }

  function applyFilter() {
    const q = normalizeString(input.value);
    let visibleCount = 0;

    rows.forEach(tr => {
      // pomijaj wiersz „Brak wyników”
      if (tr.classList.contains("table-empty")) return;

      // zlep cały tekst z komórek wiersza
      const rowText = normalizeString(tr.textContent);
      const match = q === "" || rowText.includes(q);

      tr.style.display = match ? "" : "none";
      if (match) visibleCount++;
    });

    emptyRow.style.display = visibleCount === 0 ? "" : "none";
  }

  const debounced = debounce(applyFilter, 150);

  input.addEventListener("input", debounced);
  clearBtn.addEventListener("click", () => {
    input.value = "";
    applyFilter();
    input.focus();
  });

  // jeśli chcesz: Enter = zaznacz cały tekst (wygoda UX)
  input.addEventListener("keydown", (e) => {
    if (e.key === "Escape") {
      input.value = "";
      applyFilter();
    }
  });
})();