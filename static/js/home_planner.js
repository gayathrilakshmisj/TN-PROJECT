/**
 * Home Interior Planner Controller
 */

document.addEventListener("DOMContentLoaded", () => {
  const budgetInput = document.getElementById("home-budget");
  const budgetDisplay = document.getElementById("home-budget-display");
  const homeForm = document.getElementById("form-home");
  const submitBtn = document.getElementById("btn-submit-home");

  if (budgetInput && budgetDisplay) {
    budgetInput.addEventListener("input", (e) => {
      budgetDisplay.textContent = `$${parseInt(e.target.value).toLocaleString()}`;
    });
  }

  if (homeForm) {
    homeForm.addEventListener("submit", async (e) => {
      e.preventDefault();
      const formData = new FormData(homeForm);
      const payload = {
        room_type: formData.get("room_type"),
        style: formData.get("style"),
        dimensions: formData.get("dimensions"),
        budget: parseFloat(formData.get("budget")),
        extra_notes: formData.get("extra_notes")
      };

      window.AppUI.showLoading("Consulting Gemini 1.5 Interior Architect...", "Evaluating layout, light orientation, and IKEA / Amazon catalogs...");
      window.AppUI.setButtonLoading(submitBtn, true);

      try {
        const response = await fetch("/api/home/generate", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(payload)
        });

        const resData = await response.json();

        if (response.ok && resData.status === "success") {
          renderHomeResults(resData.data);
        } else {
          alert(`Error: ${resData.message || "Failed to generate interior plan."}`);
          window.AppUI.hideLoading();
        }
      } catch (err) {
        console.error("Home Planner Fetch Error:", err);
        alert("Network or server connection issue. Please check console.");
        window.AppUI.hideLoading();
      } finally {
        window.AppUI.setButtonLoading(submitBtn, false);
      }
    });
  }

  function renderHomeResults(data) {
    window.AppUI.renderBudgetHeader({
      badge: "Home Interior Proposal",
      title: `${data.style} ${data.room_type}`,
      summary: data.design_concept || `Curated design for ${data.room_type} (${data.dimensions || "standard space"}).`,
      budgetLimit: data.budget_limit,
      totalCost: data.total_estimated_cost
    });

    // Render Context Widget: Color Palette & Specs
    const contextGrid = document.getElementById("context-widget-grid");
    contextGrid.innerHTML = `
      <div class="meta-widget">
        <h4>🎨 Cohesive Color Palette</h4>
        <div class="palette-swatches">
          ${(data.color_palette || ["Warm Linen", "Slate Gray", "Oatmeal", "Soft Sage"])
            .map(color => `<span class="swatch-chip">${color}</span>`).join("")}
        </div>
      </div>
      <div class="meta-widget">
        <h4>📐 Spatial Parameters</h4>
        <p style="font-size: 0.95rem; color: #cbd5e1;">Dimensions: <strong>${data.dimensions || "Standard"}</strong></p>
        <p style="font-size: 0.85rem; color: #94a3b8; margin-top: 4px;">Optimized for natural daylight balance and clear walkways.</p>
      </div>
    `;

    // Render Recommendations
    window.AppUI.renderRecommendations(data.recommendations || []);

    // Render Styling Tips
    window.AppUI.renderChecklist("📐 Architect Styling & Spatial Tips", data.styling_tips || [
      "Position the largest seating unit facing either the focal wall or natural light window.",
      "Anchor the layout using a textured rug extending at least 6 inches beyond furniture legs.",
      "Keep lighting warm (2700K to 3000K) to enhance comfort and materials."
    ]);

    window.AppUI.showResults();
  }
});
