import runescape_text as rst

img = rst.parse_string("wave:glow1:Hello World")
if(len(img)==1):
	rst.single_frame_save(img[0], file="out.png")
else:
	rst.multi_frame_save(img, file="out.gif")