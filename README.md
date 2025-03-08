# RFace Service

## Introduction

RFace is a service that provides facial recognition capabilities. It is built with deepface framework and mainly aim for edge devices (NanoPi R5C)

## Installation

Before installing the service, you need to have python3 installed on your device, and the recommended version is 3.12 and above. You can install python3 by running the following command.:

```bash
sudo apt-get install python3>=3.12
```

Installing dependencies:
```bash
pip install -r requirements.txt
```

The installation process on NanoPi may take a lot of time, so please be patient.

## Test
To test the service, please navigate to the test folder and run the following command:
```bash
python test_rface.py
```

## Development guide
The service has 3 main components:
- Face recognition
- Video capture
- Result publisher (Event publisher)
And follow up are database and configuration.

For more information, please refer to the development note in the assets folder or click [here](/assets/developement_note)

### Face recognition
The face recognition component is built with deepface framework. However was modified to fit the project requirements (mainly converting input and output to numpy array).

When face is registered, the service will store the face embedding in the database.
The schema of the database is as follows:
```sql
  CREATE TABLE IF NOT EXISTS faces(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL,
    embedding BLOB NOT NULL
  );
```
In this case, the name should be unique, and match the key (e.g, id, ...) of the project that uses the service. For example, the name can be the student ID, or the employee ID according to the project requirements.