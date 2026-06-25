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
