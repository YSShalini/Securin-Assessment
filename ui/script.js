const API_BASE = "http://localhost:8000/cves/list";

let limit = 10;
let offset = 0;
let total = 0;
let sortField = 'published';
let sortOrder = 'asc';
let currentPage = 1;
const maxVisiblePages = 5;

const headerMap = {
  cve_id: "CVE ID",
  published: "Published",
  last_modified: "Last Modified"
};

function formatDate(dateStr) {
  return new Date(dateStr).toLocaleDateString("en-GB", {
    day: "2-digit",
    month: "short",
    year: "numeric"
  });
}

async function loadCVEs() {
  const res = await fetch(`${API_BASE}?limit=${limit}&offset=${offset}&sortField=${sortField}&sortOrder=${sortOrder}`);
  const result = await res.json();

  total = result.total;
  document.getElementById("total").innerText = total;

  const tbody = document.querySelector("#cveTable tbody");
  tbody.innerHTML = "";

  if (sortField === 'published') {
    result.data.sort((a, b) => new Date(a.published) - new Date(b.published));
  }

  result.data.forEach(cve => {
    const row = document.createElement("tr");
    row.innerHTML = `
      <td>${cve.cve_id}</td>
      <td>${cve.identifier ?? "-"}</td>
      <td>${formatDate(cve.published)}</td>
      <td>${formatDate(cve.last_modified)}</td>
      <td>${cve.status}</td>
    `;
    row.style.cursor = "pointer";
    row.onclick = () => window.location.href = `cve.html?id=${cve.cve_id}`;
    tbody.appendChild(row);
  });

  document.getElementById("pageInfo").innerHTML =
    `<span class="page-info">${offset + 1}-${Math.min(offset + limit, total)} of ${total} records</span>`;

  renderPages();
  updateHeaderArrows();
}

function renderPages() {
  const pageCount = Math.ceil(total / limit);
  const container = document.getElementById("pageNumbers");
  container.innerHTML = "";

  const prevBtn = document.createElement("button");
  prevBtn.innerText = "<";
  prevBtn.disabled = currentPage === 1;
  prevBtn.onclick = () => { currentPage--; offset = (currentPage - 1) * limit; loadCVEs(); };
  container.appendChild(prevBtn);

  let startPage = Math.max(1, currentPage - Math.floor(maxVisiblePages / 2));
  let endPage = startPage + maxVisiblePages - 1;
  if (endPage > pageCount) {
    endPage = pageCount;
    startPage = Math.max(1, endPage - maxVisiblePages + 1);
  }

  for (let i = startPage; i <= endPage; i++) {
  const span = document.createElement("span");
  span.innerText = i;
  if (i === currentPage) span.classList.add("active");
  
  span.onclick = () => {
    currentPage = i;
    offset = (currentPage - 1) * limit;
    loadCVEs();
  };
  container.appendChild(span);
}


  const nextBtn = document.createElement("button");
  nextBtn.innerText = ">";
  nextBtn.disabled = currentPage === pageCount;
  nextBtn.onclick = () => { currentPage++; offset = (currentPage - 1) * limit; loadCVEs(); };
  container.appendChild(nextBtn);
}

function sortTable(field) {
  if (sortField === field) {
    sortOrder = sortOrder === 'asc' ? 'desc' : 'asc';
  } else {
    sortField = field;
    sortOrder = 'asc';
  }
  offset = 0;
  currentPage = 1;
  loadCVEs();
}


function updateHeaderArrows() {
  document.querySelectorAll('#cveTable th').forEach(th => {
    const field = th.getAttribute("onclick")?.match(/sortTable\('(.+)'\)/)?.[1];
    if (field) {
      const arrow = field === sortField ? (sortOrder === 'asc' ? '▲' : '▼') : '';
      th.innerText = `${headerMap[field]} ${arrow}`;
    }
  });
}

document.getElementById("pageSize").onchange = e => {
  limit = parseInt(e.target.value);
  currentPage = 1;
  offset = 0;
  loadCVEs();
};

window.addEventListener("DOMContentLoaded", loadCVEs);
