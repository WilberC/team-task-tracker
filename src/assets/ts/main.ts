import htmx from "htmx.org";
import "../../tasks/assets/ts/kanban";
import "../scss/main.scss";

declare global {
  interface Window {
    htmx: typeof htmx;
    lucide?: {
      createIcons: () => void;
    };
  }
}

window.htmx = htmx;

document.body.addEventListener("htmx:afterSwap", () => {
  window.lucide?.createIcons();
});

document.querySelectorAll<HTMLElement>("[data-auth-info-toggle]").forEach((toggle) => {
  const panelId = toggle.getAttribute("aria-controls");
  const popup = panelId ? document.getElementById(panelId) : null;
  if (!popup) {
    return;
  }
  const closeButtons = popup.querySelectorAll<HTMLElement>("[data-auth-info-close]");
  const accountButtons = popup.querySelectorAll<HTMLButtonElement>(
    "[data-auth-account-email]",
  );
  const usernameField = document.querySelector<HTMLInputElement>(
    ".auth-form input[name='username']",
  );
  const passwordField = document.querySelector<HTMLInputElement>(
    ".auth-form input[name='password']",
  );
  const submitButton = document.querySelector<HTMLButtonElement>(".auth-submit");

  const openPopup = () => {
    popup.hidden = false;
    popup.classList.add("is-open");
    toggle.setAttribute("aria-expanded", "true");
    popup.querySelector<HTMLElement>("input, button")?.focus();
  };

  const closePopup = () => {
    popup.classList.remove("is-open");
    popup.hidden = true;
    toggle.setAttribute("aria-expanded", "false");
    toggle.focus();
  };

  toggle.addEventListener("click", () => {
    if (popup.classList.contains("is-open")) {
      closePopup();
      return;
    }
    openPopup();
  });

  closeButtons.forEach((button) => {
    button.addEventListener("click", closePopup);
  });

  accountButtons.forEach((button) => {
    button.addEventListener("click", () => {
      if (!usernameField || !passwordField) {
        return;
      }

      usernameField.value = button.dataset.authAccountEmail ?? "";
      passwordField.value = button.dataset.authAccountPassword ?? "";
      usernameField.dispatchEvent(new Event("input", { bubbles: true }));
      passwordField.dispatchEvent(new Event("input", { bubbles: true }));
      usernameField.dispatchEvent(new Event("change", { bubbles: true }));
      passwordField.dispatchEvent(new Event("change", { bubbles: true }));
      closePopup();
      submitButton?.focus();
    });
  });

  popup.addEventListener("click", (event) => {
    if (event.target === popup) {
      closePopup();
    }
  });

  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape" && popup.classList.contains("is-open")) {
      closePopup();
    }
  });
});
