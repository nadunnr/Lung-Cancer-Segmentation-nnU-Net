import xml.etree.ElementTree as ET
import openpyxl
import SimpleITK as sitk
import pandas as pd

def parse_xml(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()

    coordinates = []

    for element in root.iter():
        if element.text is not None and '\\' in element.text:
            if element.text.strip() == 'CLOSED_PLANAR\n1':
                continue

            coords = element.text.split('\\')
            if '1/255/1' not in coords:
                coordinates.append(coords)

    return coordinates

def write_coordinates_to_excel(coordinates, excel_file_path):
    wb = openpyxl.Workbook()
    ws = wb.active

    # Set column headers as "x", "y", "z"
    headers = ["x", "y", "z"]
    ws.append(headers)

    for coord_set in coordinates:
        # Check if the coordinates are not (0, 255, 0)
        if coord_set != ['0', '255', '0']:
            ws.append([float(value) for value in coord_set])

    wb.save(excel_file_path)

if __name__ == "__main__":
    # Script 1: Parse XML and write to Excel
    xml_file_path = "D:/ScholarX/test/R01-001.xml"
    excel_file_path = "D:/ScholarX/test/test1.xlsx"

    try:
        parsed_coordinates = parse_xml(xml_file_path)
        write_coordinates_to_excel(parsed_coordinates, excel_file_path)
        print("Script 1 completed successfully.")
    except Exception as e:
        print(f"Error in Script 1: {e}")

    # Script 2: Load 3D medical image and create label map
    image_path = "D:/ScholarX/test/001_main.nii.gz"
    excel_path = "D:/ScholarX/test/test1.xlsx"
    label_map_path = "D:/ScholarX/test/test2.nii.gz"

    try:
        image = sitk.ReadImage(image_path)
        coordinates_df = pd.read_excel(excel_path)
        physical_coordinates = coordinates_df[['x', 'y', 'z']].values

        label_map = sitk.Image(image.GetSize(), sitk.sitkUInt8)
        label_map.SetOrigin(image.GetOrigin())
        label_map.SetSpacing(image.GetSpacing())
        label_map.SetDirection(image.GetDirection())

        for i, coord in enumerate(physical_coordinates):
            index = image.TransformPhysicalPointToIndex(coord)
            label_map[index] = i + 1  # Indexing starts from 1

        sitk.WriteImage(label_map, label_map_path)
        print("Script 2 completed successfully.")
    except Exception as e:
        print(f"Error in Script 2: {e}")
