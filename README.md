# Python Reporter

This project demonstrates a lightweight reporting tool that connects to a PostgreSQL database, aggregates data per stakeholder, generates Excel reports and emails them on a schedule.

## Setup

1. Create a Python virtual environment and install dependencies:

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

2. Copy `.env.example` to `.env` and fill in your database and SMTP credentials.

3. Run the scheduler:

```bash
python main.py
```

The scheduler is configured to run daily at 9am by default.
