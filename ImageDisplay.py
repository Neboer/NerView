from PIL.Image import Image
from PIL import Image as PILImage
from PIL import ImageTk
from viewport.viewport import ViewPort, Point
from viewport.render_vp import render
from tkinter import Tk, Label, Widget


# 这是用来显示图片的主窗口。

class ImageDisplayer(Label):
    def __init__(self, master: Widget | Tk, width: int = 800, height: int = 600, enlarge_ratio=0.8):
        super().__init__(master, width=width, height=height)
        self.current_image: Image | None = None
        self.viewport: ViewPort = ViewPort(width, height)
        self.background_image = PILImage.open("background.png")
        self.bind("<Configure>", self._on_window_resize)
        # mouse drag module
        self.mouse_down = False
        self.last_mouse_position = Point()
        self.bind("<Button-1>", self._on_mouse_press)
        self.bind("<ButtonRelease-1>", self._on_mouse_release)
        self.bind("<Motion>", self._on_mouse_move)

        # mouse wheel module
        self.enlarge_ratio = enlarge_ratio
        self.bind("<MouseWheel>", self._on_mouse_wheel)

        # display image cache
        self._image_obj = None

    def _render_image(self):
        # self.image must be not none.
        rendered_image = render(self.current_image, self.background_image, self.viewport)
        self._image_obj = ImageTk.PhotoImage(rendered_image)
        self.configure(image=self._image_obj)

    def _on_window_resize(self, resize_event):
        self.viewport.screen_width = resize_event.width
        self.viewport.screen_height = resize_event.height
        if self.current_image:
            self.viewport.adjust_viewport()
            self._render_image()

    def _on_mouse_press(self, press_event):
        self.mouse_down = True

    def _on_mouse_release(self, release_event):
        self.mouse_down = False

    def _on_mouse_move(self, mouse_event):
        if self.current_image:
            if self.mouse_down:
                x_move = mouse_event.x - self.last_mouse_position.x
                y_move = mouse_event.y - self.last_mouse_position.y
                self.viewport.drag_image(x_move, y_move)
                self._render_image()
            self.last_mouse_position.x = mouse_event.x
            self.last_mouse_position.y = mouse_event.y

    def _on_mouse_wheel(self, wheel_event):
        if self.current_image:
            win_degree = wheel_event.delta / 120  # 向上移动为正
            real_ratio = pow(self.enlarge_ratio, win_degree)
            self.viewport.stretch_image(wheel_event.x, wheel_event.y, real_ratio)
            self._render_image()

    def fit_screen(self):
        self.viewport.fit_screen_view_mode()
        self._render_image()

    def same_as_screen(self):
        self.viewport.same_as_screen_view_mode()
        self._render_image()

    def load_image(self, new_image: Image):
        self.current_image = new_image
        self.viewport.image_height = new_image.height
        self.viewport.image_width = new_image.width
        self.fit_screen()
