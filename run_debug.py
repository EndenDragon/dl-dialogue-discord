from dldialogue import app

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True, ssl_context=("keys/fullchain.pem", "keys/privkey.pem"))
