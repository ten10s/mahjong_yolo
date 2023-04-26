from PIL import Image
from PIL import ImageOps
from PIL.ExifTags import TAGS

def get_exif_rotation(orientation_num):
  #ExifのRotationの数値から、回転する数値と、ミラー反転するかどうかを取得する
  #return 回転度数,反転するか(0 1)
  if orientation_num == 1:
      return 0, 0
  if orientation_num == 2:
      return 0, 1
  if orientation_num == 3:
      return 180, 0
  if orientation_num == 4:
      return 180, 1
  if orientation_num == 5:
      return 270, 1
  if orientation_num == 6:
      return 270, 0
  if orientation_num == 7:
      return 90, 1
  if orientation_num == 8:
      return 90, 0

def rotation_exif(image):
  rotate  = 0
  reverse = 0
  img     = Image.open(image)
  # Exif データを取得
  # 存在しなければそのまま終了 空の辞書を返す
  try:
    exif = img._getexif()
  except AttributeError:
    return {}
  
  #exif情報からOrientationを取得
  exif_table = {}
  for tag_id, value in exif.items():
      tag = TAGS.get(tag_id, tag_id)
      exif_table[tag] = value

  if 'Orientation' in exif:
    rotate, reverse = get_exif_rotation(exif['Orientation'])

  data = img.getdata()
  mode = img.mode
  size = img.size
  with Image.new(mode, size) as img:
    img.putdata(data)
    if reverse == 1:
      img = ImageOps.mirror(img)
    if rotate != 0:
      img = img.rotate(rotate, expand=True)
    
  return img
