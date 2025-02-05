document.addEventListener("DOMContentLoaded", () => {
    const contentDiv = document.getElementById("content");

    // Helper: Extract the new content from the full page response.
    function extractContent(htmlString) {
        const parser = new DOMParser();
        const doc = parser.parseFromString(htmlString, "text/html");
        const newContent = doc.getElementById("content");
        return newContent ? newContent.innerHTML : htmlString;
    }

    function updatePage(htmlString) {
        const parser = new DOMParser();
        const doc = parser.parseFromString(htmlString, "text/html");

        // Update the document title if a <title> tag is present.
        const newTitleElement = doc.querySelector("title");
        if (newTitleElement) {
            document.title = newTitleElement.textContent;
        }

        // Update the content container.
        contentDiv.innerHTML = extractContent(htmlString);
    }
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let cookie of cookies) {
                cookie = cookie.trim();
                if (cookie.startsWith(name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    const csrftoken = getCookie('csrftoken');

    // Function to load new content via AJAX for link navigation.
    async function loadContent(url, addToHistory = true) {
        try {
            document.dispatchEvent(new Event("page:unload"));
            const response = await fetch(url, {
                headers: {"X-Requested-With": "XMLHttpRequest"},
                credentials: "same-origin",
            });
            if (!response.ok) throw new Error("Network response was not ok");
            const htmlText = await response.text();
            updatePage(htmlText);
            if (addToHistory) {
                history.pushState(null, "", url);
            }

            document.dispatchEvent(new Event("page:load"));
        } catch (error) {
            console.error("Failed to load content:", error);
        }
    }

    // Intercept click events on links with the class "nav-link"
    document.addEventListener("click", (event) => {
        const target = event.target.closest("a.nav-link");
        if (target) {
            event.preventDefault();
            const url = target.href;
            loadContent(url);
        }
    });

    // Use event delegation to handle form submissions for forms with class "form-link"
    document.addEventListener("submit", async (e) => {
        const form = e.target.closest("form.form-link");
        if (form) {
            e.preventDefault();
            console.log("AJAX form submission intercepted");

            let url = form.getAttribute("action");
            const method = form.getAttribute("method").toUpperCase();

            if (method === "GET") {
                // For GET requests, convert form data to query string and append it to the URL
                const formData = new FormData(form);
                const params = new URLSearchParams(formData).toString();
                url = url.includes('?') ? `${url}&${params}` : `${url}?${params}`;
                try {
                    const response = await fetch(url, {
                        method: "GET",
                        headers: {"X-Requested-With": "XMLHttpRequest"},
                        credentials: "same-origin",
                    });
                    if (!response.ok) throw new Error("Network error");
                    const html = await response.text();
                    contentDiv.innerHTML = extractContent(html);
                } catch (error) {
                    console.error("Error during AJAX GET form submission:", error);
                }
            }
            else {
                // For POST (or other methods), send the form data in the request body.
                const formData = new FormData(form);
                console.log("Submitting to URL:", url);
                try {
                    const response = await fetch(url, {
                        method: method,
                        headers: {
                            "X-Requested-With": "XMLHttpRequest",
                            "X-CSRFToken": csrftoken,
                        },
                        credentials: "same-origin",
                        body: formData,
                    });
                    if (!response.ok) throw new Error("Network error");
                    const html = await response.text();
                    contentDiv.innerHTML = extractContent(html);
                } catch (error) {
                    console.error("Error during AJAX form submission:", error);
                }
            }
        }
    });

    // Handle back/forward navigation.
    window.addEventListener("popstate", () => {
        loadContent(location.href, false);
    });
});
