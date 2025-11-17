async function loadTournaments() {
    const feed = document.getElementById("tournamentFeed");

    try {
        let res = await fetch("http://127.0.0.1:8000/tournaments"); // your FastAPI route
        let tournaments = await res.json();

        if (tournaments.length === 0) {
            feed.innerHTML = "<p>No tournaments found.</p>";
            return;
        }

        feed.innerHTML = "";

        tournaments.forEach(t => {
            const card = document.createElement("div");
            card.innerHTML = `
                <h3>${t.name}</h3>
                <p>Date: ${t.date}</p>
                <p>Created by User ID: ${t.user_id}</p>
                <hr>
            `;
            feed.appendChild(card);
        });

    } catch (error) {
        feed.innerHTML = "<p>Error loading tournaments.</p>";
        console.error(error);
    }
}

loadTournaments();
