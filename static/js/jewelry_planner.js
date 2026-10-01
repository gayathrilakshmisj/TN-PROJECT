/**
 * Jewelry Planner Controller (Multimodal Outfit Image Analysis)
 */

document.addEventListener("DOMContentLoaded", () => {
  const budgetInput = document.getElementById("jewelry-budget");
  const budgetDisplay = document.getElementById("jewelry-budget-display");
  const jewelryForm = document.getElementById("form-jewelry");
  const submitBtn = document.getElementById("btn-submit-jewelry");

  // Dropzone Elements
  const dropzone = document.getElementById("outfit-dropzone");
  const fileInput = document.getElementById("outfit-image-input");
  const dropzonePrompt = document.getElementById("dropzone-prompt");
  const dropzonePreview = document.getElementById("dropzone-preview");
  const previewImg = document.getElementById("preview-img");
  const previewFilename = document.getElementById("preview-filename");
  const btnRemoveImage = document.getElementById("btn-remove-image");

  let selectedFile = null;

  if (budgetInput && budgetDisplay) {
    budgetInput.addEventListener("input", (e) => {
      budgetDisplay.textContent = `$${parseInt(e.target.value).toLocaleString()}`;
    });
  }

  // File Dropzone Event Listeners
  if (dropzone && fileInput) {
    dropzone.addEventListener("click", (e) => {
      if (e.target !== btnRemoveImage) {
        fileInput.click();
      }
    });

    fileInput.addEventListener("change", (e) => {
      if (e.target.files && e.target.files[0]) {
        handleFileSelection(e.target.files[0]);
      }
    });

    // Drag-and-drop support
    ["dragenter", "dragover"].forEach(eventName => {
      dropzone.addEventListener(eventName, (e) => {
        e.preventDefault();
        e.stopPropagation();
        dropzone.classList.add("drag-over");
      });
    });

    ["dragleave", "drop"].forEach(eventName => {
      dropzone.addEventListener(eventName, (e) => {
        e.preventDefault();
        e.stopPropagation();
        dropzone.classList.remove("drag-over");
      });
    });

    dropzone.addEventListener("drop", (e) => {
      if (e.dataTransfer.files && e.dataTransfer.files[0]) {
        const file = e.dataTransfer.files[0];
        if (file.type.startsWith("image/")) {
          fileInput.files = e.dataTransfer.files;
          handleFileSelection(file);
        } else {
          alert("Please upload a valid image file (PNG, JPG, or WEBP).");
        }
      }
    });

    btnRemoveImage.addEventListener("click", (e) => {
      e.stopPropagation();
      clearSelectedFile();
    });
  }

  function handleFileSelection(file) {
    selectedFile = file;
    previewFilename.textContent = file.name;
    const reader = new FileReader();
    reader.onload = (event) => {
      previewImg.src = event.target.result;
      dropzonePrompt.classList.add("hidden");
      dropzonePreview.classList.remove("hidden");
    };
    reader.readAsDataURL(file);
  }

  function clearSelectedFile() {
    selectedFile = null;
    fileInput.value = "";
    previewImg.src = "";
    dropzonePreview.classList.add("hidden");
    dropzonePrompt.classList.remove("hidden");
  }

  // Form Submission
  if (jewelryForm) {
    jewelryForm.addEventListener("submit", async (e) => {
      e.preventDefault();
      const formData = new FormData(jewelryForm);

      const hasFile = selectedFile !== null;
      window.AppUI.showLoading(
        hasFile ? "Analyzing Outfit Image with Gemini 1.5 Multimodal..." : "Consulting Gemini 1.5 Luxury Stylist...",
        hasFile ? "Detecting neckline cut, fabric sheen, color undertones, and curating matching gemstones..." : "Evaluating occasion, metal harmony, and curating collections..."
      );
      window.AppUI.setButtonLoading(submitBtn, true);

      try {
        const response = await fetch("/api/jewelry/generate", {
          method: "POST",
          body: formData
        });

        const resData = await response.json();

        if (response.ok && resData.status === "success") {
          renderJewelryResults(resData.data);
        } else {
          alert(`Error: ${resData.message || "Failed to generate jewelry plan."}`);
          window.AppUI.hideLoading();
        }
      } catch (err) {
        console.error("Jewelry Planner Fetch Error:", err);
        alert("Network or server connection issue. Please check console.");
        window.AppUI.hideLoading();
      } finally {
        window.AppUI.setButtonLoading(submitBtn, false);
      }
    });
  }

  function renderJewelryResults(data) {
    window.AppUI.renderBudgetHeader({
      badge: "Jewelry Styling Proposal",
      title: `${data.metal_preference || "Fine"} Jewelry Suite`,
      summary: data.outfit_analysis || `Curated for ${data.occasion} in ${data.metal_preference}.`,
      budgetLimit: data.budget_limit,
      totalCost: data.total_estimated_cost
    });

    // Render Context Widget: Outfit Visual Match Analysis + Metal Specification
    const contextGrid = document.getElementById("context-widget-grid");
    
    let outfitThumbnailHtml = "";
    if (data.uploaded_outfit_url) {
      outfitThumbnailHtml = `
        <div style="margin-top: 10px; display: flex; align-items: center; gap: 10px;">
          <img src="${data.uploaded_outfit_url}" alt="Uploaded Outfit" style="width: 55px; height: 55px; border-radius: 8px; object-fit: cover; border: 1px solid rgba(255,255,255,0.2);">
          <span style="font-size: 0.85rem; color: #a5b4fc;">Multimodal Outfit Image Processed</span>
        </div>
      `;
    }

    contextGrid.innerHTML = `
      <div class="meta-widget">
        <h4>✨ Metal & Gem Profile</h4>
        <p style="font-size: 1.35rem; font-weight: 800; color: #f59e0b;">${data.metal_preference || "Gold"}</p>
        <p style="font-size: 0.85rem; color: #94a3b8; margin-top: 4px;">Occasion: <strong>${data.occasion}</strong></p>
      </div>
      <div class="meta-widget">
        <h4>👗 Outfit Harmony & Silhouette</h4>
        <p style="font-size: 0.9rem; color: #cbd5e1; line-height: 1.5;">${data.outfit_analysis || "Balanced accessory selection designed to elevate your attire."}</p>
        ${outfitThumbnailHtml}
      </div>
    `;

    // Render Recommendations
    window.AppUI.renderRecommendations(data.recommendations || []);

    // Render Styling Tips
    window.AppUI.renderChecklist("💎 Haute Joaillerie Styling Rules", data.styling_tips || [
      "Select one statement anchor piece (either bold earrings or a statement necklace), keeping companion pieces minimal.",
      "Pair warm skin undertones with yellow gold and rich gems (ruby, emerald); cool undertones with white gold or diamonds.",
      "Ensure bracelet clasp finishes match ring settings for cohesive hand aesthetics."
    ]);

    window.AppUI.showResults();
  }
});
