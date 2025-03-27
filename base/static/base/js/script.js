document.addEventListener("DOMContentLoaded", function () {
    // ✅ Fix: Ensure Modal is Hidden on Load
    try {
        document.getElementById("serviceModal").style.display = "none";
        document.body.style.overflow = "auto"; // Ensure scrolling is enabled
    } catch (error) {
        console.warn("Service modal not found on page load.");
    }

    // ✅ Dropdown Functionality
    const dropdownLinks = document.querySelectorAll(".dropdown > a");

    dropdownLinks.forEach(link => {
        link.addEventListener("click", function (e) {
            e.preventDefault();
            const parentDropdown = this.parentElement;
            const dropdownMenu = this.nextElementSibling;

            // Close all other dropdowns before opening the clicked one
            document.querySelectorAll(".dropdown").forEach(drop => {
                if (drop !== parentDropdown) {
                    drop.classList.remove("active");
                    let menu = drop.querySelector(".dropdown-menu");
                    if (menu) slideUp(menu);
                }
            });

            // ✅ Fix: Toggle only if necessary
            if (parentDropdown.classList.contains("active")) {
                parentDropdown.classList.remove("active");
                slideUp(dropdownMenu);
            } else {
                parentDropdown.classList.add("active");
                slideDown(dropdownMenu);
            }
        });
    });

    // ✅ Mobile Menu Toggle
    const menuToggle = document.querySelector(".menu-toggle");
    if (menuToggle) {
        menuToggle.addEventListener("click", function () {
            document.querySelector(".nav-links").classList.toggle("active");

            // Close all dropdowns when toggling mobile menu
            document.querySelectorAll(".dropdown-menu").forEach(menu => slideUp(menu));
            document.querySelectorAll(".dropdown").forEach(drop => drop.classList.remove("active"));
        });
    }

    // ✅ Hide Dropdowns when Clicking Outside
    document.addEventListener("click", function (e) {
        if (!e.target.closest(".dropdown, .menu-toggle, .nav-links")) {
            document.querySelectorAll(".dropdown-menu").forEach(menu => slideUp(menu));
            document.querySelectorAll(".dropdown").forEach(drop => drop.classList.remove("active"));
        }
    });

    // ✅ Ensure all dropdowns start hidden
    document.querySelectorAll(".dropdown-menu").forEach(menu => {
        menu.style.display = "none";
        menu.style.overflow = "hidden";
        menu.style.transition = "max-height 0.3s ease-out";
        menu.style.maxHeight = "0px";
    });

    // ✅ Function to Slide Down
    function slideDown(element) {
        element.style.display = "block";
        element.style.maxHeight = element.scrollHeight + "px";
    }

    // ✅ Function to Slide Up
    function slideUp(element) {
        element.style.maxHeight = "0px";
        setTimeout(() => element.style.display = "none", 300);
    }

    // ✅ Glide.js Carousel Initialization
    new Glide(".glide", {
        type: "carousel",
        perView: 1, // Default for larger screens
        gap: 20,
        autoplay: 5000,
        hoverpause: true,
        breakpoints: {
            1024: { perView: 1 },
            768: { perView: 1 },
            480: { perView: 1 }
        }
    }).mount();
});

// ✅ Toggle Cards
function toggleCard(card) {
    card.classList.toggle("active");
    let details = card.querySelector(".card-details");
    details.style.display = (details.style.display === "block") ? "none" : "block";
}

// ✅ Service Data
const serviceData = {
    service1: {
        title: "Essay Writing",
        description: "Our expert essay writing service ensures that students receive top-quality, well-researched essays..."
    },
    service2: {
        title: "Research Papers",
        description: "We provide meticulously researched academic papers designed to showcase critical thinking and analysis..."
    },
    service3: {
        title: "Proofreading",
        description: "Grammar errors, awkward phrasing, and unclear ideas can reduce the effectiveness of an academic paper..."
    },
    service4: {
        title: "Plagiarism Check",
        description: "We guarantee 100% plagiarism-free work..."
    }
};

// ✅ Open Service Modal
function openService(serviceKey) {
    const modal = document.getElementById("serviceModal");
    document.getElementById("modalTitle").innerText = serviceData[serviceKey].title;
    document.getElementById("modalDescription").innerText = serviceData[serviceKey].description;
    modal.style.display = "flex";
    document.body.style.overflow = "hidden";
}

// ✅ Close Service Modal
function closeService() {
    document.getElementById("serviceModal").style.display = "none";
    document.body.style.overflow = "auto";
}

// ✅ Show AI Matching Section
function showMatchForm() {
    document.getElementById("aiMatchSection").style.display = "block";
    document.getElementById("expertListSection").style.display = "none";
}

// ✅ Show Expert List Section
function showExpertList() {
    document.getElementById("expertListSection").style.display = "block";
    document.getElementById("aiMatchSection").style.display = "none";
}

// ✅ AI Matching System
function matchExpert() {
    let subject = document.getElementById("subject").value;
    let deadline = document.getElementById("deadline").value;
    let expert = subject === "Business" ? "Prof. Michael Smith" : "Dr. Sarah Johnson";
    document.getElementById("matchedExpert").innerText = `🎯 Recommended Expert: ${expert} for your ${subject} assignment due in ${deadline}`;
}

// ✅ Expert Profile Data
const expertProfiles = {
    expert1: {
        name: "Dr. Sarah Johnson",
        details: "PhD in English Literature with 10 years of academic writing experience."
    },
    expert2: {
        name: "Prof. Michael Smith",
        details: "MBA in Business Administration specializing in case studies and research papers."
    }
};

// ✅ Open Expert Profile Modal
function openExpertProfile(expertKey) {
    document.getElementById("expertName").innerText = expertProfiles[expertKey].name;
    document.getElementById("expertDetails").innerText = expertProfiles[expertKey].details;
    document.getElementById("expertModal").style.display = "flex";
}

// ✅ Close Expert Profile Modal
function closeExpertProfile() {
    document.getElementById("expertModal").style.display = "none";
}
// Function to Toggle FAQ Answers
function toggleFAQ(button) {
    let answer = button.nextElementSibling;
    let isVisible = answer.style.display === "block";

    // Close all other answers before opening new one
    document.querySelectorAll(".faq-answer").forEach(ans => ans.style.display = "none");

    // Toggle current FAQ
    answer.style.display = isVisible ? "none" : "block";
}

// Function for Live Search in FAQ
function searchFAQ() {
    let input = document.getElementById("faqSearch").value.toLowerCase();
    let faqItems = document.querySelectorAll(".faq-item");

    faqItems.forEach(item => {
        let question = item.querySelector(".faq-question").innerText.toLowerCase();
        if (question.includes(input)) {
            item.style.display = "block";
        } else {
            item.style.display = "none";
        }
    });
}
