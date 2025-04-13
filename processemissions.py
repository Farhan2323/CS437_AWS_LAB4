import json
import logging

# Configure logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Store maximum CO2 values for each vehicle
vehicle_max_co2 = {}

def process_emission_data(message):
    """
    Process vehicle emission data and calculate maximum CO2 values
    """
    try:
        logger.info(f"Processing message: {message}")
        
        # Extract device ID and data
        device_id = message.get('device_id', 'unknown')
        data = message.get('data', {})
        
        # Extract CO2 value
        co2_value = float(data.get('CO2', 0))
        
        # Update maximum CO2 value for this vehicle
        if device_id not in vehicle_max_co2:
            vehicle_max_co2[device_id] = co2_value
        elif co2_value > vehicle_max_co2[device_id]:
            vehicle_max_co2[device_id] = co2_value
            
        # Create result message
        result = {
            'device_id': device_id,
            'max_CO2': vehicle_max_co2[device_id]
        }
        
        logger.info(f"Result for {device_id}: {result}")
        return result
        
    except Exception as e:
        logger.error(f"Error processing emission data: {str(e)}")
        return {
            'error': str(e)
        }


def lambda_handler(event, context):
    """
    AWS Lambda handler function
    """
    return process_emission_data(event)

# For local testing
if __name__ == "__main__":
    # Sample test data
    test_message = {
        'device_id': 'RaspberryPi_1',
        'data': {
            'CO2': 120.5
        }
    }
    
    result = process_emission_data(test_message)
    print(f"Result: {result}")
    
    # Test with higher value
    test_message2 = {
        'device_id': 'RaspberryPi_1',
        'data': {
            'CO2': 150.7
        }
    }
    
    result2 = process_emission_data(test_message2)
    print(f"Result after higher value: {result2}")

