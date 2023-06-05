import overpy
import requests
import json
import shutil
import os

PATH = 'results'


def create_folder(folder):
    try:
        os.mkdir(folder)
    except:
        pass

def clear_folder(folder):
    try:
        shutil.rmtree(folder, True)
        os.mkdir(folder)
    except:
        print('Error folder1')


def get_folder_name(location, coords):
    return f'{PATH}/' + location + '/' + coords.replace(', ', '-')


def save_images(location, coord):
    folder = get_folder_name(location, coord)
    create_folder(folder)
    for heading in range(0, 360, 90):
        name = f'{folder}/{str(heading).rjust(3, "0")}.jpg'
        if os.path.exists(name):
            pass
            # print(f'{name} - already exists')
        else:
            res_image = requests.get('https://maps.googleapis.com/maps/api/streetview?size=2400x2400' +
                                f'&location={coord}' +
                                f'&heading={heading}' +
                                '&radius=1234&key=AIzaSyAjSPCl4G3JOz8cXWL5GGiczLQHeVV37D8', stream=True)
            with open(name, 'wb') as f:
                shutil.copyfileobj(res_image.raw, f)


def get_images(location):
    # получаем координаты
    api = overpy.Overpass()
    Data = api.query(f"""
    area[name="{location}"];
    (
        node["traffic_sign"~"maxspeed"](area);
    );
    out body;
    >;
    out skel qt;
    """)

    # записываем результаты
    coords = [str(way.lat) + ', ' + str(way.lon) for way in Data.nodes]
    coords.sort()

    print(f'Found {len(coords)} objects for location {location}')
    create_folder(f'{PATH}/{location}')

    # проверка, есть ли панорама/изображение в google steert view и если есть, то сохранить изображение
    for coord in coords:
        res = requests.get('https://maps.googleapis.com/maps/api/streetview/metadata?size=600x300&location=' +
                        coord+'&key=AIzaSyAjSPCl4G3JOz8cXWL5GGiczLQHeVV37D8')
        res_json = json.loads(res.text)
        if res_json.get('status') == 'OK':
            save_images(location, coord)

create_folder(PATH)