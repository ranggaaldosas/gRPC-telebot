import grpc
import firebase_admin
from firebase_admin import credentials, firestore
import todo_pb2
import todo_pb2_grpc
from concurrent import futures

# Inisialisasi firebase
cred = credentials.Certificate('./serviceAccountKey.json')
firebase_admin.initialize_app(cred)
db = firestore.client()


class TodoService(todo_pb2_grpc.TodoServiceServicer):

    def Create(self, request, context):
        todo_ref = db.collection('todo').document()
        todo_id = todo_ref.id
        todo_ref.set({'title': request.title})
        return todo_pb2.CreateResponse(message='Todo created with ID: ' +
                                       todo_id)

    def Read(self, request, context):
        todo_ref = db.collection('todo').document(request.id)
        todo = todo_ref.get()
        if todo.exists:
            return todo_pb2.ReadResponse(title=todo.to_dict()['title'])
        else:
            context.set_details('Todo not found')
            context.set_code(grpc.StatusCode.NOT_FOUND)
            return todo_pb2.ReadResponse()

    def Update(self, request, context):
        todo_ref = db.collection('todo').document(request.id)
        todo = todo_ref.get()
        if todo.exists:
            todo_ref.update({'title': request.title})
            return todo_pb2.UpdateResponse(message='Todo updated')
        else:
            context.set_details('Todo not found')
            context.set_code(grpc.StatusCode.NOT_FOUND)
            return todo_pb2.UpdateResponse()

    def Delete(self, request, context):
        todo_ref = db.collection('todo').document(request.id)
        todo = todo_ref.get()
        if todo.exists:
            todo_ref.delete()
            return todo_pb2.DeleteResponse(message='Todo deleted')
        else:
            context.set_details('Todo not found')
            context.set_code(grpc.StatusCode.NOT_FOUND)
            return todo_pb2.DeleteResponse()


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    todo_pb2_grpc.add_TodoServiceServicer_to_server(TodoService(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    serve()
