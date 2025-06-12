//Edycja wiersza
document.querySelectorAll(".edytuj").forEach(btn => {
  btn.addEventListener("click", function () {
    const row = this.closest("tr");
    const id = row.dataset.id;
    const nazwaTd = row.querySelector(".nazwa");
    const opisTd = row.querySelector(".opis");
    const zdjecieTd = row.querySelector(".zdjecie");

    if (this.textContent === "Edytuj") {
      const nazwa = nazwaTd.textContent.trim();
      const opis = opisTd.textContent.trim();
    //   const zdjecie = opisTd.textContent.trim();

      nazwaTd.innerHTML = `<input type="text" name="nazwa_kategorii" class="form-control" value="${nazwa}">`;
      opisTd.innerHTML = `<input type="text" name="opis_kategorii" class="form-control" value="${opis}">`;
      zdjecieTd.innerHTML = `<input type="file" name="zdjecie" class="form-control mt-2" accept="image/*"></input>`;

      this.textContent = "Zapisz";
      this.classList.remove("btn-warning");
      this.classList.add("btn-success");

    } else if (this.textContent === "Zapisz") {
      const formData = new FormData();
      formData.append("katid", row.dataset.id);
      formData.append("nazwa_kategorii", row.querySelector(".nazwa input").value);
      formData.append("opis_kategorii", row.querySelector(".opis input[type=text]").value);

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
            nazwaTd.textContent = formData.get("nazwa_kategorii");
            opisTd.textContent = formData.get("opis_kategorii");

            // ← wpisujemy URL jako tekst
            zdjecieTd.textContent = data.zdjecie_url || "brak";

            this.textContent = "Edytuj";
            this.classList.remove("btn-success");
            this.classList.add("btn-warning");
        } else {
            alert("Błąd: " + data.error);
        }
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