async function loadStats() {
    try {
        const response = await fetch(
            "http://127.0.0.1:8000/stats"
        );

        const data = await response.json();

        document.getElementById("total").innerText =
            data.total_solved;

        document.getElementById("easy").innerText =
            data.easy;

        document.getElementById("medium").innerText =
            data.medium;

        document.getElementById("hard").innerText =
            data.hard;

        createChart(
            data.easy,
            data.medium,
            data.hard
        );

    } catch (error) {
        console.error("Stats Error:", error);
    }
}

function createChart(easy, medium, hard) {

    const ctx =
        document.getElementById("difficultyChart");

    if (!ctx) return;

    new Chart(ctx, {
        type: "pie",

        data: {
            labels: [
                "Easy",
                "Medium",
                "Hard"
            ],

            datasets: [{
                data: [
                    easy,
                    medium,
                    hard
                ]
            }]
        }
    });
}

async function loadSolutions() {

    try {

        const response = await fetch(
            "http://127.0.0.1:8000/solutions"
        );

        const data = await response.json();

        const list =
            document.getElementById("solutions");

        list.innerHTML = "";

        data.forEach(solution => {

            const li =
                document.createElement("li");

            li.innerText =
                `${solution[0]} (${solution[1]})`;

            list.appendChild(li);
        });

    } catch (error) {
        console.error("Solutions Error:", error);
    }
}

function setupSearch() {

    const search =
        document.getElementById("search");

    if (!search) return;

    search.addEventListener(
        "input",
        function () {

            const value =
                this.value.toLowerCase();

            const items =
                document.querySelectorAll(
                    "#solutions li"
                );

            items.forEach(item => {

                item.style.display =
                    item.innerText
                        .toLowerCase()
                        .includes(value)

                        ? "block"
                        : "none";
            });
        }
    );
}

function loadStreak() {

    document.getElementById("streak")
        .innerText = "7 Days";
}

document.addEventListener(
    "DOMContentLoaded",
    () => {

        loadStats();
        loadSolutions();
        loadStreak();
        setupSearch();
    }
);