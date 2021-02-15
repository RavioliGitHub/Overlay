

class ReadBox:
    def __init__(self, id):
        self.x1 = 100
        self.y1 = 100
        self.x2 = 200
        self.y2 = 200
        self.bd_color = 'red'
        self.fill = 'white'
        self.width = 10
        self.name = None
        self.read_list = None
        self.id = id

    def draw(self, canvas):
        canvas.create_rectangle(self.x1, self.y1, self.x2, self.y2,
                                fill=self.fill, outline=self.bd_color, width=self.width)

    def object_to_dic(self):
        dic = {}
        for attribute in vars(self):
            print(attribute)
            dic[str(attribute)] = self.__getattribute__(attribute)
        return dic

    def dic_to_object(self, dic):
        for attribute in vars(self):
            for key, value in dic.items():
                if str(attribute) == key:
                    self.__setattr__(attribute, value)

