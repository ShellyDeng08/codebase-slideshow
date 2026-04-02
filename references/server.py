#!/usr/bin/env python3
"""Minimal HTTP server for learn-codebase skill. No external dependencies."""

import argparse
import json
import os
import signal
import sys
from http.server import HTTPServer, SimpleHTTPRequestHandler
from functools import partial


class QuietHandler(SimpleHTTPRequestHandler):
    """Serves static files and accepts quiz report POSTs."""

    def log_message(self, format, *args):
        pass  # Suppress request logging

    def do_OPTIONS(self):
        self.send_response(200)
        self._cors_headers()
        self.end_headers()

    def do_POST(self):
        if self.path == "/api/report":
            length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(length)
            try:
                data = json.loads(body)
            except json.JSONDecodeError:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(b'{"error":"invalid json"}')
                return

            chapter = data.get("chapter", "unknown")
            reports_dir = os.path.join(self.directory, "reports")
            os.makedirs(reports_dir, exist_ok=True)
            report_path = os.path.join(reports_dir, f"chapter-{chapter:0>2}.json")
            with open(report_path, "w") as f:
                json.dump(data, f, indent=2)

            self.send_response(200)
            self._cors_headers()
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(b'{"status":"ok"}')
        else:
            self.send_response(404)
            self.end_headers()

    def _cors_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, default=0, help="Port (0 = OS-assigned)")
    parser.add_argument("--dir", required=True, help="Directory to serve")
    parser.add_argument("--chapter", type=str, default="", help="Chapter number (informational)")
    args = parser.parse_args()

    serve_dir = os.path.abspath(args.dir)
    os.makedirs(serve_dir, exist_ok=True)

    handler = partial(QuietHandler, directory=serve_dir)
    server = HTTPServer(("127.0.0.1", args.port), handler)
    port = server.server_address[1]

    # Write PID file
    pid_path = os.path.join(serve_dir, ".server.pid")
    with open(pid_path, "w") as f:
        f.write(str(os.getpid()))

    def shutdown(signum, frame):
        server.shutdown()
        try:
            os.remove(pid_path)
        except OSError:
            pass
        sys.exit(0)

    signal.signal(signal.SIGTERM, shutdown)
    signal.signal(signal.SIGINT, shutdown)

    # Print port for Claude to capture
    print(f"PORT:{port}", flush=True)
    server.serve_forever()


if __name__ == "__main__":
    main()
