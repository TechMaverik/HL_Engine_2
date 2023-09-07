import cv2
import os
import pandas as pd
class PreprocessingTools:

    def convert_video_to_image(self, video_path): 
        cam = cv2.VideoCapture(video_path)
        try:          
            if not os.path.exists('data'):
                os.makedirs('data')  
        except OSError:
            print ('Error: Creating directory of data')
        currentframe = 0
        while(True):	            
            ret,frame = cam.read()
            if ret: 
                name = './data/' + str(currentframe) + '.jpg'
                print ('Creating...' + name)
                cv2.imwrite(name, frame)                
                currentframe += 1
            else:
                break
        cam.release()
        cv2.destroyAllWindows()
    
    def handpick_data(self,folder_path):
        list_dir=[]
        selection_index=[]
        handpicked_images=[]
        list_dir=os.listdir(folder_path)  
        for index in range(len(list_dir)):
            if(index%5==0):
                selection_index.append(index)
        for index in selection_index:
            handpicked_images.append(list_dir[index])
        return handpicked_images
    
    def clean_csv(self,csv_path):
        df=pd.read_csv(csv_path)
        cleaned_df=df.dropna()
        cleaned_df.to_csv("vehicle_count_classification_from_image.csv")
        return "Completed cleaning data"


        



