from client import db


# Читання (Read)
def read(*args):

    # if no params, read all the collection
    if len(args) == 0:
        print(read_all())

    # if 1 param, find cat by name
    elif len(args) == 1:
        name = args[0]
        print(read_one(name))

    # if more params, raise Error
    else:
        print(
            f"Error! Only 1 parameter (cat's name) should be provided, instead {len(args)} were given"
        )


# Реалізуйте функцію для виведення всіх записів із колекції.
def read_all():

    # read collection
    cat_docs = db.cats.find({})

    # return list of cat docs
    return [cat for cat in cat_docs]


# Реалізуйте функцію, яка дозволяє користувачеві ввести ім'я кота та виводить інформацію про цього кота.
def read_one(name):

    # find cat in collection
    result = db.cats.find_one({"name": name})

    # if found, return cat doc, otherwise return "not found" message
    return (
        result if result != None else f"There is no cat named {name} in cats database"
    )


# Оновлення (Update)


def update(*args):

    # if 3 params, find cat by name
    if len(args) == 3:
        command, name, new_value = args

        if command == "age":
            print(update_age(name, new_value))

        elif command == "feature":
            print(update_feature(name, new_value))

        else:
            print(f"There is no such command {command}, please choose: age or feature")

    # if no required params or more, raise Error
    if len(args) != 3:
        print(
            f"Error! 3 parameters should be provided: <command: age or feature> <name> <new_value>"
        )


# Створіть функцію, яка дозволяє користувачеві оновити вік кота за ім'ям.
def update_age(name, new_value):

    # find cat in collection
    result = db.cats.find_one({"name": name})

    # if found, update cat doc, otherwise return "not found" message
    if result != None:
        db.cats.update_one({"name": name}, {"$set": {"age": new_value}})
        return db.cats.find_one({"name": name})
    else:
        return f"There is no cat named {name} in cats database"


# Створіть функцію, яка дозволяє додати нову характеристику до списку features кота за ім'ям.
def update_feature(name, new_value):

    # find cat in collection
    result = db.cats.find_one({"name": name})

    # if found, update cat doc, otherwise return "not found" message
    if result != None:
        db.cats.update_one({"name": name}, {"$push": {"features": new_value}})
        return db.cats.find_one({"name": name})
    else:
        return f"There is no cat named {name} in cats database"


# Видалення (Delete)


# Реалізуйте функцію для видалення запису з колекції за ім'ям тварини.
# Реалізуйте функцію для видалення всіх записів із колекції.


if __name__ == "__main__":
    update("age", "Stacy", 10)
