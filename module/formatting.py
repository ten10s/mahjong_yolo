def formatting(label, df):
  hai = {
    '一' : '1',
    '二' : '2',
    '三' : '3',
    '四' : '4',
    '伍' : '5',
    '六' : '6',
    '七' : '7',
    '八' : '8',
    '九' : '9',
    '東' : '1',
    '南' : '2',
    '西' : '3',
    '北' : '4',
    '白' : '5',
    '發' : '6',
    '中' : '7', 
  }
  man = ''
  pin = ''
  sou = ''
  honors = ''
  dora = False

  win_tile = {
    'man' : '',
    'pin' : '',
    'sou' : '',
    'honors' : ''
  }
  melds = []
  win_man     = ''
  win_pin     = ''
  win_sou     = ''
  win_honors  = ''

  for i in df:
    for t in i:
      if label[t][-1:] == '萬':
        if label[t][:1] == '赤':
          man += '0'
          dora = True
        else:
          man += hai[label[t][:1]]
      elif label[t][-1:] == '筒':
        if label[t][:1] == '赤':
          pin += '0'
          dora = True
        else:
          pin += hai[label[t][:1]]
      elif label[t][-1:] == '索':
        if label[t][:1] == '赤':
          sou += '0'
          dora = True
        else:
          sou += hai[label[t][:1]]
      elif label[t] == '槓':
        pass
      else:
        honors += hai[label[t]]

    #アガリ牌
    if len(i) == 1:
      if label[i[0]][-1:] == '萬':
        if label[i[0]][:1] == '赤':
          win_man += '5'
        else:
          win_man += hai[label[i[0]][:1]]
      elif label[i[0]][-1:] == '筒':
        if label[i[0]][:1] == '赤':
          win_pin += '5'
        else:
          win_pin += hai[label[i[0]][:1]]
      elif label[i[0]][-1:] == '索':
        if label[i[0]][:1] == '赤':
          win_sou += '5'
        else:
          win_sou += hai[label[i[0]][:1]]
      else:
        win_honors += hai[label[i[0]]]
    #鳴き
    elif len(i) == 3:
      dst = [str(hai[label[j][:1]]) if label[j][:1] != '赤' else '5' for j in i]
      if i[0] == i[1]:
        pon_or_chi = 'PON'
      else:
        pon_or_chi = 'CHI'
      if label[i[0]][-1:] == '萬':
        melds.append({pon_or_chi:['man', ''.join(dst)]})
      elif label[i[0]][-1:] == '筒':
        melds.append({pon_or_chi:['pin', ''.join(dst)]})
      elif label[i[0]][-1:] == '索':
        melds.append({pon_or_chi:['sou', ''.join(dst)]})
      else:
        melds.append({pon_or_chi:['honors', ''.join(dst)]})

    elif len(i) == 4:
      #True:ミンカン,False:アンカン
      kan = False
      dst = []
      for j in i:
        if label[j][:1] == '赤':
          dst.append('5')
        elif label[j] == '槓':
          kan = True
        else:
          dst.append(str(hai[label[j][:1]]))
          kind = label[j][-1:]

      while len(dst) < 4:
        dst.append(dst[0])

      if kind == '萬':
        melds.append({'KAN':['man', ''.join(dst), kan]})
         #tilesのアンカン処理
        if kan:
          man += dst[0] + dst[0]
      elif kind == '筒':
        melds.append({'KAN':['pin', ''.join(dst), kan]})
         #tilesのアンカン処理
        if kan:
          pin += dst[0] + dst[0]
      elif kind == '索':
        melds.append({'KAN':['sou', ''.join(dst), kan]})
         #tilesのアンカン処理
        if kan:
          sou += dst[0] + dst[0]
      else:
        melds.append({'KAN':['honors', ''.join(dst), kan]})
         #tilesのアンカン処理
        if kan:
          honors += dst[0] + dst[0]

  tiles = {
    'man' : man,
    'pin' : pin,
    'sou' : sou,
    'honors' : honors,
  }

  if dora:
    tiles['has_aka_dora'] = True

  win_tile = {
    'man' : win_man,
    'pin' : win_pin,
    'sou' : win_sou,
    'honors' : win_honors,
  }

  return tiles, win_tile, melds

# hai = [[29, 22, 22], [37, 15, 15, 37], [0, 0, 0, 21, 22, 23, 30], [30]]
# label = {
#   0: '一萬', 1: '二萬', 2: '三萬', 3: '四萬', 4: '伍萬', 5: '六萬', 6: '七萬', 7: '八萬', 8: '九萬', 9: '一筒', 10: '二筒', 11: '三筒', 12: '四筒', 13: '伍筒', 14: '六筒', 15: '七筒', 16: '八筒', 17: '九筒', 18: '一索', 19: '二索', 20: '三索', 21: '四索', 22: '伍索', 23: '六索', 24: '七索', 25: '八索', 26: '九索', 27: '赤萬', 28: '赤筒', 29: '赤索', 30: '東', 31: '南', 32: '西', 33: '北', 34: '白', 35: '發', 36: '中', 37: '槓'
# }

# if __name__ == '__main__':
#   print(formatting(label, hai))
