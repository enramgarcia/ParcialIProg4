import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base

USER = "root"
PASSWORD = "secret"
PORT = 3808
DB = "inventory"
SERVER = "localhost"

Base = declarative_base()


class Product(Base):
    __tablename__ = 'products'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    name = sqlalchemy.Column(sqlalchemy.String(length=100), unique=True)
    sku = sqlalchemy.Column(sqlalchemy.String(length=255))


def seed():
    products = [
        {'name': 'Rolls Royce Phantom', 'sku': '12p3o1230-9'}
    ]

    for definition in products:
        result_set = session.query(Product).filter_by(sku=definition['sku'])

        if result_set.count() > 0:
            continue

        product_definition = Product(
            name=definition['name'],
            sku=definition['sku']
        )

        session.add(product_definition)

    session.commit()


def print_product(definition):
    print(f"Producto: {definition.name}, SKU: {definition.sku}")


def show(sku):
    result_set = session.query(Product).filter_by(sku=sku)

    if result_set.count() == 0:
        print(f'No se encontró el SKU: {sku}')
        return

    for result in result_set:
        print_product(result)


def show_all():
    products_list = session.query(Product).all()

    for definition in products_list:
        print_product(definition)


def update(product, sku):
    result_set = session.query(Product).filter_by(sku=sku)

    if result_set.count() == 0:
        print(f'No se encontró el sku: {sku}')
        return

    for result in result_set:
        result.name = product

    session.commit()


def add():
    sku = input('SKU: ')
    product = input('Producto: ')

    result_set = session.query(Product).filter_by(sku=sku)

    if result_set.count() > 0:
        print(f'El sku {sku} ya existe.')
        return

    add_product = Product(name=product, sku=sku)
    session.add(add_product)
    session.commit()


def delete(sku):
    session.query(Product).filter_by(sku=sku).delete()
    session.commit()


if __name__ == '__main__':
    connection_string = f"mariadb+mariadbconnector://{USER}:{PASSWORD}@{SERVER}:{PORT}"

    print(connection_string)

    db_engine = sqlalchemy.create_engine(connection_string)

    db_engine.execute(f'Create Database if not exists {DB}')

    engine = sqlalchemy.create_engine(f"{connection_string}/{DB}")

    Base.metadata.create_all(engine)

    Session = sqlalchemy.orm.sessionmaker()
    Session.configure(bind=engine)
    session = Session()

    seed()

    while True:
        print('Menu')
        print('1- Mostrar todo')
        print('2- Agregar')
        print('3- Buscar Producto')
        print('4- Actualizar Producto')
        print('5- Borrar Producto')
        print('6- Salir')
        option = int(input('Opcion (1-6): '))

        if option == 1:
            show_all()
        elif option == 2:
            add()
        elif option == 3:
            search_product = input('SKU: ')
            show(search_product)
        elif option == 4:
            update_sku = input('SKU: ')
            search_product = input('Producto: ')
            update(search_product, update_sku)
        elif option == 5:
            search_product = input('SKU: ')
            delete(search_product)
        else:
            break


