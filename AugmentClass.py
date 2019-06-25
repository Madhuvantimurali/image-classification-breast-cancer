import os
import skimage as sk
import shutil
import time
import random
from scipy import ndarray
import joblib

def download_dataset(d_name):
    def convert_size(size_bytes):
       if size_bytes == 0:
           return "0B"
       size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
       i = int(math.floor(math.log(size_bytes, 1024)))
       p = math.pow(1024, i)
       s = round(size_bytes / p, 2)
       return f'{s:.2f} {size_name[i]}'

    import math
    import requests
    import sys
    import time
    url = 'http://www.inf.ufpr.br/vri/databases/BreaKHis_v1.tar.gz'
    #r = requests.get(url)
    with open(f'{d_name}.tar.gz', 'wb') as f:
        start = time.clock()
        print(f"Downloading {d_name}.tar.gz")
        response = requests.get(url, stream=True)
        total_length = response.headers.get('content-length')

        if total_length is None: # no content length header
            f.write(response.content)
        else:
            dl = 0
            total_length = int(total_length)
            t_len=convert_size(total_length)
            for data in response.iter_content(chunk_size=4096):
                dl += len(data)
                #speed=convert_size(dl//(time.clock()-start))+'/s'
                d_len=convert_size(dl)
                print(f'[{dl/total_length*100:.2f}%][{d_len} / {t_len}] Downloaded   ',end='\r')
                f.write(data)


        #f.write(r.content)

class ImageAugment():

    def __init__ (self, d_name='BreaKHis_v1', num_files_desired=10,dest_root=None):

        self.dest_root=dest_root
        self.root = os.getcwd()
        self.d_name=d_name
        self._modify_wd()
        self.files=[]
        self.make_dest_dirs()
        self.num_files_desired = num_files_desired

        self.transforms=[   lambda img: sk.transform.rotate(img,random.choice([90,180,270])),
                            lambda img: sk.util.random_noise(img),
                            lambda img: img[:,::-1]
                        ]

        self.total_transforms = len(self.transforms)

    def _modify_wd(self):

        new_root=""
        flag=False
        for root,dirs,_ in os.walk(self.root):
            if self.d_name in dirs:
                new_root=os.path.relpath(root)
                flag=True
                break
        if flag:
            self.root=os.path.join(self.root,new_root)
            os.chdir(self.root)
            if self.dest_root is None:
                self.dest_root=self.root
            else:
                self.dest_root=os.path.abspath(self.dest_root)
        else:
            exit('Dataset is not present in any subdirectories')

    def make_dest_dirs(self):

        folders = []
        for root, dirs, files in os.walk(os.path.join(self.root,self.d_name)):
            self.files.extend([os.path.join(root,f) for f in files if self._is_valid_image(f)])
            if not dirs:
                folders.append(root)

        for each in folders:
            try:
                os.makedirs(self.path_to_aug_path(each))
            except:
                pass

    def _is_valid_image(self, image_path):
        #split image path into folder and file.
        #We discard folder
        image_name=os.path.basename(image_path)
        extns={'png','jpg','tiff','gif','bmp'} #{} is a dict or a set. if it has Key:Value pairs, it is a dict
        name=image_name.split('.')
        name,ext=name[-2],name[-1] # . is removed after split so ext will be only 'png'
        if ext in extns and 'augmented' not in name: # "substring" not in "string" is a valid way of checking
            return True
        return False

    def path_to_aug_path(self, path_name):
        ind = path_name.index(self.d_name)
        out=path_name.replace(self.d_name,self.d_name+'_Aug',1)
        out=os.path.join(self.dest_root,out[ind:])

        return out



    def augment_file(self,path):
        folder_path = os.path.dirname(path)

        img_name = os.path.basename(path)

        #print(f'\nparent folder : ...{folder_path[-20:]} image name : {img_name}')

        #ready to augment
        num_generated_files= 0
        name=img_name.split('.')[-2]
        ext = img_name.split('.')[-1]

        image_to_transform = sk.io.imread(path)
        while num_generated_files < self.num_files_desired:
            # random num of transformation to apply
            num_transformations_to_apply = random.randint(1,self.total_transforms)
            # init the target image
            transformed_image = image_to_transform.copy()

            # sample k choices from the given list in argument 1
            sequence_of_transforms=random.choices(self.transforms,k=num_transformations_to_apply)

            #sequence_of_transforms contains 1-k operations to apply in sequence
            for each in sequence_of_transforms:
                transformed_image=each(transformed_image)

            new_file_path = f'{name}_augmented_{num_generated_files}.{ext}'
            dest_folder_path = self.path_to_aug_path(folder_path)
            # write image to the disk
            sk.io.imsave(os.path.join(dest_folder_path,new_file_path), transformed_image)
            num_generated_files += 1

            #mark as visited

        #print(f"  {path[-50:]} processed..\n")
        shutil.move(path,dest_folder_path)
        return True






    def do_parallel(self,ops=['augment'],mode='processes'):
        funcs={'augment':self.augment_file}
        for op in ops:
            func = funcs[op]
            joblib.Parallel(n_jobs=-1, verbose=51, prefer=mode)(
             map(joblib.delayed(func), self.files))

if __name__ == '__main__':
    #download_dataset(d_name='BreaKHis_v1')
    a=ImageAugment()
    a.do_parallel()
