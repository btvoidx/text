import json

def load_scenes(file:str = "input.json"):
	# Open file, read it, load into scenes list
	with open(file, "r+") as f:
		scenes = json.loads(f.read())

	return scenes

def main(scenes:list):
	for scene in scenes:
		print(scene)

if __name__ == '__main__':
	scenes = load_scenes()
	main(scenes)
