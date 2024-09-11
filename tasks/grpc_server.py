import grpc
from concurrent import futures
from .models import Task
import task_pb2
import task_pb2_grpc

class TaskManagerServicer(task_pb2_grpc.TaskManagerServicer):

    def CreateTask(self, request, context):
        task = Task.objects.create(
            title=request.title,
            description=request.description
        )
        return task_pb2.TaskID(id=task.id)

    def GetTask(self, request, context):
        try:
            task = Task.objects.get(id=request.id)
            return task_pb2.Task(
                id=task.id,
                title=task.title,
                description=task.description
            )
        except Task.DoesNotExist:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details('Task not found')
            return task_pb2.Task()

    def UpdateTask(self, request, context):
        try:
            task = Task.objects.get(id=request.id)
            task.title = request.title
            task.description = request.description
            task.save()
            return task_pb2.Empty()
        except Task.DoesNotExist:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details('Task not found')
            return task_pb2.Empty()

    def DeleteTask(self, request, context):
        try:
            task = Task.objects.get(id=request.id)
            task.delete()
            return task_pb2.Empty()
        except Task.DoesNotExist:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details('Task not found')
            return task_pb2.Empty()

    def ListTasks(self, request, context):
        tasks = Task.objects.all()
        task_list = task_pb2.TaskList(
            tasks=[
                task_pb2.Task(
                    id=task.id,
                    title=task.title,
                    description=task.description
                ) for task in tasks
            ]
        )
        return task_list

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    task_pb2_grpc.add_TaskManagerServicer_to_server(TaskManagerServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("Server gRPC running on port 50051")
    server.wait_for_termination()
