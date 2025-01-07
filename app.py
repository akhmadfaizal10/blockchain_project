from flask import Flask, render_template
from web3 import Web3

app = Flask(__name__)

# Hubungkan ke node Ethereum (gunakan Infura atau node lokal)
w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:8545'))

# Mengecek apakah Ethereum node terhubung
if w3.is_connected():
    print("Connected to Ethereum network")

@app.route('/')
def index():
    # Ambil saldo Ethereum dari wallet address
    wallet_address = '0x1f1979F90475b60c7D1e63B46EEb8050b4062Fb7'  # Ganti dengan alamat wallet Anda
    balance = w3.eth.get_balance(wallet_address)
    ether_balance = w3.fromWei(balance, 'ether')

    return render_template('index.html', balance=ether_balance)

if __name__ == '__main__':
    app.run(debug=True)
