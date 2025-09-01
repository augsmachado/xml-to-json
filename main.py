# main.py

from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse, PlainTextResponse
from fastapi.middleware.cors import CORSMiddleware
import time
import xmltodict
import json
from dicttoxml import dicttoxml

app = FastAPI(
    title="XML/JSON Utility API",
    version="1.0.0",
    description="API for status, XML to JSON, and JSON to XML conversion"
)

start_time = time.time()

# Allow CORS for all origins (optional, for testing)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/status")
def status():
    uptime = int(time.time() - start_time)
    return {
        "msg": "API status 🚀",
        "name": "xml-json-api",
        "version": app.version,
        "uptime": uptime
    }

@app.post("/to-json")
async def to_json(request: Request):
    """
    Receives XML in the request body (text/plain or application/xml) and returns JSON.
    """
    xml_text = await request.body()
    try:
        xml_text = xml_text.decode("utf-8")
        data = xmltodict.parse(xml_text)
        return JSONResponse(content=data)
    except Exception as e:
        return JSONResponse(
            status_code=400,
            content={"error": "Invalid XML", "details": str(e)}
        )

@app.post("/to-xml")
async def to_xml(request: Request):
    """
    Receives JSON in the request body and returns XML as text.
    """
    try:
        json_data = await request.json()
        xml_bytes = dicttoxml(json_data, custom_root='root', attr_type=False)
        xml_str = xml_bytes.decode("utf-8")
        return PlainTextResponse(content=xml_str, media_type="application/xml")
    except Exception as e:
        return JSONResponse(
            status_code=400,
            content={"error": "Invalid JSON", "details": str(e)}
        )
