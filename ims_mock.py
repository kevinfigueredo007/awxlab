from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import boto3
from datetime import datetime, timedelta

PROFILE = "kevin"
ROLE_NAME = "my-role"

session = boto3.Session(profile_name=PROFILE)
credentials = session.get_credentials().get_frozen_credentials()

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/latest/meta-data/iam/security-credentials/":
            self.send_response(200)
            self.end_headers()
            self.wfile.write(ROLE_NAME.encode())

        elif self.path == f"/latest/meta-data/iam/security-credentials/{ROLE_NAME}":
            self.send_response(200)
            self.end_headers()

            creds = {
                "Code": "Success",
                "Type": "AWS-HMAC",
                "AccessKeyId": credentials.access_key,
                "SecretAccessKey": credentials.secret_key,
                "Token": credentials.token or "",
                "Expiration": (datetime.utcnow() + timedelta(hours=1)).isoformat() + "Z"
            }

            self.wfile.write(json.dumps(creds).encode())

server = HTTPServer(("0.0.0.0", 1338), Handler)
server.serve_forever()
