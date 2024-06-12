import gizeh
import matplotlib.pyplot as plt

# 图像的参数
WIDTH, HEIGHT = 300, 200

# 创建图像表面
surface = gizeh.Surface(WIDTH, HEIGHT, bg_color=(1, 1, 1))

# 画黑色条纹
black_stripe = gizeh.rectangle(lx=WIDTH, ly=HEIGHT / 3, xy=(WIDTH / 2, HEIGHT / 6), fill=(0, 0, 0))
black_stripe.draw(surface)

# 画白色条纹
white_stripe = gizeh.rectangle(lx=WIDTH, ly=HEIGHT / 3, xy=(WIDTH / 2, HEIGHT / 2), fill=(1, 1, 1))
white_stripe.draw(surface)

# 画绿色条纹
green_stripe = gizeh.rectangle(lx=WIDTH, ly=HEIGHT / 3, xy=(WIDTH / 2, 5 * HEIGHT / 6), fill=(0, 1, 0))
green_stripe.draw(surface)

# 画红色三角形
red_triangle = gizeh.polyline(points=[(0, HEIGHT / 6), (WIDTH / 3, HEIGHT / 2), (0, 5 * HEIGHT / 6)], fill=(1, 0, 0),
                              close_path=True)
red_triangle.draw(surface)

# 将图像表面保存为 PNG 文件
surface.write_to_png("palestine_flag.png")

img = surface.get_npimage()
plt.imshow(img)
plt.axis('off')
plt.show()
