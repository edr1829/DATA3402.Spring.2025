class Canvas:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        # Empty canvas is a matrix with element being the "space" character
        self.data = [[' '] * width for i in range(height)]

    def set_pixel(self, row, col, char='*'):
        self.data[row][col] = char

    def get_pixel(self, row, col):
        return self.data[row][col]
    
    def clear_canvas(self):
        self.data = [[' '] * self.width for i in range(self.height)]
    
    def v_line(self, x, y, w, **kargs):
        for i in range(x,x+w):
            self.set_pixel(i,y, **kargs)

    def h_line(self, x, y, h, **kargs):
        for i in range(y,y+h):
            self.set_pixel(x,i, **kargs)
            
    def line(self, x1, y1, x2, y2, **kargs):
        slope = (y2-y1) / (x2-x1)
        for y in range(y1,y2):
            x= int(slope * y)
            self.set_pixel(x,y, **kargs)
            
    def display(self):
        print("\n".join(["".join(row) for row in self.data]))
        
####################################################################################
import math
class Shape:

    def perimeter(self):
        raise NotImplementedError

    def area(self):
        raise NotImplementedError

    def check_parameters(self):
        raise NotImplementedError

    def check_x(self):
        raise NotImplementedError

    def check_y(self):
        raise NotImplementedError

    def perim_points(self):
        raise NotImplementedError

    def is_inside(self):
        raise NotImplementedError

    def overlaps(self, other):
        if any(other.is_inside(x, y) for x, y in self.perim_points()):
            return True
        if any(self.is_inside(x, y) for x, y in other.perim_points()):
            return True
        return False

    def __repr__(self):
        raise NotImplementedError

###################################################################################################

class Rectangle(Shape):
    def __init__(self, l, w, x, y):
        self.__l = l
        self.__w = w
        self.__x = x
        self.__y = y

    def perimeter(self):
        return (2 * self.__l) + (2 * self.__w)

    def area(self):
        return self.__l * self.__w

    def check_len(self):
        return self.__l

    def check_wid(self):
        return self.__w

    def check_parameters(self):
        print("Length:", self.check_len())
        print("Width:", self.check_wid())

    def check_x(self):
        return self.__x

    def check_y(self):
        return self.__y

    def perim_points(self):
        coordinates = []
        num_coordinates = min(16, self.perimeter())
        for i in range(num_coordinates):
            if i < num_coordinates // 4:
                x_point = self.__x + (i * self.__l // (num_coordinates // 4))
                y_point = self.__y
            elif i < num_coordinates // 2:
                x_point = self.__x + self.__l
                y_point = self.__y + ((i - num_coordinates // 4) * self.__w // (num_coordinates // 4))
            elif i < (3 * num_coordinates) // 4:
                x_point = self.__x + self.__l - ((i - num_coordinates // 2) * self.__l // (num_coordinates // 4))
                y_point = self.__y + self.__w
            else:
                x_point = self.__x
                y_point = self.__y + self.__w - ((i - (3 * num_coordinates) // 4) * self.__w // (num_coordinates // 4))

            coordinates.append((x_point, y_point))
        return coordinates

    def is_inside(self, x, y):
        left_x = self.__x
        right_x = self.__x + self.__l
        bottom_y = self.__y
        top_y = self.__y + self.__w
        return left_x < x < right_x and bottom_y < y < top_y

    def paint(self, canvas):
        for x, y in self.perim_points():
            if 0 <= x < canvas.width and 0 <= y < canvas.height:
                canvas.set_pixel(y, x, '*')

    def __repr__(self):
        return f"Rectangle({self.__l}, {self.__w}, {self.__x}, {self.__y})"


###################################################################################################

class Circle(Shape):
    def __init__(self, r, x, y):
        self.__r = r
        self.__x = x
        self.__y = y
        self.__pi = 3.14

    def perimeter(self):
        return (self.__pi * self.__r * 2)

    def area(self):
        return (self.__pi * self.__r) ** 2

    def check_rad(self):
        return self.__r

    def check_parameters(self):
        print("Radius:", self.__r)

    def check_x(self):
        return self.__x

    def check_y(self):
        return self.__y

    
    def perim_points(self):
        coordinates = []
        num_coordinates = 16
        for i in range(num_coordinates):
            angle = (i / num_coordinates) * 2 * math.pi
            px = int(self.__x + self.__r * math.cos(angle))
            py = int(self.__y + self.__r * math.sin(angle))
            coordinates.append((px, py))
        return coordinates

    def is_inside(self, x, y):
        center_x = self.__x
        center_y = self.__y
        radius = self.__r
        return (x - center_x) ** 2 + (y - center_y) ** 2 < radius ** 2

    def paint(self, canvas):
        for x, y in self.perim_points():
            if 0 <= x < canvas.width and 0 <= y < canvas.height:
                canvas.set_pixel(y, x, 'O')

    def __repr__(self):
        return f"Circle({self.__r}, {self.__x}, {self.__y})"


###################################################################################################

class Triangle(Shape):
    def __init__(self, a, b, c, x, y):
        self.__a = a
        self.__b = b
        self.__c = c
        self.__x = x
        self.__y = y

    def perimeter(self):
        return (self.__a + self.__b + self.__c)

    def area(self):
        semi_perim = self.perimeter() * 0.5
        return (semi_perim * (semi_perim - self.__a) * (semi_perim - self.__b) * (semi_perim - self.__c)) ** 0.5

    def check_side1(self):
        return self.__a

    def check_base(self):
        return self.__b

    def check_side2(self):
        return self.__c

    def check_parameters(self):
        print("Side 1:", self.check_side1())
        print("Base:", self.check_base())
        print("Side 2:", self.check_side2())

    def check_x(self):
        return self.__x

    def check_y(self):
        return self.__y

    def perim_points(self):
        coordinates = []
        num_coordinates = min(16, self.perimeter())
        x1, y1 = self.__x, self.__y
        x2, y2 = x1 + self.__b, y1
        x3, y3 = x1 + (self.__b // 2), y1 + self.__a
        for i in range(num_coordinates):
            if i < num_coordinates // 3:
                t = i / (num_coordinates // 3)
                px = x1 + (x3 - x1) * t
                py = y1 + (y3 - y1) * t
            elif i < (2 * num_coordinates) // 3:
                t = (i - num_coordinates // 3) / (num_coordinates // 3)
                px = x2 + (x3 - x2) * t
                py = y2 + (y3 - y2) * t
            else:
                t = (i - 2 * (num_coordinates // 3)) / (num_coordinates // 3)
                px = x1 + (x2 - x1) * t
                py = y1
            coordinates.append((int(px), int(py)))
        return coordinates


    def is_inside(self, x, y):
        x1, y1 = self.__x, self.__y
        x2, y2 = self.__x + self.__b, self.__y
        x3, y3 = self.__x + (self.__b // 2), self.__y + self.__a
        def tri_area(x1, y1, x2, y2, x3, y3):
            return abs((x1*(y2 - y3) + x2*(y3 - y1) + x3*(y1 - y2)) / 2.0)
        A = self.area()
        A1 = tri_area(x, y, x2, y2, x3, y3)
        A2 = tri_area(x1, y1, x, y, x3, y3)
        A3 = tri_area(x1, y1, x2, y2, x, y)
        return (A1 + A2 + A3 == A)

    def paint(self, canvas):
        for x, y in self.perim_points():
            if 0 <= x < canvas.width and 0 <= y < canvas.height:
                canvas.set_pixel(y, x, '^')

    def __repr__(self):
        return f"Triangle({self.__a}, {self.__b}, {self.__c}, {self.__x}, {self.__y})"

###################################################################################################

class CompoundShape(Shape):
    def __init__(self):
        self.shapes = []

    def add_shape(self, shape):
        self.shapes.append(shape)

    def paint(self, canvas):
        for shape in self.shapes:
            shape.paint(canvas)

    def __repr__(self):
        return f"CompoundShape({repr(self.shapes)})"

###################################################################################################

class RasterDrawing:
    def __init__(self, width, height, shapes=None):
        self.canvas = Canvas(width, height)
        self.shapes = shapes if shapes is not None else []

    def add_shape(self, shape):
        self.shapes.append(shape)

    def remove_shape(self, shape):
        for i, existing_shape in enumerate(self.shapes):
            if type(existing_shape) == type(shape) and existing_shape.__dict__ == shape.__dict__:
                del self.shapes[i]
                break

    def clear_shapes(self):
        self.shapes = []

    def paint(self):
        self.canvas.clear_canvas()
        for shape in self.shapes:
            shape.paint(self.canvas)
        self.canvas.display()

    def __repr__(self):
        return f"RasterDrawing({self.canvas.width}, {self.canvas.height}, {repr(self.shapes)})"

    def save(self, filename):
        with open(filename, "w") as f:
            f.write(repr(self))

    def load(filename):
        with open(filename, "r") as f:
            return eval(f.read())
