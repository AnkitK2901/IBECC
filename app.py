from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

P = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F
A = 0
B = 7
G = (2, 22)
ORDER = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141

def mod_inv(x, modulus):
    if x == 0:
        raise ValueError("Cannot compute modular inverse of zero.")
    return pow(x, modulus - 2, modulus)

def point_addition(P, Q):
    if P == (0, 0):
        return Q
    if Q == (0, 0):
        return P
    if P == Q:
        if P[1] == 0:
            return (0, 0)
        slope = (3 * P[0] * P[0] + A) * mod_inv(2 * P[1], ORDER) % ORDER
    else:
        if P[0] == Q[0]:
            return (0, 0)
        slope = (Q[1] - P[1]) * mod_inv(Q[0] - P[0], ORDER) % ORDER
    x_r = (slope * slope - P[0] - Q[0]) % ORDER
    y_r = (slope * (P[0] - x_r) - P[1]) % ORDER
    return (x_r, y_r)

def scalar_multiplication(k, P):
    result = (0, 0)
    addend = P
    while k:
        if k & 1:
            result = point_addition(result, addend)
        addend = point_addition(addend, addend)
        k >>= 1
    return result

def derive_key_from_identity(identity):
    base = 257
    identity_numeric = 0
    for char in identity:
        identity_numeric = (identity_numeric * base + ord(char)) % ORDER
    private_key = identity_numeric
    public_key = scalar_multiplication(private_key, G)
    return private_key, public_key

def shared_secret(private_key, public_key):
    shared = scalar_multiplication(private_key, public_key)
    return shared[0] % 256

def xor_encrypt_decrypt(data, key):
    if isinstance(data, str):
        data = data.encode('utf-8')
    key_stream = [key % 256 for _ in range(len(data))]
    encrypted_bytes = bytes([data[i] ^ key_stream[i] for i in range(len(data))])
    return encrypted_bytes

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/encrypt', methods=['POST'])
def encrypt():
    identity = request.form['identity']
    data = request.form['data']

    user_private_key, user_public_key = derive_key_from_identity(identity)
    ca_private_key, ca_public_key = derive_key_from_identity("CA")

    encryption_key = shared_secret(user_private_key, ca_public_key)
    encrypted_data = xor_encrypt_decrypt(data, encryption_key)

    return jsonify({'encrypted': encrypted_data.hex()})

@app.route('/decrypt', methods=['POST'])
def decrypt():
    try:
        identity = request.form['identity']
        encrypted_hex = request.form['encrypted_data']

        encrypted_data = bytes.fromhex(encrypted_hex)

        user_private_key, user_public_key = derive_key_from_identity(identity)
        ca_private_key, ca_public_key = derive_key_from_identity("CA")

        decryption_key = shared_secret(ca_private_key, user_public_key)
        decrypted_data_bytes = xor_encrypt_decrypt(encrypted_data, decryption_key)
        decrypted_data = decrypted_data_bytes.decode('utf-8')
        return jsonify({'decrypted': decrypted_data})
    except:
        return jsonify({'error': 'Decryption failed. Data does not match.'}), 400