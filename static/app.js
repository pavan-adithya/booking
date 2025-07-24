document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('bookingForm');
    const ticketsList = document.getElementById('ticketsList');

    function fetchTickets() {
        fetch('/tickets')
            .then(res => res.json())
            .then(data => {
                ticketsList.innerHTML = '';
                if (data.length === 0) {
                    ticketsList.innerHTML = '<p>No tickets booked yet.</p>';
                } else {
                    data.forEach(ticket => {
                        const div = document.createElement('div');
                        div.className = 'ticket';
                        div.textContent = `${ticket.name} booked ${ticket.quantity} for ${ticket.event}`;
                        ticketsList.appendChild(div);
                    });
                }
            });
    }

    form.addEventListener('submit', function(e) {
        e.preventDefault();
        const name = document.getElementById('name').value;
        const event = document.getElementById('event').value;
        const quantity = document.getElementById('quantity').value;
        fetch('/book', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ name, event, quantity })
        })
        .then(res => res.json())
        .then(data => {
            alert(data.message || data.error);
            fetchTickets();
            form.reset();
        });
    });

    fetchTickets();
}); 