"""
File: BobClient_receive.py
Author: Andy Xiao

References:
- ChatGPT: OpenAI. (2024, September). ChatGPT. Retrieved from https://chatgpt.com/
- GitHub Copilot: GitHub. (2025, April). Github Copilot. Retrieved from https://github.com/features/copilot?ef_id=_k_Cj0KCQjw782_BhDjARIsABTv_JDvrUsct27-PEXkLAiXl1PdcIt8sSHCqOAikO17q2LlsHSc5oLj2bgaAuZZEALw_wcB_k_&OCID=AIDcmmb150vbv1_SEM__k_Cj0KCQjw782_BhDjARIsABTv_JDvrUsct27-PEXkLAiXl1PdcIt8sSHCqOAikO17q2LlsHSc5oLj2bgaAuZZEALw_wcB_k_&gad_source=1&gclid=Cj0KCQjw782_BhDjARIsABTv_JDvrUsct27-PEXkLAiXl1PdcIt8sSHCqOAikO17q2LlsHSc5oLj2bgaAuZZEALw_wcB
"""

import socket
import ssl


def receive_messages(recipient_email, port):
    try:
        context = ssl.create_default_context()
        context.load_verify_locations(cafile="/Users/andyxiao/PostGradProjects/CryptoGuardAI/server.crt")

        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket = context.wrap_socket(client_socket, server_hostname='localhost')
        client_socket.connect(('localhost', port))

        response = client_socket.recv(1024).decode("utf-8")
        print(response)
        client_socket.send(recipient_email.encode("utf-8"))

        response = client_socket.recv(1024).decode("utf-8")
        print(response)
        client_socket.send("password123".encode("utf-8")) 

        response = client_socket.recv(1024).decode("utf-8")
        print(response)
    
        if "+OK" in response:
            client_socket.send(recipient_email.encode("utf-8"))
            response = client_socket.recv(1024).decode("utf-8")
            print(response)
            if "+OK" in response:
                while True:
                    msg_info = client_socket.recv(1024).decode("utf-8")
                    if not msg_info:
                        break
                    print(f"Email received: {msg_info}")
                    message = client_socket.recv(4096).decode("utf-8")
                    print(f"Message content: {message}")
            else:
                print("No emails to receive.")
        else:
            print("Authentication failed.")
    except ssl.SSLError as e:
        print(f"SSL error: {e}")
    except ConnectionError as e:
        print(f"Connection error: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        client_socket.close()

if __name__ == "__main__":
    receive_messages("bob@example.com", 1102)
