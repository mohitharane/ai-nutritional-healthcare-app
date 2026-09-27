// Allow only letters and spaces in the name
const nameInput = document.getElementById("name");

if (nameInput) {
  nameInput.addEventListener("input", function () {
    this.value = this.value.replace(/[^A-Za-z ]/g, "");
  });
}

// Allow only numbers in age, height and weight
const numberInputs = document.querySelectorAll("#age, #height, #weight");

numberInputs.forEach(function (input) {
  input.addEventListener("keydown", function (event) {
    // Allow: Backspace, Delete, Tab, Arrow keys
    const allowedKeys = [
      "Backspace",
      "Delete",
      "Tab",
      "ArrowLeft",
      "ArrowRight",
      "ArrowUp",
      "ArrowDown"
    ];

    if (allowedKeys.includes(event.key)) {
      return;
    }

    // Allow numbers
    if (event.key >= "0" && event.key <= "9") {
      return;
    }

    // Allow decimal point only for weight
    if (event.key === "." && input.id === "weight" && !input.value.includes(".")) {
      return;
    }

    // Block everything else
    event.preventDefault();
  });
});
const profileForm = document.getElementById("profileForm");

if (profileForm) {
  profileForm.addEventListener("submit", async function (event) {
    event.preventDefault();

    const name = document.getElementById("name").value.trim();
    const age = document.getElementById("age").value;
    const height = document.getElementById("height").value;
    const weight = document.getElementById("weight").value;
    const goal = document.getElementById("goal").value;

    const gender = document.getElementById("gender").value;
const diet = document.getElementById("diet").value;
const activity = document.getElementById("activity").value;

const profileData = {
    name: name,
    age: Number(age),
    gender: gender,
    height: Number(height),
    weight: Number(weight),
    diet: diet,
    activity: activity,
    goal: goal
};

    try {
      const response = await fetch("/api/profile", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify(profileData)
      });

      const responseText = await response.text();

        console.log("Server response:", responseText);
        console.log("HTTP status:", response.status);

        let result;

            try {
        result = JSON.parse(responseText);
            }       catch (jsonError) {
            console.error("Server did not return JSON:", responseText);
        alert("Server error. HTTP status: " + response.status);
        return;
        }

if (!response.ok) {
        alert(result.message);
        return;
      }

      // Keep localStorage for the existing dashboard functionality
      localStorage.setItem("userName", name);
      localStorage.setItem("userAge", age);
      localStorage.setItem("userHeight", height);
      localStorage.setItem("userWeight", weight);
      localStorage.setItem("userGoal", goal);
      localStorage.setItem("userDiet", diet);
      localStorage.setItem("userActivity", activity);
      localStorage.setItem("userGender", gender);
      alert("Profile saved successfully!");

      window.location.href = "dashboard.html";

    } catch (error) {
      console.error("Error:", error);
      alert("Could not connect to the Flask backend.");
    }
  });
}
const userNameElement = document.getElementById("userName");

if (userNameElement) {
  const savedName = localStorage.getItem("userName");

  if (savedName) {
    userNameElement.textContent = savedName;
  }
}
const bmiElement = document.getElementById("bmiValue");

if (bmiElement) {
  const height = Number(localStorage.getItem("userHeight"));
  const weight = Number(localStorage.getItem("userWeight"));

  if (height > 0 && weight > 0) {
    const heightInMetres = height / 100;
    const bmi = weight / (heightInMetres * heightInMetres);

    bmiElement.textContent = bmi.toFixed(1);
  }
}
const bmiCategoryElement = document.getElementById("bmiCategory");

if (bmiCategoryElement) {
    const age = Number(localStorage.getItem("userAge"));
    const height = Number(localStorage.getItem("userHeight"));
    const weight = Number(localStorage.getItem("userWeight"));

    if (age > 0 && height > 0 && weight > 0) {

        const heightInMetres = height / 100;
        const bmi = weight / (heightInMetres * heightInMetres);

        if (age < 5) {
            bmiCategoryElement.textContent =
                "BMI is not interpreted using standard categories at this age.";
        }
        else if (age < 18) {
            bmiCategoryElement.textContent =
                "For this age, BMI should be interpreted using age- and sex-specific growth charts.";
        }
        else if (bmi < 18.5) {
            bmiCategoryElement.textContent =
                "Your BMI is in the underweight range. This may indicate that your weight is below the usual healthy range for your height.";
        }
        else if (bmi < 25) {
            bmiCategoryElement.textContent =
                "Your BMI is in the healthy weight range for adults.";
        }
        else if (bmi < 30) {
            bmiCategoryElement.textContent =
                "Your BMI is in the overweight range. This may indicate that your weight is above the usual healthy range for your height.";
        }
        else {
            bmiCategoryElement.textContent =
                "Your BMI is in a high range. Consider discussing your weight and overall health with a healthcare professional.";
        }
    }
}
const reminderButtons = document.querySelectorAll(".reminder-button");

reminderButtons.forEach(function (button) {
  button.addEventListener("click", function () {
    button.textContent = "Reminder Set ✓";
    button.classList.add("reminder-set");
  });
});
// Calculate estimated daily calorie requirement
// Daily calorie requirement
const calorieElement = document.getElementById("dailyCalories");
const calorieMessage = document.getElementById("calorieMessage");

if (calorieElement) {

    const age = Number(localStorage.getItem("userAge"));
    const height = Number(localStorage.getItem("userHeight"));
    const weight = Number(localStorage.getItem("userWeight"));
    const gender = localStorage.getItem("userGender");
    const activity = localStorage.getItem("userActivity");
    const goal = localStorage.getItem("userGoal");

    if (age > 0 && height > 0 && weight > 0) {

        // Mifflin-St Jeor BMR
        let bmr;

        if (gender === "female") {
            bmr = (10 * weight) +
                  (6.25 * height) -
                  (5 * age) -
                  161;
        } else {
            bmr = (10 * weight) +
                  (6.25 * height) -
                  (5 * age) +
                  5;
        }

        // Activity level
        let activityMultiplier = 1.2;

        if (activity === "light") {
            activityMultiplier = 1.375;
        }
        else if (activity === "moderate") {
            activityMultiplier = 1.55;
        }
        else if (activity === "active") {
            activityMultiplier = 1.725;
        }

        let calories = bmr * activityMultiplier;

        // Adjust according to goal
        if (goal === "lose") {
            calories -= 300;
        }
        else if (goal === "gain") {
            calories += 300;
        }

        calories = Math.round(calories);

        calorieElement.textContent =
            calories.toLocaleString() + " kcal";

        // Explain the result
        if (calorieMessage) {

            if (goal === "lose") {
                calorieMessage.textContent =
                    'Estimated daily calories for your goal. A moderate calorie reduction is applied for weight loss.';
            }
            else if (goal === "gain") {
                calorieMessage.textContent =
                    'Estimated daily calories for your goal. A calorie increase is applied for weight gain.';
            }
            else {
                calorieMessage.textContent =
                    'Estimated calories needed each day based on your profile and activity level.';
            }
        }
    }
}
// ===============================
// HEALTH REMINDERS
// ===============================

document.querySelectorAll(".reminder-button").forEach(function(button) {

    button.addEventListener("click", function() {

        if ("Notification" in window &&
            Notification.permission === "default") {

            Notification.requestPermission();
        }

        const reminderType =
            button.getAttribute("data-reminder");

        // Create time selector popup
        const overlay = document.createElement("div");

        overlay.style.position = "fixed";
        overlay.style.inset = "0";
        overlay.style.background = "rgba(0, 0, 0, 0.55)";
        overlay.style.display = "flex";
        overlay.style.alignItems = "center";
        overlay.style.justifyContent = "center";
        overlay.style.zIndex = "9999";

        const box = document.createElement("div");

        box.style.background = "#ffffff";
        box.style.padding = "25px";
        box.style.borderRadius = "18px";
        box.style.width = "320px";
        box.style.maxWidth = "90%";
        box.style.textAlign = "center";
        box.style.boxShadow = "0 10px 40px rgba(0,0,0,0.3)";

        const title = document.createElement("h3");
        title.textContent = "Set Reminder Time";

        const subtitle = document.createElement("p");
        subtitle.textContent = "Select hour, minute and AM/PM";

        const timeRow = document.createElement("div");

        timeRow.style.display = "flex";
        timeRow.style.justifyContent = "center";
        timeRow.style.alignItems = "center";
        timeRow.style.gap = "8px";
        timeRow.style.margin = "20px 0";

        // Hour selector
        const hourSelect = document.createElement("select");

        for (let i = 1; i <= 12; i++) {

            const option = document.createElement("option");

            option.value = String(i).padStart(2, "0");
            option.textContent = String(i).padStart(2, "0");

            hourSelect.appendChild(option);
        }

        // Minute selector
        const minuteSelect = document.createElement("select");

        for (let i = 0; i < 60; i++) {

            const option = document.createElement("option");

            option.value = String(i).padStart(2, "0");
            option.textContent = String(i).padStart(2, "0");

            minuteSelect.appendChild(option);
        }

        // AM / PM selector
        const periodSelect = document.createElement("select");

        ["AM", "PM"].forEach(function(period) {

            const option = document.createElement("option");

            option.value = period;
            option.textContent = period;

            periodSelect.appendChild(option);
        });

        // Make selectors easier to scroll through
        [hourSelect, minuteSelect, periodSelect].forEach(function(select) {

            select.style.fontSize = "18px";
            select.style.padding = "8px";
            select.style.borderRadius = "8px";
            select.style.border = "1px solid #aaa";
            select.style.background = "#fff";
        });

        const colon1 = document.createElement("span");
        colon1.textContent = ":";

        const colon2 = document.createElement("span");
        colon2.textContent = ":";

        colon1.style.fontSize = "20px";
        colon2.style.fontSize = "20px";

        timeRow.appendChild(hourSelect);
        timeRow.appendChild(colon1);
        timeRow.appendChild(minuteSelect);
        timeRow.appendChild(colon2);
        timeRow.appendChild(periodSelect);

        const setButton = document.createElement("button");

        setButton.textContent = "Set Reminder";
        setButton.style.padding = "10px 18px";
        setButton.style.border = "none";
        setButton.style.borderRadius = "10px";
        setButton.style.cursor = "pointer";

        const cancelButton = document.createElement("button");

        cancelButton.textContent = "Cancel";
        cancelButton.style.padding = "10px 18px";
        cancelButton.style.marginLeft = "10px";
        cancelButton.style.borderRadius = "10px";
        cancelButton.style.cursor = "pointer";

        const buttonRow = document.createElement("div");

        buttonRow.appendChild(setButton);
        buttonRow.appendChild(cancelButton);

        box.appendChild(title);
        box.appendChild(subtitle);
        box.appendChild(timeRow);
        box.appendChild(buttonRow);

        overlay.appendChild(box);
        document.body.appendChild(overlay);

        // Set reminder
        setButton.addEventListener("click", function() {

            const time =
                hourSelect.value +
                ":" +
                minuteSelect.value +
                " " +
                periodSelect.value;

            localStorage.setItem(
                "reminder_" + reminderType,
                time
            );

            button.textContent = "Reminder Set ✓";

            const message =
                document.createElement("p");

            message.className =
                "reminder-status";

            message.textContent =
                "Reminder set for " + time;

            const card =
                button.closest(".reminder-card");

            const oldMessage =
                card.querySelector(".reminder-status");

            if (oldMessage) {
                oldMessage.remove();
            }

            card.appendChild(message);

            overlay.remove();
        });

        // Cancel
        cancelButton.addEventListener("click", function() {
            overlay.remove();
        });

    });

});
// Restore saved reminders when the page opens
document.querySelectorAll(".reminder-button").forEach(function(button) {

    const reminderType =
        button.getAttribute("data-reminder");

    const savedTime =
        localStorage.getItem("reminder_" + reminderType);

    if (savedTime) {

        button.textContent = "Reminder Set ✓";

        const card =
            button.closest(".reminder-card");

        const message = document.createElement("p");

        message.className = "reminder-status";

        message.textContent =
            "Reminder set for " + savedTime;

        card.appendChild(message);
    }
});
// ===============================
// BROWSER NOTIFICATIONS
// ===============================

if ("Notification" in window) {

    Notification.requestPermission().then(function(permission) {

        if (permission === "granted") {
            console.log("Health reminder notifications enabled.");
        }

    });

}
// ===============================
// CHECK SAVED HEALTH REMINDERS
// ===============================

function checkHealthReminders() {

    if (!("Notification" in window)) {
        return;
    }

    if (Notification.permission !== "granted") {
        return;
    }

    const now = new Date();

    const currentHour = now.getHours();
    const currentMinute = now.getMinutes();

    const reminders = [
        {
            type: "water",
            title: "💧 Water Reminder",
            message: "Time to drink some water!"
        },
        {
            type: "medicine",
            title: "💊 Medicine Reminder",
            message: "Check your scheduled medication."
        },
        {
            type: "exercise",
            title: "🏃 Exercise Reminder",
            message: "Time for your planned physical activity!"
        },
        {
            type: "sleep",
            title: "🌙 Sleep Reminder",
            message: "Time to prepare for your sleep routine."
        }
    ];

    reminders.forEach(function(reminder) {

        const savedTime =
            localStorage.getItem("reminder_" + reminder.type);

        if (!savedTime) {
            return;
        }

        // Convert saved time such as "21:45"
        // or "09:45 PM" into hour/minute.
        const match = savedTime.match(
            /^(\d{1,2}):(\d{2})\s*(AM|PM)?$/i
        );

        if (!match) {
            return;
        }

        let reminderHour = Number(match[1]);
        const reminderMinute = Number(match[2]);
        const period = match[3];

        if (period) {

            if (period.toUpperCase() === "PM" &&
                reminderHour !== 12) {
                reminderHour += 12;
            }

            if (period.toUpperCase() === "AM" &&
                reminderHour === 12) {
                reminderHour = 0;
            }
        }

        if (
            currentHour === reminderHour &&
            currentMinute === reminderMinute
        ) {

            const todayKey =
                new Date().toISOString().slice(0, 10);

            const notificationKey =
                "notification_" +
                reminder.type +
                "_" +
                todayKey;

            // Prevent repeated notifications
            // during the same minute/day.
            if (!localStorage.getItem(notificationKey)) {

                new Notification(
                    reminder.title,
                    {
                        body: reminder.message
                    }
                );

                localStorage.setItem(
                    notificationKey,
                    "true"
                );
            }
        }
    });
}
// Start checking reminders every 1 second
setInterval(checkHealthReminders, 1000);

// Also check immediately when the page loads
checkHealthReminders();

// Check every 30 seconds
setInterval(checkHealthReminders, 30000);

// Also check immediately
checkHealthReminders();
// ===============================
// AI SYMPTOM WELLNESS GUIDE
// ===============================

document.addEventListener("DOMContentLoaded", function () {

    const askAiButton = document.getElementById("askAiButton");
    const symptomsInput = document.getElementById("symptoms");
    const aiResponse = document.getElementById("aiResponse");
    const aiStatus = document.getElementById("aiStatus");

    if (!askAiButton || !symptomsInput || !aiResponse) {
        return;
    }

    askAiButton.addEventListener("click", async function () {

        const symptoms = symptomsInput.value.trim();

        if (!symptoms) {
            if (aiStatus) {
                aiStatus.textContent = "";
            }

            aiResponse.textContent =
                "Please describe how you are feeling first.";

            return;
        }

        askAiButton.disabled = true;
        askAiButton.textContent = "Getting guidance...";

        if (aiStatus) {
            aiStatus.innerHTML = `
                <span class="ai-loading">
                    🤖 AI is analyzing your symptoms
                    <span></span>
                    <span></span>
                    <span></span>
                </span>
            `;
        }

        aiResponse.textContent = "";

        try {

            const response = await fetch("/api/symptoms", {
                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify({
                    symptoms: symptoms
                })
            });

            // Read the server response safely
            const responseText = await response.text();

            console.log("Server response:", responseText);
            console.log("HTTP status:", response.status);

            let data;

            try {
                data = JSON.parse(responseText);
            } catch (jsonError) {

                console.error(
                    "Server did not return JSON:",
                    responseText
                );

                if (aiStatus) {
                    aiStatus.textContent =
                        "⚠️ Server response error";
                }

                aiResponse.textContent =
                    "The wellness service returned an unexpected response.";

                return;
            }

            if (response.ok && data.success) {

                if (aiStatus) {
                    aiStatus.textContent =
                        "✅ Wellness guidance ready";
                }

                aiResponse.textContent =
                    data.guidance;

            } else {

                if (aiStatus) {
                    aiStatus.textContent =
                        "⚠️ Unable to provide guidance";
                }

                aiResponse.textContent =
                    data.message ||
                    "Unable to provide guidance.";

                console.error("API error:", data);
            }

        } catch (error) {

            console.error("Symptom Guide Error:", error);

            if (aiStatus) {
                aiStatus.textContent =
                    "⚠️ Connection error";
            }

            aiResponse.textContent =
                "Unable to connect to the wellness guide. Please try again.";

        } finally {

            askAiButton.disabled = false;
            askAiButton.textContent =
                "Ask AI for Guidance";

        }

    });

});
// ===============================
// DASHBOARD PROFILE SUMMARY
// ===============================

const dashboardGoal = document.getElementById("dashboardGoal");
const dashboardActivity = document.getElementById("dashboardActivity");
const dashboardDiet = document.getElementById("dashboardDiet");

if (dashboardGoal) {
    let goal = localStorage.getItem("userGoal");

    if (goal === "lose") {
        goal = "Weight Loss";
    } else if (goal === "gain") {
        goal = "Weight Gain";
    } else if (goal === "maintain") {
        goal = "Maintain Weight";
    }

    dashboardGoal.textContent = goal || "Not set";
}

if (dashboardActivity) {
    let activity = localStorage.getItem("userActivity");

    if (activity === "sedentary") {
        activity = "Sedentary";
    } else if (activity === "light") {
        activity = "Lightly Active";
    } else if (activity === "moderate") {
        activity = "Moderately Active";
    } else if (activity === "active") {
        activity = "Very Active";
    }

    dashboardActivity.textContent = activity || "Not set";
}

if (dashboardDiet) {
    let diet = localStorage.getItem("userDiet");

    if (diet === "vegetarian") {
        diet = "Vegetarian";
    } else if (diet === "non-vegetarian") {
        diet = "Non-Vegetarian";
    } else if (diet === "vegan") {
        diet = "Vegan";
    }

    dashboardDiet.textContent = diet || "Not set";
}