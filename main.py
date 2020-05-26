import json
from PIL import Image, ImageDraw, ImageFont

def load_scenes(file:str = "input.json"):
	# Open file, read it, load into scenes list
	with open(file, "r+") as f:
		scenes = json.loads(f.read())

	return scenes


def get_global(parameter, scene):
	if parameter in scene:
		return scene[parameter]
	else:
		return gscenes["global"][parameter]

def main(scenes:dict):
	scene_number = 0

	global gscenes
	gscenes = scenes

	for scene in scenes["scenes"]:
		scene_number += 1

		# Create new image
		img = Image.new('RGB', tuple(scenes["global"]["dimensions"]), color = tuple(get_global("background", scene)))
		draw = ImageDraw.Draw(img)

		# If text type is just a string, we do nothing fancy
		if type(scene["text"]) == type(str()):
			font = ImageFont.truetype(f"fonts/{get_global('font', scene)}", get_global("font-size", scene))

			# Calculating position of the text to center it
			W, H = tuple(scenes["global"]["dimensions"])
			w, h = draw.textsize(scene["text"], font = font)
			position = ((W - w) / 2, (H - h) / 2)

			draw.text(position, scene["text"], fill = tuple(get_global("color", scene)), font = font)

		# But if text type is dictionary, then we do some woodoo magic
		elif type(scene["text"]) == type(list()):
			# Finding biggest font size
			bfont = sorted(get_global("font-size", x) for x in scene["text"])[-1]
			font = ImageFont.truetype(f"fonts/{scenes['global']['font']}", bfont)
			full_text = "".join(f"{x['text']} " for x in scene["text"])
			print(full_text)


		# Save the image
		img.save(f"scene{scene_number}.png")

if __name__ == '__main__':
	scenes = load_scenes()
	main(scenes)
