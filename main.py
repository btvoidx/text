import json
from PIL import Image, ImageDraw

def load_scenes(file:str = "input.json"):
	# Open file, read it, load into scenes list
	with open(file, "r+") as f:
		scenes = json.loads(f.read())

	return scenes

def main(scenes:list):
	scene_number = 0
	for scene in scenes:
		scene_number += 1
		# Create new image
		img = Image.new('RGB', tuple(scene["dimensions"]), color = tuple(scene["colors"]["background"]))
		draw = ImageDraw.Draw(img)
		draw.text((10,10), scene["text"], fill=tuple(scene["colors"]["text"]))

		# Save the image
		img.save(f"scene{scene_number}.png")

if __name__ == '__main__':
	scenes = load_scenes()
	main(scenes)
