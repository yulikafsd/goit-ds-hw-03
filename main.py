from client import db


# Читання (Read)
def read(*args):

    # if no params, read all the collection
    if len(args) == 0:
        print(readAll())

    # if 1 param, find cat by name
    elif len(args) == 1:
        name = args[0]
        print(readOne(name))

    # if more params, return Error message
    else:
        print(
            f"Error! Only 1 parameter (cat's name) can be provided, instead {len(args)} were given"
        )


# Реалізуйте функцію для виведення всіх записів із колекції.
def readAll():

    # read the collection
    cat_docs = db.cats.find({})

    # return list of cat docs
    return [cat for cat in cat_docs]


# Реалізуйте функцію, яка дозволяє користувачеві ввести ім'я кота та виводить інформацію про цього кота.
def readOne(name):

    # find cat in the collection
    result = db.cats.find_one({"name": name})

    # if found, return cat doc, otherwise return "not found" message
    return (
        result
        if result != None
        else f"Error! There is no cat named {name} in cats collection"
    )


# Оновлення (Update)
def update(*args):

    # if 3 params, find cat by name
    if len(args) == 3:
        command, name, new_value = args

        if command == "age":
            print(updateAge(name, new_value))

        elif command == "feature":
            print(updateFeature(name, new_value))

        else:
            print(
                f"Error! There is no such command {command}, please choose: age or feature"
            )

    # if no required params or more, return Error message
    if len(args) != 3:
        print(
            f"Error! 3 parameters should be provided: <command: age or feature> <name> <new_value>"
        )


# Створіть функцію, яка дозволяє користувачеві оновити вік кота за ім'ям.
def updateAge(name, new_value):

    # find cat in collection
    result = db.cats.find_one({"name": name})

    # if found, update cat doc, otherwise return "not found" message
    if result != None:
        db.cats.update_one({"name": name}, {"$set": {"age": new_value}})
        return db.cats.find_one({"name": name})
    else:
        return f"Error! There is no cat named {name} in cats collection"


# Створіть функцію, яка дозволяє додати нову характеристику до списку features кота за ім'ям.
def updateFeature(name, new_value):

    # find cat in collection
    result = db.cats.find_one({"name": name})

    # if found, update cat doc, otherwise return "not found" message
    if result != None:
        db.cats.update_one({"name": name}, {"$push": {"features": new_value}})
        return db.cats.find_one({"name": name})
    else:
        return f"Error! There is no cat named {name} in cats collection"


# Видалення (Delete)
def delete(*args):

    # if no params, delete all docs in the collection
    if len(args) == 0:
        print(deleteAll())

    # if 1 param, delete cat by name
    elif len(args) == 1:
        name = args[0]
        print(deleteOne(name))

    # if more params, return Error message
    else:
        print(
            f"Error! Only 1 parameter (cat's name) can be provided, instead {len(args)} were given"
        )


# Реалізуйте функцію для видалення запису з колекції за ім'ям тварини.
def deleteOne(name):

    # find cat in collection
    cat = db.cats.find_one({"name": name})

    # if there is no cat with this name in the collection, return Error message
    if cat == None:
        return f"Error! There is no cat {name} in cats collection"

    # if found, delete cat doc and return "deleted" message
    else:
        db.cats.delete_one({"name": name})
        result = db.cats.find_one({"name": name})
        return (
            f"Cat doc of {name} was deleted"
            # if after delete cat is still in, return "still-in" message
            if result == None
            else f"Error! Somethimg went wrong. Cat doc {name} is still in the collection. Try again"
        )


# Реалізуйте функцію для видалення всіх записів із колекції.
def deleteAll():
    db.cats.delete_many({})
    return f"All cat docs were deleted"
