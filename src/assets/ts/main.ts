import htmx from "htmx.org";
import "../scss/main.scss";

declare global {
  interface Window {
    htmx: typeof htmx;
  }
}

window.htmx = htmx;
