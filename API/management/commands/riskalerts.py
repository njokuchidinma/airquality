# from django.core.management.base import BaseCommand
from API.models import RiskAlert


def load_risk_alerts():
    risk_alerts = [
        {
            'element': 'Carbon Dioxide (CO2)',
            'threshold_high': 1000,
            'threshold_bad': 2000,
            'danger_message': 'Exposure at this level can cause headache, dizziness, and nausea.',
            'solution_message': 'Ventilate the area immediately and avoid using gas appliances until the level decreases.'
        },
        {
            'element': 'Carbon Monoxide (CO)',
            'threshold_high': 50,
            'threshold_bad': 100,
            'danger_message': 'Exposure at this level can cause headaches and flu-like symptoms.',
            'solution_message': 'Evacuate the area and seek fresh air immediately.'
        },
        {
            'element': 'Liquefied Petroleum Gas (LPG)',
            'threshold_high': 50,
            'threshold_bad': 100,
            'danger_message': 'Exposure at this level can cause dizziness and shortness of breath.',
            'solution_message': 'Ventilate the area and check for leaks.'
        },
        {
            'element': 'Smoke',
            'threshold_high': 5,
            'threshold_bad': 10,
            'danger_message': 'Exposure at this level can lead to respiratory issues and irritation.',
            'solution_message': 'Evacuate the area and call emergency services if necessary.'
        },
        {
            'element': 'Humidity',
            'threshold_high': 70,
            'threshold_bad': 90,
            'danger_message': 'High humidity can lead to mold growth and discomfort.',
            'solution_message': 'Use dehumidifiers and improve ventilation.'
        },
        {
            'element': 'Temperature',
            'threshold_high': 30,
            'threshold_bad': 35,
            'danger_message': 'High temperatures can cause heat exhaustion and dehydration.',
            'solution_message': 'Stay hydrated and use cooling measures.'
        },
    ]

    for alert in risk_alerts:
        RiskAlert.objects.update_or_create(
            element=alert['element'],
            defaults={
                'threshold_high': alert['threshold_high'],
                'threshold_bad': alert['threshold_bad'],
                'danger_message': alert['danger_message'],
                'solution_message': alert['solution_message'],
            }
        )

    print("Risk alert loaded successfully!")