from flask import Flask, render_template
from markupsafe import Markup
import os
import re

app = Flask(__name__)

# ==== CONFIG =====
SERVER_IP = "chillipepper.thddns.net:2000"

# ==== แผนที่รหัสสี Minecraft ====
mc_color_codes = {
    '0': '#000000', '1': '#0000AA', '2': '#00AA00', '3': '#00AAAA',
    '4': '#AA0000', '5': '#AA00AA', '6': '#FFAA00', '7': '#AAAAAA',
    '8': '#555555', '9': '#5555FF', 'a': '#55FF55', 'b': '#55FFFF',
    'c': '#FF5555', 'd': '#FF55FF', 'e': '#FFFF55', 'f': '#FFFFFF',
    'r': '#f0f0f0'
}

def format_motd(text):
    result = ''
    color = '#f0f0f0'
    for part in re.split(r'(§[0-9a-fr])', text):
        if part.startswith('§') and len(part) == 2:
            code = part[1].lower()
            color = mc_color_codes.get(code, '#f0f0f0')
        else:
            result += f'<span style="color:{color}">{part}</span>'
    return Markup(result.replace('\n', '<br>'))

@app.route("/")
def index():
    status_lines = []
    is_online = True
    note = ""

    if os.path.exists("data/status.md"):
        with open("data/status.md", "r", encoding="utf-8") as f:
            status_lines = f.readlines()
            if any("Failed" in line for line in status_lines):
                is_online = False

    if os.path.exists("data/custom_note.txt"):
        with open("data/custom_note.txt", "r", encoding="utf-8") as f:
            note = f.read()

    return render_template("index.html", lines=status_lines, is_online=is_online, note=note, format_motd=format_motd, server_ip=SERVER_IP)

if __name__ == "__main__":
    app.run(debug=True)
