import json
import os

def load_pricing_data():
    """Load pricing data from JSON file."""
    pricing_file = os.path.join('data', 'pricing.json')
    try:
        with open(pricing_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}
    except json.JSONDecodeError:
        return {}

def get_service_info(service_key):
    """Get information for a specific service."""
    pricing_data = load_pricing_data()
    return pricing_data.get('services', {}).get(service_key, {})

def get_pricing_tiers():
    """Get all pricing tier information."""
    pricing_data = load_pricing_data()
    return pricing_data.get('pricing_tiers', {})

def get_contact_info():
    """Get contact information."""
    pricing_data = load_pricing_data()
    return pricing_data.get('contact', {})

def get_demo_info():
    """Get demo information."""
    pricing_data = load_pricing_data()
    return pricing_data.get('demo', {})

def get_performance_metrics():
    """Get performance metrics."""
    pricing_data = load_pricing_data()
    return pricing_data.get('performance_metrics', {})

def get_use_cases():
    """Get use cases."""
    pricing_data = load_pricing_data()
    return pricing_data.get('use_cases', [])
