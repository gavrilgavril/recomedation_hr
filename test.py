
import requests, zipfile, io
#from sentence_transformers import SentenceTransformer, InputExample, losses
#from torch.utils.data import DataLoader
import itertools
import pandas as pd
##import torch
#from sklearn.metrics.pairwise import cosine_similarity
import os
import json
#url_=os.environ['URL_COURSES']
import logging
logger = logging.getLogger(__name__)
import sys



url_post='https://molga.softaria.com/api/learning/ml/guidance'
data= [{'type': 'career', 'subjectArea': 'consultingSapHcm', 'level': 3, 'courses': [840, 854, 1077, 614, 354, 663, 862, 1310, 491, 355, 1076, 1061, 794, 1177, 569, 1309, 857, 1456, 1133, 1256, 1091, 1183, 1445, 139, 151, 407, 1236, 1130, 80, 744]}, {'type': 'career', 'subjectArea': 'consultingSapHcm', 'level': 2, 'courses': [268, 270, 862, 115, 89, 69, 1229, 264, 1473, 1086, 748, 282, 773, 1084, 137, 1025, 516, 1392, 998, 809, 1116, 223, 1048, 489, 74, 214, 70, 1147, 1278, 1239]}, {'type': 'career', 'subjectArea': 'consultingSapHcm', 'level': 1, 'courses': [1031, 1046, 121, 1042, 920, 1066, 419, 873, 670, 345, 1099, 613, 671, 1028, 346, 874, 563, 1026, 1049, 357, 566, 388, 1098, 352, 1029, 1027, 489, 98, 522, 922]}, {'type': 'career', 'subjectArea': 'consultingSapHcm', 'level': 0, 'courses': [416, 1431, 948, 578, 1147, 137, 862, 1119, 908, 741, 1229, 1157, 1111, 1236, 1116, 854, 1417, 1196, 1085, 1015, 1309, 1125, 1310, 1429, 1271, 1270, 573, 906, 1124, 417]}, {'type': 'career', 'subjectArea': 'hr', 'level': 1, 'courses': [1055, 70, 188, 69, 945, 947, 931, 286, 1161, 319, 1423, 1422, 1287, 86, 1386, 1282, 1472, 946, 356, 89, 942, 1416, 187, 214, 59, 264, 1473, 223, 75, 928]}, {'type': 'career', 'subjectArea': 'hr', 'level': 0, 'courses': [1161, 69, 931, 1055, 70, 945, 86, 947, 286, 946, 319, 1423, 188, 1282, 68, 1287, 214, 1386, 223, 1416, 74, 942, 356, 1278, 264, 1404, 305, 928, 59, 187]}, {'type': 'career', 'subjectArea': 'devBackend', 'level': 3, 'courses': [571, 424, 170, 1361, 965, 1249, 171, 1452, 1325, 153, 104, 1341, 172, 181, 143, 234, 156, 253, 173, 174, 1213, 166, 272, 168, 175, 1207, 180, 155, 465, 182]}, {'type': 'career', 'subjectArea': 'devBackend', 'level': 2, 'courses': [873, 1046, 1031, 920, 121, 670, 1066, 345, 613, 671, 1042, 1028, 346, 419, 1099, 1029, 1049, 563, 388, 874, 1026, 352, 357, 1027, 1098, 98, 489, 566, 949, 522]}, {'type': 'career', 'subjectArea': 'devBackend', 'level': 1, 'courses': [873, 1046, 121, 1031, 920, 670, 1066, 1042, 345, 613, 419, 671, 346, 1099, 1028, 874, 1049, 563, 1029, 566, 357, 388, 1026, 352, 1098, 1027, 489, 522, 98, 922]}, {'type': 'career', 'subjectArea': 'devBackend', 'level': 0, 'courses': [873, 1046, 1049, 357, 1027, 670, 613, 1031, 345, 920, 1099, 1066, 388, 121, 671, 1028, 346, 822, 1029, 1098, 1042, 419, 1026, 737, 612, 823, 563, 606, 722, 958]}, {'type': 'career', 'subjectArea': 'devFrontend', 'level': 3, 'courses': [604, 480, 606, 936, 1259, 425, 387, 921, 823, 856, 822, 597, 508, 1445, 142, 842, 370, 852, 554, 839, 633, 492, 1241, 1063, 1057, 783, 449, 820, 612, 535]}, {'type': 'career', 'subjectArea': 'devFrontend', 'level': 2, 'courses': [606, 823, 1259, 604, 936, 856, 425, 839, 822, 921, 1241, 706, 612, 852, 1057, 480, 933, 484, 142, 387, 842, 603, 582, 784, 508, 771, 449, 716, 1063, 1075]}, {'type': 'career', 'subjectArea': 'devFrontend', 'level': 1, 'courses': [651, 644, 797, 817, 1343, 766, 379, 724, 557, 798, 285, 1223, 567, 206, 725, 747, 583, 584, 151, 1313, 665, 366, 480, 935, 241, 1445, 1141, 43, 1437, 298]}, {'type': 'career', 'subjectArea': 'devFrontend', 'level': 0, 'courses': [797, 651, 1343, 557, 644, 1313, 209, 724, 819, 817, 241, 665, 766, 379, 798, 1267, 43, 722, 242, 1437, 935, 997, 1100, 760, 480, 206, 1215, 1357, 1096, 827]}, {'type': 'career', 'subjectArea': 'projectManagement', 'level': 1, 'courses': [1050, 1141, 491, 1385, 1155, 1359, 1148, 1104, 1281, 488, 428, 291, 715, 1449, 91, 663, 1326, 1156, 518, 1343, 389, 1081, 1290, 348, 650, 687, 1283, 355, 598, 783]}, {'type': 'career', 'subjectArea': 'projectManagement', 'level': 0, 'courses': [1050, 1141, 491, 1385, 1155, 1359, 1148, 1104, 1281, 488, 428, 291, 715, 1449, 91, 663, 1326, 1156, 518, 1343, 389, 1081, 1290, 348, 650, 687, 1283, 355, 598, 783]}, {'type': 'career', 'subjectArea': 'hr', 'level': 1, 'courses': [1055, 70, 188, 69, 945, 947, 931, 286, 1161, 319, 1423, 1422, 1287, 86, 1386, 1282, 1472, 946, 356, 89, 942, 1416, 187, 214, 59, 264, 1473, 223, 75, 928]}, {'type': 'career', 'subjectArea': 'hr', 'level': 0, 'courses': [1161, 69, 931, 1055, 70, 945, 86, 947, 286, 946, 319, 1423, 188, 1282, 68, 1287, 214, 1386, 223, 1416, 74, 942, 356, 1278, 264, 1404, 305, 928, 59, 187]}, {'type': 'career', 'subjectArea': 'productManagement', 'level': 0, 'courses': [1187, 1198, 636, 939, 1015, 637, 1417, 1216, 129, 1214, 1186, 802, 1225, 1018, 1211, 1152, 1180, 938, 699, 1191, 1119, 1001, 937, 287, 871, 405, 1189, 934, 898, 973]}, {'type': 'career', 'subjectArea': 'productManagement', 'level': 1, 'courses': [1079, 283, 899, 1106, 1109, 117, 901, 1330, 735, 896, 1016, 431, 1076, 1190, 702, 325, 1260, 1077, 377, 889, 925, 1002, 958, 323, 375, 744, 835, 371, 130, 432]}]
def download_data():
    r= requests.get('https://molga.softaria.com/api/learning/ml/course')
    logger.warning("Загружаю данные о крусах")
    if r.status_code == 200:
        logger.warning("===> Данных о курсах успешно загружены")
    else:
        logger.warning("===> Загрузите данные о курсах на портал")
        sys.exit()
    #z = zipfile.ZipFile(io.BytesIO(r.content))
    #z.extractall("data/")
def post_data(data):
    r= requests.post(url_post, data=json.dumps(data), headers={
    'Content-type':'application/json', 
    'Accept':'application/json'})
    #print(r.json()["message"])
   # print(r.status_code)
   # print(r.content)
    #print(json.dumps(r.text, indent=4, sort_keys=True, default=lambda o:'<not serializable>'))
    if r.status_code == 200:
        logger.info("===> Данных о рекомендация загружены на портал")
    else:
       # print(r.json())
        logger.warning(r.json()["message"])
        logger.warning(f"===> не удалось загрузить рекомендации на портал: \n {r.json()["message"]}")
        #logger.warning("Altitude: {r.json()["message"]})
       # logger.warning("===> не удалось загрузить",r.json()["message"])
        sys.exit()  


def run_model():
    logging.basicConfig(format='%(levelname)s:%(asctime)s %(funcName)s - %(message)s', level=logging.INFO,
                            filename="log.txt")
    try:
        
        logger.info("SCRIPT STARTED")
        #download_data()
       # print(2*1000)
        #download_configs()
        #infernce_model=Recomedation()
        post_data(data)
        logger.info("SCRIPT FINISHED SUCCESSFULLY")
    except Exception as e:
        logger.critical(e, exc_info=True)   
logger.info("SCRIPT STARTED")
run_model()
