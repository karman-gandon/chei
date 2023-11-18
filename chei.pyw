import tkinter as tk
import socket
import threading

click_count = 0

def open_game(ip, port):
    def update_counter():
        global click_count
        click_count += 1
        label.config(text=f'У чея вырвали {click_count} волосиков')
        send_click()

    def send_click():
        client_socket.send("Clicked".encode())

    def send_message(event=None):
        message = entry.get()
        chat_list.insert(tk.END, f"You: {message}")
        entry.delete(0, tk.END)
        client_socket.send(f"Chat: {message}".encode())

    def receive():
        global click_count
        while True:
            try:
                data = client_socket.recv(1024)
                message = data.decode()
                if message.startswith('Hair count'):
                    hair_count = int(message.split(": ")[1])
                    click_count = hair_count
                    label.config(text=f'У чея вырвали {hair_count} волосиков')
                elif message.startswith('Chat:'):
                    chat_list.insert(tk.END, message[5:])
            except:
                root.deiconify()
                break

    root = tk.Toplevel(main_window)
    root.title('Многопользовательская игра')

    label = tk.Label(root, text='У чея вырвали 0 волосиков', font=('Arial', 18))
    label.pack(pady=20)

    button = tk.Button(root, text='Вырвать волосик', command=update_counter, font=('Arial', 14))
    button.pack(padx=10, pady=10)

    entry = tk.Entry(root, width=40)
    entry.pack(pady=10)
    entry.bind("<Return>", send_message)

    chat_list = tk.Listbox(root, width=60)
    chat_list.pack(padx=10, pady=10)

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        client_socket.connect((ip, port))
        client_socket.send("GetCount".encode())
        receive_thread = threading.Thread(target=receive)
        receive_thread.start()
        main_window.withdraw()
    except Exception as e:
        print(e)
        root.destroy()

def connect_to_server():
    ip = ip_entry.get()
    port = int(port_entry.get())
    open_game(ip, port)

# Создание главного окна
main_window = tk.Tk()
main_window.title('Главное меню')
main_window.geometry("300x200")

ip_label = tk.Label(main_window, text='IP сервера:')
ip_label.pack()
ip_entry = tk.Entry(main_window)
ip_entry.pack()

port_label = tk.Label(main_window, text='Порт:')
port_label.pack()
port_entry = tk.Entry(main_window)
port_entry.pack()

connect_button = tk.Button(main_window, text='Подключиться', command=connect_to_server, font=('Arial', 12))
connect_button.pack(pady=10)

main_window.mainloop()
