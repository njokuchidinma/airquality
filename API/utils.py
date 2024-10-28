import random
import string


def return_quality_message(quality_level,risk_elements,danger_message,solution_message,bad_threshold,high_threshold):
    if quality_level >= bad_threshold:
        return({
            'title': f'BAD: {risk_elements} Alert',
            'description': f"{quality_level} ppm levels detected. {danger_message} Solution: {solution_message}"
        })
    elif quality_level >= high_threshold:
        return({
            'title': f'WARNING: {risk_elements} Alert',
            'description': f"{quality_level} ppm levels detected. {danger_message} Solution: {solution_message}"
        })

def generate_random_password(length=12):
    characters = string.ascii_letters + string.digits
    password = ''.join(random.choice(characters) for i in range(length))
    return password