function requestPopup(callback) {
    if (!sessionStorage.getItem("ai_access_granted")) {
      const password = prompt(
        "This feature is currently in beta testing. Please enter the password to continue."
      );
      if (password) {
        validatePassword(password, callback);
      } else {
        alert("Password input canceled.");
      }
    } else {
      callback(); // Directly execute the button's action if access is already granted
    }
  }
  
  function validatePassword(password, callback) {
    fetch("/validate_popup", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ password: password }),
    })
      .then((res) => res.json())
      .then((data) => {
        if (data.success) {
          sessionStorage.setItem("ai_access_granted", "true"); // Store access in client
          callback(); // Execute the original action
        } else {
          alert("Incorrect password. Please try again.");
        }
      })
      .catch((err) => {
        console.error("Error validating password:", err);
        alert("Validation failed. Please try again.");
      });
  }
  