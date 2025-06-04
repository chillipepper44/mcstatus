import time
import subprocess
from mcstatus import JavaServer
from datetime import datetime

# === CONFIG ===
SERVER_ADDRESS = "chillipepper.thddns.net:2000"
SLEEP_SECONDS = 60  # ทุก 5 นาที
OUTPUT_FILE = "data/status.md"

def update_status():
    while True:
        try:
            server = JavaServer.lookup(SERVER_ADDRESS)
            status = server.status()
            players = status.players.online
            motd = status.description
            latency = status.latency
            now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
                f.write(f"# Server Status\n\n")
                f.write(f"🖥 Server: {SERVER_ADDRESS}\n")
                f.write(f"👥 Players Online: {players}\n")
                f.write(f"📶 Latency: {latency} ms\n")
                f.write(f"MOTD: {motd}\n")

                # 🧍 Player list (ถ้ามี)
                if status.players.sample:
                    f.write("👤 Player List:\n")
                    for player in status.players.sample:
                        f.write(f"- {player.name}\n")

                f.write(f"⏰ Last Checked: {now}\n")

        except Exception as e:
            with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
                f.write(f"# Server Status\n\n")
                f.write(f"❌ Failed to fetch status: {e}\n")

        # 🔁 Push to GitHub
        try:
            subprocess.run(["git", "add", OUTPUT_FILE])
            subprocess.run(["git", "commit", "-m", f"Auto update at {now}"], stderr=subprocess.DEVNULL)
            subprocess.run(["git", "push"])
        except Exception as git_error:
            print("⚠️ Git push failed:", git_error)

        print(f"[{now}] ✅ Server status updated and pushed.")
        time.sleep(SLEEP_SECONDS)

if __name__ == "__main__":
    update_status()
