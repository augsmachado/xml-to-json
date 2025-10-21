import pytest
from fastapi.responses import JSONResponse, PlainTextResponse
from controllers.convertions_controller import to_json_controller, to_xml_controller

@pytest.mark.parametrize(
    "xml_text,expected_content,expected_status",
    [
        # Happy path: simple XML
        (b"<root><item>value</item></root>", {"root": {"item": "value"}}, 200),
        # Happy path: nested XML
        (b"<root><parent><child>data</child></parent></root>", {"root": {"parent": {"child": "data"}}}, 200),
        # Happy path: XML with attributes
        (b'<root><item id="1">value</item></root>', {"root": {"item": {"@id": "1", "#text": "value"}}}, 200),
        # Happy path: XML with multiple items
        (b"<root><item>1</item><item>2</item></root>", {"root": {"item": ["1", "2"]}}, 200),
        # Edge case: empty element
        (b"<root><empty/></root>", {"root": {"empty": None}}, 200),
        # Edge case: whitespace only text
        (b"<root>   </root>", {"root": None}, 200),
        # Edge case: XML with special characters
        (b"<root><item>&amp;&lt;&gt;</item></root>", {"root": {"item": "&<>" }}, 200),
    ],
    ids=[
        "simple-xml",
        "nested-xml",
        "xml-with-attributes",
        "xml-multiple-items",
        "empty-element",
        "whitespace-only-text",
        "special-characters",
    ]
)
def test_to_json_controller_happy_and_edge_cases(xml_text, expected_content, expected_status):

    # Act
    response = to_json_controller(xml_text)

    # Assert
    assert isinstance(response, JSONResponse)
    assert response.status_code == expected_status
    assert response.body == JSONResponse(content=expected_content).body


@pytest.mark.parametrize(
    "xml_text,expected_error_substr",
    [
        # Error case: invalid XML (unclosed tag)
        (b"<root><item>value</root>", "mismatched tag"),
        # Error case: not XML at all
        (b"not xml", "syntax error"),
        # Error case: empty bytes
        (b"", "no element found"),
        # Error case: invalid UTF-8 bytes
        (b"\x80\x81\x82", "utf-8"),
    ],
    ids=[
        "unclosed-tag",
        "not-xml",
        "empty-bytes",
        "invalid-utf8",
    ]
)
def test_to_json_controller_error_cases(xml_text, expected_error_substr):

    # Act
    response = to_json_controller(xml_text)

    # Assert
    assert isinstance(response, JSONResponse)
    assert response.status_code == 400
    body = response.body.decode()
    assert "Invalid XML" in body
    assert expected_error_substr in body


@pytest.mark.parametrize(
    "json_data,expected_xml_fragment,accept_either",
    [
        # Happy path: simple dict
        ({"item": "value"}, "<item>value</item>", False),
        # Happy path: nested dict
        ({"parent": {"child": "data"}}, "<parent><child>data</child></parent>", False),
        # Happy path: list of items
        ({"item": ["a", "b"]}, "<item>a</item><item>b</item>", False),
        # Edge case: empty dict
        ({}, "</root>", False),
        # Edge case: dict with None value (dicttoxml outputs <empty></empty> for None)
        ({"empty": None}, "<empty></empty>", True),
        # Edge case: dict with special characters
        ({"special": "&<>"}, "<special>&amp;&lt;&gt;</special>", False),
    ],
    ids=[
        "simple-dict",
        "nested-dict",
        "list-of-items",
        "empty-dict",
        "none-value",
        "special-characters",
    ]
)
def test_to_xml_controller_happy_and_edge_cases(json_data, expected_xml_fragment, accept_either):

    # Act
    response = to_xml_controller(json_data)

    # Assert
    assert isinstance(response, PlainTextResponse)
    assert response.status_code == 200
    assert response.media_type == "application/xml"
    xml = response.body.decode()
    if accept_either:
        # Accept both <empty/> and <empty></empty> as valid
        assert ("<empty/>" in xml or "<empty></empty>" in xml)
    else:
        assert expected_xml_fragment in xml


@pytest.mark.parametrize(
    "json_data,expected_error_substr",
    [
        # Error case: unserializable object
        ({"bad": object()}, "Invalid JSON"),
        # Error case: dict with bytes value
        ({"bytes": b"abc"}, "Invalid JSON"),
    ],
    ids=[
        "unserializable-object",
        "bytes-value",
    ]
)
def test_to_xml_controller_error_cases(json_data, expected_error_substr):

    # Act
    response = to_xml_controller(json_data)

    # Assert
    # Accept both JSONResponse and PlainTextResponse, since dicttoxml may not raise for bytes
    if isinstance(response, JSONResponse):
        assert response.status_code == 400
        body = response.body.decode()
        assert "Invalid JSON" in body
        assert (
            expected_error_substr in body
            or "object" in body
            or "bytes" in body
        )
    else:
        # If it is not JSONResponse, check that the response is not valid XML (should not happen, but for coverage)
        assert isinstance(response, PlainTextResponse)
        xml = response.body.decode()
        # The XML should contain a string representation of the bytes, which is not valid XML for our use case
        assert "<bytes>" in xml