from rate.models import *
from django.db.models import Q
from django.db import connection, transaction

masterCustomer = Customer.objects.get(domain="MASTER")

error = False
print("Deleting records...")
try:
  #customers = Customer.objects.filter(~Q(domain="MASTER")).delete()
  Template.objects.filter(~Q(customer=masterCustomer)).delete()
  TemplateStaticColumn.objects.filter(~Q(customer=masterCustomer)).delete()
  TemplateDynamicColumn.objects.filter(~Q(customer=masterCustomer)).delete()
  TemplateDynamicColumnValue.objects.filter(~Q(customer=masterCustomer)).delete()
  csv_files = CsvFile.objects.filter(~Q(customer=masterCustomer))
  csv_file_id_list = [(csv_file.id) for csv_file in csv_files]
  CsvStructure.objects.filter(id__in = csv_file_id_list).delete()
  CsvFile.objects.filter(~Q(customer=masterCustomer)).delete()

  transaction.commit()
  print("Tables deleted")
except Exception as ex:
  print("Failed to delete table " + str(ex))
  error = True

if not error:
  print("Resetting sequence...")
  try:
    cursor = connection.cursor()
    #cursor.execute("UPDATE sqlite_sequence SET seq = (SELECT MAX(id) FROM rate_customer) WHERE LOWER(name) = 'rate_customer'")
    cursor.execute("UPDATE sqlite_sequence SET seq = (SELECT MAX(id) FROM rate_template) WHERE LOWER(name) = 'rate_template'")
    cursor.execute("UPDATE sqlite_sequence SET seq = (SELECT MAX(id) FROM rate_templatestaticcolumn) WHERE LOWER(name) = 'rate_templatestaticcolumn'")
    cursor.execute("UPDATE sqlite_sequence SET seq = (SELECT MAX(id) FROM rate_templatedynamiccolumn) WHERE LOWER(name) = 'rate_templatedynamiccolumn'")
    cursor.execute("UPDATE sqlite_sequence SET seq = (SELECT MAX(id) FROM rate_templatedynamiccolumnvalue) WHERE LOWER(name) = 'rate_templatedynamiccolumnvalue'")
    cursor.execute("UPDATE sqlite_sequence SET seq = (SELECT MAX(id) FROM rate_csvfile) WHERE LOWER(name) = 'rate_csvfile'")
    cursor.execute("UPDATE sqlite_sequence SET seq = (SELECT MAX(id) FROM rate_csvstructure) WHERE LOWER(name) = 'rate_csvstructure'")
    transaction.commit()
    print("Done!")
  except Exception as ex:
    print("Failed to reset sequence " + str(ex))
    error = True