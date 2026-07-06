<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>PHQ-9 Mental Health Assessment</title>
    <style>
        :root {
            --primary: #2563eb;
            --bg: #f8fafc;
            --card: #ffffff;
            --text: #1e293b;
            --border: #e2e8f0;
        }
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            background-color: var(--bg);
            color: var(--text);
            line-height: 1.5;
            padding: 2rem 1rem;
            margin: 0;
        }
        .container {
            max-width: 650px;
            margin: 0 auto;
            background: var(--card);
            padding: 2rem;
            border-radius: 12px;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        }
        h1 { margin-top: 0; font-size: 1.75rem; color: #0f172a; }
        p.instructions { color: #64748b; margin-bottom: 2rem; }
        .question-block {
            margin-bottom: 1.75rem;
            padding-bottom: 1.5rem;
            border-bottom: 1px solid var(--border);
        }
        .question-text { font-weight: 600; margin-bottom: 0.75rem; }
        .options {
            display: grid;
            grid-template-columns: 1fr;
            gap: 0.5rem;
        }
        @media(min-width: 480px) {
            .options { grid-template-columns: repeat(4, 1fr); }
        }
        label {
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 0.75rem;
            background: #f1f5f9;
            border: 1px solid var(--border);
            border-radius: 6px;
            cursor: pointer;
            font-size: 0.9rem;
            text-align: center;
            transition: all 0.2s;
        }
        label:hover { background: #e2e8f0; }
        input[type="radio"] { display: none; }
        input[type="radio"]:checked + span { font-weight: bold; }
        input[type="radio"]:checked ~ label {
            background: var(--primary);
            color: white;
            border-color: var(--primary);
        }
        button {
            width: 100%;
            background: var(--primary);
            color: white;
            border: none;
            padding: 1rem;
            font-size: 1rem;
            font-weight: 600;
            border-radius: 6px;
            cursor: pointer;
            margin-top: 1rem;
        }
        button:hover { background: #1d4ed8; }
        #result {
            display: none;
            margin-top: 2rem;
            padding: 1.5rem;
            border-radius: 8px;
            font-weight: 500;
        }
        .severity-minimal { background: #dcfce7; color: #166534; }
        .severity-mild { background: #fef9c3; color: #854d0e; }
        .severity-moderate { background: #ffedd5; color: #9a3412; }
        .severity-severe { background: #fee2e2; color: #991b1b; }
        .alert-box {
            margin-top: 1rem;
            background: #fff1f2;
            border: 1px solid #fecdd3;
            color: #9f1239;
            padding: 1rem;
            border-radius: 6px;
            display: none;
            font-weight: bold;
        }
    </style>
</head>
<body>

<div class="container">
    <h1>Mental Health Assessment (PHQ-9)</h1>
    <p class="instructions">Over the last 2 weeks, how often have you been bothered by any of the following problems?</p>
    
    <form id="quizForm">
        <!-- Questions will be auto-generated here by JavaScript -->
        <div id="questionsContainer"></div>
        
        <button type="button" onclick="calculateScore()">Submit Assessment</button>
    </form>

    <div id="result"></div>
    <div id="alertBox" class="alert-box">
        ⚠️ Notice: Your responses indicate thoughts of self-harm. Please reach out to a professional or a crisis helpline immediately.
    </div>
</div>

<script>
    const questions = [
        "Little interest or pleasure in doing things",
        "Feeling down, depressed, or hopeless",
        "Trouble falling or staying asleep, or sleeping too much",
        "Feeling tired or having little energy",
        "Poor appetite or overeating",
        "Feeling bad about yourself — or that you are a failure or have let yourself or your family down",
        "Trouble concentrating on things, such as reading the newspaper or watching television",
        "Moving or speaking so slowly that other people could have noticed? Or the opposite — being so fidgety or restless that you have been moving around a lot more than usual",
        "Thoughts that you would be better off dead or of hurting yourself in some way"
    ];

    const options = ["Not at all", "Several days", "More than half the days", "Nearly every day"];
    const container = document.getElementById('questionsContainer');

    // Dynamically build the questionnaire form
    questions.forEach((q, qIdx) => {
        const qBlock = document.createElement('div');
        qBlock.className = 'question-block';
        
        const qText = document.createElement('div');
        qText.className = 'question-text';
        qText.innerText = `${qIdx + 1}. ${q}`;
        qBlock.appendChild(qText);

        const optionsDiv = document.createElement('div');
        optionsDiv.className = 'options';

        options.forEach((opt, oIdx) => {
            const id = `q${qIdx}_o${oIdx}`;
            
            const input = document.createElement('input');
            input.type = 'radio';
            input.name = `q${qIdx}`;
            input.value = oIdx;
            input.id = id;
            input.required = true;

            const label = document.createElement('label');
            label.htmlFor = id;
            label.innerText = opt;

            optionsDiv.appendChild(input);
            optionsDiv.appendChild(label);
        });

        qBlock.appendChild(optionsDiv);
        container.appendChild(qBlock);
    });

    function calculateScore() {
        const form = document.getElementById('quizForm');
        if (!form.checkValidity()) {
            alert("Please answer all 9 questions before submitting.");
            return;
        }

        let totalScore = 0;
        let selfHarmTriggered = false;

        questions.forEach((_, qIdx) => {
            const selected = document.querySelector(`input[name="q${qIdx}"]:checked`);
            const value = parseInt(selected.value);
            totalScore += value;

            // Question index 8 is the self-harm question
            if (qIdx === 8 && value > 0) {
                selfHarmTriggered = true;
            }
        });

        displayResult(totalScore, selfHarmTriggered);
    }

    function displayResult(score, selfHarm) {
        const resultDiv = document.getElementById('result');
        const alertBox = document.getElementById('alertBox');
        
        resultDiv.style.display = 'block';
        alertBox.style.display = selfHarm ? 'block' : 'none';
        
        let severity = "";
        let className = "";

        if (score <= 4) {
            severity = "Minimal Depression";
            className = "severity-minimal";
        } else if (score <= 9) {
            severity = "Mild Depression";
            className = "severity-mild";
        } else if (score <= 14) {
            severity = "Moderate Depression";
            className = "severity-moderate";
        } else if (score <= 19) {
            severity = "Moderately Severe Depression";
            className = "severity-moderate";
        } else {
            severity = "Severe Depression";
            className = "severity-severe";
        }

        resultDiv.className = className;
        resultDiv.innerHTML = `<strong>Your Score: ${score} / 27</strong><br>Classification: ${severity}<br><br><small>Disclaimer: This screening tool is for educational purposes and does not replace a professional clinical diagnosis.</small>`;
        
        // Optional: Smooth scroll to results
        resultDiv.scrollIntoView({ behavior: 'smooth' });
    }
</script>

</body>
</html>
