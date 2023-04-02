import grpc
import todo_pb2
import todo_pb2_grpc
import telegram
from telegram.ext import CommandHandler, Updater, PicklePersistence

# Inisialisasi bot telegram
bot = telegram.Bot(token='YOUR_TELEBOT_TOKEN')
updater = Updater(token='YOUR_TELEBOT_TOKEN', use_context=True)
dispatcher = updater.dispatcher

import grpc
import todo_pb2
import todo_pb2_grpc


class TodoServiceClient:

    def __init__(self, host='localhost', port=50051):
        self.channel = grpc.insecure_channel(f"{host}:{port}")
        self.stub = todo_pb2_grpc.TodoServiceStub(self.channel)

    def Create(self, title):
        request = todo_pb2.CreateRequest(title=title)
        return self.stub.Create(request)

    def Read(self, id):
        request = todo_pb2.ReadRequest(id=id)
        return self.stub.Read(request)

    def Update(self, id, title):
        request = todo_pb2.UpdateRequest(id=id, title=title)
        return self.stub.Update(request)

    def Delete(self, id):
        request = todo_pb2.DeleteRequest(id=id)
        return self.stub.Delete(request)

    def List(self):
        request = todo_pb2.ListRequest()
        return self.stub.List(request)


todo_service = TodoServiceClient('localhost:50051')
dispatcher.bot_data['todo_service'] = todo_service


def start(update, context):
    message = "Halo! Gunakan daftar command berikut untuk menggunakan Aplikasi\n\n"
    message += "Berikut adalah daftar command yang tersedia:\n"
    message += "/add <judul todo> - untuk menambahkan todo list\n"
    message += "/read <id todo> - untuk membaca todo list\n"
    message += "/update <id todo> <judul baru> - untuk mengubah todo list\n"
    message += "/delete <id todo> - untuk menghapus todo list\n"
    message += "/list - untuk melihat semua todo list"
    context.bot.send_message(chat_id=update.effective_chat.id, text=message)


def add(update, context):
    title = context.args[0]
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = todo_pb2_grpc.TodoServiceStub(channel)
        response = stub.Create(todo_pb2.CreateRequest(title=title))
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=response.message)


def read(update, context):
    id = context.args[0]
    try:
        with grpc.insecure_channel('localhost:50051') as channel:
            stub = todo_pb2_grpc.TodoServiceStub(channel)
            response = stub.Read(todo_pb2.ReadRequest(id=id))
            context.bot.send_message(chat_id=update.effective_chat.id,
                                     text=response.todo.title)
    except grpc.RpcError as e:
        context.bot.send_message(chat_id=update.effective_chat.id, text=str(e))


def update(update, context):
    id = context.args[0]
    title = context.args[1]
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = todo_pb2_grpc.TodoServiceStub(channel)
        try:
            response = stub.Update(todo_pb2.UpdateRequest(id=id, title=title))
            context.bot.send_message(chat_id=update.effective_chat.id,
                                     text=response.message)
        except grpc.RpcError as e:
            context.bot.send_message(chat_id=update.effective_chat.id,
                                     text=str(e))


def delete(update, context):
    id = context.args[0]
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = todo_pb2_grpc.TodoServiceStub(channel)
        try:
            response = stub.Delete(todo_pb2.DeleteRequest(id=id))
            context.bot.send_message(chat_id=update.effective_chat.id,
                                     text=response.message)
        except grpc.RpcError as e:
            context.bot.send_message(chat_id=update.effective_chat.id,
                                     text=str(e))


def list(update, context):
    try:
        with grpc.insecure_channel('localhost:50051') as channel:
            stub = todo_pb2_grpc.TodoServiceStub(channel)
            response = stub.List(todo_pb2.ListRequest())
            todo_list = response.todos
            if not todo_list:
                context.bot.send_message(chat_id=update.effective_chat.id,
                                         text="Tidak ada todo list")
                return
            message = 'Todo list:\n'
            for todo in todo_list:
                message += f"- {todo.title} (ID: {todo.id})\n"
            context.bot.send_message(chat_id=update.effective_chat.id,
                                     text=message)
    except Exception as e:
        print(e)
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text="Gagal mengambil todo list")


start_handler = CommandHandler('start', start)
add_handler = CommandHandler('add', add)
read_handler = CommandHandler('read', read)
update_handler = CommandHandler('update', update)
delete_handler = CommandHandler('delete', delete)
list_handler = CommandHandler('list', list)
dispatcher.add_handler(start_handler)
dispatcher.add_handler(add_handler)
dispatcher.add_handler(read_handler)
dispatcher.add_handler(update_handler)
dispatcher.add_handler(delete_handler)
dispatcher.add_handler(list_handler)

updater.start_polling()
