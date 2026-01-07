import glob
import cv2
import os
import random

# Enter the target dimensions of the image tiles here: (DINOv2 expects 224x224 px images)
TargetDimension = 224

DataSetPath = "ImageStore/OriginalImages/"
SaveBasePath = "ImageStore/Cropped/"

if not os.path.isdir(SaveBasePath):
    os.mkdir(SaveBasePath)

for ImagePath in glob.glob(DataSetPath + "/*.tif"):
    ActiveImage = cv2.imread(ImagePath)
    ImageName = ImagePath.split("\\")[1][:-4]
    ImageDimensionsXY = (ActiveImage.shape[1], ActiveImage.shape[0])
    ReminderXY = tuple(a % TargetDimension for a in ImageDimensionsXY)
    NumberOfCropsAsFloatXY = tuple((a - b) / TargetDimension for a, b in zip(ImageDimensionsXY, ReminderXY))

    if all(Entry % int(Entry) == 0 for Entry in NumberOfCropsAsFloatXY):
        NumberOfCropsXY = tuple(int(Entry) for Entry in NumberOfCropsAsFloatXY)
    else:
        print(NumberOfCropsAsFloatXY)
        raise SystemExit("Non integer number of crops. Stopping program!")
    RollingCounter = 0
    for YCropPosition in range(NumberOfCropsXY[1]):
        for XCropPosition in range(NumberOfCropsXY[0]):
            RandomString = "".join(str(random.randint(0, 9)) for _ in range(15))
            SavePath = f"{SaveBasePath}{ImageName}_{RandomString}.tif"
            CropStartXY  = (int(0.5 * ReminderXY[0] + XCropPosition * TargetDimension),int(0.5 * ReminderXY[1] + YCropPosition * TargetDimension))
            CropFinishXY = tuple(CropStart + TargetDimension for CropStart in CropStartXY)
            CroppedImage = ActiveImage[CropStartXY[1]:CropFinishXY[1], CropStartXY[0]:CropFinishXY[0]]
            cv2.imwrite(SavePath,CroppedImage)