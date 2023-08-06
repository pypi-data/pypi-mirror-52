from caloriestracker.mem import MemConsole
from caloriestracker.datetime_functions import dtnaive2string
from caloriestracker.libcaloriestracker import Product, CompanySystem, CompanySystemManager, ProductManager
from caloriestracker.libcaloriestrackerfunctions import b2s
from caloriestracker.admin_pg import AdminPG
from caloriestracker.database_update import database_update
from caloriestracker.text_inputs import input_YN, input_string
from colorama import Style, Fore
from datetime import datetime
from os import system

def print_table_status(con):
    personalproducts=con.cursor_one_field("select count(*) from personalproducts")
    products=con.cursor_one_field("select count(*) from products")
    companies=con.cursor_one_field("select count(*) from companies")
    return (companies, products, personalproducts)

## Generate a dump for the collaborator
## @param mem Current database to extract personal data only
def generate_contribution_dump(mem):
    database_version=int(mem.con.cursor_one_field("select value from globals where id=1"))
    filename="caloriestracker_collaboration_{}.sql".format(database_version)
    f=open(filename, "w")
    f.write("select;\n")#For no personal data empty files
    for company in mem.data.companies.arr:
        if company.system_company==False:
            f.write(company.insert_string("personalcompanies") + ";\n")
    for product in mem.data.products.arr:
        if product.system_product==False and product.elaboratedproducts_id==None:
            f.write(product.insert_string("personalproducts") + ";\n")
    f.close()
    print(Style.BRIGHT + Fore.GREEN + "Generated '{}'. Please send to '' without rename it".format(filename)+ Style.RESET_ALL)

## Parses generated dump of the collborator. 
## 1. Uses mem.con to generate a new conexión an database
## 2. Load personal data from collaborator
## 3. Generates files to pass personal data to system data
## 4. Tries generated files and shows results
def parse_contribution_dump(mem):        
        datestr=dtnaive2string(datetime.now(), 3).replace(" ", "")
        database="caloriestracker"+datestr
        admin=AdminPG(mem.con.user, mem.con.password, mem.con.server, mem.con.port)
        newcon=admin.create_new_database_and_return_new_conexion(database)
        database_update(newcon)        
        print ("1. After setting database to default",  *print_table_status(newcon))
        newcon.load_script(mem.args.parse_collaboration_dump)
        newcon.commit()
        print ("2. After loading personal data from collaborator",  *print_table_status(newcon))
        new_database_generates_files_from_personal_data(datestr, newcon)
        #Checking
        
        print ("3. After generating files collaboration. Emulates launching update_table",  *print_table_status(newcon))
        newcon.load_script("XXXXXXXXXXXX.sql")
        print ("4. After trying XXXXXXXXXXXX.sql",  *print_table_status(newcon))
        
        print("5. After updating collaborator database")
        newcon.load_script("XXXXXXXXXXXX_version_needed_update_first_in_github.sql")
        print ("After loading updating collaborator return.sql",  *print_table_status(newcon))
       
        newcon.commit()
        newcon.disconnect()
        input_string("Press ENTER to delete database: " + database)
        admin.drop_db(database)
        
        question=input_YN("Do you want to add {}.sql to caloriestracker/sql/?".format(datestr),  "?")
        if question==True:
            system("mv XXXXXXXXXXXX.sql caloriestracker/sql/{}.sql".format(datestr))
            system("mv XXXXXXXXXXXX_version_needed_update_first_in_github.sql {}_version_needed_update_first_in_github.sql".format(datestr))

## With th new database generate files to convert local to string, asking wich one
def new_database_generates_files_from_personal_data(datestr, newcon):
    mem=MemConsole()
    mem.run()
    
    ## GENERATING XXXXXXXXXXXX.sql
    package_sql_filename="XXXXXXXXXXXX.sql".format(datestr)        
    package_sql=open(package_sql_filename, "w")
    package_sql.write("select;\n")#For no personal data empty files
    #companies
    companies_map={}
    products_map={}
    new_system_companies_id=newcon.cursor_one_field("select max(id)+1 from companies")
    new_system_companies=CompanySystemManager(mem)
    for company in mem.data.companies.arr:
        if company.system_company==False:
            question=input_YN("Do you want to convert this company '{}' to a system one?".format(company), "Y")
            if question==True:
                system_company=CompanySystem(mem, company.name, company.starts, company.ends, new_system_companies_id)
                new_system_companies.append(system_company)
                companies_map[company.string_id()]=system_company.string_id()
                new_system_companies_id=new_system_companies_id+1
                package_sql.write(system_company.insert_string("companies")+ ";\n")
                mem.data.companies.append(system_company) ##Appends new sistem company to mem.data
                #print ("Company will change from {} to {}".format(company.string_id(), system_company.string_id()))
    #products
    new_system_products_id=newcon.cursor_one_field("select max(id)+1 from products")
    new_system_products=ProductManager(mem)
    for product in mem.data.products.arr: 
        if product.system_product==False:
            question=input_YN("Do you want to convert this product '{}' to a system one?".format(product.fullName(True)), "Y")
            #Selects a company
            if product.company!=None:
                if product.system_company==False:
                    company=mem.data.companies.find_by_id_system(*CompanySystem.string_id2tuple(companies_map[product.company.string_id()]))
                else:
                    company=product.company
                system_company=True
            else:
                company=None
                system_company=None
            #Create product
            if question==True:
                system_product=Product(
                    mem, 
                    product.name, 
                    product.amount, 
                    product.fat, 
                    product.protein, 
                    product.carbohydrate, 
                    company, 
                    product.ends, 
                    product.starts, 
                    product.elaboratedproducts_id, 
                    product.languages, 
                    product.calories, 
                    product.salt, 
                    product.cholesterol, 
                    product.sodium, 
                    product.potassium, 
                    product.fiber, 
                    product.sugars, 
                    product.saturated_fat, 
                    system_company,  
                    new_system_products_id)
                new_system_products.append(system_product)
                products_map[product.string_id()]=system_product.string_id()
                new_system_products_id=new_system_products_id+1
                #print ("Product will change from {} to {}".format(product, system_product))
                #if company!=None:
                #    print ("Its company will change from {} to {}".format(product.company.string_id(), company.string_id()))
                package_sql.write(system_product.insert_string("products") + ";\n")
    package_sql.close()
    
    ## GENERATING COLLABORATION UPDATE FOR COLLABORATOR
    return_sql_filename="XXXXXXXXXXXX_version_needed_update_first_in_github.sql"  
    return_sql=open(return_sql_filename, "w")
    return_sql.write("select;\n")#For no personal data empty files
    #COMPANIES
    for origin, destiny in companies_map.items():#k,v strings_id
        origin_personal_company=mem.data.companies.find_by_string_id(origin)
        #destiny_system_company=new_system_companies.find_by_string_id(destiny)
        #Delete old personal companies
        return_sql.write("-- " + origin_personal_company.fullName() + "\n")
        return_sql.write("delete from personalcompanies where id=" + str(origin_personal_company.id) + ";\n")
        return_sql.write("\n")
        
    #PRODUCTS
    for origin, destiny in products_map.items():
        origin_personal_product=ProductManager.find_by_string_id(mem.data.products, origin)
        destiny_system_product=ProductManager.find_by_string_id(new_system_products, destiny)
        #Delete old personal companies
        return_sql.write("-- " + origin_personal_product.fullName() + "\n")
        return_sql.write(b2s(mem.con.mogrify("delete from personalproducts where id=%s;", (origin_personal_product.id, )))+"\n")
        #UPDATING PRODUCTS IN THE REST OF TABLES
        for table in ['formats', 'meals', 'products_in_elaboratedproducts']:
            return_sql.write(b2s(mem.con.mogrify("update "+table+" set products_id=%s, system_product=%s where products_id=%s and system_product=%s;", 
                (destiny_system_product.id, destiny_system_product.system_product, origin_personal_product.id, origin_personal_product.system_product)))+"\n")
        return_sql.write("\n")
    return_sql.close()
