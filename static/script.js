async function encryptData() {
    document.getElementById('encrypt-error').innerText = '';
    document.getElementById('encrypted-result').innerText = '';

    const identity = document.getElementById('identity').value;
    const data = document.getElementById('data').value;

    try {
        const response = await fetch('/encrypt', {
            method: 'POST',
            headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
            body: `identity=${encodeURIComponent(identity)}&data=${encodeURIComponent(data)}`
        });

        const result = await response.json();

        if (!response.ok) {
            document.getElementById('encrypt-error').innerText = result.error;
        } else {
            document.getElementById('encrypted-result').innerText = 'Encrypted Data: ' + result.encrypted;
        }
    } catch (error) {
        document.getElementById('encrypt-error').innerText = 'An error occurred while encrypting data.';
    }
}

async function decryptData() {
    document.getElementById('decrypt-error').innerText = '';
    document.getElementById('decrypted-result').innerText = '';

    const identity = document.getElementById('identity').value;
    const encryptedData = document.getElementById('encrypted_data').value;

    try {
        const response = await fetch('/decrypt', {
            method: 'POST',
            headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
            body: `identity=${encodeURIComponent(identity)}&encrypted_data=${encodeURIComponent(encryptedData)}`
        });

        const result = await response.json();

        if (!response.ok) {
            document.getElementById('decrypt-error').innerText = result.error;
        } else {
            document.getElementById('decrypted-result').innerText = 'Decrypted Data: ' + result.decrypted;
        }
    } catch (error) {
        document.getElementById('decrypt-error').innerText = 'An error occurred while decrypting data.';
    }
}

document.addEventListener('DOMContentLoaded', (event) => {
    document.getElementById("data").value = "Amount: 4500 INR, To: USER";
});