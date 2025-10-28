### Estimate training time based on FTP of the rider

#### To execute this code you will need:

##### linux/macOS:
- python3 -m venv venv
- source venv/bin/activate

##### Windows (powershell):
- python -m venv venv
- .\venv\Scripts\Activate.ps1

##### install dependencies:
- pip install -r requirements.txt

##### Running the application
- uvicorn main:app --reload

##### The API will be available at:
- localhost:8000
- localhost:8000/docs (swagger UI)