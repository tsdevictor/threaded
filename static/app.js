document.addEventListener("DOMContentLoaded", function () {
  const form = document.querySelector("#chat-form");
  const textarea = document.querySelector("#product");
  const submitButton = form.querySelector("button");
  const chatContainer = document.getElementById("chat-container");
  const charCounter = document.getElementById("char-counter");

  let currentController = null;
  let isLoading = false;

  function autosizeTextarea() {
    requestAnimationFrame(() => {
      textarea.style.height = "auto";
      textarea.style.height = `${textarea.scrollHeight}px`;
    });
  }

  function scrollElementToTopIfOffscreen(container, element) {
    const containerRect = container.getBoundingClientRect();
    const elementRect = element.getBoundingClientRect();
    const isOffscreen = elementRect.bottom > containerRect.bottom;

    if (isOffscreen) {
      element.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
  }

  autosizeTextarea();

  textarea.addEventListener("input", () => {
    autosizeTextarea();
    charCounter.innerText = `${textarea.value.length} / ${textarea.maxLength}`;
  });

  textarea.addEventListener("focus", () => {
    setTimeout(() => {
      window.scrollTo({ top: document.body.scrollHeight, behavior: "smooth" });
    }, 300);
  });

  function setLoadingState(loading) {
    isLoading = loading;
    textarea.disabled = loading;
    submitButton.disabled = false;

    if (loading) {
      submitButton.innerHTML = `
        <svg xmlns="http://www.w3.org/2000/svg" class="stop-icon" fill="none" viewBox="0 0 24 24" stroke="white" stroke-width="2">
          <rect x="6" y="6" width="12" height="12" rx="2" />
        </svg>`;
    } else {
      submitButton.innerHTML = `
        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="white" stroke-width="1.5">
          <path stroke-linecap="round" stroke-linejoin="round" d="M3 10.5l16.5-6-6 16.5-2.625-7.875L3 10.5z" />
        </svg>`;
    }
  }

  form.addEventListener("submit", async function (e) {
    e.preventDefault();
    if (isLoading) return;

    const intro = document.getElementById("intro-message");
    if (intro) intro.style.display = "none";

    const userInput = textarea.value.trim();
    if (!userInput) return;

    setLoadingState(true);

    textarea.value = "";
    autosizeTextarea();
    charCounter.innerText = "0 / 500";

    const userBubble = document.createElement("div");
    userBubble.className = "user-bubble";
    userBubble.innerText = userInput;
    chatContainer.appendChild(userBubble);
    scrollElementToTopIfOffscreen(chatContainer, userBubble);

    const loading = document.createElement("div");
    loading.className = "loader-container";
    loading.innerText = "Finding relevant subreddits...";
    chatContainer.appendChild(loading);

    currentController = new AbortController();

    submitButton.onclick = () => {
      if (currentController) {
        currentController.abort();
        loading.innerText = "Request cancelled.";
        setLoadingState(false);
        currentController = null;
      }
    };

    try {
      const formData = new FormData();
      formData.append("product", userInput);

      const response = await fetch("/", {
        method: "POST",
        body: formData,
        signal: currentController.signal
      });

      const html = await response.text();
      const parser = new DOMParser();
      const doc = parser.parseFromString(html, "text/html");
      const newMessages = doc.querySelector(".messages");

      if (newMessages) {
        loading.replaceWith(newMessages);
        scrollElementToTopIfOffscreen(chatContainer, newMessages);
      } else {
        loading.innerText = "No results found.";
      }
    } catch (err) {
      if (err.name === "AbortError") {
        console.log("Request aborted.");
      } else {
        console.error("Error during fetch:", err);
        loading.innerText = "Something went wrong. Please try again.";
      }
    }

    setLoadingState(false);
    textarea.disabled = false;
    textarea.focus();
    submitButton.onclick = null;
    currentController = null;
  });
});
