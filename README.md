# AI Multi-Planner Studio (Home, Party & Jewelry)

A full-stack intelligent curation platform built with **Flask**, **Google Gemini 1.5 Multimodal API**, and a modern web frontend.

---

## 🌟 Features Across the 5 Epics

### 🛋️ 1. Home Interior Planner
- **Intelligent Spatial Curation**: Recommends coordinated furniture and decor according to room dimensions, style (Minimalist, Japandi, Bohemian, etc.), and functional needs.
- **Budget Hard Limit**: Strictly caps total estimated spending within the user's budget ceiling.
- **Retailer Allocation**: Realistic pricing and direct links for **IKEA**, **Amazon Home**, and **Urban Ladder**.
- **Cohesive Color Swatches & Styling Tips**: Generates color harmony palettes and layout advice.

### 🎉 2. Party & Event Planner
- **Guest-Scaled Planning**: Calculates catering and supply requirements tailored to headcount (4 to 150+ guests).
- **Per-Head Viability**: Automatically computes budget per person and itemizes catering (**Zomato / Swiggy**), decor (**Amazon Party**), and desserts.
- **Itinerary Timeline & Host Checklist**: Produces a structured event timeline and pre-event checklist.

### 💎 3. Jewelry & Outfit Stylist (Multimodal)
- **Multimodal Visual Analysis**: Accepts drag-and-drop outfit image uploads (PNG, JPG, WEBP up to 16MB) or text descriptions.
- **Silhouette & Color Harmonization**: Gemini 1.5 inspects neckline cuts, fabric sheens, and colors to curate matching jewelry suites (necklaces, earrings, rings, cuffs).
- **Luxury Vendors**: Recommendations from **Tanishq**, **CaratLane**, **Swarovski**, and **Tiffany**.

### 🛡️ 4. Fallback & Mock Catalog Resilience
- When `GEMINI_API_KEY` is not provided or during offline demos, the backend seamlessly falls back to a simulated scraping and vendor catalog engine (`services/mock_catalog.py`).

---

## 📂 Project Structure

```text
VAN/
├── app.py                      # Flask application factory and server entrypoint
├── config.py                   # Application and upload configurations
├── requirements.txt            # Python dependencies
├── .env.example                # Environment variables template
├── .env                        # Local configuration
├── services/
│   ├── __init__.py
│   ├── gemini_client.py        # Gemini 1.5 client, multimodal handler & budget validator
│   ├── prompt_templates.py     # Prompt engineering & strict JSON schemas
│   └── mock_catalog.py         # Mock retailer integration (IKEA, Amazon, Zomato, etc.)
├── routes/
│   ├── __init__.py             # Modular blueprint setup
│   ├── home_routes.py          # /api/home/generate & /generate-home
│   ├── party_routes.py         # /api/party/generate & /generate-party
│   └── jewelry_routes.py       # /api/jewelry/generate & /generate-jewelry (file upload)
├── static/
│   ├── css/
│   │   └── style.css           # Glassmorphism design system & responsive styling
│   ├── js/
│   │   ├── app.js              # Application coordinator, tabs, and shared UI helpers
│   │   ├── home_planner.js     # Home planner controller
│   │   ├── party_planner.js    # Party planner controller
│   │   └── jewelry_planner.js  # Jewelry planner & multimodal dropzone controller
│   └── uploads/                # Ephemeral local storage for outfit image uploads
├── templates/
│   └── index.html              # Unified interactive interface
└── tests/
    └── test_planners.py        # Unit and integration test suite
```

---

## 🚀 Quickstart Guide

### 1. Install Dependencies
```bash
python -m pip install -r requirements.txt
```

### 2. Configure Your Gemini API Key
Edit `.env` (or copy `.env.example`):
```ini
GEMINI_API_KEY=your_gemini_api_key_here
GEMINI_MODEL=gemini-1.5-flash
```
> *Note: If no API key is specified, the application automatically runs in fallback catalog mode.*

### 3. Run the Application
```bash
python app.py
```
Open your browser and navigate to:
👉 **[http://127.0.0.1:5000](http://127.0.0.1:5000)**

---

## 🧪 Running Tests
Execute the automated test suite:
```bash
python -m unittest tests/test_planners.py
```

---

## 📡 API Endpoints

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/api/health` | Health status and Gemini readiness |
| `POST` | `/api/home/generate` (or `/generate-home`) | Interior design proposal and furniture recommendations |
| `POST` | `/api/party/generate` (or `/generate-party`) | Event itinerary, catering, and budget breakdown |
| `POST` | `/api/jewelry/generate` (or `/generate-jewelry`) | Multimodal jewelry matching (accepts `outfit_image`) |
