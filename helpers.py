def calculate_overall_coefficient(temperature, humidity):
    temperature_weight = 0.5
    humidity_weight = 0.5
    normalized_temperature = temperature / 100
    normalized_humidity = humidity / 100
    overall_coefficient = (
            (normalized_temperature * temperature_weight) /
            (normalized_humidity * humidity_weight)
    )
    return overall_coefficient
