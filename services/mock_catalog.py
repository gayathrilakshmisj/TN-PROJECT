"""Mock Catalog and Simulated Scraping Engine for IKEA, Amazon, Zomato, and Jewelry Vendors.
Provides fallback data and simulated product retrieval when AI responses need supplementation.
"""

import random

# Curated High-Quality Unsplash Imagery
IMAGE_POOLS = {
    "furniture": [
        "https://images.unsplash.com/photo-1555041469-a586c61ea9bc?auto=format&fit=crop&w=600&q=80", # Sofa
        "https://images.unsplash.com/photo-1586023492125-27b2c045efd7?auto=format&fit=crop&w=600&q=80", # Modern chair
        "https://images.unsplash.com/photo-1533090161767-e6ffed986c88?auto=format&fit=crop&w=600&q=80", # Dining table
        "https://images.unsplash.com/photo-1505693416388-ac5ce068fe85?auto=format&fit=crop&w=600&q=80", # Bed
        "https://images.unsplash.com/photo-1518455027359-f3f8164ba6bd?auto=format&fit=crop&w=600&q=80", # Desk
        "https://images.unsplash.com/photo-1507473885765-e6ed057f782c?auto=format&fit=crop&w=600&q=80", # Lamp
    ],
    "party": [
        "https://images.unsplash.com/photo-1511795409834-ef04bbd61622?auto=format&fit=crop&w=600&q=80", # Party setup
        "https://images.unsplash.com/photo-1464349095431-e9a21285b5f3?auto=format&fit=crop&w=600&q=80", # Cake & treats
        "https://images.unsplash.com/photo-1530103862676-de8c9debad1d?auto=format&fit=crop&w=600&q=80", # Balloons
        "https://images.unsplash.com/photo-1555244162-803834f70033?auto=format&fit=crop&w=600&q=80", # Catering buffet
    ],
    "jewelry": [
        "https://images.unsplash.com/photo-1599643478518-a784e5dc4c8f?auto=format&fit=crop&w=600&q=80", # Necklace
        "https://images.unsplash.com/photo-1605100804763-247f67b3557e?auto=format&fit=crop&w=600&q=80", # Rings
        "https://images.unsplash.com/photo-1630019852942-f89202989a59?auto=format&fit=crop&w=600&q=80", # Earrings
        "https://images.unsplash.com/photo-1611591475152-473523dd665e?auto=format&fit=crop&w=600&q=80", # Bracelet
    ]
}

def get_fallback_home_plan(room_type: str, style: str, budget: float, dimensions: str = "") -> dict:
    """Generate a realistic structured Home Interior Plan within the given budget."""
    budget = max(budget, 100.0)
    
    # Define budget allocation proportions
    allocations = [
        {"item": f"{style.capitalize()} Statement Sofa / Bed Unit", "pct": 0.40, "vendor": "IKEA", "img": IMAGE_POOLS["furniture"][0]},
        {"item": "Modular Storage / Side Console", "pct": 0.20, "vendor": "IKEA", "img": IMAGE_POOLS["furniture"][1]},
        {"item": "Accent Ergonomic Table / Desk", "pct": 0.15, "vendor": "Amazon Home", "img": IMAGE_POOLS["furniture"][2]},
        {"item": "Ambient LED Floor Lamp & Sconces", "pct": 0.10, "vendor": "Amazon Home", "img": IMAGE_POOLS["furniture"][5]},
        {"item": "Textured Area Rug & Cushions", "pct": 0.15, "vendor": "Urban Ladder", "img": IMAGE_POOLS["furniture"][3]}
    ]
    
    items = []
    total_estimated = 0.0
    
    for alloc in allocations:
        cost = round(budget * alloc["pct"], 2)
        total_estimated += cost
        items.append({
            "name": alloc["item"],
            "vendor": alloc["vendor"],
            "price": cost,
            "category": "Furniture & Decor",
            "description": f"Optimized for {room_type.lower()} with {style.lower()} aesthetics and space efficiency.",
            "image_url": alloc["img"],
            "product_url": f"https://www.{alloc['vendor'].lower().replace(' ', '')}.com/search?q={alloc['item'].replace(' ', '+')}"
        })
        
    return {
        "planner_type": "Home Interior Planner",
        "room_type": room_type,
        "style": style,
        "dimensions": dimensions or "Standard Room Dimensions",
        "budget_limit": budget,
        "total_estimated_cost": round(total_estimated, 2),
        "currency": "USD",
        "design_concept": f"A refined {style} design maximizing light, comfort, and functionality in your {room_type}.",
        "color_palette": ["Warm Neutral", "Earthy Charcoal", "Champagne Gold", "Muted Sage"],
        "recommendations": items,
        "styling_tips": [
            "Maintain at least 3 feet of clear walking pathway between major pieces.",
            "Layer ambient warm lighting (2700K-3000K) to create an inviting atmosphere.",
            "Use vertical wall shelving to preserve usable floor space."
        ],
        "is_fallback": True
    }


def get_fallback_party_plan(event_type: str, guest_count: int, budget: float, theme: str = "") -> dict:
    """Generate a realistic structured Party Plan within the given budget."""
    budget = max(budget, 50.0)
    guest_count = max(guest_count, 1)
    per_head = round(budget / guest_count, 2)
    theme = theme or "Celebration Chic"
    
    allocations = [
        {"item": "Catering & Gourmet Platters", "pct": 0.45, "vendor": "Zomato Catering", "img": IMAGE_POOLS["party"][3]},
        {"item": "Artisan Tier Cake & Dessert Bar", "pct": 0.20, "vendor": "Local Bakery / Swiggy", "img": IMAGE_POOLS["party"][1]},
        {"item": "Theme Balloon Arch & Backdrop", "pct": 0.15, "vendor": "Amazon Party Store", "img": IMAGE_POOLS["party"][2]},
        {"item": "Party Tableware & Eco Drinkware", "pct": 0.10, "vendor": "Amazon Party Store", "img": IMAGE_POOLS["party"][0]},
        {"item": "Curated Playlist & Ambient Lighting", "pct": 0.10, "vendor": "Amazon Basics", "img": IMAGE_POOLS["party"][0]}
    ]
    
    items = []
    total_estimated = 0.0
    for alloc in allocations:
        cost = round(budget * alloc["pct"], 2)
        total_estimated += cost
        items.append({
            "name": alloc["item"],
            "vendor": alloc["vendor"],
            "price": cost,
            "category": "Event Essential",
            "description": f"Tailored for {guest_count} guests with {theme} theme.",
            "image_url": alloc["img"],
            "product_url": f"https://www.{alloc['vendor'].split()[0].lower()}.com"
        })
        
    return {
        "planner_type": "Party Planner",
        "event_type": event_type,
        "theme": theme,
        "guest_count": guest_count,
        "budget_limit": budget,
        "per_person_cost": per_head,
        "total_estimated_cost": round(total_estimated, 2),
        "currency": "USD",
        "event_timeline": [
            {"time": "00:00", "activity": "Guest Arrival, Welcome Mocktails & Music"},
            {"time": "01:00", "activity": "Appetizers & Social Mingling / Photo Session"},
            {"time": "02:00", "activity": "Main Course Dining & Cake Cutting Celebration"},
            {"time": "03:00", "activity": "Fun Games / Dance Session & Dessert"}
        ],
        "recommendations": items,
        "host_checklist": [
            "Confirm head count 48 hours prior to final catering placement.",
            "Prep ice buckets, chillers, and accessible trash/recycling stations.",
            "Have an emergency cleaning kit handy for beverage spills."
        ],
        "is_fallback": True
    }


def get_fallback_jewelry_plan(occasion: str, budget: float, metal_preference: str = "Gold", outfit_description: str = "") -> dict:
    """Generate a realistic structured Jewelry Recommendation within budget."""
    budget = max(budget, 50.0)
    metal = metal_preference or "Yellow Gold"
    outfit_info = outfit_description or "Elegant Evening Attire"
    
    allocations = [
        {"name": f"Delicate {metal} Pendant Necklace", "pct": 0.40, "vendor": "CaratLane", "img": IMAGE_POOLS["jewelry"][0], "type": "Neckpiece"},
        {"name": f"Sparkling {metal} Stud / Huggie Earrings", "pct": 0.30, "vendor": "Tanishq", "img": IMAGE_POOLS["jewelry"][2], "type": "Earrings"},
        {"name": f"Minimalist Stackable {metal} Ring", "pct": 0.15, "vendor": "Swarovski", "img": IMAGE_POOLS["jewelry"][1], "type": "Rings"},
        {"name": f"Sleek Tennis / Cuff Bracelet", "pct": 0.15, "vendor": "Amazon Luxury", "img": IMAGE_POOLS["jewelry"][3], "type": "Bracelet"}
    ]
    
    items = []
    total_estimated = 0.0
    for alloc in allocations:
        cost = round(budget * alloc["pct"], 2)
        total_estimated += cost
        items.append({
            "name": alloc["name"],
            "type": alloc["type"],
            "vendor": alloc["vendor"],
            "price": cost,
            "metal": metal,
            "description": f"Carefully paired to complement {outfit_info} for a {occasion}.",
            "image_url": alloc["img"],
            "product_url": f"https://www.{alloc['vendor'].lower().replace(' ', '')}.com/search"
        })
        
    return {
        "planner_type": "Jewelry Planner",
        "occasion": occasion,
        "metal_preference": metal,
        "outfit_analysis": f"The ensemble ({outfit_info}) creates a stunning focal point. Pairing with balanced {metal} pieces enhances neckline elegance without competing with fabrics.",
        "budget_limit": budget,
        "total_estimated_cost": round(total_estimated, 2),
        "currency": "USD",
        "recommendations": items,
        "styling_tips": [
            "If the outfit has an ornate neckline, focus on statement earrings and keep the necklace subtle.",
            "Match warm outfit undertones (crimson, emerald, gold) with yellow gold; cool undertones with white gold or silver.",
            "Keep ring and bracelet metals unified for cohesive hand styling."
        ],
        "is_fallback": True
    }
