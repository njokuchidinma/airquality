from API.models import HealthTip
from datetime import datetime


def load_health_tips():
    health_tips = [
        ("Proper Ventilation", "Ensure adequate ventilation in your living space by opening windows and using exhaust fans. Good airflow helps to reduce indoor air pollutants and maintain a healthy environment."),
        ("Air Purifiers", "Consider using air purifiers to remove pollutants from indoor air, especially if you have allergies or respiratory conditions."),
        ("Regular Cleaning", "Regularly clean your living space to reduce dust, mold, and other allergens. Use a vacuum with a HEPA filter for best results."),
        ("Houseplants", "Certain houseplants can improve indoor air quality by absorbing toxins and releasing oxygen. Examples include spider plants and peace lilies."),
        ("Avoid Smoking Indoors", "Do not smoke indoors, as it significantly deteriorates indoor air quality and poses health risks to everyone in the space."),
        ("Monitor Indoor Air Quality", "Use air quality monitors to keep track of pollutants in your home. Being aware of the air quality can help you take necessary precautions."),
        ("Limit Use of Aerosols and VOCs", "Reduce the use of aerosol sprays and products containing volatile organic compounds (VOCs) like paints and cleaners. Opt for natural or low-VOC products."),
        ("Keep Humidity Levels in Check", "Maintain indoor humidity levels between 30% and 50% to prevent mold growth and dust mites. Use dehumidifiers if necessary."),
        ("Regular HVAC Maintenance", "Schedule regular maintenance for your heating, ventilation, and air conditioning (HVAC) systems to ensure they function efficiently and filter out pollutants."),
        ("Use Non-Toxic Cleaning Products", "Choose non-toxic cleaning products that do not emit harmful fumes. Homemade cleaning solutions with vinegar and baking soda can be effective alternatives."),
        ("Remove Carpets and Rugs", "If possible, remove carpets and rugs that can trap dust and allergens. Consider using hard flooring options like tile or hardwood for easier cleaning."),
        ("Properly Store Chemicals", "Store household chemicals and paints in well-ventilated areas and out of reach of children. Always follow manufacturer guidelines for storage."),
        ("Ventilate During Cooking", "Use exhaust fans while cooking to help remove smoke, odors, and moisture from the kitchen, which can contribute to indoor air pollution."),
        ("Avoid Using Scented Candles", "Be cautious with scented candles and incense, as they can release harmful chemicals into the air. Opt for natural alternatives, such as essential oil diffusers."),
        ("Limit Dust Accumulation", "Dust surfaces regularly and use microfiber cloths to trap dust effectively. Pay attention to areas where dust tends to accumulate, such as vents and electronics."),
        ("Keep Windows Clean", "Regularly clean windows and screens to prevent dust and pollen buildup. Clean windows allow more natural light and fresh air into your home."),
        ("Designate a No-Shoes Policy", "Implement a no-shoes policy indoors to minimize the amount of dirt, allergens, and pollutants tracked into your home."),
        ("Use Air-Filtering Plants", "In addition to houseplants, consider using air-filtering plants like snake plants and pothos that can help purify the air naturally."),
        ("Install Smoke and Carbon Monoxide Detectors", "Ensure you have working smoke and carbon monoxide detectors installed in your home. Regularly check and replace batteries to ensure functionality."),
        ("Educate Family Members", "Educate all household members about the importance of indoor air quality and encourage them to adopt habits that contribute to a healthier environment."),
        ("Seal Windows and Doors", "Ensure that windows and doors are properly sealed to prevent outdoor pollutants from entering your home. Use weather stripping or caulk to fix gaps."),
        ("Limit Electronic Device Emissions", "Keep electronic devices away from sleeping areas to reduce exposure to electromagnetic fields (EMFs). Turn off devices when not in use."),
        ("Maintain Clean Air Ducts", "Schedule regular cleaning of air ducts in your home to reduce dust and allergens circulating in the air. This helps improve overall air quality."),
        ("Use Humidifiers Wisely", "In dry environments, use humidifiers to maintain adequate moisture levels, but ensure they are cleaned regularly to prevent mold growth."),
        ("Install an Exhaust Fan in the Bathroom", "Use exhaust fans in bathrooms to help reduce humidity and prevent mold growth after showers or baths."),
        ("Limit Use of Air Fresheners", "Avoid using chemical air fresheners that can emit harmful substances. Instead, use natural scents like essential oils or fresh flowers."),
        ("Choose Low-Emitting Furniture", "When purchasing furniture, look for items made from low-emitting materials, which release fewer pollutants into the air."),
        ("Opt for Natural Fabrics", "Choose curtains, bedding, and upholstery made from natural fibers such as cotton or linen to reduce exposure to harmful chemicals."),
        ("Keep Pets Clean", "Regularly bathe and groom pets to minimize dander and allergens in your home. Consider using air purifiers to help reduce pet allergens."),
        ("Practice Safe Cooking Techniques", "Use ventilation hoods while cooking to remove smoke and odors, and avoid using non-stick pans that can release harmful fumes at high temperatures."),
        ("Limit Candle Use", "If using candles, choose those made from natural materials like soy or beeswax and avoid paraffin candles, which can release toxins."),
        ("Wash Bedding Weekly", "Wash bed linens, pillowcases, and blankets weekly in hot water to eliminate dust mites, allergens, and bacteria."),
        ("Keep Indoor Plants Dust-Free", "Regularly wipe down the leaves of indoor plants to prevent dust accumulation, which can hinder their air-purifying abilities."),
        ("Educate Yourself on Air Quality", "Stay informed about local air quality levels and take precautions during high pollution days, such as limiting outdoor activities."),
        ("Create a Clean Zone", "Designate areas in your home, such as a no-food zone, to reduce crumbs and attractants for pests that can affect indoor air quality."),
        ("Implement a Cleaning Schedule", "Create and follow a regular cleaning schedule to ensure that dust, dirt, and allergens are kept under control throughout your home."),
        ("Utilize Natural Pest Control", "Use natural methods for pest control, such as essential oils and traps, to avoid chemicals that can harm indoor air quality."),
        ("Avoid Excessive Use of Technology", "Limit screen time for devices and take regular breaks to improve mental health and reduce exposure to blue light."),
        ("Promote Outdoor Activities", "Encourage outdoor activities to enhance overall well-being. Fresh air and physical activity contribute positively to mental health."),
    ]

    for title, description in health_tips:
        HealthTip.objects.get_or_create(title=title, description=description, timestamp=datetime.now())

    print("Health tips loaded successfully!")