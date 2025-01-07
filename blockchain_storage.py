import hashlib
import json
from flask import Flask, request, jsonify

app = Flask(__name__)

# Simpan blockchain dalam memory
blockchain = []

# Fungsi untuk membuat block baru
def create_block(previous_hash, document_hash=None):
    block = {
        'index': len(blockchain) + 1,
        'previous_hash': previous_hash,
        'document_hash': document_hash
    }
    blockchain.append(block)
    return block

# Inisialisasi genesis block
def initialize_blockchain():
    create_block(previous_hash="0")  # Genesis block tanpa dokumen

initialize_blockchain()

# Fungsi untuk menghitung hash dokumen
def calculate_hash(file_content):
    return hashlib.sha256(file_content).hexdigest()
@app.route('/')
def home():
    return jsonify({
        "message": "Welcome to the Document Blockchain API",
        "endpoints": {
            "upload": "POST /upload (Form-data with 'file')",
            "verify": "POST /verify (Form-data with 'file')",
            "blockchain": "GET /blockchain"
        }
    }), 200

# Endpoint untuk upload dokumen
@app.route('/upload', methods=['POST'])
def upload_document():
    if 'file' not in request.files:
        return jsonify({"message": "No file uploaded"}), 400
    file = request.files['file']
    file_content = file.read()
    document_hash = calculate_hash(file_content)
    
    # Tambahkan ke blockchain
    previous_hash = blockchain[-1]['document_hash'] if blockchain else "0"
    block = create_block(previous_hash, document_hash)
    
    return jsonify({
        "message": "Document uploaded and recorded in blockchain",
        "block": block
    }), 201

# Endpoint untuk verifikasi dokumen
@app.route('/verify', methods=['POST'])
def verify_document():
    if 'file' not in request.files:
        return jsonify({"message": "No file uploaded"}), 400
    file = request.files['file']
    file_content = file.read()
    document_hash = calculate_hash(file_content)
    
    # Cek apakah hash ada di blockchain
    for block in blockchain:
        if block['document_hash'] == document_hash:
            return jsonify({
                "message": "Document is valid and exists in blockchain",
                "block": block
            }), 200

    return jsonify({"message": "Document not found in blockchain"}), 404

# Endpoint untuk melihat seluruh blockchain
@app.route('/blockchain', methods=['GET'])
def get_blockchain():
    return jsonify({"blockchain": blockchain}), 200

if __name__ == '__main__':
    app.run(debug=True)
