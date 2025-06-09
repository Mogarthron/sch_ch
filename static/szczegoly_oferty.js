document.querySelectorAll(".edytujWiersz").forEach(button => {
    button.addEventListener("click", function () {
        const row = this.closest("tr");
        const opisTd = row.querySelector(".opis");
        const iloscTd = row.querySelector(".ilosc");
        const cenaTd = row.querySelector(".cena");

        if (this.textContent === "Edytuj") {
            const opis = opisTd.textContent
            const ilosc = iloscTd.textContent.trim();
            const cena = cenaTd.textContent.trim();

            opisTd.innerHTML = `<input type="text" value="${opis}" class="form-control">`;
            iloscTd.innerHTML = `<input type="text" value="${ilosc}" class="form-control">`;
            cenaTd.innerHTML = `<input type="text" value="${cena}" class="form-control">`;

            this.textContent = "Zatwierdź";
            this.classList.remove("btn-warning");
            this.classList.add("btn-success");

        } else {
            const id = row.dataset.id;
            const opis = opisTd.querySelector("input").value;
            const ilosc = iloscTd.querySelector("input").value;
            const cena = cenaTd.querySelector("input").value;

            fetch("/szczegoly_oferty_edytuj_wiersz", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ id: id, opis: opis, ilosc: ilosc, cena: cena })
            })
            .then(resp => resp.json())
            .then(data => {
                if (data.success) {
                    opisTd.textContent = opis;
                    iloscTd.textContent = ilosc;
                    cenaTd.textContent = cena;
                    this.textContent = "Edytuj";
                    this.classList.remove("btn-success");
                    this.classList.add("btn-warning");
                } else {
                    alert("Błąd przy zapisie: " + data.error);
                }
            });
        }
    });
});