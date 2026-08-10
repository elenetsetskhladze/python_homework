const TODOS_URL = "https://jsonplaceholder.typicode.com/todos";

const statusEl = document.getElementById("status");
const detailEl = document.getElementById("todo-detail");

function renderTodo(todo) {
  const { userId, id, title, completed } = todo;

  detailEl.innerHTML = `
    <dt>ID</dt>
    <dd>${id}</dd>

    <dt>User ID</dt>
    <dd>${userId}</dd>

    <dt>Title</dt>
    <dd>${title}</dd>

    <dt>Completed</dt>
    <dd>${completed ? "Yes" : "No"}</dd>
  `;
}

async function loadTodo() {
  const params = new URLSearchParams(window.location.search);
  const id = params.get("id");

  if (!id) {
    statusEl.textContent = "No todo id provided.";
    statusEl.classList.add("error");
    return;
  }

  statusEl.textContent = "Loading todo...";
  statusEl.classList.remove("error");

  try {
    const response = await fetch(`${TODOS_URL}/${id}`);

    if (!response.ok) {
      throw new Error(`Request failed with status ${response.status}`);
    }

    const todo = await response.json();

    renderTodo(todo);
    statusEl.textContent = "";
  } catch (error) {
    statusEl.textContent = `Failed to load todo: ${error.message}`;
    statusEl.classList.add("error");
  }
}

loadTodo();
