import cv2
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import json
import requests
import base64
import crop
import key
import img2text
crop.cropping("ex0")
reply = img2text.gpt4o()
print(reply)