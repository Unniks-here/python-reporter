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
   Create `config.json` from `config.json.example` and configure your queries,
   recipients and schedule.

3. Manage configuration using the CLI:

```bash
python manage.py add-query --name sales_by_region \
    --sql "SELECT region, SUM(amount) AS total_sales FROM sales WHERE stakeholder_email = :email GROUP BY region" \
    --recipients user1@example.com user2@example.com
python manage.py set-schedule "0 9 * * *"
```

4. Run the scheduler:

```bash
python main.py
```

The scheduler is configured to run daily at 9am by default.
