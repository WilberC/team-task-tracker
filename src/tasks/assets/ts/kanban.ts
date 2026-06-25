let draggedCard: HTMLElement | null = null;
let originParent: HTMLElement | null = null;
let originNextSibling: ChildNode | null = null;

const cardSelector = "[data-kanban-card]";
const dropzoneSelector = "[data-kanban-dropzone]";

function csrfToken(): string {
  const match = document.cookie.match(/(?:^|; )csrftoken=([^;]+)/);
  return match ? decodeURIComponent(match[1]) : "";
}

function createElementFromHtml(html: string): HTMLElement | null {
  const template = document.createElement("template");
  template.innerHTML = html.trim();
  const element = template.content.firstElementChild;
  return element instanceof HTMLElement ? element : null;
}

function refreshIcons(): void {
  const lucide = window.lucide;
  if (lucide && typeof lucide.createIcons === "function") {
    lucide.createIcons();
  }
}

function rollbackCard(): void {
  if (!draggedCard || !originParent) {
    return;
  }
  originParent.insertBefore(draggedCard, originNextSibling);
  draggedCard.classList.remove("is-saving", "is-dragging");
}

async function persistStatus(card: HTMLElement, status: string): Promise<void> {
  const url = card.dataset.statusUrl;
  if (!url) {
    throw new Error("Missing status URL.");
  }

  const formData = new FormData();
  formData.append("status", status);
  formData.append("response", "card");

  const response = await fetch(url, {
    method: "POST",
    credentials: "same-origin",
    headers: {
      "HX-Request": "true",
      "X-Kanban-Drop": "true",
      "X-CSRFToken": csrfToken()
    },
    body: formData
  });

  if (!response.ok) {
    throw new Error("Status update rejected.");
  }

  const replacement = createElementFromHtml(await response.text());
  if (replacement) {
    card.replaceWith(replacement);
    refreshIcons();
  }
}

document.addEventListener("dragstart", (event) => {
  const target = event.target;
  if (!(target instanceof Element)) {
    return;
  }

  const card = target.closest<HTMLElement>(cardSelector);
  if (!card) {
    return;
  }

  draggedCard = card;
  originParent = card.parentElement;
  originNextSibling = card.nextSibling;
  card.classList.add("is-dragging");
  event.dataTransfer?.setData("text/plain", card.dataset.taskId ?? "");
  if (event.dataTransfer) {
    event.dataTransfer.effectAllowed = "move";
  }
});

document.addEventListener("dragover", (event) => {
  const target = event.target;
  if (!(target instanceof Element)) {
    return;
  }

  const dropzone = target.closest<HTMLElement>(dropzoneSelector);
  if (!dropzone || !draggedCard) {
    return;
  }

  event.preventDefault();
  dropzone.classList.add("is-drop-target");
});

document.addEventListener("dragleave", (event) => {
  const target = event.target;
  if (target instanceof Element) {
    target.closest<HTMLElement>(dropzoneSelector)?.classList.remove("is-drop-target");
  }
});

document.addEventListener("drop", (event) => {
  const target = event.target;
  if (!(target instanceof Element) || !draggedCard) {
    return;
  }

  const dropzone = target.closest<HTMLElement>(dropzoneSelector);
  const nextStatus = dropzone?.dataset.kanbanDropzone;
  if (!dropzone || !nextStatus) {
    return;
  }

  event.preventDefault();
  dropzone.classList.remove("is-drop-target");
  dropzone.querySelector(".kanban-empty")?.remove();

  const previousStatus = draggedCard.dataset.taskStatus;
  dropzone.appendChild(draggedCard);

  if (previousStatus === nextStatus) {
    draggedCard.classList.remove("is-dragging");
    return;
  }

  draggedCard.classList.add("is-saving");
  void persistStatus(draggedCard, nextStatus).catch(() => {
    rollbackCard();
  });
});

document.addEventListener("dragend", () => {
  document
    .querySelectorAll<HTMLElement>(dropzoneSelector)
    .forEach((dropzone) => dropzone.classList.remove("is-drop-target"));
  draggedCard?.classList.remove("is-dragging");
});
