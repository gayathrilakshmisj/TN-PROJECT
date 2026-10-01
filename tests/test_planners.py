"""Unit and Integration Test Suite for AI Multi-Planner Suite (Epics 1-5).
Tests endpoints, budget adherence, multimodal upload handling, and edge cases.
"""

import io
import unittest
from PIL import Image
from app import create_app

class TestMultiPlannerSuite(unittest.TestCase):
    """Test cases for Flask API routes, validation, and planner responses."""

    def setUp(self):
        self.app = create_app()
        self.app.config["TESTING"] = True
        self.client = self.app.test_client()

    def test_health_check(self):
        """Verify API health endpoint responds with 200 and proper metadata."""
        response = self.client.get("/api/health")
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data.get("status"), "healthy")
        self.assertIn("gemini_configured", data)
        self.assertIn("fallback_enabled", data)

    def test_home_planner_valid(self):
        """Test /api/home/generate with valid parameters and strict budget enforcement."""
        payload = {
            "room_type": "Living Room",
            "style": "Scandinavian & Cozy",
            "dimensions": "16ft x 14ft",
            "budget": 1200.0,
            "extra_notes": "Needs pet-friendly couch"
        }
        response = self.client.post("/api/home/generate", json=payload)
        self.assertEqual(response.status_code, 200)
        res = response.get_json()
        self.assertEqual(res.get("status"), "success")
        data = res.get("data")
        self.assertIn("recommendations", data)
        self.assertGreater(len(data["recommendations"]), 0)
        # Verify budget adherence
        self.assertLessEqual(data["total_estimated_cost"], payload["budget"])
        # Verify vendor assignments
        vendors = [item.get("vendor") for item in data["recommendations"]]
        self.assertTrue(any("IKEA" in v or "Amazon" in v for v in vendors))

    def test_home_planner_invalid_budget(self):
        """Test home planner edge cases: negative budget or zero."""
        response = self.client.post("/api/home/generate", json={"budget": -100})
        self.assertEqual(response.status_code, 400)
        response_zero = self.client.post("/api/home/generate", json={"budget": 0})
        self.assertEqual(response_zero.status_code, 400)

    def test_party_planner_valid(self):
        """Test /api/party/generate with valid guest count and budget."""
        payload = {
            "event_type": "Birthday Celebration",
            "guest_count": 30,
            "budget": 900.0,
            "theme": "Retro Disco"
        }
        response = self.client.post("/api/party/generate", json=payload)
        self.assertEqual(response.status_code, 200)
        res = response.get_json()
        self.assertEqual(res.get("status"), "success")
        data = res.get("data")
        self.assertIn("recommendations", data)
        self.assertIn("event_timeline", data)
        self.assertLessEqual(data["total_estimated_cost"], payload["budget"])
        # Verify per person viability
        self.assertIn("per_person_cost", data)
        self.assertGreater(data["per_person_cost"], 0)

    def test_party_planner_invalid_guests(self):
        """Test party planner edge case: 0 guests or negative guest count."""
        response = self.client.post("/api/party/generate", json={"guest_count": 0, "budget": 500})
        self.assertEqual(response.status_code, 400)

    def test_jewelry_planner_text_only(self):
        """Test /api/jewelry/generate without outfit image."""
        payload = {
            "occasion": "Cocktail Evening",
            "metal_preference": "Rose Gold",
            "budget": 500.0,
            "outfit_description": "Navy blue evening silk gown"
        }
        response = self.client.post("/api/jewelry/generate", json=payload)
        self.assertEqual(response.status_code, 200)
        res = response.get_json()
        self.assertEqual(res.get("status"), "success")
        data = res.get("data")
        self.assertIn("recommendations", data)
        self.assertLessEqual(data["total_estimated_cost"], payload["budget"])

    def test_jewelry_planner_multimodal_image_upload(self):
        """Test /api/jewelry/generate with an uploaded outfit image buffer."""
        # Generate an in-memory sample JPEG image
        img_buffer = io.BytesIO()
        test_img = Image.new("RGB", (200, 200), color=(180, 50, 75))
        test_img.save(img_buffer, format="JPEG")
        img_buffer.seek(0)

        data = {
            "occasion": "Wedding Reception",
            "metal_preference": "Yellow Gold",
            "budget": "750",
            "outfit_image": (img_buffer, "outfit_sample.jpg")
        }

        response = self.client.post(
            "/api/jewelry/generate",
            data=data,
            content_type="multipart/form-data"
        )
        self.assertEqual(response.status_code, 200)
        res = response.get_json()
        self.assertEqual(res.get("status"), "success")
        plan = res.get("data")
        self.assertIn("uploaded_outfit_url", plan)
        self.assertTrue(plan["uploaded_outfit_url"].startswith("/static/uploads/"))
        self.assertLessEqual(plan["total_estimated_cost"], 750.0)

    def test_alias_routes_compatibility(self):
        """Verify Epic 3 Story 1 routes (/generate-home, /generate-party, /generate-jewelry)."""
        r1 = self.client.post("/generate-home", json={"room_type": "Office", "budget": 600})
        self.assertEqual(r1.status_code, 200)

        r2 = self.client.post("/generate-party", json={"event_type": "Dinner", "guest_count": 10, "budget": 300})
        self.assertEqual(r2.status_code, 200)

        r3 = self.client.post("/generate-jewelry", json={"occasion": "Gala", "budget": 450})
        self.assertEqual(r3.status_code, 200)

if __name__ == "__main__":
    unittest.main()
