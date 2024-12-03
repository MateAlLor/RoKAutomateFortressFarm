import os.path
from adb_actions import automatizar
from cmd_Actions import iniciarADB


def principal():
    with open(os.path.join('data', 'ports.txt'), 'rt') as archivo:
        lineas = archivo.readlines()
        mainPort = lineas[0].replace('\n', '').split(':')[1]
        joinerPort = lineas[1].replace('\n', '').split(':')[1]

    mainID = f'localhost:{mainPort}'
    joinerID = f'localhost:{joinerPort}'

    iniciarADB(mainID, joinerID)

    automatizar(mainID, joinerID)


if __name__ == '__main__':
    principal()


