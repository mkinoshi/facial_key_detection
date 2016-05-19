from PIL import Image
import time
import data

def show_pictures_data(filename):
	traindata = data.FacialData(filename)
	#print "headers", traindata.get_headers()
	image_column = traindata.get_image_data()
	return image_column

def show_picture(pixel_list):
	image = Image.new("RGB", (960, 960))
	count = 0
	while (count < 100):
		if count <  len(pixel_list):
			each_picture = pixel_list[count]
			for row in range(96):
				for column in range(96):
					image.putpixel((column+(count%10)*96, row+(count/10)*96), (int(each_picture[row*96+column]),int(each_picture[row*96+column]),int(each_picture[row*96+column]),0))
		count += 1

	image.show()

def show_picture_estimate(pixel_list, estimate):
	image = Image.new("RGB", (960, 960))
	count = 0
	while (count < 100):
		if count <  len(pixel_list):
			each_picture = pixel_list[count]
			for row in range(96):
				for column in range(96):
					if row == estimate[1] and column == estimate[0]:
						image.putpixel((column+(count%10)*96, row+(count/10)*96), (255, 0, 0))
					else:
						image.putpixel((column+(count%10)*96, row+(count/10)*96), (int(each_picture[row*96+column]),int(each_picture[row*96+column]),int(each_picture[row*96+column]),0))
		count += 1

	image.show()
def main():
	d = data.Data("dataX.csv")
	pixel = d.get_data(d.get_headers())
	show_picture(pixel.tolist())

if __name__ == "__main__":
    main()