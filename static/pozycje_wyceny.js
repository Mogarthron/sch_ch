//Edycja wiersza
// document.querySelectorAll(".edytuj").forEach(btn => {
//   btn.addEventListener("click", function () {
//     const row = this.closest("tr");
//     const id = row.dataset.id;
//     const pozycjaTd = row.querySelector(".pozycja");
//     const cenaTd = row.querySelector(".cena");
//     const miaraTd = row.querySelector(".miara");

//     if (this.textContent === "Edytuj") {
//       const pozycja = pozycjaTd.textContent.trim();
//       const cena = cenaTd.textContent.trim();
//       const miara = opisTd.textContent.trim();

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

document.querySelectorAll(".edytuj").forEach(btn => {
  btn.addEventListener("click", function () {
    const row = this.closest("tr");
    const id = row.dataset.id;

    const pozycjaTd = row.querySelector(".pozycja");
    const cenaTd = row.querySelector(".cena");
    const materialTd = row.querySelector(".cena_mat");
    const miaraTd = row.querySelector(".miara");

    if (this.textContent === "Edytuj") {
      const pozycja = pozycjaTd.textContent.trim();
      const cena = cenaTd.textContent.trim();
      const material = cenaTd.textContent.trim();
      const miara = miaraTd.textContent.trim();

      pozycjaTd.innerHTML = `<input type="text" class="form-control" value="${pozycja}">`;
      cenaTd.innerHTML = `<input type="number" step="0.01" class="form-control" value="${cena}">`;
      materialTd.innerHTML = `<input type="number" step="0.01" class="form-control" value="${material}">`;
      miaraTd.innerHTML = `<input type="text" class="form-control" value="${miara}">`;

      this.textContent = "Zapisz";
      this.classList.remove("btn-warning");
      this.classList.add("btn-success");
    } else if (this.textContent === "Zapisz") {
      const nowaPozycja = pozycjaTd.querySelector("input").value;
      const nowaCena = cenaTd.querySelector("input").value;
      const nowaMaterial = cenaTd.querySelector("input").value;
      const nowaMiara = miaraTd.querySelector("input").value;

      fetch("/edytuj_pozycje_wyceny", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          cid: id,
          pozycja: nowaPozycja,
          cena_jednostkowa: nowaCena,
          cena_materialu: nowaMaterial,
          jednostka_miary: nowaMiara
        })
      })
      .then(res => res.json())
      .then(data => {
        if (data.success) {
          // Aktualizuj wiersz
          pozycjaTd.textContent = nowaPozycja;
          cenaTd.textContent = parseFloat(nowaCena).toFixed(2);
          materialTd.textContent = parseFloat(nowaMaterial).toFixed(2);
          miaraTd.textContent = nowaMiara;

          this.textContent = "Edytuj";
          this.classList.remove("btn-success");
          this.classList.add("btn-warning");

          const dataEdytowana = new Date().toISOString().slice(0, 19).replace("T", " ");
          row.querySelector(".data_edycja").textContent = dataEdytowana;
        } else {
          alert("Błąd: " + data.error);
        }
      })
      .catch(err => {
        console.error("Błąd sieci:", err);
        alert("Błąd połączenia z serwerem.");
      });
    }
  });
});


// lista unikalych wartosci z kolumny nazwa kategorii
document.addEventListener("DOMContentLoaded", () => {
  fetch("pobierz_nazwy_podkategorii")
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


// // obsługa formularza dodawania
document.addEventListener("DOMContentLoaded", function () {
  const form = document.getElementById("formularzPozycjeWyceny");

  form.addEventListener("submit", function (e) {
    e.preventDefault();

    const formData = new FormData(form);

    fetch("/dodaj_pozycje_wyceny", {
      method: "POST",
      body: formData
    })
    .then(async (res) => {
      if (!res.ok) {
        const text = await res.text();
        throw new Error(`HTTP ${res.status} – ${text}`);
      }
      return res.json();
    })
    .then(data => {
      if (data.success) {
        // Sukces: np. reload lub dynamiczne dodanie
        location.reload();
      } else {
        alert("Błąd aplikacji: " + data.error);
      }
    })
    .catch(err => {
      console.error("Błąd sieci, JSON lub serwera:", err);
      alert("Wystąpił błąd:\n" + err.message);
    });

    return false; // zabezpieczenie przed domyślnym submitem
  });
});


// dodaj modal
document.addEventListener("DOMContentLoaded", function () {
  const modalEl = document.getElementById('dodajModal');
  const modal = new bootstrap.Modal(modalEl);  // działa tylko, jeśli modalEl istnieje
});


// filtorwanie tabeli 
document.addEventListener("DOMContentLoaded", () => {
  const filtrKategoria = document.getElementById("filtr_kategoria");
  const filtrNazwa = document.getElementById("filtr_nazwa");

  // Automatyczne generowanie unikalnych opcji do selecta z kolumny "nazwa_kategorii"
  const kategorieSet = new Set();
  document.querySelectorAll("table tbody tr").forEach(row => {
    const kategoria = row.querySelector(".nazwa_kategorii").textContent.trim();
    if (kategoria) kategorieSet.add(kategoria);
  });

  const selectKategoria = document.getElementById("filtr_kategoria");
  [...kategorieSet].sort().forEach(kat => {
    const option = document.createElement("option");
    option.value = kat;
    option.textContent = kat;
    selectKategoria.appendChild(option);
  });

  const filtrujTabele = () => {
    const kategoriaWartosc = filtrKategoria.value.toLowerCase();
    const nazwaWartosc = filtrNazwa.value.toLowerCase();

    document.querySelectorAll("table tbody tr").forEach(row => {
      const kolKategoria = row.querySelector(".nazwa_kategorii").textContent.toLowerCase();
      const kolNazwa = row.querySelector(".pod_kategoria").textContent.toLowerCase();

      const pokaz =
        kolKategoria.includes(kategoriaWartosc) &&
        kolNazwa.includes(nazwaWartosc);

      row.style.display = pokaz ? "" : "none";
    });
  };

  filtrKategoria.addEventListener("input", filtrujTabele);
  filtrNazwa.addEventListener("input", filtrujTabele);
});
