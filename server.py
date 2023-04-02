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
        todo_ref.set({'title': request.title})
        return todo_pb2.CreateResponse(message='Todo created')

    def Read(self, request, context):
        todo_ref = db.collection('todo').document(request.id).get()
        if todo_ref.exists:
            todo_dict = todo_ref.to_dict()
            todo_dict['id'] = todo_ref.id
            return todo_pb2.ReadResponse(**todo_dict)
        else:
            context.set_details('Todo not found')
            context.set_code(grpc.StatusCode.NOT_FOUND)
            return todo_pb2.ReadResponse()

    def Update(self, request, context):
        todo_ref = db.collection('todo').document(request.id)
        if todo_ref.get().exists:
            todo_ref.update({'title': request.title})
            return todo_pb2.UpdateResponse(message='Todo updated')
        else:
            context.set_details('Todo not found')
            context.set_code(grpc.StatusCode.NOT_FOUND)
            return todo_pb2.UpdateResponse()

    def Delete(self, request, context):
        todo_ref = db.collection('todo').document(request.id)
        if todo_ref.get().exists:
            todo_ref.delete()
            return todo_pb2.DeleteResponse(message='Todo deleted')
        else:
            context.set_details('Todo not found')
            context.set_code(grpc.StatusCode.NOT_FOUND)
            return todo_pb2.DeleteResponse()

    def List(self, request, context):
        try:
            todos = []
            for todo in db.collection('todo').get():
                todo_dict = todo.to_dict()
                todo_dict['id'] = todo.id
                todos.append(todo_dict)
            return todo_pb2.ListResponse(todos=todos)
        except Exception as e:
            context.set_details(str(e))
            context.set_code(grpc.StatusCode.INTERNAL)
            return todo_pb2.ListResponse()


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    todo_pb2_grpc.add_TodoServiceServicer_to_server(TodoService(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    serve()
