import pytest
import time

# Patch start_time in the module under test
import controllers.status_controller as status_controller

@pytest.mark.parametrize(
    "mock_version, mock_start_time, mock_now, expected_uptime, expected_name, expected_msg, description",
    [
        # Happy path: uptime 10 seconds
        ("1.0.0", 1000, 1010, 10, "timestamp-api", "API status 🚀", "uptime 10s"),
        # Happy path: uptime 0 seconds
        ("2.1.3", 2000, 2000, 0, "timestamp-api", "API status 🚀", "uptime 0s"),
        # Edge case: negative uptime (system clock issue)
        ("3.0.0", 3000, 2990, -10, "timestamp-api", "API status 🚀", "negative uptime"),
        # Edge case: large uptime
        ("4.2.0", 100, 100000, 99900, "timestamp-api", "API status 🚀", "large uptime"),
    ],
    ids=[
        "uptime-10s",
        "uptime-0s",
        "negative-uptime",
        "large-uptime",
    ]
)
def test_get_status_happy_and_edge_cases(
    mock_version, mock_start_time, mock_now, expected_uptime, expected_name, expected_msg, description, monkeypatch
):
    # Arrange
    class MockApp:
        version = mock_version

    monkeypatch.setattr("controllers.status_controller.start_time", mock_start_time)
    monkeypatch.setattr("controllers.status_controller.time.time", lambda: mock_now)
    monkeypatch.setattr("main.app", MockApp)

    # Act
    result = status_controller.get_status()

    # Assert
    assert result["msg"] == expected_msg, f"Failed: {description} (msg)"
    assert result["name"] == expected_name, f"Failed: {description} (name)"
    assert result["version"] == mock_version, f"Failed: {description} (version)"
    assert result["uptime"] == expected_uptime, f"Failed: {description} (uptime)"


@pytest.mark.parametrize(
    "patch_app, patch_start_time, patch_time, error_type, description",
    [
        # Error case: app.version missing
        (object(), 1000, 1010, AttributeError, "app missing version"),
        # Error case: time function missing
        ("1.0.0", 1000, None, TypeError, "time missing"),
    ],
    ids=[
        "app-missing-version",
        "time-missing",
    ]
)
def test_get_status_error_cases(patch_app, patch_start_time, patch_time, error_type, description, monkeypatch):
    # Arrange
    if isinstance(patch_app, str):
        class MockApp:
            version = patch_app
        monkeypatch.setattr("main.app", MockApp)
    else:
        monkeypatch.setattr("main.app", patch_app)

    if patch_time is not None:
        monkeypatch.setattr(
            "controllers.status_controller.time.time",
            lambda: patch_time
        )
    else:
        # Simula erro de chamada de time.time, lançando TypeError
        def raise_type_error():
            raise TypeError("Simulated time.time missing")
        monkeypatch.setattr(
            "controllers.status_controller.time.time",
            raise_type_error
        )

    # Act & Assert
    with pytest.raises(error_type):
        status_controller.get_status()
