document.addEventListener("DOMContentLoaded", function () {
    let registerButton = document.querySelector("#register-submit");

    if (!registerButton) {
        console.error("Register button not found!");
        return;
    }

    registerButton.addEventListener("click", async function (event) {
        event.preventDefault(); // Previne reîncărcarea paginii

        console.log("Register button clicked!");

        let usernameInput = document.querySelector("#username-register");
        let passwordInput = document.querySelector("#password-register");
        let confirmPasswordInput = document.querySelector("#confirm-password-register");
        let emailInput = document.querySelector("#email-register");
        let countryInput = document.querySelector("#country-register");
        let countyInput = document.querySelector("#county-register");

        if (!usernameInput || !passwordInput || !confirmPasswordInput || !emailInput || !countryInput || !countyInput) {
            console.error("Form inputs not found!");
            alert("Something went wrong. Please refresh the page.");
            return;
        }

        let username = usernameInput.value.trim();
        let email = emailInput.value.trim();
        let password = passwordInput.value.trim();
        let confirmPassword = confirmPasswordInput.value.trim();
        let country = countryInput.value.trim();
        let county = countyInput.value.trim();

        if (username === "" || email === "" || password === "" || confirmPassword === "") {
            alert("Please fill in all required fields.");
            return;
        }

        // Verifică dacă parolele se potrivesc
        if (password !== confirmPassword) {
            alert("Passwords do not match!");
            return;
        }

        // Trimite cererea către server pentru înregistrare
        try {
            let response = await fetch("http://127.0.0.1:5000/register", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ username, email, password, country, county }),
            });

            let data = await response.json();

            if (!response.ok) {
                throw new Error(data.message || "Registration failed!");
            }

            console.log("Server response:", data);
            alert("Registration successful!");

            // Poți redirecționa utilizatorul la pagina de login sau dashboard
            window.location.href = "/user_page.html";
        } catch (error) {
            console.error("Error:", error);
            alert(error.message);
        }
    });


      // Login event listener
      let loginButton = document.querySelector("#login-form button[type='submit']");
    
      if (!loginButton) {
          console.error("Login button not found!");
          return;
      }
  
      loginButton.addEventListener("click", async function (event) {
        event.preventDefault();
    
        console.log("Login button clicked!");
    
        let email = document.querySelector("#email-login").value.trim();
        let password = document.querySelector("#password-login").value.trim();
        let username = document.querySelector("#username-login").value.trim();
    
        if (username === "" || email === "" || password === "") {
            alert("Please fill in all fields.");
            return;
        }
    
        try {
            let response = await fetch("http://127.0.0.1:5000/login", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ username, email, password }),
            });
    
            let data = await response.json();
    
            if (!response.ok) {
                throw new Error(data.message || "Login failed!");
            }
    
            console.log("Server response:", data);
            alert("Login successful!");
    
            // 🔹 Salvăm datele utilizatorului în sessionStorage
            sessionStorage.setItem("userEmail", email);
    
            // Redirecționăm utilizatorul la pagina dorită
            window.location.href = "user_page.html";
        } catch (error) {
            console.error("Error:", error);
            alert(error.message);
        }
    });



    function adjustDescriptionPosition() {
        const description = document.getElementById("description-box");
        const loginForm = document.getElementById("login-form");
        const registerForm = document.getElementById("register-form");
    
        if (window.innerWidth < 1350 && (loginForm.classList.contains("show") || registerForm.classList.contains("show"))) {
            // Mută description box mai jos și îi reduce lățimea
            description.style.top = "auto"; 
            description.style.bottom = "20px"; 
            description.style.left = "40%";
            description.style.transform = "translateX(-50%)";
            description.style.width = "60%";  // Reduce lățimea la 60%
    
            // Mută formularul mai sus
            loginForm.style.top = "35%";
            registerForm.style.top = "35%";
            registerForm.style.maxHeight = "300px"; // Limitează înălțimea
            registerForm.style.overflowY = "auto";  // Activează scrollbar-ul vertical

        } else {
            // Revine la poziția originală când ecranul este mare sau formularul nu e deschis
            description.style.top = "200px"; 
            description.style.left = "20px"; 
            description.style.bottom = "auto"; 
            description.style.transform = "none";
            description.style.width = "400px";  // Lățime mai mică decât înainte
    
            // Revine la poziția inițială a formularului
            loginForm.style.top = "50%";
            registerForm.style.top = "50%";
        }
    }
    
    // Evenimente care declanșează ajustarea poziției
    window.addEventListener("resize", adjustDescriptionPosition);
    document.getElementById("login-button").addEventListener("click", adjustDescriptionPosition);
    document.getElementById("register-button").addEventListener("click", adjustDescriptionPosition);
    
});
