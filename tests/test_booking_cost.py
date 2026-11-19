import pytest
from src.booking_cost import calculate_booking_cost


@pytest.mark.parametrize(
    "nights, nightly_rate_cents, expected",
    [
        (1, 10000, 10000),      # Lower boundary: 1 night
        (6, 10000, 60000),      # Just below 7 nights
        (7, 10000, 70000),      # 7 nights (exposes planted long-stay discount defect)
        (15, 5000, 75000),      # Mid-range stay
        (30, 10000, 300000),    # Upper boundary: 30 nights
        (5, 0, 0),              # Zero nightly rate boundary
    ],
)
def test_calculate_booking_cost_valid_inputs_returns_expected_charge(
    nights, nightly_rate_cents, expected
):
    # Act
    result = calculate_booking_cost(nights, nightly_rate_cents)

    # Assert
    assert result == expected


@pytest.mark.parametrize(
    "nights, nightly_rate_cents",
    [
        (0, 10000),     # Below lower boundary (nights < 1)
        (-1, 10000),    # Negative nights
        (31, 10000),    # Above upper boundary (nights > 30)
        (5, -1),        # Negative nightly rate
    ],
)
def test_calculate_booking_cost_out_of_range_raises_value_error(
    nights, nightly_rate_cents
):
    # Act and Assert
    with pytest.raises(ValueError):
        calculate_booking_cost(nights, nightly_rate_cents)


@pytest.mark.parametrize(
    "nights, nightly_rate_cents",
    [
        (True, 10000),      # Bool is not a valid int
        (5, False),         # Bool is not a valid int
        (5.0, 10000),       # Float nights
        (5, 99.99),         # Float rate
        ("5", 10000),       # String nights
        (None, 10000),      # NoneType
    ],
)
def test_calculate_booking_cost_invalid_type_raises_type_error(
    nights, nightly_rate_cents
):
    # Act and Assert
    with pytest.raises(TypeError):
        calculate_booking_cost(nights, nightly_rate_cents)
