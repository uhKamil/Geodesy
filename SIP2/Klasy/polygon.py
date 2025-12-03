class Polygon:

    def __init__(self):
        self.points = []

    def add(self, *params):
        for p in params:
            self.points.append(p)
        print(self.points)

    def remove_point(self, p_index):
        del self.points[p_index]

    # def calculate_area(self):
    #     S = 0
    #     self.add(self.points[0])
    #     if len(self.points) > 3:
    #         for i in range(len(self.points)):
    #     else:
    #         return 0

    def __str__(self):
        p = ""
        i = 0
        for x, y in self.points:
            if i == len(self.points)-1:
                p += f"{x} {y}"
            else:
                p += f"{x} {y}" + ", "
            i += 1
        return "POLYGON (" + p + ")"


poly = Polygon()
poly.add([2, 2], [3, 3])
print(poly)
poly.remove_point(0)
print(poly)