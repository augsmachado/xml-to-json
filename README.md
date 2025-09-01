# XML/JSON Utility API Documentation

A simple FastAPI service for status checking, XML to JSON, and JSON to XML conversion.

---

## Endpoints

### 1. `GET /status`

Returns the status of the API, including name, version, and uptime (in seconds).

**Response Example:**

```json
{
	"msg": "API status 🚀",
	"name": "xml-json-api",
	"version": "1.0.0",
	"uptime": 1234
}
```

### 2. `POST /to-json`

Converts any XML text to JSON.

-   **Request Body**: Raw XML (`Content-Type: text/plain or application/xml`)
-   **Response**: JSON representation of the XML.

**Request Example**:

```xml
<note>
    <to>User</to>
    <from>API</from>
    <heading>Reminder</heading>
    <body>Hello, world!</body>
</note>
```

**Response Example**:

```json
{
	"note": {
		"to": "User",
		"from": "API",
		"heading": "Reminder",
		"body": "Hello, world!"
	}
}
```

**Error Response Example**:

```json
{
	"error": "Invalid XML",
	"details": "mismatched tag: line 1, column 42"
}
```

### 3. `POST /to-xml`

Converts any JSON object to XML.

-   **Request Body**: JSON (Content-Type: `application/json`)
-   **Response**: XML as plain text (Content-Type: `application/xml`)

**Request Example**:

```json
{
	"note": {
		"to": "User",
		"from": "API",
		"heading": "Reminder",
		"body": "Hello, world!"
	}
}
```

**Response Example**:

```xml
<root>
    <note>
        <to>User</to>
        <from>API</from>
        <heading>Reminder</heading>
        <body>Hello, world!</body>
    </note>
</root>
```

**Error Response Example**:

```json
{
	"error": "Invalid JSON",
	"details": "Expecting value: line 1 column 1 (char 0)"
}
```

### CORS

CORS is enabled for all origins.

## How to Run Locally

-   Install dependencies:
    `pip install fastapi uvicorn xmltodict dicttoxml`
-   Start the server:
    `uvicorn main:app --reload`
-   Access the docs at:
    `http://localhost:8000/docs`

## Notes

-   The `/to-json` endpoint expects valid XML in the request body.
-   The `/to-xml` endpoint expects valid JSON in the request body.
-   All endpoints return error details in case of invalid input.
