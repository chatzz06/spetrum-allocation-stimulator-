/* =========================================================
   SpectrumSim - Main JavaScript
   File: static/js/script.js
   ========================================================= */

document.addEventListener("DOMContentLoaded", function () {

    console.log("SpectrumSim JavaScript loaded successfully.");

    /* =====================================================
       1. ACTIVE SIDEBAR MENU
       ===================================================== */

    const currentPath = window.location.pathname;

    const menuLinks = document.querySelectorAll(".menu a");

    menuLinks.forEach(function (link) {

        const href = link.getAttribute("href");

        if (!href || href === "#") {
            return;
        }

        try {
            const linkPath = new URL(
                href,
                window.location.origin
            ).pathname;

            if (linkPath === currentPath) {
                menuLinks.forEach(function (item) {
                    item.classList.remove("active");
                });

                link.classList.add("active");
            }

        } catch (error) {
            console.log("Navigation path error:", error);
        }
    });


    /* =====================================================
       2. PREVENT EMPTY # LINKS
       ===================================================== */

    const hashLinks = document.querySelectorAll('a[href="#"]');

    hashLinks.forEach(function (link) {

        link.addEventListener("click", function (event) {

            event.preventDefault();

        });

    });


    /* =====================================================
       3. ALLOCATION FORM
       ===================================================== */

    const allocationForm = document.querySelector(
        'form[action*="allocation"]'
    );

    if (allocationForm) {

        allocationForm.addEventListener("submit", function (event) {

            const userInput = document.getElementById("user");
            const typeInput = document.getElementById("type");
            const frequencyInput = document.getElementById("frequency");
            const bandwidthInput = document.getElementById("bandwidth");
            const algorithmInput = document.getElementById("algorithm");

            if (
                !userInput ||
                !typeInput ||
                !frequencyInput ||
                !bandwidthInput
            ) {
                return;
            }

            const user = userInput.value.trim();
            const type = typeInput.value;
            const frequency = parseFloat(frequencyInput.value);
            const bandwidth = parseFloat(bandwidthInput.value);

            /* Empty fields */

            if (user === "") {

                event.preventDefault();

                showNotification(
                    "Please enter a User / Service Name.",
                    "error"
                );

                userInput.focus();

                return;
            }


            if (type === "") {

                event.preventDefault();

                showNotification(
                    "Please select a Service Type.",
                    "error"
                );

                typeInput.focus();

                return;
            }


            if (isNaN(frequency)) {

                event.preventDefault();

                showNotification(
                    "Please enter a valid frequency.",
                    "error"
                );

                frequencyInput.focus();

                return;
            }


            if (isNaN(bandwidth) || bandwidth <= 0) {

                event.preventDefault();

                showNotification(
                    "Bandwidth must be greater than 0 MHz.",
                    "error"
                );

                bandwidthInput.focus();

                return;
            }


            /* Frequency limits */

            if (frequency < 700 || frequency > 950) {

                event.preventDefault();

                showNotification(
                    "Frequency must be between 700 MHz and 950 MHz.",
                    "error"
                );

                frequencyInput.focus();

                return;
            }


            /* Check ending frequency */

            const endFrequency = frequency + bandwidth;

            if (endFrequency > 950) {

                event.preventDefault();

                showNotification(
                    "Frequency range cannot exceed 950 MHz.",
                    "error"
                );

                bandwidthInput.focus();

                return;
            }


            /* Confirmation */

            const algorithm =
                algorithmInput ?
                algorithmInput.value :
                "First Fit";

            const message =
                "Confirm Spectrum Allocation\n\n" +
                "User / Service: " + user + "\n" +
                "Service Type: " + type + "\n" +
                "Frequency: " + frequency + " MHz\n" +
                "Bandwidth: " + bandwidth + " MHz\n" +
                "Algorithm: " + algorithm;

            const confirmed = window.confirm(message);

            if (!confirmed) {
                event.preventDefault();
            }

        });

    }


    /* =====================================================
       4. LIVE END FREQUENCY CALCULATION
       ===================================================== */

    const frequencyInput = document.getElementById("frequency");
    const bandwidthInput = document.getElementById("bandwidth");

    if (frequencyInput && bandwidthInput) {

        const endFrequencyText = document.createElement("div");

        endFrequencyText.id = "end-frequency-display";

        endFrequencyText.style.marginTop = "8px";
        endFrequencyText.style.fontSize = "13px";
        endFrequencyText.style.color = "#64748b";

        bandwidthInput.parentElement.appendChild(
            endFrequencyText
        );


        function updateEndFrequency() {

            const frequency =
                parseFloat(frequencyInput.value);

            const bandwidth =
                parseFloat(bandwidthInput.value);

            if (
                !isNaN(frequency) &&
                !isNaN(bandwidth) &&
                bandwidth > 0
            ) {

                const endFrequency =
                    frequency + bandwidth;

                endFrequencyText.textContent =
                    "End Frequency: " +
                    endFrequency +
                    " MHz";

                if (endFrequency > 950) {

                    endFrequencyText.style.color =
                        "#dc2626";

                } else {

                    endFrequencyText.style.color =
                        "#64748b";
                }

            } else {

                endFrequencyText.textContent = "";

            }

        }


        frequencyInput.addEventListener(
            "input",
            updateEndFrequency
        );

        bandwidthInput.addEventListener(
            "input",
            updateEndFrequency
        );

    }


    /* =====================================================
       5. SPECTRUM UTILIZATION
       ===================================================== */

    const utilizationValue =
        document.querySelector(".percentage");

    const circle =
        document.querySelector(".circle");

    if (utilizationValue && circle) {

        const text =
            utilizationValue.textContent.trim();

        const value =
            parseFloat(text.replace("%", ""));

        if (!isNaN(value)) {

            const degrees =
                Math.min(Math.max(value, 0), 100) * 3.6;

            circle.style.background =
                "conic-gradient(" +
                "#2864e6 0deg " +
                degrees +
                "deg, " +
                "#e2e8f0 " +
                degrees +
                "deg 360deg)";

        }

    }


    /* =====================================================
       6. TABLE ROW HOVER EFFECT
       ===================================================== */

    const tableRows =
        document.querySelectorAll("tbody tr");

    tableRows.forEach(function (row) {

        row.addEventListener("mouseenter", function () {

            row.style.backgroundColor =
                "#f8fafc";

        });

        row.addEventListener("mouseleave", function () {

            row.style.backgroundColor =
                "";

        });

    });


    /* =====================================================
       7. AUTO HIDE NOTIFICATIONS
       ===================================================== */

    const alerts =
        document.querySelectorAll(
            ".alert, .flash-message"
        );

    alerts.forEach(function (alert) {

        setTimeout(function () {

            alert.style.opacity = "0";

            setTimeout(function () {

                alert.remove();

            }, 400);

        }, 4000);

    });


    /* =====================================================
       8. MOBILE SIDEBAR
       ===================================================== */

    createMobileMenu();


    /* =====================================================
       9. KEYBOARD SHORTCUT
       ===================================================== */

    document.addEventListener("keydown", function (event) {

        /* Escape closes mobile sidebar */

        if (event.key === "Escape") {

            const sidebar =
                document.querySelector(".sidebar");

            if (sidebar) {
                sidebar.classList.remove("mobile-open");
            }

        }

    });

});


/* =========================================================
   NOTIFICATION FUNCTION
   ========================================================= */

function showNotification(message, type = "info") {

    const existing =
        document.querySelector(".spectrumsim-notification");

    if (existing) {
        existing.remove();
    }


    const notification =
        document.createElement("div");

    notification.className =
        "spectrumsim-notification";


    /* Notification colors */

    let background = "#2864e6";

    if (type === "error") {
        background = "#dc2626";
    }

    if (type === "success") {
        background = "#16a34a";
    }

    if (type === "warning") {
        background = "#d97706";
    }


    notification.style.position = "fixed";
    notification.style.top = "25px";
    notification.style.right = "25px";
    notification.style.zIndex = "9999";
    notification.style.padding = "15px 20px";
    notification.style.borderRadius = "10px";
    notification.style.background = background;
    notification.style.color = "white";
    notification.style.fontSize = "14px";
    notification.style.fontWeight = "bold";
    notification.style.boxShadow =
        "0 8px 25px rgba(0,0,0,0.18)";
    notification.style.maxWidth = "350px";
    notification.style.transition =
        "opacity 0.3s ease";


    notification.textContent = message;


    document.body.appendChild(notification);


    setTimeout(function () {

        notification.style.opacity = "0";

        setTimeout(function () {

            notification.remove();

        }, 300);

    }, 3500);

}


/* =========================================================
   MOBILE MENU
   ========================================================= */

function createMobileMenu() {

    const sidebar =
        document.querySelector(".sidebar");

    if (!sidebar) {
        return;
    }


    /* Only create button once */

    if (document.querySelector(".mobile-menu-button")) {
        return;
    }


    const button =
        document.createElement("button");

    button.className =
        "mobile-menu-button";

    button.innerHTML = "☰";


    button.style.display = "none";
    button.style.position = "fixed";
    button.style.top = "15px";
    button.style.left = "15px";
    button.style.zIndex = "10001";
    button.style.width = "45px";
    button.style.height = "45px";
    button.style.border = "none";
    button.style.borderRadius = "8px";
    button.style.background = "#2864e6";
    button.style.color = "white";
    button.style.fontSize = "22px";
    button.style.cursor = "pointer";


    document.body.appendChild(button);


    button.addEventListener("click", function () {

        sidebar.classList.toggle(
            "mobile-open"
        );

    });


    /* Responsive CSS */

    const style =
        document.createElement("style");

    style.textContent = `

        @media (max-width: 700px) {

            .mobile-menu-button {
                display: block !important;
            }

            .sidebar {
                transform: translateX(-100%);
                transition: transform 0.3s ease;
                z-index: 10000;
            }

            .sidebar.mobile-open {
                transform: translateX(0);
            }

            .main {
                margin-left: 0 !important;
                padding-top: 75px !important;
            }

        }

    `;

    document.head.appendChild(style);

}


/* =========================================================
   CONFIRM DELETE / RESET FUNCTION
   ========================================================= */

function confirmAction(message) {

    return window.confirm(
        message || "Are you sure you want to continue?"
    );

}


/* =========================================================
   RESET ALLOCATION FORM
   ========================================================= */

function resetAllocationForm() {

    const form =
        document.querySelector(
            'form[action*="allocation"]'
        );

    if (form) {

        form.reset();

        showNotification(
            "Allocation form has been reset.",
            "info"
        );

    }

}


/* =========================================================
   CALCULATE END FREQUENCY
   ========================================================= */

function calculateEndFrequency(start, bandwidth) {

    const startFrequency =
        parseFloat(start);

    const bandwidthValue =
        parseFloat(bandwidth);

    if (
        isNaN(startFrequency) ||
        isNaN(bandwidthValue)
    ) {

        return null;

    }

    return startFrequency + bandwidthValue;

}


/* =========================================================
   SPECTRUM RANGE VALIDATION
   ========================================================= */

function validateSpectrumRange(
    startFrequency,
    bandwidth
) {

    const start =
        parseFloat(startFrequency);

    const width =
        parseFloat(bandwidth);

    if (isNaN(start) || isNaN(width)) {

        return false;

    }

    if (start < 700) {

        return false;

    }

    if (start + width > 950) {

        return false;

    }

    return true;

}