import PIL
from PIL import Image 
import os 
picture = Image.open(os.path.join('Mecha.png'))

width, height = picture.size
for i in range(width) :
    for j in range (height) :
        current_color = picture.getpixel( (i,j) )
        r=current_color[0]
        g=current_color[1]
        b=current_color[2]
        if (b-r >30 ) :
            new_color = (current_color[0] , current_color[2]+50, current_color[1]-15  )
            picture.putpixel( (i,j), new_color)

picture.save("mod.png")
