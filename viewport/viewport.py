class Point:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y


class Rectangle:
    def __init__(self, p1, p2):
        self.left_top = p1
        self.right_bottom = p2

    def intersect(self, other):
        left = max(self.left_top.x, other.left_top.x)
        top = max(self.left_top.y, other.left_top.y)
        right = min(self.right_bottom.x, other.right_bottom.x)
        bottom = min(self.right_bottom.y, other.right_bottom.y)
        if left < right and bottom > top:
            return Rectangle(Point(left, top), Point(right, bottom))
        else:
            return None

    def width(self):
        return self.right_bottom.x - self.left_top.x

    def height(self):
        return self.right_bottom.y - self.left_top.y

    def to_pil_corr(self):
        return self.left_top.x, self.left_top.y, self.right_bottom.x, self.right_bottom.y

    def __getitem__(self, item) -> Point | None:
        if item == 0:
            return self.left_top
        elif item == 1:
            return self.right_bottom
        else:
            return None


class ViewPort:
    def __init__(self, screen_width: int, screen_height: int):
        # screen_是屏幕中能够用来展示图片的窗口实际大小，它与viewport的长宽比始终保持一致。
        self.screen_width = screen_width
        self.screen_height = screen_height
        # image_是图片的实际大小，它在视口坐标系中的位置始终是(0,0)到(image_width, image_height)。
        self.image_width = 0
        self.image_height = 0
        # 视口是动态变化的，但是其长宽比始终和屏幕相等。
        self.viewport: Rectangle = Rectangle(Point(), Point())

    def image_rect(self):
        return Rectangle(Point(0, 0), Point(self.image_width, self.image_height))

    # v/s
    def viewport_screen_ratio(self):
        return self.viewport.width() / self.screen_width

    def same_as_screen_view_mode(self):
        # 一比一的视图方法。屏幕像素唯一对应图片像素。
        self.viewport[0].x = 0
        self.viewport[0].y = 0
        self.viewport[1].x = self.screen_width
        self.viewport[1].y = self.screen_height
        self.adjust_viewport()

    def fit_screen_view_mode(self):
        # 适合屏幕的显示方法，图像会被缩放到直到屏幕完全能装下为止。视口大小正好可以覆盖整个图像。
        window_ratio = self.screen_width / self.screen_height
        image_ratio = self.image_width / self.image_height
        if image_ratio < window_ratio:
            self.viewport[0].y = 0
            self.viewport[1].y = self.image_height
            self.viewport[0].x = 0
            self.viewport[1].x = self.image_height * window_ratio
        elif image_ratio > window_ratio:
            self.viewport[0].x = 0
            self.viewport[1].x = self.image_width
            self.viewport[0].y = 0
            self.viewport[1].y = self.image_width / window_ratio
        self.adjust_viewport()

    def reset_image(self, image_width: int, image_height: int):
        # 图片完全锁定在0, 0处，此处viewport适应image的大小。
        self.image_height = image_height
        self.image_width = image_width

    def adjust_viewport(self):
        pass
        # 在保持视口大小不变的前提下调整视口的位置，使得视口不至于超出许可范围。
        # if self.viewport.width() > self.image_width:
        #     # 保持居中，无法移动。
        #     self.viewport[0].x = self.image_width / 2 - self.viewport.width() / 2
        #     self.viewport[1].x = self.image_width / 2 + self.viewport.width() / 2
        # else:
        #     # 超出边缘，向内推移
        #     if self.viewport[0].x < 0:
        #         offset = 0 - self.viewport[0].x
        #     elif self.viewport[1].x > self.image_width:
        #         offset = self.image_width - self.viewport[1].x
        #     else:
        #         offset = 0
        #     self.viewport[0].x += offset
        #     self.viewport[1].x += offset
        #
        # if self.viewport.height() > self.image_height:
        #     self.viewport[0].y = self.image_height / 2 - self.viewport.height() / 2
        #     self.viewport[1].y = self.image_height / 2 + self.viewport.height() / 2
        # else:
        #     # 超出边缘，向内推移
        #     if self.viewport[0].y < 0:
        #         offset = 0 - self.viewport[0].y
        #     elif self.viewport[1].y > self.image_height:
        #         offset = self.image_height - self.viewport[1].y
        #     else:
        #         offset = 0
        #     self.viewport[0].y += offset
        #     self.viewport[1].y += offset

    def drag_image(self, mouse_move_x, mouse_move_y):
        # mouse pixel
        viewport_offset_x = - mouse_move_x * self.viewport_screen_ratio()
        viewport_offset_y = - mouse_move_y * self.viewport_screen_ratio()

        self.viewport[0].x += viewport_offset_x
        self.viewport[1].x += viewport_offset_x
        self.viewport[0].y += viewport_offset_y
        self.viewport[1].y += viewport_offset_y

        self.adjust_viewport()

    def stretch_image(self, mouse_pos_x, mouse_pos_y, stretch_ratio):
        # pos是相对screen的。我们默认左上是坐标原点。ratio是比例系数，ratio = 新屏幕/旧屏幕。
        # stretch_ratio > 1 时，图像会缩小。反之扩大。
        current_amplifier_ratio = self.viewport.width() / self.screen_width
        gravity_center_x = self.viewport[0].x + mouse_pos_x * current_amplifier_ratio
        gravity_center_y = self.viewport[0].y + mouse_pos_y * current_amplifier_ratio
        # gravity_center是鼠标位置在画布上对应的坐标。
        new_viewport_left_x = gravity_center_x - (gravity_center_x - self.viewport[0].x) * stretch_ratio
        new_viewport_right_x = gravity_center_x + (self.viewport[1].x - gravity_center_x) * stretch_ratio
        new_viewport_up_y = gravity_center_y - (gravity_center_y - self.viewport[0].y) * stretch_ratio
        new_viewport_down_y = gravity_center_y + (self.viewport[1].y - gravity_center_y) * stretch_ratio
        self.viewport[0].x = new_viewport_left_x
        self.viewport[0].y = new_viewport_up_y
        self.viewport[1].x = new_viewport_right_x
        self.viewport[1].y = new_viewport_down_y

        self.adjust_viewport()
