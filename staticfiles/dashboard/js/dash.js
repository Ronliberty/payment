document.addEventListener("DOMContentLoaded", () => {
    // === THEME TOGGLE ===
    const themeToggle = document.getElementById("theme-toggle");
    const body = document.body;

    if (localStorage.getItem("theme") === "dark") {
        body.classList.add("dark-mode");
        themeToggle.innerHTML = `<i class="fa fa-sun"></i> Light Mode`;
    } else {
        body.classList.remove("dark-mode");
        themeToggle.innerHTML = `<i class="fa fa-moon"></i> Dark Mode`;
    }

    themeToggle.addEventListener("click", () => {
        body.classList.toggle("dark-mode");
        if (body.classList.contains("dark-mode")) {
            localStorage.setItem("theme", "dark");
            themeToggle.innerHTML = `<i class="fa fa-sun"></i> Light Mode`;
        } else {
            localStorage.setItem("theme", "light");
            themeToggle.innerHTML = `<i class="fa fa-moon"></i> Dark Mode`;
        }
    });

    // === PROFILE DROPDOWN ===
    document.querySelector('.profile-img').addEventListener('click', function() {
        document.querySelector('.dropdown-menu').classList.toggle('active');
    });

    // === SIDEBAR TOGGLE ===
    const menuToggle = document.getElementById("menu-toggle");
    const sidebar = document.querySelector(".sidebar");

    menuToggle.addEventListener("click", () => {
        sidebar.classList.toggle("collapsed");
    });

    // === SEARCH FUNCTIONALITY ===
    const searchInput = document.getElementById("search-input");
    const overlaySearch = document.getElementById("overlay-search");
    const searchResults = document.getElementById("search-results");
    const overlayResults = document.getElementById("overlay-results");
    const searchOverlay = document.getElementById("search-overlay");
    const closeSearch = document.getElementById("close-search");

    const data = [
        "Order #1001 - Research Paper",
        "Order #1002 - Essay on Technology",
        "Order #1003 - Business Report",
        "Message from Client A",
        "Message from Client B",
        "New Order Request",
        "More Features Requested"
    ];

    function filterResults(query) {
        if (!query.trim()) {
            clearResults();
            return;
        }

        const filtered = data.filter(item =>
            item.toLowerCase().includes(query.toLowerCase())
        );

        displayResults(filtered);
    }

    function displayResults(results) {
        let resultHTML = results.length
            ? results.map(item => `<div class="search-item">${item}</div>`).join("")
            : `<div class="search-item">No results found</div>`;

        if (window.innerWidth <= 768) {
            overlayResults.innerHTML = resultHTML;
            overlayResults.style.display = "block";
        } else {
            searchResults.innerHTML = resultHTML;
            searchResults.style.display = "block";
        }

        // Add click event to each result item
        document.querySelectorAll(".search-item").forEach(item => {
            item.addEventListener("click", () => {
                alert(`You selected: ${item.textContent}`);
                clearResults();
            });
        });
    }

    function clearResults() {
        searchResults.innerHTML = "";
        overlayResults.innerHTML = "";
        searchResults.style.display = "none";
        overlayResults.style.display = "none";
    }

    // Open Search Overlay on Mobile
    searchInput.addEventListener("focus", () => {
        if (window.innerWidth <= 768) {
            searchOverlay.classList.add("active");
            overlaySearch.focus();
        }
    });

    // Close Search Overlay
    closeSearch.addEventListener("click", () => {
        searchOverlay.classList.remove("active");
        clearResults();
    });

    // Show results while typing
    searchInput.addEventListener("input", () => {
        if (window.innerWidth > 768) {
            filterResults(searchInput.value);
            searchResults.style.display = "block";
        }
    });

    overlaySearch.addEventListener("input", () => {
        filterResults(overlaySearch.value);
        overlayResults.style.display = "block";
    });

    // Hide results when clicking outside
    document.addEventListener("click", (e) => {
        if (!searchResults.contains(e.target) && e.target !== searchInput) {
            searchResults.style.display = "none";
        }
        if (!overlayResults.contains(e.target) && e.target !== overlaySearch) {
            overlayResults.style.display = "none";
        }
    });

    // Prevent closing results when clicking inside search results
    searchResults.addEventListener("click", (e) => e.stopPropagation());
    overlayResults.addEventListener("click", (e) => e.stopPropagation());

    // Ensure overlay doesn't open on desktops when resizing window
    window.addEventListener("resize", () => {
        if (window.innerWidth > 768) {
            searchOverlay.classList.remove("active");
            clearResults();
        }
    });
});
