import pickle
import xlsxwriter
import pandas as pd

# load the encodings + names dictionary
with open("labels_lfw.pickle", "rb") as f:
    names = pickle.load(f)

# Create an new Excel file and add a worksheet.
workbook = xlsxwriter.Workbook("images.xlsx")
worksheet = workbook.add_worksheet()


worksheet.set_column("A:A", 30)
worksheet.set_column("B:B", 30)
worksheet.set_column("C:C", 10)
worksheet.set_column("D:D", 30)
worksheet.set_column("E:E", 30)
worksheet.write("A1", "Matching Face Photo Name")
worksheet.write("B1", "Test Face Photo Name")
worksheet.write("C1", "Similarity")
worksheet.write("D1", "Matching Face Photo")
worksheet.write("E1", "Test Face Photo")
for i in range(len(names)):
    if names[i]["Correct_Similarity"] == True:
        cf = workbook.add_format({'bg_color': 'yellow'})
    if names[i]["Correct_Similarity"] == False:
        cf = workbook.add_format({'bg_color': 'red'})
    if names[i]["Find_Face"] == False:
        cf = workbook.add_format({'bg_color': 'blue'})
    image_comp=""
    image_base=""
    if names[i][" Test Photo Name"]!=None:
        str = ""
        for item in names[i][" Test Photo Name"].split('_')[:-1]:
            str=str+item+"_"
        image_comp=f"""dataset/{str[:-1]}/{names[i][" Test Photo Name"]}"""
        worksheet.insert_image(f"D{i + 2}", image_comp,
                               {"x_scale": 0.8, "y_scale": 0.8, "x_offset": 10, "y_offset": 10})
    if names[i]["Matching Face Poto Name"] != None:
        str = ""
        for item in names[i]["Matching Face Poto Name"].split('_')[:-1]:
            str = str + item + "_"
        image_base=f"""dataset/{str[:-1]}/{names[i]["Matching Face Poto Name"]}"""
        worksheet.insert_image(f"E{i + 2}", image_base,
                               {"x_scale": 0.8, "y_scale": 0.8, "x_offset": 10, "y_offset": 10})

    worksheet.set_row_pixels(i+1,250)
    worksheet.write(f"A{i+2}", names[i][" Test Photo Name"],cf)
    worksheet.write(f"B{i+2}", names[i]["Matching Face Poto Name"],cf)
    worksheet.write(f"C{i+2}", names[i]["Similarity"],cf)

worksheet_1 = workbook.add_worksheet()
worksheet_1.set_column("A:A", 30)
worksheet_1.set_column("B:B", 30)
worksheet_1.write(f"A1:B1", "Eşleşme Sayısı")
worksheet_1.write(f"D1:E1", "Yüz Bulunup Bulunamama Sayısı")
worksheet_1.set_column("C:C", 10)
worksheet_1.set_column("D:D", 30)
worksheet_1.set_column("E:E", 30)
df = pd.DataFrame(names)

cr_sm = df.Correct_Similarity.value_counts()
ff = df.Find_Face.value_counts()
worksheet_1.write(f"B2", cr_sm.to_list()[0])
worksheet_1.write(f"B3", cr_sm.to_list()[1])
worksheet_1.write(f"A2", "Doğru")
worksheet_1.write(f"A3", "Yanlış")

worksheet_1.write(f"E2", ff.to_list()[0])
worksheet_1.write(f"E3", ff.to_list()[1])
worksheet_1.write(f"D2", "Bulundu")
worksheet_1.write(f"D3", "Bulunamadı")

workbook.close()
