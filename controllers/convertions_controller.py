import xmltodict
import json

from dicttoxml import dicttoxml

from fastapi.responses import JSONResponse, PlainTextResponse

def to_json_controller(xml_text: bytes):
    """
    Receives XML in the request body and returns JSON as text.
    """
    try:
        data = xmltodict.parse(xml_text.decode("utf-8"))
        return JSONResponse(content=data)
    except Exception as e:
        return JSONResponse(
            status_code=400,
            content={"error": "Invalid XML", "details": str(e)}
        )

def to_xml_controller(json_data: dict):
    """
    Receives JSON in the request body and returns XML as text.
    """
    try:
        xml_bytes = dicttoxml(json_data, custom_root='root', attr_type=False)
        xml_str = xml_bytes.decode("utf-8")
        return PlainTextResponse(content=xml_str, media_type="application/xml")
    except Exception as e:
        return JSONResponse(
            status_code=400,
            content={"error": "Invalid JSON", "details": str(e)}
        )