import json
from fastapi import APIRouter, Request
from controllers.convertions_controller import to_json_controller, to_xml_controller

router = APIRouter()

@router.post("/to-json")
async def convert_to_json(request: Request):
    xml_text = await request.body()
    return to_json_controller(xml_text)

@router.post("/to-xml")
async def convert_to_xml(request: Request):
    json_data = await request.json()
    return to_xml_controller(json_data)
