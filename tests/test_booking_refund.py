import pytest
from src.booking_refund import is_refundable


@pytest.mark.parametrize(
    "hours_before_checkin, flexible_rate",
    [
        (48, True),     # Boundary: exact 48 hours (exposes planted > 48 defect)
        (49, True),     # Just above 48 hours
        (100, True),    # Well above 48 hours
    ],
)
def test_is_refundable_eligible_cancellation_returns_true(
    hours_before_checkin, flexible_rate
):
    # Act
    result = is_refundable(hours_before_checkin, flexible_rate)

    # Assert
    assert result is True


@pytest.mark.parametrize(
    "hours_before_checkin, flexible_rate",
    [
        (47, True),     # Just below 48 hours
        (0, True),      # Lower boundary: 0 hours
        (48, False),    # Non-flexible rate at 48 hours
        (72, False),    # Non-flexible rate above 48 hours
        (0, False),     # Non-flexible rate at 0 hours
    ],
)
def test_is_refundable_ineligible_cancellation_returns_false(
    hours_before_checkin, flexible_rate
):
    # Act
    result = is_refundable(hours_before_checkin, flexible_rate)

    # Assert
    assert result is False


@pytest.mark.parametrize(
    "hours_before_checkin, flexible_rate",
    [
        (-1, True),     # Just below lower boundary
        (-10, False),   # Negative hours
    ],
)
def test_is_refundable_negative_hours_raises_value_error(
    hours_before_checkin, flexible_rate
):
    # Act and Assert
    with pytest.raises(ValueError):
        is_refundable(hours_before_checkin, flexible_rate)


@pytest.mark.parametrize(
    "hours_before_checkin, flexible_rate",
    [
        (True, True),       # Bool for hours_before_checkin
        (48.0, True),       # Float for hours_before_checkin
        ("48", True),       # String for hours_before_checkin
        (48, 1),            # Int instead of bool for flexible_rate
        (48, "True"),       # String instead of bool
        (48, None),         # NoneType
    ],
)
def test_is_refundable_invalid_type_raises_type_error(
    hours_before_checkin, flexible_rate
):
    # Act and Assert
    with pytest.raises(TypeError):
        is_refundable(hours_before_checkin, flexible_rate)
