# DOL-ILAB Data Manipulation for Bureau for International Labor Affairs

The development language is Python. The core data standard used is XML. MySQL is the database used.

The mission of this project is to convert the data provided by the Office of Forced and Child Labor (in DOL), hereafter called OFCL) to machine-readable forms. 

The data provided by OFCL is:
- Three excel spreadsheets, which contains 1) goods, 2) products, 3) master data for the countries monitored by OFCL
- Around 150 Word documents that describe information on the countries that the office monitors.

The sample code in the code folder enables the processing of the data in the goods.xls (and products.xls) into an array of goods (and products).
	
generate_good.py does the conversion from XL to a goods_list. It also creates XML files located in the output folder (ordered by country or by good). It also produces a raw dump of the XL sheet into JSON.

generate_product.py does the same thing as generate_good.py but for products

generate_db generates a MySQL db and dump the countries, goods and products into it. This is ongoing work. The mappings will be dumped next. 
	
The difference between goods and products is a legsilative one. Products are defined those things that the Bureau are 100% sure involve forced labor.

XML Formats are:

-- Products By Country --
<Product_List>
	<Year>
		<Year_Name></Year_Name>
		<Country>
			<Country_Name> </Country_Name>
			<Products>
			 	<Product_Name></Product_Name>
			 	
			</Products>
		</Country>
		...
	</Year>
	...
</Product_List>


-- Products By Product --
<Product_List>
	<Year>
		<Year_Name></Year_Name>
		<Product>
			<Product_Name> </Product_Name>
			<Countries>
			 	<Country_Name></Country_Name>
			 	...
			</Countries>
		</Product>
		...
	</Year>
	...
</Product_List>

----- GOODS

-- Goods By Country --
<Good_List>
	<Year>
		<Year_Name> </Year_Name>
		<Country>
			<Country_Name> </Country_Name>
			<Goods>
				<Good>
			 		<Good_Name> </Good_Name>
			 		<Child_Labor> </Child_Labor>
			 		<Forced_Labor> </Forced_Labor>
			 	</Good>
			 	...
			</Goods>
		</Country>
		...
	</Year>
	...
</Good_List>

-- Goods By Good --
<Good_List>
	<Year>
		<Year_Name></Year_Name>
		<Good>
			<Good_Name> </Good_Name>
			<Country>
			 	<Country_Name> </Country_Name>
			 	<Child_Labor> </Child_Labor>
			 	<Forced_Labor> </Forced_Labor>
			</Country>
			...
		</Good>
		...
	</Year>
	...
</Good_List>


-- Master Data --

<Master_Data>
<Country>
	<Name>  </Name>
	<Survey_Name> </Survey_Name>
	<Childrens_Work_Statistics>
		<Year> </Year>
		<Survey_Source> </Survey_Source>
		<Age_Range> </Age_Range>
		<Total_Child_Population> </Total_Child_Population>
		<Total_Percentage_of_Working_Children> </Total_Percentage_of_Working_Children>
		<Total_Working_Population></Total_Working_Population>
		<Agriculture> </Agriculture>
		<Services> </Services>
		<Industry> </Industry>
	</Childrens_Work_Statistics>
	<Education_Statistics_Attendance_Statistics>
		<Year> </Year>
		<Age_Range> </Age_Range>
		<Percentage> </Percentage>
	</Education_Statistics_Attendance_Statistics>
	<Children_Work_And_Studying>
		<Year> </Year>
		<Age_Range> </Age_Range>
		<Total></Total>
	</Children_Work_And_Studying>
	<Unesco_Primary_Completion_Rate>
		<Year> </Year>
		<Rate> </Rate>
	</Unesco_Primary_Completion_Rate>
</Country>
...
</Master_Data>
