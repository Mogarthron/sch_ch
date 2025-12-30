function dodajWiersz(button) {
      const sekcja = button.closest(".tabela-sekcja");
      const tabela = sekcja.querySelector("table tbody");

      const nowyWiersz = tabela.insertRow();

      // Komórka: Opis
      const komorkaOpis = nowyWiersz.insertCell(0);
      const inputOpis = document.createElement("input");
      inputOpis.type = "text";
      inputOpis.name = "tabela_opis[]";
      inputOpis.className = "form-control";
      komorkaOpis.appendChild(inputOpis);

      // Komórka: Ilość
      const komorkaIlosc = nowyWiersz.insertCell(1);
      const inputIlosc = document.createElement("input");
      inputIlosc.type = "text";
      inputIlosc.name = "tabela_ilosc[]";
      inputIlosc.className = "form-control";
      inputIlosc.addEventListener("keypress", function (e) {
          const char = String.fromCharCode(e.which);

          // Zezwól tylko na cyfry i kropkę
          if (!/[0-9.]/.test(char)) {
            e.preventDefault();
          }

          // Blokuj wprowadzenie drugiej kropki
          if (char === "." && this.value.includes(".")) {
            e.preventDefault();
          }

          // Blokuj przecinek jako separator
          if (char === ",") {
            e.preventDefault();
          }
      });
      komorkaIlosc.appendChild(inputIlosc);

      // Komórka: Cena
      const komorkaCena = nowyWiersz.insertCell(2);
      const inputGroup = document.createElement("div");
      inputGroup.className = "input-group";

      const inputCena = document.createElement("input");
      inputCena.type = "text";
      inputCena.name = "tabela_cena[]";
      inputCena.className = "form-control";

      const addon = document.createElement("span");
      addon.className = "input-group-text";
      addon.textContent = "zł";

      inputGroup.appendChild(inputCena);
      inputGroup.appendChild(addon);
      komorkaCena.appendChild(inputGroup);

      // Komórka: Usuń
      const komorkaUsun = nowyWiersz.insertCell(3);
      const btnUsun = document.createElement("button");
      btnUsun.type = "button";
      btnUsun.className = "btn btn-danger btn-sm";
      btnUsun.textContent = "Usuń";
      btnUsun.onclick = function () {
        nowyWiersz.remove();
      };
      komorkaUsun.appendChild(btnUsun);
    }

function zatwierdzTabele(button) {
  const sekcja = button.closest('.tabela-sekcja');
  const tabela = sekcja.querySelector('table');
  const tbody = tabela.querySelector('tbody');
  const sekcjaNazwa = sekcja.getAttribute("data-sekcja");
  const nrZlecenia = sekcja.getAttribute("data-nr_zlecenia");

  const wiersze = [];

  for (const row of tbody.rows) {
    const cells = row.cells;

    const opisInput = cells[0].querySelector("input");
    const iloscInput = cells[1].querySelector("input");
    const cenaInput = cells[2].querySelector("input");

    const opis = opisInput ? opisInput.value : "";
    const ilosc = iloscInput ? iloscInput.value : "";
    const cena = cenaInput ? parseFloat(cenaInput.value) || 0 : 0;

    // Zamień inputy na tekst
    cells[0].textContent = opis;
    cells[1].textContent = ilosc;
    cells[2].textContent = cena.toFixed(2) + " zł";

    // Zapisz dane do wysyłki
    wiersze.push({ opis, ilosc, cena });
  }

  // Usuń kolumnę przycisków
  for (const row of tabela.rows) {
    row.deleteCell(-1);
  }

  // Usuń wszystkie przyciski
  sekcja.querySelectorAll("button").forEach(btn => btn.remove());

  // // Dodaj przycisk "Edytuj"
  // const btnEdytuj = document.createElement("button");
  // btnEdytuj.type = "button";
  // btnEdytuj.className = "btn btn-secondary mt-2";
  // btnEdytuj.textContent = "Edytuj";
  // btnEdytuj.onclick = function () {
  //   edytujTabele(btnEdytuj);
  // };
  // sekcja.appendChild(btnEdytuj);

  // Przygotuj dane do wysyłki
  const dane = {
    nr_zlecenia: nrZlecenia,
    sekcja: sekcjaNazwa,
    wiersze: wiersze
  };

  // Wyślij do backendu
  fetch(`/oferta_szczegoly/${nrZlecenia}`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(dane),
  })
    .then((res) => {
      if (!res.ok) throw new Error("Błąd zapisu danych");
      return res.text();
    })
    .then(msg => console.log("Zapisano:", msg))
    .catch(err => console.error("Błąd zapisu:", err));
}

function edytujTabele(button) {
    const sekcja = button.closest(".tabela-sekcja");
    const tabela = sekcja.querySelector("table");
    const tbody = tabela.querySelector("tbody");

    for (const row of tbody.rows) {
      const opis = row.cells[0].textContent;
      const ilosc = row.cells[1].textContent;
      const cena = row.cells[2].textContent.replace(" zł", "");

      row.innerHTML = "";

      // Opis
      const cellOpis = row.insertCell(0);
      const inputOpis = document.createElement("input");
      inputOpis.type = "text";
      inputOpis.name = "tabela_opis[]";
      inputOpis.className = "form-control";
      inputOpis.value = opis;
      cellOpis.appendChild(inputOpis);

      // Ilość
      const cellIlosc = row.insertCell(1);
      const inputIlosc = document.createElement("input");
      inputIlosc.type = "text";
      inputIlosc.name = "tabela_ilosc[]";
      inputIlosc.className = "form-control";
      inputIlosc.value = ilosc;
      cellIlosc.appendChild(inputIlosc);

      // Cena
      const cellCena = row.insertCell(2);
      const inputGroup = document.createElement("div");
      inputGroup.className = "input-group";
      const inputCena = document.createElement("input");
      inputCena.type = "text";
      inputCena.name = "tabela_cena[]";
      inputCena.className = "form-control";
      inputCena.value = cena;
      const addon = document.createElement("span");
      addon.className = "input-group-text";
      addon.textContent = "zł";
      inputGroup.appendChild(inputCena);
      inputGroup.appendChild(addon);
      cellCena.appendChild(inputGroup);

      // Usuń
      const cellUsun = row.insertCell(3);
      const btnUsun = document.createElement("button");
      btnUsun.type = "button";
      btnUsun.className = "btn btn-danger btn-sm";
      btnUsun.textContent = "Usuń";
      btnUsun.onclick = function () {
        row.remove();
      };
      cellUsun.appendChild(btnUsun);
    }

    // Usuń przycisk "Edytuj"
    button.remove();

    // Dodaj przyciski "Dodaj wiersz" i "Zatwierdź"
    const btnDodaj = document.createElement("button");
    btnDodaj.type = "button";
    btnDodaj.className = "btn btn-success me-2";
    btnDodaj.textContent = "+ Dodaj wiersz";
    btnDodaj.onclick = function () {
      dodajWiersz(btnDodaj);
    };

    const btnZatwierdz = document.createElement("button");
    btnZatwierdz.type = "button";
    btnZatwierdz.className = "btn btn-primary";
    btnZatwierdz.textContent = "Zatwierdź tabelę";
    btnZatwierdz.onclick = function () {
      zatwierdzTabele(btnZatwierdz);
    };

    sekcja.appendChild(btnDodaj);
    sekcja.appendChild(btnZatwierdz);
  }
