from ultralytics import YOLO
import module
import pandas as pd
import shutil
import cv2
import os


def main(data, img) :
  #画像を横に整形する
  # img = module.rotation_exif('./yolo_test3.JPG')
  #認証処理
  model = YOLO("runs/detect/train/weights/best.pt")
  results = model(img, iou=0.6, conf=0.3, save=True, exist_ok=True)
  #, save=True, save_txt=True, exist_ok=True
  #y軸で絞り込み(グループ化)
  try:
    df = pd.DataFrame(results[0].boxes.numpy().xywhn)
    y_diff = abs(df[1] - df.iloc[0,1])
    y_diff = y_diff[y_diff < 0.1]
    df_y = df.iloc[y_diff.index].sort_values(0)
    df_x = df.drop(y_diff.index, axis=0).sort_values(0)
    #x軸で絞り込み(グループ化)
    def x_group(df):
      list_index = 0
      hai = [[]]
      for index, row in df.iterrows():
        if row[0] > 0.1:
          list_index += 1
          hai.append([])
        hai[list_index].append(int(results[0].boxes.numpy().data[index][-1:]))
      return hai

    hai = x_group(df_y.diff()) + x_group(df_x.diff())

    #ラベル抽出
    label = results[0].names
    #データの整形・手牌
    formatting = module.formatting(label, hai, data)
    tiles = formatting[0]
    #アガリ牌
    win_tile = formatting[1]
    #鳴き
    melds = formatting[2]
    #ドラ
    dora = formatting[3]
    # #オプション
    config = formatting[4]

    if tiles.get('has_aka_dora'):
        config['has_aka_dora'] = True

    #計算処理
    mahjong = module.mahjong_calculation(tiles, win_tile, melds, dora, config, debug=False)
    result = mahjong.print_hand_result()
    
    #転移学習用に保存
    try :
      files = os.listdir("./meta")
      max_num = str(max([int(i[5:8]) for i in files])+1).zfill(3)
    except:
      max_num = "001" 
      
    result_img = cv2.imread('runs/detect/predict/image0.jpg')
    cv2.imwrite('meta/image' + max_num + '.jpg', result_img)
    
    return result

  except:
    
    #不要な画像を削除(上書き保存なので無くてもいい)
    shutil.rmtree('runs/detect/predict/')
    
    error = '牌が認識出来ません'
    
    return error
  # except Exception as e:
  #   print(e)


# if __name__ == '__main__':
#   data = {'agari': ['ツモ'], 'zikaze': ['東'], 'bakaze': ['北'], 'dora': ['伍萬,七萬,']}
#   main(data, "./yolo_test3.JPG")
