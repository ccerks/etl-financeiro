import pytest
from pydantic import ValidationError
from main import MarketDataContract

def test_valid_market_data_contract():
    """Test if the Pydantic contract accepts valid data."""
    valid_data = {
        "date": "2026-04-27",
        "asset": "Bitcoin",
        "price_usd": 64000.50
    }
    contract = MarketDataContract(**valid_data)
    
    assert contract.asset == "Bitcoin"
    assert contract.price_usd == 64000.50

def test_invalid_market_data_negative_price():
    """Test if the Pydantic contract rejects negative prices."""
    invalid_data = {
        "date": "2026-04-27",
        "asset": "Ethereum",
        "price_usd": -50.0  # Impossible price
    }
    
    with pytest.raises(ValidationError):
        MarketDataContract(**invalid_data)

def test_invalid_market_data_missing_field():
    """Test if the Pydantic contract rejects missing required fields."""
    invalid_data = {
        "date": "2026-04-27",
        # Missing 'asset'
        "price_usd": 100.0
    }
    
    with pytest.raises(ValidationError):
        MarketDataContract(**invalid_data)