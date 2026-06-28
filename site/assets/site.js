const endpointRows = document.querySelectorAll("[data-copy]");

endpointRows.forEach((button) => {
  button.addEventListener("click", async () => {
    const value = button.dataset.copy;
    try {
      await navigator.clipboard.writeText(new URL(value, window.location.origin).toString());
      button.dataset.state = "copied";
      button.textContent = "Copied";
      window.setTimeout(() => {
        button.dataset.state = "";
        button.textContent = "Copy";
      }, 1200);
    } catch {
      window.location.href = value;
    }
  });
});

const skillsTable = document.querySelector("[data-skills-table]");
const routeGrid = document.querySelector("[data-route-grid]");
const countNode = document.querySelector("[data-skill-count]");
const searchInput = document.querySelector("[data-skill-search]");
const axisButtons = document.querySelectorAll("[data-axis]");

let registry = null;
let activeAxis = "all";

function axisLabel(axis) {
  return registry?.axes.find((item) => item.id === axis)?.label || axis;
}

function skillMatches(skill, query) {
  const haystack = [skill.slug, skill.name, skill.description, skill.axes.join(" ")].join(" ").toLowerCase();
  return haystack.includes(query.toLowerCase());
}

function renderSkills() {
  if (!registry || !skillsTable) return;

  const query = searchInput?.value.trim() || "";
  const skills = registry.skills.filter((skill) => {
    const axisOk = activeAxis === "all" || skill.axes.includes(activeAxis);
    return axisOk && skillMatches(skill, query);
  });

  skillsTable.innerHTML = skills
    .map(
      (skill) => `
        <tr>
          <td><a href="${skill.github_url}">${skill.slug}</a></td>
          <td>${skill.axes.map((axis) => `<span>${axisLabel(axis)}</span>`).join("")}</td>
          <td>${skill.description}</td>
          <td><code>${skill.install_command}</code></td>
        </tr>
      `
    )
    .join("");

  if (countNode) countNode.textContent = `${skills.length} skills`;
}

function renderRoutes() {
  if (!registry || !routeGrid) return;

  routeGrid.innerHTML = registry.axes
    .map(
      (axis) => `
        <article class="route-row">
          <div>
            <strong>${axis.label}</strong>
            <a href="#skills">${axis.route}</a>
          </div>
          <p>${axis.summary}</p>
          <code>${axis.skills.join("  ")}</code>
        </article>
      `
    )
    .join("");
}

axisButtons.forEach((button) => {
  button.addEventListener("click", () => {
    activeAxis = button.dataset.axis;
    axisButtons.forEach((item) => item.setAttribute("aria-pressed", String(item === button)));
    renderSkills();
  });
});

searchInput?.addEventListener("input", renderSkills);

fetch("/skills.json")
  .then((response) => response.json())
  .then((data) => {
    registry = data;
    renderRoutes();
    renderSkills();
  })
  .catch(() => {
    if (countNode) countNode.textContent = "offline fallback";
  });
