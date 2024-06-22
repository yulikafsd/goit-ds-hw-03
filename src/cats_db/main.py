from client import db


# Читання (Read)
def read(*args):

    # if no params, read all the collection
    if len(args) == 0:
        print(read_all())

    # if 1 param, find cat by name
    elif len(args) == 1:
        print(read_one(args[0]))

    # if more params, return Error message
    else:
        print(
            f"Error! Only 1 parameter (cat's name) can be provided, instead {len(args)} were given"
        )


# Реалізуйте функцію для виведення всіх записів із колекції.
def read_all() -> list:

    # read the collection and return list of cat docs
    return list(db.cats.find({}))


# Реалізуйте функцію, яка дозволяє користувачеві ввести ім'я кота та виводить інформацію про цього кота.
def read_one(name: str):

    # find cat in the collection
    result = db.cats.find_one({"name": name})

    # if found, return cat doc, otherwise return "not found" message
    return (
        result if result else f"Error! There is no cat named {name} in cats collection"
    )


# Оновлення (Update)
def update(*args):

    # if less required params or more, return Error message
    if len(args) != 3:
        print(
            f"Error! 3 parameters should be provided: <command: age or feature> <name> <new_value>"
        )
        return

    # if 3 params, find cat by name
    command, name, new_value = args

    if command == "age":
        print(update_age(name, new_value))

    elif command == "feature":
        print(update_feature(name, new_value))

    # If wrong command
    else:
        print(
            f"Error! There is no such command {command}, please choose: age or feature"
        )


# Створіть функцію, яка дозволяє користувачеві оновити вік кота за ім'ям.
def update_age(name: str, new_value: str):
    return update_cat(name, {"age": new_value})


# Створіть функцію, яка дозволяє додати нову характеристику до списку features кота за ім'ям.
def update_feature(name: str, new_value: str):
    return update_cat(name, {"$push": {"features": new_value}})


def update_cat(name: str, update: dict):

    # find cat in collection
    result = db.cats.find_one({"name": name})

    # if found, update cat doc, otherwise return "not found" message
    if result:
        db.cats.update_one(
            {"name": name}, {"$set": update} if "$push" not in update else update
        )
        return db.cats.find_one({"name": name})
    else:
        return f"Error! There is no cat named {name} in cats collection"


# Видалення (Delete)
def delete(*args):

    # if no params, delete all docs in the collection
    if len(args) == 0:
        print(delete_all())

    # if 1 param, delete cat by name
    elif len(args) == 1:
        print(delete_one(args[0]))

    # if more params, return Error message
    else:
        print(
            f"Error! Only 1 parameter (cat's name) can be provided, instead {len(args)} were given"
        )


# Реалізуйте функцію для видалення запису з колекції за ім'ям тварини.
def delete_one(name: str):

    # find cat in collection
    cat = db.cats.find_one({"name": name})

    # if there is no cat with this name in the collection, return Error message
    if not cat:
        return f"Error! There is no cat {name} in cats collection"

    # if found, delete cat doc and return "deleted" message
    db.cats.delete_one({"name": name})
    return (
        f"Cat doc of {name} was deleted"
        if not db.cats.find_one({"name": name})
        # if after delete cat is still in, return "still-in" message
        else f"Error! Somethimg went wrong. Cat doc {name} is still in the collection. Try again"
    )


# Реалізуйте функцію для видалення всіх записів із колекції.
def delete_all():
    db.cats.delete_many({})
    return f"All cat docs were deleted"


if __name__ == "__main__":
    # read()
    # read("Jonathan")
    # update("age", "Jonathan", 6)
    # update("feature", "Jonathan", "гладкий")
    # delete("Uberto")
