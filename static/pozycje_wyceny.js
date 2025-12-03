// document.querySelectorAll(".edytuj").forEach(btn => {
//   btn.addEventListener("click", function () {
//     const row = this.closest("tr");
//     const id = row.dataset.id;

//     const pozycjaTd = row.querySelector(".pozycja");
//     const cenaTd = row.querySelector(".cena");
//     const materialTd = row.querySelector(".cena_mat");
//     const miaraTd = row.querySelector(".miara");

//     if (this.textContent === "Edytuj") {
//       const pozycja = pozycjaTd.textContent.trim();
//       const cena = cenaTd.textContent.trim();
//       const material = materialTd.textContent.trim();
//       const miara = miaraTd.textContent.trim();

//       pozycjaTd.innerHTML = `<input type="text" class="form-control" value="${pozycja}">`;
//       cenaTd.innerHTML = `<input type="number" step="0.01" class="form-control" value="${cena}">`;
//       materialTd.innerHTML = `<input type="number" step="0.01" class="form-control" value="${material}">`;
//       miaraTd.innerHTML = `<input type="text" class="form-control" value="${miara}">`;

//       this.textContent = "Zapisz";
//       this.classList.remove("btn-warning");
//       this.classList.add("btn-success");
//     } else if (this.textContent === "Zapisz") {
//       const nowaPozycja = pozycjaTd.querySelector("input").value;
//       const nowaCena = cenaTd.querySelector("input").value;
//       const nowaMaterial = materialTd.querySelector("input").value;
//       const nowaMiara = miaraTd.querySelector("input").value;

//       fetch("/edytuj_pozycje_wyceny", {
//         method: "POST",
//         headers: { "Content-Type": "application/json" },
//         body: JSON.stringify({
//           cid: id,
//           pozycja: nowaPozycja,
//           cena_jednostkowa: nowaCena,
//           cena_materialu: nowaMaterial,
//           jednostka_miary: nowaMiara
//         })
//       })
//       .then(res => res.json())
//       .then(data => {
//         if (data.success) {
//           // Aktualizuj wiersz
//           pozycjaTd.textContent = nowaPozycja;
//           cenaTd.textContent = parseFloat(nowaCena).toFixed(2);
//           materialTd.textContent = parseFloat(nowaMaterial).toFixed(2);
//           miaraTd.textContent = nowaMiara;

//           this.textContent = "Edytuj";
//           this.classList.remove("btn-success");
//           this.classList.add("btn-warning");

//           const dataEdytowana = new Date().toISOString().slice(0, 19).replace("T", " ");
//           row.querySelector(".data_edycja").textContent = dataEdytowana;
//         } else {
//           alert("Błąd: " + data.error);
//         }
//       })
//       .catch(err => {
//         console.error("Błąd sieci:", err);
//         alert("Błąd połączenia z serwerem.");
//       });
//     }
//   });
// });


// // lista unikalych wartosci z kolumny nazwa kategorii
// document.addEventListener("DOMContentLoaded", () => {
//   fetch("pobierz_nazwy_podkategorii")
//     .then(res => res.json())
//     .then(dane => {
//       const datalist = document.getElementById("lista_kategorii");
//       datalist.innerHTML = "";  // wyczyść

//       dane.forEach(nazwa => {
//         const option = document.createElement("option");
//         option.value = nazwa;
//         datalist.appendChild(option);
//       });
//     })
//     .catch(err => {
//       console.error("Nie udało się pobrać listy kategorii:", err);
//     });
// });


// // // obsługa formularza dodawania
// document.addEventListener("DOMContentLoaded", function () {
//   const form = document.getElementById("formularzPozycjeWyceny");

//   form.addEventListener("submit", function (e) {
//     e.preventDefault();

//     const formData = new FormData(form);

//     fetch("/dodaj_pozycje_wyceny", {
//       method: "POST",
//       body: formData
//     })
//     .then(async (res) => {
//       if (!res.ok) {
//         const text = await res.text();
//         throw new Error(`HTTP ${res.status} – ${text}`);
//       }
//       return res.json();
//     })
//     .then(data => {
//       if (data.success) {
//         // Sukces: np. reload lub dynamiczne dodanie
//         location.reload();
//       } else {
//         alert("Błąd aplikacji: " + data.error);
//       }
//     })
//     .catch(err => {
//       console.error("Błąd sieci, JSON lub serwera:", err);
//       alert("Wystąpił błąd:\n" + err.message);
//     });

//     return false; // zabezpieczenie przed domyślnym submitem
//   });
// });


// // dodaj modal
// document.addEventListener("DOMContentLoaded", function () {
//   const modalEl = document.getElementById('dodajModal');
//   const modal = new bootstrap.Modal(modalEl);  // działa tylko, jeśli modalEl istnieje
// });


// // filtorwanie tabeli 
// document.addEventListener("DOMContentLoaded", () => {
//   const filtrKategoria = document.getElementById("filtr_kategoria");
//   const filtrNazwa = document.getElementById("filtr_nazwa");

//   // Automatyczne generowanie unikalnych opcji do selecta z kolumny "nazwa_kategorii"
//   const kategorieSet = new Set();
//   document.querySelectorAll("table tbody tr").forEach(row => {
//     const kategoria = row.querySelector(".nazwa_kategorii").textContent.trim();
//     if (kategoria) kategorieSet.add(kategoria);
//   });

//   const selectKategoria = document.getElementById("filtr_kategoria");
//   [...kategorieSet].sort().forEach(kat => {
//     const option = document.createElement("option");
//     option.value = kat;
//     option.textContent = kat;
//     selectKategoria.appendChild(option);
//   });

//   const filtrujTabele = () => {
//     const kategoriaWartosc = filtrKategoria.value.toLowerCase();
//     const nazwaWartosc = filtrNazwa.value.toLowerCase();

//     document.querySelectorAll("table tbody tr").forEach(row => {
//       const kolKategoria = row.querySelector(".nazwa_kategorii").textContent.toLowerCase();
//       const kolNazwa = row.querySelector(".pod_kategoria").textContent.toLowerCase();

//       const pokaz =
//         kolKategoria.includes(kategoriaWartosc) &&
//         kolNazwa.includes(nazwaWartosc);

//       row.style.display = pokaz ? "" : "none";
//     });
//   };

//   filtrKategoria.addEventListener("input", filtrujTabele);
//   filtrNazwa.addEventListener("input", filtrujTabele);
// });

document.querySelectorAll(".edytuj").forEach(btn => {
  btn.addEventListener("click", function () {
    const row = this.closest("tr");
    const id = row.dataset.id;

    const pozycjaTd = row.querySelector(".pozycja");
    const cenaTd = row.querySelector(".cena");
    const materialTd = row.querySelector(".cena_mat");
    const miaraTd = row.querySelector(".miara");
    const zdjecieTd = row.querySelector(".zdjecie");

    if (this.textContent === "Edytuj") {
      const pozycja = pozycjaTd.textContent.trim();
      const cena = cenaTd.textContent.trim();
      const material = materialTd.textContent.trim();
      const miara = miaraTd.textContent.trim();

      const aktualnyTekstZdjecia = zdjecieTd.textContent.trim();

      pozycjaTd.innerHTML = `<input type="text" class="form-control" value="${pozycja}">`;
      cenaTd.innerHTML = `<input type="number" step="0.01" class="form-control" value="${cena}">`;
      materialTd.innerHTML = `<input type="number" step="0.01" class="form-control" value="${material}">`;
      miaraTd.innerHTML = `<input type="text" class="form-control" value="${miara}">`;

      // input file zamiast textboxa na url
      zdjecieTd.innerHTML = `
        <input type="file" class="form-control" accept="image/*">
        <div class="small text-muted mt-1">
          Aktualnie: ${aktualnyTekstZdjecia || "brak zdjęcia"}
        </div>
      `;

      this.textContent = "Zapisz";
      this.classList.remove("btn-warning");
      this.classList.add("btn-success");

    } else if (this.textContent === "Zapisz") {
      const nowaPozycja = pozycjaTd.querySelector("input").value;
      const nowaCena = cenaTd.querySelector("input").value;
      const nowaMaterial = materialTd.querySelector("input").value;
      const nowaMiara = miaraTd.querySelector("input").value;
      const fileInput = zdjecieTd.querySelector('input[type="file"]');

      const formData = new FormData();
      formData.append("cid", id);
      formData.append("pozycja", nowaPozycja);
      formData.append("cena_jednostkowa", nowaCena);
      formData.append("cena_materialu", nowaMaterial);
      formData.append("jednostka_miary", nowaMiara);

      if (fileInput && fileInput.files.length > 0) {
        formData.append("zdjecie", fileInput.files[0]);
      }

      fetch("/edytuj_pozycje_wyceny", {
        method: "POST",
        body: formData
      })
      .then(res => res.json())
      .then(data => {
        if (data.success) {
          // Aktualizuj wiersz
          pozycjaTd.textContent = nowaPozycja;
          cenaTd.textContent = parseFloat(nowaCena || 0).toFixed(2);
          materialTd.textContent = parseFloat(nowaMaterial || 0).toFixed(2);
          miaraTd.textContent = nowaMiara;

          if (data.zdjecie_url) {
            zdjecieTd.textContent = data.zdjecie_url;
          } else {
            zdjecieTd.innerHTML = `<span class="text-muted small">brak zdjęcia</span>`;
          }

          this.textContent = "Edytuj";
          this.classList.remove("btn-success");
          this.classList.add("btn-warning");

          const dataEdytowana = new Date().toISOString().slice(0, 16).replace("T", " ");
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
