# TodoBot: Efficient Todo List Management using gRPC and Telegram Bot


## Description
Sebuah project aplikasi todo list  menggunakan gRPC API dan protobuf untuk melakukan komunikasi antara client dan server, serta bot telegram sebagai interface untuk berkomunikasi dengan user. Aplikasi ini memungkinkan user untuk menambahkan, membaca, mengubah, dan menghapus todo list dengan mudah dan efisien melalui bot telegram. Aplikasi ini menggunakan database Firebase sebagai media penyimpanan data nya.

## Workflow
- Membuat protokol dengan menggunakan protobuf (**todo.proto**) untuk mendefinisikan struktur dan format pesan yang akan dikirimkan antara client dan server
- Menggunakan protobuf untuk menggenerate kode pada bahasa pemrograman Python yang akan digunakan untuk membuat server dan client ()
- Membuat server (**server.py**) pada bahasa pemrograman Python yang di-generate oleh protobuf, dengan menggunakan gRPC untuk mengekspos endpoint-endpoint yang dapat diakses oleh client
- Membuat client (**client.py**) pada bahasa pemrograman Python yang di-generate oleh protobuf, dengan menggunakan bot telegram sebagai interface untuk berkomunikasi dengan user dan mengakses endpoint-endpoint yang disediakan oleh server
- User mengirimkan command /add, /read, /update, atau /delete pada bot telegram
- Bot telegram mengirimkan request dengan data yang dibutuhkan ke server menggunakan protokol yang telah didefinisikan oleh protobuf
- Server melakukan operasi CRUD pada database Firebase sesuai dengan request yang diterima, dan mengembalikan response berupa pesan bahwa operasi telah berhasil dilakukan
- Seluruh komunikasi antara client dan server menggunakan protokol yang telah didefinisikan oleh protobuf dan diimplementasikan menggunakan gRPC, yang memastikan bahwa pesan yang dikirimkan antara client dan server memiliki format dan struktur yang sama, sehingga komunikasi dapat berjalan dengan efektif dan efisien.


## Deployment

How to run this project


#### Install Python Libraries
```bash
pip install grpcio grpcio-tools google-auth google-auth-oauthlib google-auth-httplib2 firebase-admin python-telegram-bot
```

#### Compile file proto

```bash
 python -m grpc_tools.protoc -I . --python_out=. --grpc_python_out=. todo.proto
```

#### Run Server

```bash
 python .\server.py  
```

#### Run Client

```bash
 python .\client.py  
```



## Documentation 

## Screenshots

![App Screenshot](https://i.ibb.co/LpTTFx8/Screenshot-34.png)
![App Screenshot](https://i.ibb.co/0nxqb1G/Screenshot-35.png)
