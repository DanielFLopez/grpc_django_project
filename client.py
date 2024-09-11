import grpc
import task_pb2
import task_pb2_grpc

def run():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = task_pb2_grpc.TaskManagerStub(channel)

        task = task_pb2.Task(title="gRPC", description="just a descrioption")
        task_id = stub.CreateTask(task)
        print(f"Task created ID: {task_id.id}")

        task = stub.GetTask(task_id)
        print(f"Task: {task}")

        task.description = "Just sending a description"
        stub.UpdateTask(task)
        print("Task updated")

        task_list = stub.ListTasks(task_pb2.Empty())
        print("List of tasks:")
        for t in task_list.tasks:
            print(t)

        stub.DeleteTask(task_id)
        print("Task removed")

        task_list = stub.ListTasks(task_pb2.Empty())
        print("Updated list of tasks")
        for t in task_list.tasks:
            print(t)

if __name__ == '__main__':
    run()
