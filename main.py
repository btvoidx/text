from json import loads
from PIL import Image, ImageDraw, ImageFont
from statistics import mean

def load_scenes(file:str = "input.json"):
	# Open file, read it, load into scenes list
	with open(file, "r+") as f:
		scenes = loads(f.read())

	return scenes


def get_global(parameter, scene):
	if parameter in scene:
		return scene[parameter]
	else:
		return gscenes["global"][parameter]

def draw(scenes:dict):
	global gscenes
	gscenes = scenes

	for scene in scenes["scenes"]:
		scene_number = scenes["scenes"].index(scene)

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

			img.save(f"output/scene{scene_number}.png")

		# But if text type is dictionary, then we do some woodoo magic
		elif type(scene["text"]) == type(list()):
			# Finding average font size
			afont = int(mean(get_global("font-size", x) for x in scene["text"]))
			afont = ImageFont.truetype(f"fonts/{scenes['global']['font']}", afont)

			full_text = "".join(f"{x['text']} " for x in scene["text"])
			current_text = ""

			for part in scene["text"]:
				part_number = scene["text"].index(part)

				current_text += part["text"]

				W, H = tuple(scenes["global"]["dimensions"])
				w, h = draw.textsize(current_text, font = afont)

				offset = (W - w) / 2

				for part in scene["text"]:
					if part_number < scene["text"].index(part):
						continue

					# Getting new font and position
					font = ImageFont.truetype(f"fonts/{get_global('font', part)}", get_global("font-size", part))
					_, h = draw.textsize(current_text, font = font)
					position = offset, (H - h) / 2

					draw.text(position, part["text"], fill = tuple(get_global("color", part)), font = font)

					offset += draw.textsize(part["text"], font = font)[0]

				img.save(f"output/scene{scene_number}_{part_number}.png")
				img.paste(tuple(get_global("background", scene)), tuple([0, 0] + scenes["global"]["dimensions"]))


if __name__ == '__main__':
	scenes = load_scenes()
	draw(scenes)
