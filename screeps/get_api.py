import screepsapi

TOKEN = '02065424-0901-4b8d-ada3-0542a94ffad7'
api = screepsapi.API(token=TOKEN)
memory = api.memory('', 'shard3')['data']

api.set_memory()