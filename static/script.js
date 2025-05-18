
document.getElementById('allocateForm').onsubmit = async (e) => {
    e.preventDefault();
    const res = await fetch('/allocate', { method: 'POST' });
    const data = await res.json();
    alert(data.message);

    const container = document.getElementById('results');
    container.innerHTML = '';
    for (let room in data.rooms) {
        const div = document.createElement('div');
        div.innerHTML = `<h3>Room ${room}</h3>`;
        const ul = document.createElement('ul');
        data.rooms[room].forEach(student => {
            const li = document.createElement('li');
            li.textContent = `${student.Name} (${student.StudentID}) - Year ${student.Year}`;
            ul.appendChild(li);
        });
        div.appendChild(ul);
        container.appendChild(div);
    }
};

async function searchStudent() {
    const query = document.getElementById('studentSearch').value;
    const res = await fetch('/search_student?query=' + query);
    const data = await res.json();
    document.getElementById('studentResult').innerText = JSON.stringify(data, null, 2);
}

async function viewRoom() {
    const query = document.getElementById('roomSearch').value;
    const res = await fetch('/view_room?room_id=' + query);
    const data = await res.json();
    document.getElementById('roomResult').innerText = JSON.stringify(data, null, 2);
}
