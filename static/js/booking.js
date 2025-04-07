document.addEventListener("DOMContentLoaded", function() {
    const tabs = document.querySelectorAll(".tab-btn");
    const tabContents = document.querySelectorAll(".tab-content");
    const reviewBtn = document.querySelectorAll(".review-btn");
    tabs.forEach(tab => {
      tab.addEventListener("click", function() {
        tabs.forEach(t => t.classList.remove("active"));
        tabContents.forEach(content => content.classList.remove("active"));
        this.classList.add("active");
        document.getElementById(this.getAttribute("data-tab")).classList.add("active");
      });
    });

    const searchInputIncoming = document.getElementById("search-input-incoming");
    const statusFilterIncoming = document.getElementById("status-filter-incoming");
    const bookingCardsIncoming = document.querySelectorAll("#bookingsCards-incoming .booking-card");
    const exportBtnIncoming = document.getElementById("export-btn-incoming");
    
    function filterCardsIncoming() {
        const query = searchInputIncoming.value.toLowerCase().trim();
        const statusValue = statusFilterIncoming.value;
        let visibleCount = 0;
        bookingCardsIncoming.forEach(card => {
            const cardStatus = card.getAttribute("data-status");
            const cardClient = card.getAttribute("data-client");
            const cardProblem = card.getAttribute("data-problem");
            const statusMatch = !statusValue || (cardStatus === statusValue);
            const searchMatch = cardClient.includes(query) || cardProblem.includes(query);
            if (statusMatch && searchMatch) {
                card.style.display = "";
                visibleCount++;
            } else {
                card.style.display = "none";
            }
        });
        document.getElementById("no-results-incoming").style.display = visibleCount === 0 ? "block" : "none";
    }
    searchInputIncoming.addEventListener("input", filterCardsIncoming);
    statusFilterIncoming.addEventListener("change", filterCardsIncoming);

    exportBtnIncoming.addEventListener("click", function() {
        let csvContent = "data:text/csv;charset=utf-8,Клиент;Описание;Интервалы;Дата создания;Статус\n";
        bookingCardsIncoming.forEach(card => {
            if (card.style.display !== "none") {
                const client = card.getAttribute("data-client");
                const problem = card.getAttribute("data-problem");
                const paragraphs = card.querySelectorAll("p");
                const intervals = paragraphs[1].innerText.replace("Предпочтительные интервалы:", "").trim();
                const createdAt = paragraphs[2].innerText.replace("Дата создания:", "").trim();
                const status = paragraphs[3].innerText.replace("Статус:", "").trim();
                csvContent += [client, problem, intervals, createdAt, status].join(";") + "\n";
            }
        });
        const encodedUri = encodeURI(csvContent);
        const link = document.createElement("a");
        link.setAttribute("href", encodedUri);
        link.setAttribute("download", "incoming_bookings_export.csv");
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    });

    const searchInputOutgoing = document.getElementById("search-input-outgoing");
    const statusFilterOutgoing = document.getElementById("status-filter-outgoing");
    const bookingCardsOutgoing = document.querySelectorAll("#bookingsCards-outgoing .booking-card");
    const exportBtnOutgoing = document.getElementById("export-btn-outgoing");
    
    function filterCardsOutgoing() {
        const query = searchInputOutgoing.value.toLowerCase().trim();
        const statusValue = statusFilterOutgoing.value;
        let visibleCount = 0;
        bookingCardsOutgoing.forEach(card => {
            const cardStatus = card.getAttribute("data-status");
            const cardClient = card.getAttribute("data-client");
            const cardProblem = card.getAttribute("data-problem");
            const statusMatch = !statusValue || (cardStatus === statusValue);
            const searchMatch = cardClient.includes(query) || cardProblem.includes(query);
            if (statusMatch && searchMatch) {
                card.style.display = "";
                visibleCount++;
            } else {
                card.style.display = "none";
            }
        });
        document.getElementById("no-results-outgoing").style.display = visibleCount === 0 ? "block" : "none";
    }
    searchInputOutgoing.addEventListener("input", filterCardsOutgoing);
    statusFilterOutgoing.addEventListener("change", filterCardsOutgoing);

    exportBtnOutgoing.addEventListener("click", function() {
        let csvContent = "data:text/csv;charset=utf-8,Эксперт;Описание;Интервалы;Дата создания;Статус\n";
        bookingCardsOutgoing.forEach(card => {
            if (card.style.display !== "none") {
                const client = card.getAttribute("data-client");
                const problem = card.getAttribute("data-problem");
                const paragraphs = card.querySelectorAll("p");
                const intervals = paragraphs[1].innerText.replace("Предпочтительные интервалы:", "").trim();
                const createdAt = paragraphs[2].innerText.replace("Дата создания:", "").trim();
                const status = paragraphs[3].innerText.replace("Статус:", "").trim();
                csvContent += [client, problem, intervals, createdAt, status].join(";") + "\n";
            }
        });
        const encodedUri = encodeURI(csvContent);
        const link = document.createElement("a");
        link.setAttribute("href", encodedUri);
        link.setAttribute("download", "outgoing_bookings_export.csv");
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    });

    document.querySelectorAll(".btn-delete").forEach(button => {
        button.addEventListener("click", async function() {
            if (!confirm("Вы уверены, что хотите удалить запись?")) return;
            const bookingId = this.getAttribute("data-id");
            const url = `/booking/${bookingId}/delete/`;
            try {
                const response = await fetch(url, {
                    method: "POST",
                    headers: {
                        "X-CSRFToken": getCsrfToken(),
                        "Content-Type": "application/json"
                    }
                });
                if (!response.ok) throw new Error("Ошибка удаления!");
                this.closest(".booking-card").remove();
            } catch (error) {
                console.error("❌ Ошибка при удалении:", error);
            }
        });
    });

    function getCsrfToken() {
        return document.querySelector("[name=csrfmiddlewaretoken]").value;
    }
});