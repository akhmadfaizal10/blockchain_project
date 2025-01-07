// Function to get the blockchain data from Flask server
function fetchBlockchain() {
    fetch('/chain')
        .then(response => response.json())
        .then(data => {
            const chainElement = document.getElementById('chain');
            chainElement.textContent = JSON.stringify(data.chain, null, 4);
        });
}

// Function to create a new transaction
document.getElementById('transaction-form').addEventListener('submit', function(event) {
    event.preventDefault();

    const sender = document.getElementById('sender').value;
    const recipient = document.getElementById('recipient').value;
    const amount = document.getElementById('amount').value;

    const transactionData = {
        sender: sender,
        recipient: recipient,
        amount: amount
    };

    fetch('/transactions/new', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(transactionData)
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('response').textContent = data.message;
        fetchBlockchain();
    })
    .catch(error => console.error('Error:', error));
});

// Function to mine a new block
document.getElementById('mine-button').addEventListener('click', function() {
    fetch('/mine')
        .then(response => response.json())
        .then(data => {
            document.getElementById('response').textContent = data.message;
            fetchBlockchain();
        })
        .catch(error => console.error('Error:', error));
});

// Fetch the blockchain data when the page loads
document.addEventListener('DOMContentLoaded', fetchBlockchain);
