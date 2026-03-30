const API = "http://127.0.0.1:8000"

async function searchPapers() {
    const query = document.getElementById("searchInput").value

    const res = await fetch(`${API}/search`, {
        method: "POST",
        headers: {"Content-Type":"application/json"},
        body: JSON.stringify({query})
    })

    const data = await res.json()

    document.getElementById("searchResults").innerHTML =
    data.results.map((p, i) => `
    <div class="card">

    <b>${p.title}</b>

    <p>
    ${p.abstract.substring(0,180)}
    <span id="dots-${i}">...</span>
    <span id="more-${i}" style="display:none;">
    ${p.abstract.substring(180)}
    </span>
    </p>

    <div style="margin-top:10px;">
    <button 
    id="btn-${i}" 
    data-expanded="false"
    onclick="toggleReadMore(${i})">
    Read More
    </button>

    <a href="${p.pdf_url}" target="_blank">
    <button>Open PDF</button>
    </a>
    </div>

    </div>
    `).join("")
}

async function askAI() {
    const question = document.getElementById("askInput").value

    const res = await fetch(`${API}/ask`, {
        method:"POST",
        headers: {"Content-Type":"application/json"},
        body: JSON.stringify({question})
    })

    const data = await res.json()

    document.getElementById("askResults").innerHTML = `
        <div class="card">
            <b>Answer:</b>
            <p>${data.answer}</p>
        </div>
    `
}


async function explainPaper() {
    const text = document.getElementById("explainInput").value

    const res = await fetch(`${API}/explain`, {
        method:"POST",
        headers: {"Content-Type":"application/json"},
        body: JSON.stringify({text})
    })

    const data = await res.json()

    document.getElementById("explainResults").innerHTML = `
        <div class="card">
            <b>${data.title}</b>
            <p>${data.explanation}</p>
        </div>
    `
}

function toggleReadMore(i) {
    const dots = document.getElementById(`dots-${i}`)
    const more = document.getElementById(`more-${i}`)
    const btn = document.getElementById(`btn-${i}`)

    if (btn.dataset.expanded === "true") {
        // collapse
        more.style.display = "none"
        dots.style.display = "inline"
        btn.innerText = "Read More"
        btn.dataset.expanded = "false"
    } else {
        // expand
        more.style.display = "inline"
        dots.style.display = "none"
        btn.innerText = "Read Less"
        btn.dataset.expanded = "true"
    }
}

