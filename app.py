from flask import Flask, request, render_template_string, jsonify
from collections import Counter
import re

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Log Analyzer</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 900px; margin: 40px auto; padding: 0 20px; background: #f4f4f4; }
        h1 { color: #333; }
        .card { background: white; padding: 20px; border-radius: 8px; margin: 20px 0; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
        .stats { display: flex; gap: 20px; flex-wrap: wrap; }
        .stat-box { padding: 15px 25px; border-radius: 8px; color: white; min-width: 120px; text-align: center; }
        .error   { background: #e74c3c; }
        .warning { background: #f39c12; }
        .info    { background: #27ae60; }
        .debug   { background: #2980b9; }
        .stat-box h2 { margin: 0; font-size: 2em; }
        .stat-box p  { margin: 5px 0 0; font-size: 0.9em; }
        table { width: 100%; border-collapse: collapse; }
        th, td { text-align: left; padding: 10px; border-bottom: 1px solid #ddd; }
        th { background: #f8f8f8; font-weight: bold; }
        tr:hover { background: #fafafa; }
        input[type=file] { margin: 10px 0; }
        button { background: #3498db; color: white; border: none; padding: 10px 20px; border-radius: 5px; cursor: pointer; font-size: 1em; }
        button:hover { background: #2980b9; }
        .badge { padding: 3px 8px; border-radius: 4px; color: white; font-size: 0.8em; font-weight: bold; }
        .tag-error   { background: #e74c3c; }
        .tag-warning { background: #f39c12; }
        .tag-info    { background: #27ae60; }
        .tag-debug   { background: #2980b9; }
        .tag-unknown { background: #95a5a6; }
    </style>
</head>
<body>
    <h1>📋 Log File Analyzer</h1>

    <div class="card">
        <h3>Upload a Log File</h3>
        <form method="POST" enctype="multipart/form-data">
            <input type="file" name="logfile" accept=".log,.txt" required><br>
            <button type="submit">Analyze</button>
        </form>
    </div>

    {% if stats %}
    <div class="card">
        <h3>Summary</h3>
        <p>Total Lines: <strong>{{ stats.total_lines }}</strong> &nbsp;|&nbsp; Log Entries Found: <strong>{{ stats.total_entries }}</strong></p>
        <div class="stats">
            <div class="stat-box error">
                <h2>{{ stats.counts.ERROR }}</h2>
                <p>ERRORS</p>
            </div>
            <div class="stat-box warning">
                <h2>{{ stats.counts.WARNING }}</h2>
                <p>WARNINGS</p>
            </div>
            <div class="stat-box info">
                <h2>{{ stats.counts.INFO }}</h2>
                <p>INFO</p>
            </div>
            <div class="stat-box debug">
                <h2>{{ stats.counts.DEBUG }}</h2>
                <p>DEBUG</p>
            </div>
        </div>
    </div>

    <div class="card">
        <h3>Top 10 Most Frequent Messages</h3>
        <table>
            <tr><th>#</th><th>Level</th><th>Message</th><th>Count</th></tr>
            {% for item in stats.top_messages %}
            <tr>
                <td>{{ loop.index }}</td>
                <td><span class="badge tag-{{ item.level | lower }}">{{ item.level }}</span></td>
                <td>{{ item.message }}</td>
                <td><strong>{{ item.count }}</strong></td>
            </tr>
            {% endfor %}
        </table>
    </div>

    <div class="card">
        <h3>All Error Lines</h3>
        {% if stats.error_lines %}
        <table>
            <tr><th>Line #</th><th>Log Entry</th></tr>
            {% for entry in stats.error_lines %}
            <tr>
                <td>{{ entry.line_no }}</td>
                <td style="font-family: monospace; font-size: 0.85em;">{{ entry.text }}</td>
            </tr>
            {% endfor %}
        </table>
        {% else %}
        <p>No ERROR lines found 🎉</p>
        {% endif %}
    </div>
    {% endif %}

</body>
</html>
"""

def parse_log(content):
    lines = content.splitlines()
    total_lines = len(lines)

    # Matches common log formats: [LEVEL], LEVEL:, or just the word
    log_pattern = re.compile(r'\b(ERROR|WARNING|WARN|INFO|DEBUG|CRITICAL)\b', re.IGNORECASE)

    counts = {"ERROR": 0, "WARNING": 0, "INFO": 0, "DEBUG": 0, "CRITICAL": 0}
    message_list = []
    error_lines = []
    total_entries = 0

    for i, line in enumerate(lines, start=1):
        match = log_pattern.search(line)
        if match:
            total_entries += 1
            level = match.group(1).upper()
            if level == "WARN":
                level = "WARNING"

            counts[level] = counts.get(level, 0) + 1

            # Extract message after the log level keyword
            msg = line[match.end():].strip(" :-|[]").strip()
            msg = msg[:120]  # truncate long lines
            if msg:
                message_list.append((level, msg))

            if level in ("ERROR", "CRITICAL"):
                error_lines.append({"line_no": i, "text": line.strip()[:150]})

    # Top 10 frequent messages
    msg_counter = Counter(message_list)
    top_messages = [
        {"level": lvl, "message": msg, "count": cnt}
        for (lvl, msg), cnt in msg_counter.most_common(10)
    ]

    return {
        "total_lines": total_lines,
        "total_entries": total_entries,
        "counts": counts,
        "top_messages": top_messages,
        "error_lines": error_lines[:50]  # limit to 50
    }


@app.route("/", methods=["GET", "POST"])
def index():
    stats = None
    if request.method == "POST":
        f = request.files.get("logfile")
        if f:
            content = f.read().decode("utf-8", errors="ignore")
            stats = parse_log(content)
    return render_template_string(HTML, stats=stats)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
