/**
 * AI Multi-Planner Main Application Coordinator & UI Utilities
 */

// Global UI Helper Module
window.AppUI = {
  showLoading: (title, step) => {
    const resultsArea = document.getElementById("results-area");
    const loadingState = document.getElementById("loading-state");
    const resultsContent = document.getElementById("results-content");
    const loadingTitle = document.getElementById("loading-title");
    const loadingStep = document.getElementById("loading-step");

    if (loadingTitle && title) loadingTitle.textContent = title;
    if (loadingStep && step) loadingStep.textContent = step;

    resultsArea.classList.remove("hidden");
    loadingState.classList.remove("hidden");
    resultsContent.classList.add("hidden");

    // Smooth scroll down to loading container
    resultsArea.scrollIntoView({ behavior: "smooth", block: "start" });
  },

  hideLoading: () => {
    const loadingState = document.getElementById("loading-state");
    if (loadingState) loadingState.classList.add("hidden");
  },

  showResults: () => {
    const loadingState = document.getElementById("loading-state");
    const resultsContent = document.getElementById("results-content");
    if (loadingState) loadingState.classList.add("hidden");
    if (resultsContent) {
      resultsContent.classList.remove("hidden");
      resultsContent.scrollIntoView({ behavior: "smooth", block: "start" });
    }
  },

  setButtonLoading: (btn, isLoading) => {
    if (!btn) return;
    const textSpan = btn.querySelector(".btn-text");
    const spinner = btn.querySelector(".btn-spinner");

    btn.disabled = isLoading;
    if (isLoading) {
      if (spinner) spinner.classList.remove("hidden");
    } else {
      if (spinner) spinner.classList.add("hidden");
    }
  },

  renderBudgetHeader: ({ badge, title, summary, budgetLimit, totalCost }) => {
    const badgeEl = document.getElementById("result-badge-type");
    const titleEl = document.getElementById("result-title");
    const summaryEl = document.getElementById("result-summary");
    const limitEl = document.getElementById("result-budget-limit");
    const totalEl = document.getElementById("result-total-cost");
    const savingsEl = document.getElementById("result-savings");

    if (badgeEl) badgeEl.textContent = badge;
    if (titleEl) titleEl.textContent = title;
    if (summaryEl) summaryEl.textContent = summary;

    const limit = parseFloat(budgetLimit) || 0;
    const total = parseFloat(totalCost) || 0;
    const variance = limit - total;

    if (limitEl) limitEl.textContent = `$${limit.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`;
    if (totalEl) totalEl.textContent = `$${total.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`;
    
    if (savingsEl) {
      if (variance >= 0) {
        savingsEl.textContent = `+$${variance.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 })} under`;
        savingsEl.className = "stat-val positive";
      } else {
        savingsEl.textContent = `-$${Math.abs(variance).toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 })} over`;
        savingsEl.className = "stat-val";
      }
    }
  },

  renderRecommendations: (items) => {
    const grid = document.getElementById("recommendations-grid");
    const countEl = document.getElementById("recommendation-count");
    if (countEl) countEl.textContent = items.length;

    if (!grid) return;
    grid.innerHTML = "";

    if (!items || items.length === 0) {
      grid.innerHTML = "<p style='color: #94a3b8; grid-column: 1 / -1;'>No specific items returned. Please refine your inputs.</p>";
      return;
    }

    items.forEach(item => {
      const card = document.createElement("article");
      card.className = "product-card";

      const imgSrc = item.image_url || "https://images.unsplash.com/photo-1555041469-a586c61ea9bc?auto=format&fit=crop&w=600&q=80";
      const vendor = item.vendor || "Retailer";
      const category = item.category || item.type || "Catalog Item";
      const price = parseFloat(item.price) || 0.0;
      const productUrl = item.product_url || `https://www.google.com/search?q=${encodeURIComponent(item.name + " " + vendor)}`;

      card.innerHTML = `
        <div class="card-img-wrap">
          <img src="${imgSrc}" alt="${item.name}" loading="lazy" onerror="this.src='https://images.unsplash.com/photo-1555041469-a586c61ea9bc?auto=format&fit=crop&w=600&q=80'">
          <span class="vendor-pill">${vendor}</span>
          <span class="category-pill">${category}</span>
        </div>
        <div class="card-body">
          <div class="card-price-row">
            <span class="card-price">$${price.toFixed(2)}</span>
          </div>
          <h4 class="card-name">${item.name}</h4>
          <p class="card-desc">${item.description || "Curated recommendation adhering to aesthetic style and strict budget limit."}</p>
          <a href="${productUrl}" target="_blank" rel="noopener noreferrer" class="card-action-btn">
            View on ${vendor} ↗
          </a>
        </div>
      `;
      grid.appendChild(card);
    });
  },

  renderChecklist: (title, checklistItems) => {
    const container = document.getElementById("tips-container");
    const titleEl = document.getElementById("tips-title");
    const listEl = document.getElementById("tips-list");

    if (titleEl) titleEl.textContent = title;
    if (listEl) {
      listEl.innerHTML = "";
      (checklistItems || []).forEach(tip => {
        const li = document.createElement("li");
        li.textContent = tip;
        listEl.appendChild(li);
      });
    }
  }
};

// Document Init
document.addEventListener("DOMContentLoaded", () => {
  // Tab Switching Logic
  const tabs = document.querySelectorAll(".tab-btn");
  const sections = document.querySelectorAll(".planner-section");

  tabs.forEach(tab => {
    tab.addEventListener("click", () => {
      tabs.forEach(t => {
        t.classList.remove("active");
        t.setAttribute("aria-selected", "false");
      });
      sections.forEach(s => s.classList.remove("active"));

      tab.classList.add("active");
      tab.setAttribute("aria-selected", "true");

      const targetId = tab.getAttribute("aria-controls");
      const targetSection = document.getElementById(targetId);
      if (targetSection) {
        targetSection.classList.add("active");
      }
    });
  });

  // Action Buttons
  const btnPrint = document.getElementById("btn-print-plan");
  if (btnPrint) {
    btnPrint.addEventListener("click", () => {
      window.print();
    });
  }

  const btnScrollTop = document.getElementById("btn-scroll-top");
  if (btnScrollTop) {
    btnScrollTop.addEventListener("click", () => {
      window.scrollTo({ top: 0, behavior: "smooth" });
    });
  }

  // Health Status Checker
  checkApiHealth();
});

async function checkApiHealth() {
  const statusBadge = document.getElementById("system-status-badge");
  const indicator = statusBadge?.querySelector(".status-indicator");
  const statusText = document.getElementById("status-text");

  try {
    const res = await fetch("/api/health");
    if (res.ok) {
      const data = await res.json();
      if (data.gemini_configured) {
        indicator?.classList.add("connected");
        if (statusText) statusText.textContent = `Gemini Active (${data.model})`;
      } else {
        indicator?.classList.add("connected");
        if (statusText) statusText.textContent = "AI Fallback / Mock Engine Ready";
      }
    }
  } catch (e) {
    if (statusText) statusText.textContent = "Offline Mode";
  }
}
