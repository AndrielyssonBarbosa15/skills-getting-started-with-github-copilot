document.addEventListener("DOMContentLoaded", () => {
  const activitiesList = document.getElementById("activities-list");
  const activitySelect = document.getElementById("activity");
  const signupForm = document.getElementById("signup-form");
  const messageDiv = document.getElementById("message");

  function escapeHtml(value) {
    return value
      .replaceAll("&", "&amp;")
      .replaceAll("<", "&lt;")
      .replaceAll(">", "&gt;")
      .replaceAll('"', "&quot;")
      .replaceAll("'", "&#39;");
  }

  function showMessage(type, text) {
    messageDiv.textContent = text;
    messageDiv.className = type;
    messageDiv.classList.remove("hidden");

    setTimeout(() => {
      messageDiv.classList.add("hidden");
    }, 5000);
  }

  function renderParticipants(activityName, participants) {
    if (!participants.length) {
      return '<p class="empty-participants">No participants enrolled yet.</p>';
    }

    const encodedActivity = encodeURIComponent(activityName);
    const items = participants
      .map((participant) => {
        const safeParticipant = escapeHtml(participant);
        const encodedParticipant = encodeURIComponent(participant);

        return `
          <li class="participant-item">
            <span class="participant-email">${safeParticipant}</span>
            <button
              type="button"
              class="delete-participant-btn"
              data-activity="${encodedActivity}"
              data-email="${encodedParticipant}"
              aria-label="Remove participant ${safeParticipant}"
              title="Remove participant"
            >&times;</button>
          </li>
        `;
      })
      .join("");

    return `<ul class="participants-list">${items}</ul>`;
  }

  async function removeParticipant(activityName, email) {
    const response = await fetch(
      `/activities/${encodeURIComponent(activityName)}/participants?email=${encodeURIComponent(email)}`,
      {
        method: "DELETE",
      }
    );

    const result = await response.json();

    if (!response.ok) {
      throw new Error(result.detail || "Failed to remove participant");
    }

    return result;
  }

  // Function to fetch activities from API
  async function fetchActivities() {
    try {
      const response = await fetch("/activities");
      const activities = await response.json();

      // Clear loading message
      activitiesList.innerHTML = "";
      activitySelect.innerHTML = '<option value="">-- Select an activity --</option>';

      // Populate activities list
      Object.entries(activities).forEach(([name, details]) => {
        const activityCard = document.createElement("div");
        activityCard.className = "activity-card";

        const spotsLeft = details.max_participants - details.participants.length;

        activityCard.innerHTML = `
          <h4>${name}</h4>
          <p>${details.description}</p>
          <p><strong>Schedule:</strong> ${details.schedule}</p>
          <p><strong>Availability:</strong> ${spotsLeft} spots left</p>
          <div class="participants-section">
            <p class="participants-title"><strong>Participants</strong></p>
            ${renderParticipants(name, details.participants)}
          </div>
        `;

        activitiesList.appendChild(activityCard);

        // Add option to select dropdown
        const option = document.createElement("option");
        option.value = name;
        option.textContent = name;
        activitySelect.appendChild(option);
      });
    } catch (error) {
      activitiesList.innerHTML = "<p>Failed to load activities. Please try again later.</p>";
      console.error("Error fetching activities:", error);
    }
  }

  // Handle form submission
  signupForm.addEventListener("submit", async (event) => {
    event.preventDefault();

    const email = document.getElementById("email").value;
    const activity = document.getElementById("activity").value;

    try {
      const response = await fetch(
        `/activities/${encodeURIComponent(activity)}/signup?email=${encodeURIComponent(email)}`,
        {
          method: "POST",
        }
      );

      const result = await response.json();

      if (response.ok) {
        showMessage("success", result.message);
        signupForm.reset();
        fetchActivities();
      } else {
        showMessage("error", result.detail || "An error occurred");
      }
    } catch (error) {
      showMessage("error", "Failed to sign up. Please try again.");
      console.error("Error signing up:", error);
    }
  });

  activitiesList.addEventListener("click", async (event) => {
    const deleteButton = event.target.closest(".delete-participant-btn");
    if (!deleteButton) {
      return;
    }

    const activityName = decodeURIComponent(deleteButton.dataset.activity || "");
    const email = decodeURIComponent(deleteButton.dataset.email || "");

    if (!activityName || !email) {
      showMessage("error", "Unable to identify participant.");
      return;
    }

    try {
      const result = await removeParticipant(activityName, email);
      showMessage("success", result.message);
      fetchActivities();
    } catch (error) {
      showMessage("error", error.message || "Failed to remove participant.");
      console.error("Error removing participant:", error);
    }
  });

  // Initialize app
  fetchActivities();
});
