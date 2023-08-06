Install using 'pip3 install digilib'

Check test.py file for usage

import digilib 
def test():
	print("starting simple downlad test")
	book_name = "the road to reality"
	digilib.get_book_libgen(book_name)
	print("book downloaded...")



	directory = '../book_lib'
	txt_file = 'txt_file.txt'
	catalogue_dir = 'catalogue_dir'

	print("directory traversal catalogue test ...")
	digilib.create_catalogue(directory,catalogue_dir)
	print("created catalogue by directory traversal...")
	print("starting to create library using catalogue file 'catalogue_dir'")
	digilib.create_library(catalogue_dir)
	print("library creation completed")


	catalogue_txt = 'catalogue_txt'
	print("txt file reading catalogue test ...")
	digilib.create_catalogue(txt_file, catalogue_txt)
	print("created catalogue by reading txt file")
	print("starting to created library using catalogue file 'catalogue_txt'")
	digilib.create_library(catalogue_txt)
	print("library creation completed")





test()
