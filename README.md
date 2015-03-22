# DOL-ILAB
Data Manipulation for Bureau for International Labor Affairs

This effort uses Python.

THe sample code in the code folder enables the processing of the data in the goods.xls (and products.xls) into an array of goods (and products). NB. All good is rough and this is my first attempt coding in Python. 

generate_good.py does the conversion from XL to a goods_list. It also creates XML files located in the output folder (ordered by country or by good). It also produces a raw dump of the XL sheet into JSON.
generate_product.py does the same thing as generate_good.py but for products
generate_db generates a MySQL db and dump the countries, goods and products into it. This is ongoing work. The mappings will be dumped next. 

The difference between goods and products is a legsilative one. Products are defined those things that the Bureau are 100% sure involve forced labor.

For Goods: 

The XML format is (by Good):

<?xml version="1.0" encoding="UTF-8"?>
<Good List>
	<Year>
		<Year_Name> </Year_Name>
			<Good>
				<Good_Name>  </Good_Name>
					<Countries>
						<Country>
							<Country_Name> </Country_Name>
							<Child_Labor> </Child_Labor>
							<Forced_Labor> </Forced_Labor>
						</Country>
						...
					</Countries>
			</Good>
			..
	</Year>	
	...
</Good List>

The XML format is (by Country):

<?xml version="1.0" encoding="UTF-8"?>
<Goods List>
	<Year>
		<Year_Name> </Year_Name>
		<Country>
			<Country_Name> </Country_Name>
			<Goods>
				<Good>
						<Good_Name> </Good_Name>
						<Child_Labor> </Child_Labor>
						<Forced_Labor></Forced_Labor>
				</Good>
        ..
			</Goods>
		</Country>
		...
  </Year>
  ...
</Goods List>  

For Products:

The XML format is (by Product):

<?xml version="1.0" encoding="UTF-8"?>
<Products List>
	<Year>
		<Year_Name> </Year_Name>
		<Product>
			<Product_Name> </Product_Name>
			<Countries>
				<Country_Name> </Country_Name>
        ..
			</Countries>
		</Product>
		...
	</Year>
	...
</Products List>

The XML format is (by Country):

<?xml version="1.0" encoding="UTF-8"?>
<Products List>
	<Year>
		<Year_Name> </Year_Name>
		<Country>
			<Country_Name> </Country_Name>
			<Products>
				<Product_Name> </Product_Name>
				...
			</Products>
		</Country>
		...
	</Year>
	...
</Products List>	
	
