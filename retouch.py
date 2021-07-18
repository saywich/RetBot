import cv2 as cv
import numpy as np
import json
# import requests
# import bs4


class DMCColor:
    def __init__(self, name, color, code):
        super().__init__()
        self.name = name
        self.color = color
        self.code = int(code)


def get_dmc_colors():
    # page = requests.get("https://www.csh.rit.edu/~vance/pages/color.html")
    # print(page.status_code)
    # parser = bs4.BeautifulSoup(page.text, "html.parser")
    # dmcColorsInfo = parser.findAll('tr')
    # dmcColorsInfo.remove(dmcColorsInfo[0])
    # tds = []
    # tds = np.append(tds, parser.findAll('td'))
    # info = np.ndarray(shape=(len(tds) // 7, 7), dtype=bs4.element.Tag, buffer=tds)
    # dmc_colors_list = [DMCColor(info_elem[1].text,
    #                             (info_elem[2].text, int(info_elem[3].text), int(info_elem[4].text)),
    #                             info_elem[0].text) for info_elem in info]
    # for color in dmc_colors_list:
    #     if color.color[0] == '':
    #         color.color = ('255', 233, 233)
    #     else:
    #         color.color = (int(color.color[0]), color.color[1], color.color[2])
    # color_json = [color.__dict__ for color in dmc_colors_list]
    # with open('../data/dmc_colors.json', 'w') as f:
    #     json.dump(color_json, f)
    with open('data/json_files/dmc_colors.json') as f:
        data = json.load(f)
        dmc_colors_list = [DMCColor(color['name'], color['color'], color['code']) for color in data]
    return dmc_colors_list


def color_count(image):

    res = np.reshape(image, (image.size // 3, 3))
    return len(res), np.unique(res, axis=0)


def get_your_color(image_colors, dmc_colors_list):
    nearest_colors = []
    dmc_list_colors = [tuple(color.color) for color in dmc_colors_list]
    for color in image_colors:
        nearest = nearest_colour(dmc_list_colors, color)
        nearest_colors.append(nearest)
    return nearest_colors


def nearest_colour(subjects, color):
    return min(subjects, key=lambda subject: sum(abs((int(s) - int(q))) for s, q in zip(subject, color)))


def geniously_thing(image_path: [str, bytes], save_path: [str, bytes]):
    dmc_list = get_dmc_colors()
    dmc_list_colors = [tuple(color.color) for color in dmc_list]
    image = cv.imread(image_path)
    scale = max(len(image), len(image[0])) // 75
    for x in range(0, len(image[0]), scale):
        for y in range(0, len(image), scale):
            current_color = (image[y][x][0],
                             image[y][x][1],
                             image[y][x][2])
            current_color = nearest_colour(dmc_list_colors, current_color)
            for x1 in range(x, x + scale):
                for y1 in range(y, y + scale):
                    if y1 >= len(image) or x1 >= len(image[0]):
                        break
                    if y1 + scale >= len(image) > y1 or x1 + scale >= len(image[0]) > x1:
                        np.delete(image[y1], x1)
                    image[y1][x1] = current_color
    print(f'Высота: {len(image) // scale} крестиков')
    print(f'Ширина: {len(image[0]) // scale} крестиков')

    cv.imwrite(save_path, image)  # сохраняем результат :)
    colors = color_count(image)
    # print(colors[0], list(colors[1][0]))
    dmc_info = [(color.color, color.code, color.name) for color in dmc_list]
    ret_str = ''
    for color in colors[1]:
        for i in dmc_info:
            if list(color) == i[0]:
                ret_str += f'RGB: {i[0]} Code: {i[1]} Name: {i[2]}\n'

    return True, ret_str
