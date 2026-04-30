# DVWA SQL Injection Tester

A small Python script that automates testing of common SQL injection
payloads against a locally hosted DVWA (Damn Vulnerable Web Application)
instance. Built as part of a personal learning project on web application
security.

## What it does

- Logs into DVWA (handling the dynamic CSRF token)
- Sets the security level to LOW
- Iterates through a list of SQL injection payloads
- Reports which payloads triggered SQL errors or extracted data

## Payloads covered

- Basic quote test (vulnerability confirmation)
- Always-true bypass (`1' OR '1'='1`)
- UNION-based credential extraction
- Database version and name disclosure
- `information_schema` enumeration

## Requirements

- Python 3.7 or higher
- `requests` library (`pip install requests`)
- A locally running DVWA instance on XAMPP

## Setup

1. Install XAMPP and start Apache + MySQL.
2. Install DVWA into `htdocs/dvwa/` and run `setup.php` to create the database.
3. Log into DVWA at `http://localhost/dvwa/login.php` with `admin` / `password`.
4. Set the security level to LOW from the DVWA Security page.

## Usage

```bash
pip install requests
python sqli_tester.py
```

## Disclaimer

This script is strictly for educational use against your own local DVWA
installation. Running SQL injection payloads against systems you do not own
or have explicit written permission to test is illegal in most jurisdictions.

## What I learned

- How SQL injection works at the query level (string concatenation is the
  root cause, not just "bad input")
- Why prepared statements eliminate the entire vulnerability class, while
  escaping and filtering are partial fixes
- How to handle CSRF tokens when automating browser-based logins
- How `UNION` injections require column-count matching, and how to enumerate
  it with `ORDER BY`

## License

MIT
