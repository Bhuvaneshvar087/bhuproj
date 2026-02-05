let startTime = Date.now();

const topicSelect = document.getElementById("topicSelect");
const questionEl = document.getElementById("question");

topicSelect.addEventListener("change", () => {
    fetch(`/question?topic=${topicSelect.value}`)
        .then(res => res.json())
        .then(q => {
            questionEl.innerText = q;
            startTime = Date.now();
        });
});

function submitAnswer() {
    const timeTaken = (Date.now() - startTime) / 1000;

    fetch("/submit", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            topic: topicSelect.value,
            answer: document.getElementById("answer").value,
            time: timeTaken
        })
    })
    .then(res => res.json())
    .then(data => {
        document.getElementById("feedback").innerText =
            data.status === "correct" ? "✅ Correct Answer" : "❌ Incorrect Answer";
        document.getElementById("answer").value = "";
        startTime = Date.now();
    });
}

function loadReport() {
    fetch("/report")
        .then(res => res.json())
        .then(data => {
            let html = "<h3>📊 Weak-Area Report</h3>";
            data.forEach(r => {
                html += `<p><b>${r.topic}</b> → ${r.status}
                (Accuracy: ${r.accuracy}%, Avg Time: ${r.avg_time}s)</p>`;
            });
            document.getElementById("report").innerHTML = html;
        });
}
