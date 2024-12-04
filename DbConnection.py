from motor.motor_asyncio import AsyncIOMotorClient

# client = AsyncIOMotorClient("mongodb://localhost:27017")
client = AsyncIOMotorClient("mongodb+srv://dottcorsoraffaele:RaurVSCNgoMP1mrf@cluster0.xpffn.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client.my_database
collection = db.items
