from src.repository import gpt, user, fitness

modules = [
    gpt,
    user,
    fitness,
]



# Alias for Repository
def Repository(model, session):
    name = f"{model.__name__}Repository"
    for module in modules:
        if name in dir(module):
            return getattr(module, name)(session=session)
    else:
        raise Exception(f"Repository {name} not found.")
