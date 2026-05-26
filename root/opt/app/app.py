import html
import datetime
import os
import codecs
from flask import Flask, jsonify, request, redirect, render_template_string

print()
app = Flask(__name__)


APP_TITLE = "Request Catcher"
APP_SUBTITLE = "CTF Webhook & Payload Capture Console"


def get_file():
    log_dir = os.environ.get("LOG_DIR", "/tmp/request-catcher")
    os.makedirs(log_dir, exist_ok=True)
    return os.path.join(log_dir, datetime.datetime.today().strftime("%Y-%m-%d") + ".log")


def log_request(method):
    file_url = get_file()
    with codecs.open(file_url, "a", "utf-8") as the_file:
        the_file.write("URL: " + str(request.url) + "\n")
        the_file.write("METHOD: " + method + "\n")
        the_file.write("IP: " + str(request.remote_addr) + "\n")
        the_file.write("Time: " + datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S") + "\n")
        the_file.write("Headers:\n" + str(request.headers).strip() + "\n")

        if method == "POST":
            body = request.get_data(as_text=True)
            the_file.write("Body:\n" + body + "\n")
        else:
            query = request.query_string.decode("utf-8", errors="replace")
            the_file.write("QueryString:\n" + query + "\n")

        the_file.write("===================================================\n")


@app.after_request
def add_cors_headers(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    return response


def page_template(content, active="home"):
    return render_template_string("""
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <link rel="icon" href="data:,">
  <title>{{ title }}</title>
  <style>
    :root {
      --bg: #05070d;
      --panel: rgba(12, 18, 32, 0.88);
      --panel-2: rgba(8, 12, 24, 0.96);
      --text: #d7f7ff;
      --muted: #7c96a7;
      --green: #2fffa4;
      --cyan: #25d9ff;
      --pink: #ff3df2;
      --red: #ff4d6d;
      --border: rgba(47, 255, 164, 0.28);
      --shadow: 0 0 40px rgba(37, 217, 255, 0.12);
    }

    * { box-sizing: border-box; }

    body {
      margin: 0;
      min-height: 100vh;
      color: var(--text);
      font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", monospace;
      background:
        radial-gradient(circle at 20% 10%, rgba(37, 217, 255, 0.16), transparent 28%),
        radial-gradient(circle at 85% 15%, rgba(255, 61, 242, 0.11), transparent 30%),
        linear-gradient(135deg, #05070d 0%, #070b14 52%, #020309 100%);
      overflow-x: hidden;
    }

    body::before {
      content: "";
      position: fixed;
      inset: 0;
      pointer-events: none;
      background-image:
        linear-gradient(rgba(47,255,164,.055) 1px, transparent 1px),
        linear-gradient(90deg, rgba(47,255,164,.055) 1px, transparent 1px);
      background-size: 34px 34px;
      mask-image: linear-gradient(to bottom, rgba(0,0,0,.8), rgba(0,0,0,.12));
    }

    body::after {
      content: "";
      position: fixed;
      inset: 0;
      pointer-events: none;
      background: repeating-linear-gradient(
        to bottom,
        rgba(255,255,255,.025) 0,
        rgba(255,255,255,.025) 1px,
        transparent 1px,
        transparent 4px
      );
      opacity: .4;
      mix-blend-mode: overlay;
    }

    a { color: inherit; text-decoration: none; }

    .wrap {
      width: min(1120px, calc(100% - 32px));
      margin: 0 auto;
      padding: 36px 0 48px;
      position: relative;
      z-index: 1;
    }

    .hero {
      display: grid;
      gap: 18px;
      margin-bottom: 28px;
    }

    .badge {
      display: inline-flex;
      align-items: center;
      gap: 10px;
      width: fit-content;
      color: var(--green);
      border: 1px solid var(--border);
      background: rgba(47,255,164,.06);
      border-radius: 999px;
      padding: 8px 13px;
      box-shadow: 0 0 24px rgba(47,255,164,.12);
      font-size: 13px;
    }

    .pulse {
      width: 9px;
      height: 9px;
      border-radius: 99px;
      background: var(--green);
      box-shadow: 0 0 16px var(--green);
      animation: pulse 1.6s infinite;
    }

    @keyframes pulse {
      0%, 100% { opacity: .4; transform: scale(.88); }
      50% { opacity: 1; transform: scale(1.15); }
    }

    h1 {
      margin: 0;
      font-size: clamp(42px, 8vw, 92px);
      letter-spacing: -5px;
      line-height: .88;
      text-transform: uppercase;
      font-weight: 900;
      position: relative;
    }

    .title-wrap {
      position: relative;
      display: inline-block;
      padding: 10px 18px 16px;
      border-radius: 24px;
      background:
        linear-gradient(135deg, rgba(37,217,255,.08), rgba(255,61,242,.08));
      border: 1px solid rgba(37,217,255,.18);
      box-shadow:
        0 0 40px rgba(37,217,255,.15),
        inset 0 0 18px rgba(255,255,255,.04);
      overflow: hidden;
    }

    .title-wrap::before {
      content: "";
      position: absolute;
      inset: 0;
      background: linear-gradient(90deg,
        transparent,
        rgba(255,255,255,.08),
        transparent);
      transform: translateX(-100%);
      animation: sweep 6s linear infinite;
    }

    @keyframes sweep {
      to {
        transform: translateX(100%);
      }
    }

    .title-main {
      background: linear-gradient(180deg, #ffffff 0%, #8cecff 40%, #2fffa4 100%);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      background-clip: text;
      position: relative;
      z-index: 1;
      text-shadow:
        0 0 10px rgba(37,217,255,.25),
        0 0 30px rgba(47,255,164,.2);
    }

    .title-shadow {
      position: absolute;
      inset: 0;
      color: rgba(37,217,255,.12);
      filter: blur(12px);
      transform: translateY(8px) scale(1.02);
      pointer-events: none;
    }

    .glitch {
      position: relative;
      display: inline-block;
    }

    .glitch::before,
    .glitch::after {
      content: attr(data-text);
      position: absolute;
      left: 0;
      top: 0;
      opacity: .55;
    }

    .glitch::before { color: var(--cyan); transform: translate(2px, 0); clip-path: inset(0 0 58% 0); }
    .glitch::after { color: var(--pink); transform: translate(-2px, 0); clip-path: inset(46% 0 0 0); }

    .subtitle {
      margin: 0;
      color: var(--muted);
      max-width: 760px;
      line-height: 1.65;
      font-size: 16px;
    }

    .nav {
      display: flex;
      flex-wrap: wrap;
      gap: 12px;
      margin: 24px 0;
    }

    .nav a, .button {
      display: inline-flex;
      align-items: center;
      gap: 9px;
      border: 1px solid rgba(37,217,255,.28);
      background: rgba(37,217,255,.065);
      color: var(--text);
      border-radius: 14px;
      padding: 12px 15px;
      box-shadow: var(--shadow);
      transition: transform .15s ease, border-color .15s ease, background .15s ease;
    }

    .nav a:hover, .button:hover {
      transform: translateY(-2px);
      border-color: rgba(47,255,164,.65);
      background: rgba(47,255,164,.09);
    }

    .nav a.active {
      border-color: rgba(47,255,164,.8);
      color: var(--green);
      background: rgba(47,255,164,.11);
    }

    .grid {
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 16px;
      margin: 22px 0;
    }

    .card, .terminal {
      border: 1px solid var(--border);
      background: linear-gradient(180deg, var(--panel), var(--panel-2));
      border-radius: 24px;
      box-shadow: var(--shadow), inset 0 1px 0 rgba(255,255,255,.06);
      overflow: hidden;
    }

    .card {
      padding: 20px;
      min-height: 156px;
    }

    .card h3 {
      margin: 0 0 12px;
      color: var(--green);
      font-size: 16px;
    }

    .card p, .card li {
      color: var(--muted);
      line-height: 1.55;
      font-size: 14px;
    }

    .card ul { padding-left: 18px; margin: 0; }

    .terminal-head {
      display: flex;
      align-items: center;
      gap: 8px;
      padding: 14px 18px;
      background: rgba(255,255,255,.045);
      border-bottom: 1px solid rgba(47,255,164,.18);
      color: var(--muted);
      font-size: 13px;
    }

    .dot { width: 11px; height: 11px; border-radius: 99px; background: var(--red); box-shadow: 0 0 12px rgba(255,77,109,.5); }
    .dot:nth-child(2) { background: #ffd166; box-shadow: 0 0 12px rgba(255,209,102,.5); }
    .dot:nth-child(3) { background: var(--green); box-shadow: 0 0 12px rgba(47,255,164,.5); }

    .terminal-body {
      padding: 20px;
      line-height: 1.7;
      color: #bceeff;
      white-space: pre-wrap;
      word-break: break-word;
    }

    .prompt { color: var(--green); }
    .cyan { color: var(--cyan); }
    .pink { color: var(--pink); }
    .muted { color: var(--muted); }

    code {
      color: var(--green);
      background: rgba(47,255,164,.08);
      border: 1px solid rgba(47,255,164,.18);
      padding: 2px 7px;
      border-radius: 8px;
    }

    .status {
      display: inline-flex;
      align-items: center;
      gap: 9px;
      margin-top: 16px;
      color: var(--green);
      font-size: 14px;
    }

    .log-empty {
      color: var(--muted);
      padding: 20px;
    }

    .footer {
      margin-top: 28px;
      color: var(--muted);
      font-size: 13px;
      text-align: center;
    }

    @media (max-width: 860px) {
      .grid { grid-template-columns: 1fr; }
      h1 { letter-spacing: -2px; }
    }
  </style>
</head>
<body>
  <main class="wrap">
    <section class="hero">
      <div class="badge"><span class="pulse"></span> listener online · {{ date }}</div>
      <div class="title-wrap">
        <h1>
          <span class="title-shadow">{{ title }}</span>
          <span class="title-main glitch" data-text="{{ title }}">{{ title }}</span>
        </h1>
      </div>
      <p class="subtitle">{{ subtitle }}</p>
    </section>

    <nav class="nav">
      <a class="{{ 'active' if active == 'home' else '' }}" href="/">⌂ Usage</a>
      <a class="{{ 'active' if active == 'debug' else '' }}" href="/debug">▣ Captured Requests</a>
      <a class="{{ 'active' if active == 'clear' else '' }}" href="/clear">⌫ Clear Log</a>
    </nav>

    {{ content|safe }}

    <div class="footer">capture everything · trust nothing · sanitize output</div>
  </main>
</body>
</html>
""", title=APP_TITLE, subtitle=APP_SUBTITLE, content=content, active=active, date=datetime.datetime.today().strftime("%Y-%m-%d"))


@app.route('/', defaults={'any': ''}, methods=['POST'])
@app.route('/<path:any>', methods=['POST'])
def catchItPOST(any):
    log_request("POST")
    return jsonify(True)


@app.route('/', methods=['GET'])
def print_usage():
    if request.args:
        log_request("GET")
        return jsonify(True)

    content = """
<section class="grid">
  <article class="card">
    <h3>01 · Usage</h3>
    <p>Send GET requests with query strings or POST requests to any path. Captured data is written to today&apos;s log file.</p>
  </article>
  <article class="card">
    <h3>02 · Endpoints</h3>
    <ul>
      <li><code>/</code> usage screen</li>
      <li><code>/debug</code> show captured requests</li>
      <li><code>/clear</code> clear captured requests</li>
    </ul>
  </article>
  <article class="card">
    <h3>03 · Not Captured</h3>
    <ul>
      <li><code>/</code> without query string</li>
      <li><code>/clear</code></li>
      <li><code>/debug</code></li>
      <li><code>/favicon.ico</code></li>
    </ul>
  </article>
</section>

<section class="terminal">
  <div class="terminal-head"><span class="dot"></span><span class="dot"></span><span class="dot"></span><span>operator@request-catcher:~</span></div>
  <div class="terminal-body"><span class="prompt">$</span> curl -k "http://127.0.0.1/test?flag=HL{demo}"\n<span class="cyan">true</span>\n\n<span class="prompt">$</span> curl -k -X POST "http://127.0.0.1/webhook" -d "payload=hello"\n<span class="cyan">true</span>\n\n<span class="muted">Open</span> <span class="pink">/debug</span> <span class="muted">to inspect the captured headers, body, IP address, and timestamp.</span></div>
</section>
"""
    return page_template(content, active="home")


@app.route('/favicon.ico', methods=['GET'])
def empty():
    return ""


@app.route('/clear', methods=['GET'])
def clear():
    file_url = get_file()
    try:
        if os.path.isfile(file_url):
            with codecs.open(file_url, 'r+', "utf-8") as the_file:
                the_file.truncate(0)
    finally:
        timestamp = datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S")
        content = f"""
<section class="terminal">
  <div class="terminal-head"><span class="dot"></span><span class="dot"></span><span class="dot"></span><span>clear-log</span></div>
  <div class="terminal-body"><span class="prompt">$</span> truncate {html.escape(file_url)}\n<span class="cyan">Log cleared:</span> {html.escape(timestamp)}\n\n<a class="button" href="/debug">▣ View empty capture buffer</a></div>
</section>
"""
        return page_template(content, active="clear")


@app.route('/debug', methods=['GET'])
def file_downloads():
    try:
        file_url = get_file()
        text = ""
        if os.path.isfile(file_url):
            with codecs.open(file_url, 'r', "utf-8") as the_file:
                text = html.escape(the_file.read())

                # Remove excessive empty lines for cleaner terminal output
                lines = [line.rstrip() for line in text.splitlines()]
                cleaned_lines = []
                previous_empty = False

                for line in lines:
                    is_empty = line.strip() == ""
                    if is_empty and previous_empty:
                        continue
                    cleaned_lines.append(line)
                    previous_empty = is_empty

                text = "\n".join(cleaned_lines)

        if text.strip():
            # Keep line breaks readable while preserving escaped content.
            safe_log = text.replace('\n', '<br>')
            content = f"""
<section class="terminal">
  <div class="terminal-head"><span class="dot"></span><span class="dot"></span><span class="dot"></span><span>{html.escape(file_url)}</span></div>
  <div class="terminal-body">{safe_log}</div>
</section>
"""
        else:
            content = f"""
<section class="terminal">
  <div class="terminal-head"><span class="dot"></span><span class="dot"></span><span class="dot"></span><span>{html.escape(file_url)}</span></div>
  <div class="log-empty">No captured requests yet. Fire a GET with a query string or any POST request.</div>
</section>
"""
        return page_template(content, active="debug")
    except Exception:
        return redirect('/')


@app.route('/<path:any>', methods=['GET'])
def catchItGET(any):
    log_request("GET")
    return jsonify(True)


if __name__ == "__main__":
    # Keep port 80 if you run as root or with the required capability.
    # For normal local testing, use port 5000 instead.
    app.run(host="0.0.0.0", port=80, debug=True)


