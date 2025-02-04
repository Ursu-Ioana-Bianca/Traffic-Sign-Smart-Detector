document.getElementById("menuToggle").addEventListener("click", function () {
    document.getElementById("sideMenu").classList.add("open");
});

document.getElementById("closeMenu").addEventListener("click", function () {
    document.getElementById("sideMenu").classList.remove("open");
});

document.getElementById("showCategories").addEventListener("click", function () {
    fetchCategories();
});

const userEmail = sessionStorage.getItem("userEmail");

function fetchCategories() {

    fetch('http://127.0.0.1:5000/get_signs')
        .then(response => response.json())
        .then(data => {

            displayCategories(data);

        })
        .catch(error => console.error('Error fetching categories:', error));

    history.pushState({}, "", "/get_signs");
}

document.getElementById("showCategories").addEventListener("click", function () {
    
    const container = document.getElementById("categoriesContainer");

    // Verificăm dacă containerul este vizibil și îl ascundem/afișăm
    if (container.style.display === "none" || container.style.display === "") {
        fetchCategories();
        container.style.display = "block";
    } else {
        container.style.display = "none";
    }


});

function displayCategories(categoriesData) {

    if (!userEmail) {
        alert("❌ You need to be logged in to see categories.");
        return;
    }


    const container = document.getElementById("categoriesContainer");
    container.innerHTML = "";
    document.getElementById("signsContainer").innerHTML = "";

    for (let category in categoriesData) {
        let btn = document.createElement("button");
        btn.style.backgroundColor = "#e38705"; // Setează culoarea fundalului când apare
        btn.innerText = addSpacesToCamelCase(category);
        btn.classList.add("category-btn");
        btn.onclick = function () {
            fetchSigns(categoriesData, category);
        history.pushState({}, "", `/get_signs?category=${category}`);
        };
        container.appendChild(btn);
    }
}

// Funcția care adaugă spațiu între litere mici și mari
function addSpacesToCamelCase(text) {
    return text.replace(/([a-z])([A-Z])/g, '$1 $2');
}

function fetchSigns(categoriesData, category) {
    const nearbySignsContainer = document.getElementById("nearbySignsContainer");
    nearbySignsContainer.innerHTML = "";  

    const container = document.getElementById("signsContainer");
    container.innerHTML = `<h1 id="category-header" style="color:rgb(0, 0, 0);">${addSpacesToCamelCase(category)}</h1>`;

    let rowDiv = document.createElement("div");
    rowDiv.classList.add("row");

    categoriesData[category].forEach((sign, index) => {
        let signDiv = document.createElement("div");
        signDiv.classList.add("sign");
        signDiv.style.position = "relative"; // Pentru a poziționa corect

        let textParts = [sign.name];

        if (sign.shape) {
            textParts.push("It has " + sign.shape + " shape.");
        }
        if (sign.background) {
            textParts.push("The background color is: " + sign.background + ".");
        }
        if (sign.contour) {
            textParts.push("The border color is: " + sign.contour + ".");
        }


        let signDescription = textParts.join(" "); // Construim textul pentru redare vocală

        let signInterpretation = sign.name + "sign. " +  sign.description

        signDiv.innerHTML = `
            <h2>${sign.name}</h2>
            <img src="${sign.image}" alt="${sign.name}">
            <p>${sign.description}</p>

            <!-- Buton pentru redare text detaliat (stânga jos) -->
            <button class="speak-btn left-btn" onclick="toggleSpeech('${signDescription.replace(/'/g, "\\'")}')">
                🔊
            </button>

            <!-- Buton pentru redare descriere (dreapta jos) -->
            <button class="speak-btn right-btn" onclick="toggleSpeech('${signInterpretation.replace(/'/g, "\\'")}')">
                📝
            </button>

           <span id="associated-sign-name">
                ${
                    sign.associatedSigns.length > 0 
                        ? `<b>Associated sign:</b> 
                        <div style="display: flex; flex-direction: column; align-items: center;">
                            <div style="display: flex; gap: 10px;">` +
                            sign.associatedSigns.map(assocSign => 
                                `<span>${assocSign.name}</span>`
                            ).join('') +
                            `</div>
                            <div style="display: flex; gap: 10px; margin-top: 5px;">` +
                            sign.associatedSigns.map(assocSign => 
                                `<img src="${assocSign.image}" alt="${assocSign.name}" style="width: 70px; height: 60px;">`
                            ).join('') +
                            `</div>
                        </div>`
                        : ''
                }
            </span>
        `;

        rowDiv.appendChild(signDiv);

        if ((index + 1) % 3 === 0 || index === categoriesData[category].length - 1) {
            container.appendChild(rowDiv);
            rowDiv = document.createElement("div");
            rowDiv.classList.add("row");
        }
    });
}

// Variabilă globală pentru gestionarea vocii
let synth = window.speechSynthesis;
let currentUtterance = null;

// Funcție pentru a porni/opri citirea vocală
function toggleSpeech(text) {
    if (synth.speaking) {
        synth.cancel(); // Oprește vorbirea dacă deja se vorbește
    } else {
        currentUtterance = new SpeechSynthesisUtterance(text);
        currentUtterance.lang = "en-US"; // Schimbă limba dacă e nevoie
        synth.speak(currentUtterance);
    }
}


// 📍 Când se apasă pe "Find Signs Nearby", afișează opțiunile de locație
document.getElementById("findSigns").addEventListener("click", function () {
    const findMethodContainer = document.getElementById("findMethodContainer");

    // Verificăm dacă containerul este vizibil și îl ascundem/afișăm
    if (findMethodContainer.style.display === "none" || findMethodContainer.style.display === "") {
        displayFindMethods();
        findMethodContainer.style.display = "block";
    } else {
        nearbySignsContainer.innerHTML = "";
        findMethodContainer.style.display = "none";
    }

    // Deschidem meniul lateral (dacă nu este deja deschis)
    document.getElementById("sideMenu").classList.add("open");
});

// Funcție pentru a crea și afișa butoanele de alegere a metodei de locație
function displayFindMethods() {

    if (!userEmail) {
        alert("❌ You need to be logged in to search signs.");
        return;
    }


    const findMethodContainer = document.getElementById("findMethodContainer");
    findMethodContainer.innerHTML = ""; // Curățăm containerul înainte de a adăuga butoanele
    findMethodContainer.style.display = "flex"; //
    

    let findLocationBtn = document.createElement("button");
    findLocationBtn.style.backgroundColor = "#e38705"; // Setează culoarea fundalului când apare
    findLocationBtn.innerText = "Find Location";
    findLocationBtn.classList.add("category-btn");
    findLocationBtn.onclick = function () {
        fetchLocationFromGeolocation();
    };

    let manuallyLocationBtn = document.createElement("button");
    manuallyLocationBtn.style.backgroundColor = "#e38705"; // Setează culoarea fundalului când apare
    manuallyLocationBtn.innerText = "Manually Enter Location";
    manuallyLocationBtn.classList.add("category-btn");
    manuallyLocationBtn.onclick = function () {
        promptForManualLocation();
    };

    findMethodContainer.appendChild(findLocationBtn);
    findMethodContainer.appendChild(manuallyLocationBtn);
}


// 📡 Funcție pentru obținerea locației prin geolocația browserului (API-ul de Geolocație al browserului)
function fetchLocationFromGeolocation() {
    const nearbySignsContainer = document.getElementById("nearbySignsContainer");
    nearbySignsContainer.innerHTML = "";  // Curățăm conținutul anterior

    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(
            function (position) {
                let latitude = position.coords.latitude;
                let longitude = position.coords.longitude;

                console.log("📍 Location retrieved:", latitude, longitude);
                fetchNearbySigns(latitude, longitude);
            },
            function (error) {
                console.error("❌ Geolocation error:", error);
                alert("Error getting location: " + error.message);
            }
        );
    } else {
        alert("❌ Geolocation is not supported by your browser.");
    }
}

// ✍️ Funcție pentru introducerea manuală a locației
function promptForManualLocation() {
    const latitude = prompt("Enter latitude:");
    const longitude = prompt("Enter longitude:");

    if (latitude && longitude) {
        console.log("📍 Manually entered location:", latitude, longitude);
        fetchNearbySigns(latitude, longitude);
    } else {
        alert("❌ Invalid location entered.");
    }
}

// 📡 Funcție  pentru a obține semnele din apropiere
function fetchNearbySigns(latitude, longitude) {
    fetch(`http://127.0.0.1:5000/get_nearby_signs?lat=${latitude}&lon=${longitude}`)
        .then(response => response.json())
        .then(data => {
            console.log("📡 Nearby signs data received:", data);
            displayNearbySigns(data);
        })
        .catch(error => console.error('❌ Error fetching nearby signs:', error));
    history.pushState({}, "", `/get_nearby_signs?lat=${latitude}&lon=${longitude}`);
}

// 📌 Funcție pentru afișarea semnelor din apropiere
function displayNearbySigns(signsData) {
    const container = document.getElementById("nearbySignsContainer");
    container.innerHTML = `<h1 id="category-header" style="color:rgb(0, 0, 0);">Nearby Traffic Signs</h1>`;

    if (signsData.length === 0) {
        container.innerHTML += `<h1 style="color: white;">No signs found nearby.</h1>`;
        return;
    }

    let rowDiv = document.createElement("div");
    rowDiv.classList.add("row");

    signsData.forEach((sign, index) => {
        let signDiv = document.createElement("div");
        signDiv.classList.add("sign");

        signDiv.innerHTML = `
            <h3>${sign.name}</h3>
            <h4>${addSpacesToCamelCase(sign.category)}</h4>
            <img src="${sign.image}" alt="${sign.name}">
            <p>${sign.description}</p>
            <p><strong>Distance:</strong> ${sign.distance} km</p>
        `;

        rowDiv.appendChild(signDiv);

        // Grupăm semnele câte 3 pe rând
        if ((index + 1) % 3 === 0 || index === signsData.length - 1) {
            container.appendChild(rowDiv);
            rowDiv = document.createElement("div");
            rowDiv.classList.add("row");
        }
    });

    // Adăugăm butonul pentru afișarea hărții
    const mapButton = document.createElement("button");
    mapButton.textContent = "🗺️ Show Map";
    mapButton.style.display = "block";
    mapButton.style.margin = "30px auto";
    mapButton.style.height = "80px";
    mapButton.style.width = "180px";
    mapButton.style.fontSize = "22px";
    mapButton.onclick = () => displayMap(signsData);

    container.appendChild(mapButton);

    // Creăm div-ul pentru hartă (inițial ascuns)
    const mapDiv = document.createElement("div");
    mapDiv.id = "map";
    mapDiv.style.height = "500px";
    mapDiv.style.display = "none"; // Harta este ascunsă inițial
    container.appendChild(mapDiv);
}

function displayMap(signsData) {
    console.log("📡 Rendering map with traffic signs:", signsData);

    const mapDiv = document.getElementById("map");
    mapDiv.style.display = "block"; // Afișează harta

    if (window.myMap) {
        window.myMap.remove();
    }

    // Geolocație: Obține poziția utilizatorului
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(position => {
            const userLat = position.coords.latitude;
            const userLon = position.coords.longitude;

            console.log(`📍 User location: ${userLat}, ${userLon}`);

            // Inițializează harta pe poziția utilizatorului
            initMap(userLat, userLon, signsData);
        }, () => {
            console.warn("⚠️ Geolocation denied! Using default sign location.");
            useFirstSignLocation(signsData);
        });
    } else {
        console.warn("⚠️ Geolocation not supported!");
        useFirstSignLocation(signsData);
    }
}

function useFirstSignLocation(signsData) {
    if (signsData.length > 0) {
        const firstSign = signsData[0];
        initMap(firstSign.latitude, firstSign.longitude, signsData);
    } else {
        console.error("❌ No signs available to show on the map!");
    }
}

function initMap(latitude, longitude, signsData) {
    console.log("📡 Rendering map with coordinates:", latitude, longitude);
    console.log("🚦 Traffic signs data:", signsData);

    // Inițializează harta cu Leaflet.js
    window.myMap = L.map("map").setView([latitude, longitude], 14);

    // Adaugă stratul OpenStreetMap
    L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
        attribution: '&copy; OpenStreetMap contributors'
    }).addTo(window.myMap);

    // Adaugă marker pentru locația utilizatorului
    L.marker([latitude, longitude], {
        icon: L.icon({ iconUrl: 'https://maps.google.com/mapfiles/ms/icons/blue-dot.png' })
    }).addTo(window.myMap)
    .bindPopup("📍 You are here")
    .openPopup();

    // Adaugă marker pentru fiecare semn de circulație
    signsData.forEach(sign => {
        L.marker([sign.latitude, sign.longitude], {
            icon: L.icon({ iconUrl: 'https://maps.google.com/mapfiles/ms/icons/red-dot.png' })
        }).addTo(window.myMap)
        .bindPopup(`<b>${sign.name}</b>`);
    });

    console.log("✅ Map rendered successfully.");
}




document.getElementById("raport").addEventListener("click", function () {

    document.getElementById("reportFormContainer").style.display = "flex";
    history.pushState({}, "", "/report");
});

document.getElementById("closeReport").addEventListener("click", function () {
    document.getElementById("reportFormContainer").style.display = "none";
});

document.getElementById("submitReport").addEventListener("click", function () {

    if (!userEmail) {
        alert("❌ You need to be logged in to send report.");
        return;
    }

    let country = document.getElementById("country").value;
    let county = document.getElementById("county").value;
    let street = document.getElementById("street").value;
    let datetime = document.getElementById("datetime").value;
    let description = document.getElementById("description").value;

    if (county && street && description) {
        // Construim payload-ul pentru request
        let reportData = {
            country: country,
            county: county,
            street: street,
            datetime: datetime,
            description: description,
            userEmail: userEmail
        };

        // Trimitem datele către backend
        fetch('http://127.0.0.1:5000/report', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(reportData)
        })
        .then(response => response.json())
        .then(data => {
            if (data.message === "Report submitted successfully") {
                alert("✅ Report submitted successfully!");
                document.getElementById("reportFormContainer").style.display = "none";
            } else {
                alert("❌ Error submitting report: " + data.message);
            }
        })
        .catch(error => {
            console.error("❌ Error:", error);
            alert("❌ Could not submit report. Please try again.");
        });

    } else {
        alert("⚠️ Please fill in all fields.");
    }
});




document.getElementById("notification").addEventListener("click", function () {
    const notificationContainer = document.getElementById("notificationContainer");

    // Dacă notificările sunt deja afișate, doar le ascundem
    if (notificationContainer.style.display === "block") {
        notificationContainer.style.display = "none";
    } else {
        // Luăm email-ul din sesiune în loc să cerem manual
        let userEmail = sessionStorage.getItem("userEmail");

        if (!userEmail) {
            alert("❌ You need to be logged in to see notifications.");
            return;
        }

        fetchNotifications(userEmail);
    }
});

function fetchNotifications(userEmail) {
    fetch(`http://127.0.0.1:5000/notifications?email=${userEmail}`)
        .then(response => response.json())
        .then(data => {
            displayNotifications(data);
        })
        .catch(error => {
            console.error('❌ Error fetching notifications:', error);
            alert("❌ There was an issue fetching notifications.");
        });

    history.pushState({}, "", `/notifications?email=${userEmail}`);
}

function displayNotifications(notifications) {
    const container = document.getElementById("notificationContainer");
    const list = document.getElementById("notificationList");

    list.innerHTML = ""; // Ștergem notificările vechi

    if (notifications.length === 0) {
        list.innerHTML = "<li>No new notifications.</li>";
    } else {
        notifications.forEach(notification => {
            let listItem = document.createElement("li");
            listItem.id = `notification-${notification.id}`;  // Adăugăm ID-ul notificării pentru a o putea identifica

            listItem.innerHTML = `
                <span style="font-size: 20px;">${notification.message}</span>
                <button onclick="deleteNotification(${notification.id})">Delete</button>
            `;
            list.appendChild(listItem);
        });
    }

    container.style.display = "block"; // Afișăm notificările
}

// Funcția pentru ștergerea notificării
function deleteNotification(notificationId) {
    if (!userEmail) {
        alert("❌ You need to be logged in to delete notifications.");
        return;
    }

    // Confirmă ștergerea
      fetch(`http://127.0.0.1:5000/delete_notification/${notificationId}`, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ email: userEmail }),  // Include emailul utilizatorului în cerere
        })
        .then(response => {
            console.log("Raw response:", response);
            return response.json();
        })
        .then(data => {
            console.log("Server response:", data); // Debugging
            // Afișează mesajul de succes sau eroare
            if (data.message && data.message === "Notification deleted successfully") {
                // Elimină notificarea din listă
                const notificationElement = document.getElementById(`notification-${notificationId}`);
                if (notificationElement) {
                    notificationElement.remove();
                    alert("Notification deleted successfully!");
                }
            } else {
                // Dacă nu e succes, afișăm mesajul de eroare
                alert(`Error deleting notification: ${data.message}`);
            }
        })
        .catch(error => {
            console.error("❌ Error:", error);
            alert("Error deleting notification.");
        });

        history.pushState({}, "", `/delete_notification/${notificationId}`);

}



document.getElementById("profileButton").addEventListener("click", function () {
    const infoContainer = document.getElementById("profileInfo");

    if (infoContainer.style.display === "block") {
        infoContainer.style.display = "none";
    } else {
        fetchUserInfo();
    }
});

async function fetchUserInfo() {
    let userEmail = sessionStorage.getItem("userEmail");

    if (!userEmail) {
        alert("❌ Email is required to fetch user information.");
        return;
    }

    try {
        let response = await fetch(`http://127.0.0.1:5000/get_user_info?email=${userEmail}`);
        
        if (!response.ok) {
            throw new Error(`❌ HTTP Error: ${response.status}`);
        }

        let data = await response.json();
        console.log("✅ Response:", data);
        displayUserInfo(data);
    } catch (error) {
        console.error("❌ Fetch Error:", error);
    }

    history.pushState({}, "", `/get_user_info?email=${userEmail}`);
}

function displayUserInfo(user) {
    const infoContainer = document.getElementById("profileInfo");
    let userEmail = sessionStorage.getItem("userEmail");
    console.log(user.profile_image);
    if (!userEmail) {
        infoContainer.innerHTML = "<h2>No user found with this email.</h2>";
    } else {
        infoContainer.innerHTML = `
            <h1 style="text-align: center;">User Profile</h1>
            <h3><strong>Username:</strong> ${user.username}</h3>
            <h3><strong>Email:</strong> ${user.email}</h3>
            <h3><strong>Country:</strong> ${user.country}</h3>
            <h3><strong>County:</strong> ${user.county}</h3>
            <button id="changeImageButton"></button>
            
        `;
        
        
        if (user.profile_image) {
            sessionStorage.setItem("profileImage", user.profile_image);
            localStorage.setItem("profileImage", user.profile_image);
            document.getElementById("profileImage").src = user.profile_image + "?t=" + new Date().getTime();
            
        }
    }

    infoContainer.style.display = "block";

    let changeImageButton = document.getElementById("changeImageButton");
    if (changeImageButton) {
        changeImageButton.onclick = function () {
            document.getElementById("imageUpload").click();
        };
    }
}

// Gestionăm încărcarea imaginii
document.getElementById("imageUpload").addEventListener("change", function (event) {
    event.preventDefault();  // Oprire refresh pagină
    let file = this.files[0];
    if (!file) return;

    let formData = new FormData();
    formData.append("email", sessionStorage.getItem("userEmail"));
    formData.append("profile_image", file);

    fetch("http://127.0.0.1:5000/upload_profile_image", {
        method: "POST",
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        console.log("✅ Server response:", data);  // Vezi răspunsul complet în consolă
        if (data.image_url) {
            sessionStorage.setItem("profileImage", data.image_url);
            localStorage.setItem("profileImage", data.image_url);
            document.getElementById("profileImage").src = data.image_url + "?t=" + new Date().getTime();
            alert("✅ Profile image updated successfully!");
        } else {
            alert("❌ Error updating profile image.");
        }
    })
    .catch(error => console.error("❌ Fetch Error:", error));

    history.pushState({}, "", "/upload_profile_image");
});

// La încărcarea paginii, setează imaginea din sessionStorage
window.onload = function () {
    setTimeout(() => {
        let savedProfileImage = sessionStorage.getItem("profileImage");
        console.log("✅ Stored image in session:", savedProfileImage);
        
        if (savedProfileImage) {
            let profileImageElement = document.getElementById("profileImage");
            

            if (profileImageElement ||  localStorage.getItem("profileImage")) {
                profileImageElement.src = savedProfileImage + "?t=" + new Date().getTime();
            } else {
                console.error("❌ Elementul #profileImage nu a fost găsit!");
            }
        }
    }, 1000); // Așteaptă 1 secundă înainte de a seta imaginea
};



document.addEventListener("DOMContentLoaded", function () {
    let savedProfileImage = sessionStorage.getItem("profileImage");

    if (savedProfileImage) {
        let profileImageElement = document.getElementById("profileImage");

        if (profileImageElement) {
            profileImageElement.src = savedProfileImage + "?t=" + new Date().getTime();
        } else {
            console.warn("⚠️ Elementul #profileImage nu a fost găsit. Se mai încearcă...");
            
            // Verifică din nou la fiecare 500ms până când găsește elementul (max 5 secunde)
            let checkExist = setInterval(() => {
                profileImageElement = document.getElementById("profileImage");
                if (profileImageElement) {
                    profileImageElement.src = savedProfileImage + "?t=" + new Date().getTime();
                    clearInterval(checkExist);
                }
            }, 500);

            // Oprește căutarea după 5 secunde
            setTimeout(() => clearInterval(checkExist), 5000);
        }
    }
});



document.getElementById("logout").addEventListener("click", async function () {
    try {
        let response = await fetch("http://127.0.0.1:5000/logout", {
            method: "POST",
            credentials: "include", // Asigură trimiterea cookie-urilor de sesiune
            headers: { "Content-Type": "application/json" },
        });

        history.pushState({}, "", "/logout");

        let data = await response.json();

        if (!response.ok) {
            throw new Error(data.message || "Logout failed!");
        }

        console.log("Logout successful:", data.message);
        alert("✅ Logged out successfully!");

        // 🔹 Ștergem datele din sessionStorage
        sessionStorage.removeItem("userEmail");
        
        // 🔹 Redirecționăm utilizatorul la pagina de login
        window.location.href = "/home";
    } catch (error) {
        console.error("Error:", error);
        alert("❌ Error logging out. Please try again.");
    }

});





