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

## Test
To test the service, please navigate to the test folder and run the following command:
```bash
python test_rface.py
```