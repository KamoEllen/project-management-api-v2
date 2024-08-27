from motor.motor_asyncio import AsyncIOMotorClient

# MONGO_DETAILS = "mongodb+srv://kamoellenkganakga:rPwflpR0FkblQKOa@manage-projects.hw9janx.mongodb.net/final-project-management-api?retryWrites=true&w=majority"
MONGO_DETAILS = "mongodb+srv://kamoellenkganakga:rPwflpR0FkblQKOa@manage-projects.hw9janx.mongodb.net/?retryWrites=true&w=majority&appName=final-project-management-api"

client = AsyncIOMotorClient(MONGO_DETAILS)

database = client['final-project-management-api']

projects_collection = database.get_collection("projects")

tasks_collection = database.get_collection("tasks")

milestones_collection = database.get_collection("milestones")

user_collection = database.get_collection("users")

progress_collection = database.get_collection("progress")
