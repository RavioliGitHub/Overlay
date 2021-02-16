from typing import List, Any

from src.UI_Elements.ReadBoxFile import ReadBox
from src.UI_Elements.configFile import read_box_dic_list
from src.Control.FocusManager import FocusManager


class ReadBoxManager:
    box_list: List[ReadBox]

    def __init__(self):
        self.box_list = []
        self.configFile = "configFile.py"
        self.config_list_name = "read_box_dic_list"
        self.free_ids = list(range(1, 100))
        self.setup()

    def setup(self):
        for box_dic in read_box_dic_list:
            box = ReadBox(box_dic['id'])
            box.dic_to_object(box_dic)
            self.box_list.append(box)
            self.free_ids.remove(box.id)

    def create_new_read_box(self):
        id = self.free_ids.pop()
        box = ReadBox(id)
        self.box_list.append(box)
        return box

    def save_to_config(self):
        new_config_list = []
        for box in self.box_list:
            new_config_list.append(box.object_to_dic())

        config_str = "read_box_dic_list =" + str(new_config_list)
        writer = open(self.configFile, "w")
        writer.write(config_str)
        writer.close()

    def delete_box(self, box: ReadBox):
        id = box.id
        box.id = None
        self.free_ids.append(id)
        self.box_list.remove(box)

    def draw_all(self, canvas):
        for box in self.box_list:
            box.draw(canvas)

