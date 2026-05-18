import socket
from datetime import datetime
from logger import log_attack

from database import (
    insert_attack,
    insert_command,
    init_db,
    get_location
)

HOST = "0.0.0.0"
PORT = 2222


def start_honeypot():

    server = socket.socket(
        socket.AF_INET,
        socket.SOCK_STREAM
    )

    server.bind((HOST, PORT))

    server.listen(5)

    print(f"[+] SSH Honeypot running on port {PORT}")

    init_db()

    while True:

        client, addr = server.accept()

        print(f"[!] Connection from {addr}")

        log_attack(f"Connection from {addr}")

        client.send(
            b"Fake SSH Server\nLogin: "
        )

        username = client.recv(1024).decode().strip()

        client.send(b"Password: ")

        password = client.recv(1024).decode().strip()

        ip = addr[0]

        # CURRENT TIME

        current_time = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        # GET LOCATION

        country, city, latitude, longitude = get_location(ip)

        # INSERT ATTACK

        insert_attack(
            ip,
            username,
            password,
            country,
            city,
            latitude,
            longitude,
            current_time
        )

        client.send(
            b"\nAccess Granted!\n"
        )

        fake_files = {

            "passwords.txt":
            "admin:admin123\nroot:toor",

            "secret.txt":
            "Top Secret Internal Data",

            "config.txt":
            "Server Configuration Loaded"
        }

        while True:

            client.send(
                b"\nroot@server:~$ "
            )

            command = client.recv(
                1024
            ).decode().strip()

            # LOG COMMAND

            command_time = datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )

            insert_command(
                ip,
                command,
                command_time
            )

            # COMMANDS

            if command == "ls":

                client.send(
                    b"passwords.txt secret.txt config.txt\n"
                )

            elif command == "pwd":

                client.send(
                    b"/root\n"
                )

            elif command == "whoami":

                client.send(
                    b"root\n"
                )

            elif command == "help":

                client.send(
                    b"Commands: ls, pwd, whoami, cat, help, clear, exit\n"
                )

            elif command == "clear":

                client.send(b"\033c")

            elif command.startswith("cat "):

                parts = command.split(" ")

                if len(parts) > 1:

                    filename = parts[1]

                    if filename in fake_files:

                        content = fake_files[filename]

                        client.send(
                            content.encode() + b"\n"
                        )

                    else:

                        client.send(
                            b"File not found\n"
                        )

                else:

                    client.send(
                        b"Usage: cat <filename>\n"
                    )

            elif command == "exit":

                client.send(
                    b"Session terminated...\n"
                )

                break

            else:

                client.send(
                    b"Command not found\n"
                )

        log_attack(
            f"{ip} → {username}:{password}"
        )

        print(
            f"[DATABASE] {ip} → {username}:{password}"
        )

        client.close()