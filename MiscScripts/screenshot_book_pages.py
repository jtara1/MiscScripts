import os, sys, time, pyautogui


def main(pages, ss_region, get_next_key="right", 
		output_path=os.path.join(os.getcwd(), 'Output-'+str(int(time.time()))),
		ext=".png",):
	"""Takes a screenshot then goes to next page by pressing the get_next_key
	button
	
	:param pages: number of pages to take a screenshot of
	:param get_next_key: key pressed to go to next page_delay
	:param output_path: path to safe screenshots to
	:param ext: extension of each image file
	:param ss_region: screenshot region (box region), defaults to entire screen
	:param type: tuple containing 4 integers

	:todo: use module screeninfo to get screen resolution
	"""
		
	start_delay = 8
	page_delay = 0.4

	if not os.path.isdir(output_path):
		os.mkdir(output_path)
	
	print("Running this script for %s pages in region %s" % (pages, ss_region))
	print("Beginning script in %s seconds." % start_delay)
	time.sleep(start_delay)
	
	for i in range(pages):
		file_path = os.path.join(output_path, str(i) + ext)
		img = pyautogui.screenshot(file_path, region = ss_region)
		pyautogui.press(get_next_key)
		time.sleep(page_delay)
		

if __name__ == "__main__":
	# (left, top, width, height)
	k_laptop_region = (465, 5, 719, 895)
	kindle_reader_fullscreen_1440p_region = (46, 0, 2560-46, 1440)
	kindle_cropped_1440p_region = (725, 0, 1880-725, 1440)
	
	main(pages=2, ss_region=kindle_cropped_1440p_region)
	
