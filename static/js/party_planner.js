/**
 * Party & Event Planner Controller
 */

document.addEventListener("DOMContentLoaded", () => {
  const guestInput = document.getElementById("party-guests");
  const guestDisplay = document.getElementById("party-guests-display");
  const budgetInput = document.getElementById("party-budget");
  const budgetDisplay = document.getElementById("party-budget-display");
  const partyForm = document.getElementById("form-party");
  const submitBtn = document.getElementById("btn-submit-party");

  if (guestInput && guestDisplay) {
    guestInput.addEventListener("input", (e) => {
      guestDisplay.textContent = `${e.target.value} Guests`;
    });
  }

  if (budgetInput && budgetDisplay) {
    budgetInput.addEventListener("input", (e) => {
      budgetDisplay.textContent = `$${parseInt(e.target.value).toLocaleString()}`;
    });
  }

  if (partyForm) {
    partyForm.addEventListener("submit", async (e) => {
      e.preventDefault();
      const formData = new FormData(partyForm);
      const payload = {
        event_type: formData.get("event_type"),
        theme: formData.get("theme"),
        guest_count: parseInt(formData.get("guest_count")),
        budget: parseFloat(formData.get("budget")),
        dietary_notes: formData.get("dietary_notes")
      };

      window.AppUI.showLoading("Consulting Gemini 1.5 Event Planner...", "Simulating catering quotes from Zomato and party decor from Amazon...");
      window.AppUI.setButtonLoading(submitBtn, true);

      try {
        const response = await fetch("/api/party/generate", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(payload)
        });

        const resData = await response.json();

        if (response.ok && resData.status === "success") {
          renderPartyResults(resData.data);
        } else {
          alert(`Error: ${resData.message || "Failed to generate event plan."}`);
          window.AppUI.hideLoading();
        }
      } catch (err) {
        console.error("Party Planner Fetch Error:", err);
        alert("Network or server connection issue. Please check console.");
        window.AppUI.hideLoading();
      } finally {
        window.AppUI.setButtonLoading(submitBtn, false);
      }
    });
  }

  function renderPartyResults(data) {
    window.AppUI.renderBudgetHeader({
      badge: "Event & Party Blueprint",
      title: `${data.theme || "Signature"} ${data.event_type}`,
      summary: `Tailored celebration for ${data.guest_count} guests with curated catering, decor, and scheduled itinerary.`,
      budgetLimit: data.budget_limit,
      totalCost: data.total_estimated_cost
    });

    // Render Context Widget: Per-Guest Cost + Event Timeline
    const contextGrid = document.getElementById("context-widget-grid");
    const timelineHtml = (data.event_timeline || [])
      .map(item => `
        <div class="timeline-step">
          <span class="timeline-time">${item.time}</span>
          <span class="timeline-activity">${item.activity}</span>
        </div>
      `).join("");

    contextGrid.innerHTML = `
      <div class="meta-widget">
        <h4>👥 Guest Economics</h4>
        <p style="font-size: 1.4rem; font-weight: 800; color: #38bdf8;">$${data.per_person_cost ? data.per_person_cost.toFixed(2) : (data.total_estimated_cost / data.guest_count).toFixed(2)} <span style="font-size: 0.85rem; color: #94a3b8; font-weight: 500;">/ guest</span></p>
        <p style="font-size: 0.85rem; color: #94a3b8; margin-top: 4px;">Optimized for ${data.guest_count} attendees with balanced food and drink allotments.</p>
      </div>
      <div class="meta-widget">
        <h4>⏱️ Event Schedule Timeline</h4>
        <div class="timeline-container">
          ${timelineHtml || "<p style='color:#94a3b8;'>Custom schedule included in recommendations.</p>"}
        </div>
      </div>
    `;

    // Render Recommendations
    window.AppUI.renderRecommendations(data.recommendations || []);

    // Render Host Checklist
    window.AppUI.renderChecklist("📋 Host Execution Checklist", data.host_checklist || [
      "Send digital invitations and collect RSVPs 10 days in advance.",
      "Confirm bulk catering order delivery window 24 hours prior.",
      "Chill beverages 4 hours before guest arrival time.",
      "Designate an easily accessible coat and gift check zone."
    ]);

    window.AppUI.showResults();
  }
});
