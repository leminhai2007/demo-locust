# demo-locust

for demo

## Create virtual environment

MacOS
```
python3 -m venv .venv
source .venv/bin/activate
```
Windows
```
python -m venv .venv
.venv\Scripts\activate.bat
.venv\Scripts\Activate.ps1

```

**Note:** deactivate virtual environment
```
deactivate
```

## Install required packages
```
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## Running with WebUI
```
locust
```

## Running without WebUI
```
locust --headless --only-summary
```
