async function createPoll() {
    const title = document.getElementById('poll-title').value;
    const optionsRaw = document.getElementById('poll-options').value;
    
    const options = optionsRaw.split(',').map(opt => opt.trim()).filter(opt => opt !== "");

    if(!title || options.length < 2) {
        alert("Isi judul dan minimal 2 opsi (pisahkan dengan koma) brok!");
        return;
    }

    try {
        const response = await fetch('/api/create', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ title, options })
        });
        
        const result = await response.json();
        if(result.status === "sukses") {
            const link = window.location.origin + '/vote/' + result.poll_id;
            const linkDiv = document.getElementById('result-link');
            linkDiv.innerHTML = `
                <p style="color: #4CAF50; margin-bottom: 10px;">Berhasil dibikin!</p>
                <p>Bagikan link ini:</p>
                <a href="${link}" style="color: #e94057; font-weight: bold; word-break: break-all;">${link}</a>
            `;
        } else {
            alert(result.message);
        }
    } catch (error) {
        console.error("Error:", error);
        // INI TAMBAHANNYA: Biar lu tau kalo servernya nolak
        alert("Waduh error brok, server gagal nyimpen data!"); 
    }
}

async function submitVote(pollId, pilihan) {
    try {
        const response = await fetch(`/api/vote/${pollId}`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ choice: pilihan })
        });
        
        const result = await response.json();
        if(result.status === "sukses") {
            alert("Thanks brok! Vote lu udah terekam.");
            window.location.href = `/dashboard/${pollId}`; 
        }
    } catch (error) {
        console.error("Error:", error);
    }
}

async function loadAnalytics(pollId) {
    try {
        const response = await fetch(`/api/stats/${pollId}`);
        const data = await response.json();
        
        const listContainer = document.getElementById('analytics-list');
        listContainer.innerHTML = '';

        if(data.length === 0) {
            listContainer.innerHTML = '<p>Belum ada data masuk.</p>';
            return;
        }

        data.reverse().forEach(vote => {
            const div = document.createElement('div');
            div.className = 'vote-item';
            div.innerHTML = `
                <strong>Pilihan:</strong> ${vote.choice} <br>
                <span class="time">Waktu: ${vote.waktu_ngisi}</span>
            `;
            listContainer.appendChild(div);
        });
    } catch (error) {
        console.error("Error loading stats:", error);
    }
}
