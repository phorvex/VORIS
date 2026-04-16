import re

CONVERSIONS = {
    # Length
    ("miles", "kilometers"): lambda x: x * 1.60934,
    ("kilometers", "miles"): lambda x: x / 1.60934,
    ("feet", "meters"): lambda x: x * 0.3048,
    ("meters", "feet"): lambda x: x / 0.3048,
    ("inches", "centimeters"): lambda x: x * 2.54,
    ("centimeters", "inches"): lambda x: x / 2.54,
    ("yards", "meters"): lambda x: x * 0.9144,
    ("meters", "yards"): lambda x: x / 0.9144,
    # Weight
    ("pounds", "kilograms"): lambda x: x * 0.453592,
    ("kilograms", "pounds"): lambda x: x / 0.453592,
    ("ounces", "grams"): lambda x: x * 28.3495,
    ("grams", "ounces"): lambda x: x / 28.3495,
    ("tons", "kilograms"): lambda x: x * 907.185,
    ("kilograms", "tons"): lambda x: x / 907.185,
    # Temperature
    ("celsius", "fahrenheit"): lambda x: (x * 9/5) + 32,
    ("fahrenheit", "celsius"): lambda x: (x - 32) * 5/9,
    ("celsius", "kelvin"): lambda x: x + 273.15,
    ("kelvin", "celsius"): lambda x: x - 273.15,
    # Speed
    ("mph", "kph"): lambda x: x * 1.60934,
    ("kph", "mph"): lambda x: x / 1.60934,
    ("knots", "mph"): lambda x: x * 1.15078,
    ("mph", "knots"): lambda x: x / 1.15078,
    # Volume
    ("gallons", "liters"): lambda x: x * 3.78541,
    ("liters", "gallons"): lambda x: x / 3.78541,
    ("cups", "milliliters"): lambda x: x * 236.588,
    ("milliliters", "cups"): lambda x: x / 236.588,
    ("fluid ounces", "milliliters"): lambda x: x * 29.5735,
    ("milliliters", "fluid ounces"): lambda x: x / 29.5735,
    # Data
    ("gigabytes", "megabytes"): lambda x: x * 1024,
    ("megabytes", "gigabytes"): lambda x: x / 1024,
    ("terabytes", "gigabytes"): lambda x: x * 1024,
    ("gigabytes", "terabytes"): lambda x: x / 1024,
    ("megabytes", "kilobytes"): lambda x: x * 1024,
    ("kilobytes", "megabytes"): lambda x: x / 1024,
}

UNIT_ALIASES = {
    "mile": "miles", "km": "kilometers", "kilometer": "kilometers",
    "ft": "feet", "foot": "feet", "m": "meters", "meter": "meters",
    "in": "inches", "inch": "inches", "cm": "centimeters", "centimeter": "centimeters",
    "yd": "yards", "yard": "yards",
    "lb": "pounds", "pound": "pounds", "lbs": "pounds",
    "kg": "kilograms", "kilogram": "kilograms",
    "oz": "ounces", "ounce": "ounces", "g": "grams", "gram": "grams",
    "ton": "tons",
    "c": "celsius", "f": "fahrenheit", "k": "kelvin",
    "degrees f": "fahrenheit", "degrees c": "celsius", "degrees fahrenheit": "fahrenheit",
    "degrees celsius": "celsius", "degree f": "fahrenheit", "degree c": "celsius",
    "°f": "fahrenheit", "°c": "celsius",
    "l": "liters", "liter": "liters", "ml": "milliliters", "milliliter": "milliliters",
    "gal": "gallons", "gallon": "gallons",
    "gb": "gigabytes", "gigabyte": "gigabytes",
    "mb": "megabytes", "megabyte": "megabytes",
    "tb": "terabytes", "terabyte": "terabytes",
    "kb": "kilobytes", "kilobyte": "kilobytes",
}

def normalize_unit(unit):
    unit = unit.lower().strip()
    return UNIT_ALIASES.get(unit, unit)

def convert(text):
    text = text.lower()
    text = text.replace("convert ", "").replace("what is ", "").replace("how many ", "").replace("how much is ", "")

    pattern = r'([\d.]+)\s*([a-z ]+?)\s+(?:to|in|into)\s+([a-z ]+)'
    match = re.search(pattern, text)
    if not match:
        return None

    value = float(match.group(1))
    from_unit = normalize_unit(match.group(2).strip())
    to_unit = normalize_unit(match.group(3).strip())

    key = (from_unit, to_unit)
    if key in CONVERSIONS:
        result = CONVERSIONS[key](value)
        if isinstance(result, float) and result.is_integer():
            result = int(result)
        else:
            result = round(result, 4)
        return f"{value} {from_unit} = {result} {to_unit}"

    return None