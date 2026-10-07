# GeoMeasure

GeoMeasure is a FastAPI-based backend API for processing geospatial files and calculating measurements from their geometries.

The API accepts KML files and ZIP archives containing Shapefiles, extracts their geospatial features, handles coordinate reference systems (CRS), and calculates measurements such as polygon area and line length.

---

## Features

- Upload `.kml` files
- Upload `.zip` files containing a Shapefile
- Extract geospatial features and their properties
- Detect geometry types
- Detect and handle Coordinate Reference Systems (CRS)
- Automatically transform geographic CRS to a suitable projected CRS
- Calculate:
  - Polygon → Area
  - LineString → Length
  - Point → No measurement
- Store processed files with unique IDs
- Retrieve file information using its ID
- Retrieve measurements for a processed file
- Interactive API documentation using Swagger UI
- Basic validation and error handling

---

## Tech Stack

- **Python 3.12+**
- **FastAPI** — REST API framework
- **Uvicorn** — ASGI server
- **GeoPandas** — Geospatial data processing
- **Shapely** — Geometry operations and measurements
- **PyProj** — Coordinate transformations
- **Fiona / Pyogrio** — Geospatial file I/O
- **FastKML** — KML-related support
- **uv** — Python package and dependency management

---

## Project Structure

```text
GeoMeasure/
├── apps/
│   └── api/
│       ├── files.py
│       ├── models/
│       ├── schemas/
│       ├── services/
│       │   ├── crs.py
│       │   ├── file_processor.py
│       │   ├── measurement.py
│       │   └── file_store.py
│       ├── utils/
│       └── main.py
│
├── tests/
│
├── uploads/
│
├── .gitignore
├── .python-version
├── pyproject.toml
├── README.md
├── requirements.txt
└── uv.lock

Absolutely. Here is a **complete `README.md`** you can copy-paste directly into your repository.

```markdown
# GeoMeasure

GeoMeasure is a FastAPI-based backend API for processing geospatial files and calculating measurements from their geometries.

The API accepts KML files and ZIP archives containing Shapefiles, extracts their geospatial features, handles coordinate reference systems (CRS), and calculates measurements such as polygon area and line length.

---

## Features

- Upload `.kml` files
- Upload `.zip` files containing a Shapefile
- Extract geospatial features and their properties
- Detect geometry types
- Detect and handle Coordinate Reference Systems (CRS)
- Automatically transform geographic CRS to a suitable projected CRS
- Calculate:
  - Polygon → Area
  - LineString → Length
  - Point → No measurement
- Store processed files with unique IDs
- Retrieve file information using its ID
- Retrieve measurements for a processed file
- Interactive API documentation using Swagger UI
- Basic validation and error handling

---

## Tech Stack

- **Python 3.12+**
- **FastAPI** — REST API framework
- **Uvicorn** — ASGI server
- **GeoPandas** — Geospatial data processing
- **Shapely** — Geometry operations and measurements
- **PyProj** — Coordinate transformations
- **Fiona / Pyogrio** — Geospatial file I/O
- **FastKML** — KML-related support
- **uv** — Python package and dependency management

---

## Project Structure

```text
GeoMeasure/
├── apps/
│   └── api/
│       ├── files.py
│       ├── models/
│       ├── schemas/
│       ├── services/
│       │   ├── crs.py
│       │   ├── file_processor.py
│       │   ├── measurement.py
│       │   └── file_store.py
│       ├── utils/
│       └── main.py
│
├── tests/
│
├── uploads/
│
├── .gitignore
├── .python-version
├── pyproject.toml
├── README.md
├── requirements.txt
└── uv.lock
```

---

# Getting Started

## Prerequisites

Make sure you have the following installed:

- Python 3.12 or higher
- `uv`

You can verify Python with:

```bash
python --version
```

and uv with:

```bash
uv --version
```

---

## Installation

Clone the repository:

```bash
git clone https://github.com/ooppssss/GeoMeasure.git
```

Move into the project directory:

```bash
cd GeoMeasure
```

Install the project dependencies:

```bash
uv sync
```

---

# Running the API

Start the development server using:

```bash
uv run uvicorn apps.api.main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

---

# API Documentation

GeoMeasure provides interactive API documentation through FastAPI.

Open:

```text
http://127.0.0.1:8000/docs
```

This opens Swagger UI where you can upload files and test all available endpoints directly from the browser.

---

# API Endpoints

## 1. Upload and Process a File

### Request

```http
POST /api/files/
```

The endpoint accepts:

- `.kml`
- `.zip` containing a Shapefile

### Example

Using Swagger UI:

1. Open `/docs`
2. Select `POST /api/files/`
3. Click **Try it out**
4. Select a KML or Shapefile ZIP
5. Click **Execute**

### Example Response

```json
{
  "id": 1,
  "message": "File processed successfully",
  "filename": "polygons.kml",
  "feature_count": 1,
  "source_crs": "EPSG:4326",
  "measurement_crs": "EPSG:32618"
}
```

The returned `id` can be used to retrieve information about the processed file.

---

# 2. Get File Information

### Request

```http
GET /api/files/{file_id}/
```

Example:

```http
GET /api/files/1/
```

### Response

```json
{
  "id": 1,
  "filename": "polygons.kml",
  "feature_count": 1,
  "source_crs": "EPSG:4326",
  "measurement_crs": "EPSG:32618"
}
```

This provides information about the processed file and the CRS used for measurement calculations.

---

# 3. Get Measurements

### Request

```http
GET /api/files/{file_id}/measurements/
```

Example:

```http
GET /api/files/1/measurements/
```

### Response

```json
{
  "file_id": 1,
  "filename": "polygons.kml",
  "measurements": [
    {
      "id": 0,
      "geometry_type": "Polygon",
      "measurement": {
        "measurement_type": "area",
        "value": 144511.23152711667,
        "unit": "square_meters"
      }
    }
  ]
}
```

---

# Geospatial Processing Flow

The processing pipeline follows these steps:

```text
             Upload File
                  │
                  ▼
          Validate File Type
                  │
                  ▼
       ┌─────────────────────┐
       │                     │
       ▼                     ▼
      KML              Shapefile ZIP
       │                     │
       └──────────┬──────────┘
                  ▼
          Read with GeoPandas
                  │
                  ▼
          Extract Geometries
                  │
                  ▼
            Check CRS
                  │
                  ▼
       Transform to Projected CRS
                  │
                  ▼
       Calculate Measurements
                  │
                  ▼
        Store Processing Result
                  │
                  ▼
            Return File ID
```

---

# Feature Processing

Each input feature is processed individually.

The application extracts information such as:

- Feature ID / index
- Geometry type
- Geometry
- CRS
- Feature properties / attributes
- Measurement, when applicable

For example, a polygon feature may be represented internally as:

```text
Feature
├── ID
├── Geometry Type → Polygon
├── Geometry
├── Properties
└── Measurement
      ├── Type → area
      ├── Value
      └── Unit → square_meters
```

---

# Measurement Logic

GeoMeasure calculates measurements based on the geometry type.

| Geometry | Measurement | Unit |
|---|---|---|
| Polygon | Area | square meters |
| LineString | Length | meters |
| Point | No measurement | - |

### Polygon

For polygons:

```text
Polygon → Area
```

Example:

```json
{
  "measurement_type": "area",
  "value": 144511.23,
  "unit": "square_meters"
}
```

### LineString

For lines:

```text
LineString → Length
```

Example:

```json
{
  "measurement_type": "length",
  "value": 1250.42,
  "unit": "meters"
}
```

### Point

Points do not have an area or length measurement, so the API returns:

```json
{
  "measurement_type": null,
  "value": null,
  "unit": null
}
```

---

# CRS Handling

Coordinate Reference Systems are important when calculating geospatial measurements.

Many KML files use a geographic CRS such as:

```text
EPSG:4326
```

EPSG:4326 represents coordinates as latitude and longitude.

Calculating distances or areas directly using latitude/longitude values would produce incorrect results because those coordinates are expressed in angular degrees rather than meters.

Therefore, GeoMeasure checks the input CRS.

If the CRS is geographic, the application estimates a suitable projected CRS and transforms the geometries before performing measurements.

For example:

```text
Input CRS
EPSG:4326
     │
     ▼
Estimate suitable projected CRS
     │
     ▼
EPSG:32618
     │
     ▼
Calculate area / length
```

This allows measurements to be calculated in meaningful units such as:

```text
meters
square meters
```

If the input data already uses a projected CRS, the application can use that CRS directly.

---

# Architecture

The application separates API handling from geospatial processing.

```text
FastAPI
   │
   ▼
files.py
   │
   ├── File Upload
   ├── Validation
   ├── API Responses
   │
   ├───────────────┐
   ▼               ▼
file_processor.py  crs.py
   │               │
   │               └── CRS detection/transformation
   │
   └── Read KML / Shapefile
           │
           ▼
      GeoDataFrame
           │
           ▼
     measurement.py
           │
           └── Area / Length calculations
```

### `main.py`

Creates the FastAPI application and registers the API router.

### `files.py`

Contains the HTTP endpoints for:

- Uploading files
- Retrieving file information
- Retrieving measurements

### `file_processor.py`

Responsible for reading:

- KML files
- Shapefile ZIP archives

and converting them into GeoDataFrames.

### `crs.py`

Responsible for:

- Checking the source CRS
- Detecting geographic CRS
- Selecting a suitable projected CRS
- Transforming geometries

### `measurement.py`

Contains the geometry measurement logic.

### `file_store.py`

Stores processed file information and assigns unique IDs for retrieving results through the API.

---

# Error Handling

GeoMeasure validates uploaded files before processing them.

Examples of handled errors include:

### Unsupported file type

```json
{
  "detail": "File type is not supported"
}
```

### Missing filename

```json
{
  "detail": "Filename is missing"
}
```

### File not found

```json
{
  "detail": "File not found"
}
```

### Invalid geospatial input

Processing errors are converted into appropriate API errors instead of exposing internal stack traces to the client.

---

# Example Workflow

A typical user workflow looks like this:

### Step 1 — Upload

```http
POST /api/files/
```

Upload:

```text
polygons.kml
```

### Step 2 — Receive ID

```json
{
  "id": 1,
  "filename": "polygons.kml",
  "feature_count": 1
}
```

### Step 3 — Retrieve File Information

```http
GET /api/files/1/
```

### Step 4 — Retrieve Measurements

```http
GET /api/files/1/measurements/
```

### Step 5 — Receive Measurement

```json
{
  "file_id": 1,
  "filename": "polygons.kml",
  "measurements": [
    {
      "id": 0,
      "geometry_type": "Polygon",
      "measurement": {
        "measurement_type": "area",
        "value": 144511.23152711667,
        "unit": "square_meters"
      }
    }
  ]
}
```

---

# Design Decisions

## Why GeoPandas?

GeoPandas provides a convenient abstraction for working with geospatial vector data and integrates well with common geospatial formats and CRS transformations.

It also allows KML and Shapefile data to be represented using a common `GeoDataFrame` structure.

## Why Shapely?

Shapely provides geometry objects and geometric operations such as:

```text
Polygon.area
LineString.length
```

This makes the measurement logic simple and separated from file parsing.

## Why PyProj?

PyProj is used through the GeoPandas CRS functionality to transform geometries between coordinate reference systems.

This is important because measurements should not be calculated directly from geographic coordinates.

## Why FastAPI?

FastAPI provides:

- Simple API development
- Automatic request validation
- Automatic OpenAPI documentation
- Swagger UI
- Good support for file uploads

---

# Current Storage

The current implementation stores processed file information in memory.

This keeps the project simple and focuses on the core geospatial processing and API architecture.

Because the storage is in memory:

- Data is lost when the server restarts.
- IDs restart when the application restarts.
- It is not intended for production-scale persistent storage.

A production version could use PostgreSQL with PostGIS or another persistent database.

---

# Security Considerations

Uploaded files are stored inside the `uploads/` directory.

The repository ignores uploaded files using `.gitignore`:

```gitignore
uploads/*
!uploads/.gitkeep
```

This prevents potentially sensitive geospatial files from accidentally being committed to GitHub.

Environment files and local development files are also excluded from version control.

---

# Testing

Tests can be added under:

```text
tests/
```

Important scenarios to test include:

- Valid KML upload
- Valid Shapefile ZIP upload
- Polygon area calculation
- LineString length calculation
- Point processing
- Unsupported file types
- Invalid files
- Missing CRS
- Nonexistent file IDs
- CRS transformation

Run the test suite with:

```bash
uv run pytest
```

---

# Future Improvements

Possible improvements for a production-ready version include:

- Persistent database storage
- PostGIS integration
- Pydantic response schemas
- More comprehensive automated tests
- Support for MultiPolygon and MultiLineString
- Improved ZIP validation and secure extraction
- Better handling of datasets spanning multiple UTM zones
- Background processing for large geospatial files
- File size limits
- Authentication and authorization
- Job/status tracking for long-running processing
- GeoJSON output
- Pagination for large feature collections
- Docker support
- Cloud storage for uploaded files

---
