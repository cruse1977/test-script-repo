import shutil

for filename in ["random_10MB.json", "random_7_5MB.csv"]:
 for x in range(1, 50):
   shutil.copyfile(filename, filename.replace("MB",f"MB{x}"))

