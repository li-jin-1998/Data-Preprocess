import gizeh
import numpy as np
from moviepy.editor import VideoClip

# 设置图像尺寸
WIDTH, HEIGHT = 800, 600
NUM_STARS = 100  # 星星的数量
DURATION = 10  # 动画持续时间（秒）

stars = np.random.rand(NUM_STARS, 2) * [WIDTH, HEIGHT]


def make_frame(t):
    # 生成星星的位置和初始亮度
    colors = np.random.rand(NUM_STARS, 3)  # 随机生成星星的颜色
    surface = gizeh.Surface(WIDTH, HEIGHT, bg_color=(0, 0, 0))

    # 绘制月亮
    # moon = gizeh.circle(r=50, xy=(WIDTH - 100, HEIGHT - 100), fill=(1, 1, 0.8))
    # moon.draw(surface)

    # 绘制星星
    for i in range(NUM_STARS):
        # 随机调整星星的亮度，使其闪烁
        current_brightness = 0.5 + 0.5 * np.sin(2 * np.pi * t + i)
        star_color = (colors[i][0], colors[i][1], colors[i][2], current_brightness)
        star = gizeh.circle(r=8, xy=stars[i], fill=star_color)
        star.draw(surface)

    return surface.get_npimage()


# 创建视频剪辑
video_clip = VideoClip(make_frame, duration=DURATION)

# 设置视频帧率
video_clip = video_clip.set_fps(24)

# 保存动画到 GIF 文件
video_clip.write_gif("twinkling_stars_with_moon.gif", fps=24)

