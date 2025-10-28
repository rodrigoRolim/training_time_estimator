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

### How to test in the swagger
1. Generate the Route Segments.
Start by calling the endpoint:
POST /workout/estimate-training-time
This endpoint processes your uploaded route file and returns an estimated time and segmented route.
Example response:
```json
{
  "estimated_time": {
    "hours": 0,
    "minutes": 5,
    "seconds": 49
  },
  "total_distance": 2.26805,
  "segments": [
    {
      "index": 1,
      "distance": 128.53,
      "grade": -1.5560489230329917,
      "heading": 74.48418968420884,
      "zone": "Z2",
      "power_w": 162.5,
      "time_min": 0.2171245835528138
    },
    {
      "index": 2,
      "distance": 328.432,
      "grade": 2.4358151082792974,
      "heading": 78.70797878184408,
      "zone": "Z3",
      "power_w": 206.25,
      "time_min": 0.9632074063912552
    },
  ]
}
```
2. Generate the Workout File
Next, use the endpoint:
POST /workout/create-workout
Copy the entire segments array from the previous response and paste it into the request body here.
Example request body:
```json
{
  "ftp": 250,
  "segments": [
    {
      "index": 1,
      "distance": 128.53,
      "grade": -1.5560489230329917,
      "heading": 74.48418968420884,
      "zone": "Z2",
      "power_w": 162.5,
      "time_min": 0.2171245835528138
    },
    {
      "index": 2,
      "distance": 328.432,
      "grade": 2.4358151082792974,
      "heading": 78.70797878184408,
      "zone": "Z3",
      "power_w": 206.25,
      "time_min": 0.9632074063912552
    },
  ]
}
```
After executing this request, a downloadable workout file will be generated.

3.Estimate FTP Required to Match a Target Time
Finally, call the endpoint:
POST /workout/estimate-training-ftp
Here, you need to paste the same segments from step 1 and fill in the remaining fields as shown below:
```json
{
  "segments": [
    {
      "index": 1,
      "distance": 128.53,
      "grade": -1.5560489230329917,
      "heading": 74.48418968420884,
      "zone": "Z2",
      "power_w": 162.5,
      "time_min": 0.2171245835528138
    },
    {
      "index": 2,
      "distance": 328.432,
      "grade": 2.4358151082792974,
      "heading": 78.70797878184408,
      "zone": "Z3",
      "power_w": 206.25,
      "time_min": 0.9632074063912552
    },
  ],
  "wind_dir": 30, // the same value on the firts request
  "wind_speed": 10, // the same value on the firts request
  "rider_mass": 80, // the same value on the firts request
  "bike_mass": 10, // the same value on the firts request
  "target_time_sec": 300 // this is the target time
}
```