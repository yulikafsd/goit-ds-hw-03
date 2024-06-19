from client import db


# Читання (Read)
def read(*args):

    # if no params, read all the collection
    if len(args) == 0:
        print(readAll())

    # if 1 param, find cat by name
    elif len(args) == 1:
        print(readOne(args[0]))

    # if more params, raise Error
    else:
        print(
            f"Error! Only 1 parameter (cat's name) should be provided, instead {len(args)} were given"
        )


# Реалізуйте функцію для виведення всіх записів із колекції.
def readAll():

    # read collection
    cat_docs = db.cats.find({})

    # return list of cat docs
    return [cat for cat in cat_docs]


# Реалізуйте функцію, яка дозволяє користувачеві ввести ім'я кота та виводить інформацію про цього кота.
def readOne(name):

    # find cat in collection
    result = db.cats.find_one({"name": name})

    # if found, return cat doc, otherwise return "not found" message
    return (
        result if result != None else f"There is no cat named {name} in cats database"
    )


# Оновлення (Update)


# Створіть функцію, яка дозволяє користувачеві оновити вік кота за ім'ям.
# Створіть функцію, яка дозволяє додати нову характеристику до списку features кота за ім'ям.
def update():
    pass


# Видалення (Delete)


# Реалізуйте функцію для видалення запису з колекції за ім'ям тварини.
# Реалізуйте функцію для видалення всіх записів із колекції.
def delete():
    pass


if __name__ == "__main__":
    read("Giuseppina")
