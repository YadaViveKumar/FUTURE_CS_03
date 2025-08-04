Secure File Sharing System
This project is a secure file sharing web application built using Python Flask. It allows users to upload files, encrypt them using AES encryption with a password, and download them by entering the same password for decryption.

The encryption is done using AES-256 in EAX mode, and the key is derived from the password using PBKDF2. No encryption keys are stored on the server — the password itself is used to derive the key for each file.

The web interface is simple and allows:

Uploading a file with a password

Downloading the encrypted file using its filename and password

All encryption and decryption is handled securely using PyCryptodome.