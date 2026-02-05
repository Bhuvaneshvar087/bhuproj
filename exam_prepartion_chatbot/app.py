from flask import Flask, render_template, request, jsonify
import time, json
from database import load_performance, save_performance

app = Flask(__name__)

TIME_THRESHOLD = 60

with open("data/questions.json", "r") as f:
    QUESTIONS = json.load(f)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/question")
def get_question():
    topic = request.args.get("topic")
    return jsonify(QUESTIONS[topic]["question"])

@app.route("/submit", methods=["POST"])
def submit_answer():
    data = request.json
    topic = data["topic"]
    answer = data["answer"].lower()
    time_taken = data["time"]

    correct_answer = QUESTIONS[topic]["answer"]
    is_correct = correct_answer in answer

    performance = load_performance()

    if topic not in performance:
        performance[topic] = {
            "attempts": 0,
            "incorrect": 0,
            "total_time": 0,
            "repeated_errors": 0
        }

    performance[topic]["attempts"] += 1
    performance[topic]["total_time"] += time_taken

    if not is_correct:
        performance[topic]["incorrect"] += 1
        performance[topic]["repeated_errors"] += 1

    save_performance(performance)

    return jsonify({
        "status": "correct" if is_correct else "incorrect"
    })

@app.route("/report")
def report():
    performance = load_performance()
    report = []

    for topic, d in performance.items():
        accuracy = (d["attempts"] - d["incorrect"]) / d["attempts"]
        avg_time = d["total_time"] / d["attempts"]

        weak = (
            accuracy < 0.6 or
            avg_time > TIME_THRESHOLD or
            d["repeated_errors"] >= 2
        )

        report.append({
            "topic": topic,
            "accuracy": round(accuracy * 100),
            "avg_time": round(avg_time, 2),
            "status": "WEAK" if weak else "STRONG"
        })

    return jsonify(report)

if __name__ == "__main__":
    app.run(debug=True)
