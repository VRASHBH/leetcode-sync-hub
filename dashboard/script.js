async function loadStats(){

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
}

async function loadSolutions(){

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
}

loadStats();
loadSolutions();