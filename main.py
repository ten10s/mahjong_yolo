from ultralytics import YOLO
import module
import pandas as pd

#画像を横に整形する
img = module.rotation_exif("./yolo_test13.JPG")
#認証処理
model = YOLO("runs/detect/train/weights/best.pt")
results = model(img, iou=0.5, conf=0.3)
#, save=True, save_txt=True, exist_ok=True
#y軸で絞り込み(グループ化)
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

#牌の情報を抽出
result = [int(i[-1:][0]) for i in results[0].boxes.numpy().data]
#ラベル抽出
label = results[0].names
#データの整形・手牌
######################修正##############################
kan = False
formatting = module.formatting(result, label, hai, kan)
tiles = formatting[0]
#アガリ牌
win_tile = formatting[1]
#鳴き
melds = formatting[2]
#ドラ
dora = {
}
# #オプション
config = {
  'is_tsumo' : True,
  'round_wind' : 'EAST',
  'player_wind' : 'EAST',
}
if tiles.get('has_aka_dora'):
    config['has_aka_dora'] = True

#計算処理
mahjong = module.mahjong_calculation(tiles, win_tile, melds, dora, config)
mahjong.print_hand_result()
