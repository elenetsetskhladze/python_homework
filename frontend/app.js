const TODOS_URL = "https://jsonplaceholder.typicode.com/todos";
const PAGE_SIZE = 20;

const statusEl = document.getElementById("status");
const listEl = document.getElementById("todo-list");
const paginationEl = document.getElementById("pagination");
const searchInput = document.getElementById("search-input");
const userFilter = document.getElementById("user-filter");
const completedFilter = document.getElementById("completed-filter");

let allTodos = [];
let filteredTodos = [];
let currentPage = 1;

function renderTodos(todos) {
  listEl.innerHTML = "";

  todos.forEach((todo) => {
    const { id, title, completed } = todo;

    const li = document.createElement("li");
    li.className = "todo-item";

    li.innerHTML = `
      <a class="todo-link" href="detail.html?id=${id}">
        <input type="checkbox" ${completed ? "checked" : ""} disabled />
        <span class="title">${title}</span>
      </a>
    `;

    listEl.appendChild(li);
  });
}

function populateUserFilter(todos) {
  const userIds = [...new Set(todos.map((todo) => todo.userId))].sort(
    (a, b) => a - b
  );

  userIds.forEach((userId) => {
    const option = document.createElement("option");
    option.value = String(userId);
    option.textContent = `User ${userId}`;
    userFilter.appendChild(option);
  });
}

function applyFilters() {
  const searchTerm = searchInput.value.trim().toLowerCase();
  const userId = userFilter.value;
  const completedValue = completedFilter.value;

  filteredTodos = allTodos.filter((todo) => {
    const matchesSearch = todo.title.toLowerCase().includes(searchTerm);
    const matchesUser = userId === "all" || String(todo.userId) === userId;
    const matchesCompleted =
      completedValue === "all" ||
      (completedValue === "completed" && todo.completed) ||
      (completedValue === "incomplete" && !todo.completed);

    return matchesSearch && matchesUser && matchesCompleted;
  });

  goToPage(1);
}

function renderPagination(totalItems) {
  paginationEl.innerHTML = "";

  const totalPages = Math.ceil(totalItems / PAGE_SIZE);
  if (totalPages <= 1) {
    return;
  }

  const prevBtn = document.createElement("button");
  prevBtn.textContent = "Prev";
  prevBtn.disabled = currentPage === 1;
  prevBtn.addEventListener("click", () => goToPage(currentPage - 1));
  paginationEl.appendChild(prevBtn);

  for (let page = 1; page <= totalPages; page++) {
    const pageBtn = document.createElement("button");
    pageBtn.textContent = String(page);
    pageBtn.className = page === currentPage ? "active" : "";
    pageBtn.addEventListener("click", () => goToPage(page));
    paginationEl.appendChild(pageBtn);
  }

  const nextBtn = document.createElement("button");
  nextBtn.textContent = "Next";
  nextBtn.disabled = currentPage === totalPages;
  nextBtn.addEventListener("click", () => goToPage(currentPage + 1));
  paginationEl.appendChild(nextBtn);
}

function goToPage(page) {
  currentPage = page;
  const start = (currentPage - 1) * PAGE_SIZE;
  const pageTodos = filteredTodos.slice(start, start + PAGE_SIZE);

  renderTodos(pageTodos);
  renderPagination(filteredTodos.length);
  statusEl.textContent = `Showing ${filteredTodos.length} of ${allTodos.length} todos`;
}

async function loadTodos() {
  statusEl.textContent = "Loading todos...";
  statusEl.classList.remove("error");

  try {
    const response = await fetch(TODOS_URL);

    if (!response.ok) {
      throw new Error(`Request failed with status ${response.status}`);
    }

    allTodos = await response.json();
    filteredTodos = allTodos;

    populateUserFilter(allTodos);
    goToPage(1);
  } catch (error) {
    statusEl.textContent = `Failed to load todos: ${error.message}`;
    statusEl.classList.add("error");
  }
}

searchInput.addEventListener("input", applyFilters);
userFilter.addEventListener("change", applyFilters);
completedFilter.addEventListener("change", applyFilters);

loadTodos();
