# breastcancerclassification
Classification of histopathological breast cancer histopathological images using Inception v3.
 The dataset is available at:
https://web.inf.ufpr.br/vri/databases/breast-cancer-histopathological-database-breakhis/

pngtojpeg.py - conversion of png images(default type of dataset) to jpeg(requirement of Inception v3)

AugmentClass.py - Data Augmentation techniques of scaling,flipping,rotation by 90,120 and 270 degrees and addition of white noise are implemented.

retrain.py -
Transfer Learning is adopted to reduce computational complexity. The Inception v3 model which has been trained from scratch on ImageNet dataset
is retrained using this script.The program produces a graph object as the output.

quantize_graph.py - quantizes the output graph

evaluate.py - 
Evaluates the retrained graph and calculates classification accuracy. 

Dedup Images.ipnyb - Jupyter notebook that enables de-duplication of images in a given location
