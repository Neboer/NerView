# render a image in viewport
from .viewport import ViewPort
from PIL.Image import Image, NEAREST


def render(full_image: Image, background_image: Image, vp: ViewPort) -> Image:
    # 背景图片必须尽可能大，它最小的大小应该等于vp中的屏幕大小。full_image的大小应该等于vp中image_的大小。
    # 求出视口与图片的相交区域，然后把它放大到视口-屏幕相同的比例。
    viewport_ratio = vp.screen_width / vp.viewport.width()
    intersected_box = vp.viewport.intersect(vp.image_rect())
    cropped_image = full_image.crop(box=intersected_box.to_pil_corr())
    resized_cropped_image = cropped_image.resize(size=(int(cropped_image.width * viewport_ratio), int(cropped_image.height * viewport_ratio)), resample=NEAREST)
    paste_offset_x = (0 - vp.viewport[0].x if 0 - vp.viewport[0].x > 0 else 0) * viewport_ratio
    paste_offset_y = (0 - vp.viewport[0].y if 0 - vp.viewport[0].y > 0 else 0) * viewport_ratio
    cropped_background_image = background_image.crop(box=(0, 0, vp.screen_width, vp.screen_height))
    cropped_background_image.paste(resized_cropped_image, (int(paste_offset_x), int(paste_offset_y)))
    return cropped_background_image
