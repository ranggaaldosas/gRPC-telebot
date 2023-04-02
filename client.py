import grpc
import todo_pb2
import todo_pb2_grpc
import telegram
from telegram.ext import CommandHandler, Updater, PicklePersistence

# Inisialisasi bot telegram
bot = telegram.Bot(token='6116776439:AAFsxLB9FF_GMDWNAq3OGx6Qi1cjE3U6SrA')
updater = Updater(token='6116776439:AAFsxLB9FF_GMDWNAq3OGx6Qi1cjE3U6SrA',
                  use_context=True)
dispatcher = updater.dispatcher


def start(update, context):
    message = "Halo! Gunakan /add <judul todo> untuk menambahkan todo list\n\n"
    message += "Berikut adalah daftar command yang tersedia:\n"
    message += "/add <judul todo> - untuk menambahkan todo list\n"
    message += "/read <id todo> - untuk membaca todo list\n"
    message += "/update <id todo> <judul baru> - untuk mengubah todo list\n"
    message += "/delete <id todo> - untuk menghapus todo list"
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
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = todo_pb2_grpc.TodoServiceStub(channel)
        try:
            response = stub.Read(todo_pb2.ReadRequest(id=id))
            context.bot.send_message(chat_id=update.effective_chat.id,
                                     text=response.title)
        except grpc.RpcError as e:
            context.bot.send_message(chat_id=update.effective_chat.id,
                                     text=str(e))


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


start_handler = CommandHandler('start', start)
add_handler = CommandHandler('add', add)
read_handler = CommandHandler('read', read)
update_handler = CommandHandler('update', update)
delete_handler = CommandHandler('delete', delete)
dispatcher.add_handler(start_handler)
dispatcher.add_handler(add_handler)
dispatcher.add_handler(read_handler)
dispatcher.add_handler(update_handler)
dispatcher.add_handler(delete_handler)

updater.start_polling()
