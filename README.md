# Patients Appointments Bot

---

## Description

This simple bot can help doctors to manage their patients appointments.

Doctors can add patient appointment to the system and it will be added to the system.
Later doctors can overview all appointments for current day and current week.

## How to Install and Run

### Prerequisites

- Docker installed on your machine OR
- Python 3.11 or higher installed on your machine.

### Steps to Install

#### 1. Using docker

1. Clone the repository:
    ```bash
    git clone https://github.com/usbtypec1/patient-appointments-bot
    cd patient-appointments-bot
    ```

2. Create `TELEGRAM_BOT_TOKEN` env variable:

```shell
export TELEGRAM_BOT_TOKEN=your_telegram_bot_token
```

3. Run the app:
    ```bash
    docker-compose up
    ```

#### 2. Using Python directly

1. Clone the repository:
    ```bash
    git clone https://github.com/usbtypec1/patient-appointments-bot
    cd patient-appointments-bot
    ```

2. Create and activate a virtual environment (recommended):
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4. Create `TELEGRAM_BOT_TOKEN` env variable:
    ```shell
    export TELEGRAM_BOT_TOKEN=your_telegram_bot_token
    ```

5. Run the app:
    ```bash
    python main.py
    ```

## 4. How to Run Tests

To run the tests, first ensure all test dependencies are installed. You can install them with:

```bash
pip install -r requirements.txt
```

Run the test suite using:

```bash
pytest
```

This will automatically discover and run all test cases under the `tests/` directory.
