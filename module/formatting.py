def formatting(result, label, df, kan):
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

  for i in result:
    if label[i][-1:] == '萬':
      if label[i][:1] == '赤':
        man += '0'
        dora = True
      else:
        man += hai[label[i][:1]]
    elif label[i][-1:] == '筒':
      if label[i][:1] == '赤':
        pin += '0'
        dora = True
      else:
        pin += hai[label[i][:1]]
    elif label[i][-1:] == '索':
      if label[i][:1] == '赤':
        sou += '0'
        dora = True
      else:
        sou += hai[label[i][:1]]
    else:
      honors += hai[label[i]]

  tiles = {
    'man' : man,
    'pin' : pin,
    'sou' : sou,
    'honors' : honors,
  }
  if dora:
    tiles['has_aka_dora'] = True

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
      dst = [str(hai[label[j][:1]]) for j in i]
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
      dst = [str(hai[label[j][:1]]) for j in i]
      if label[i[0]][-1:] == '萬':
        melds.append({'KAN':['man', ''.join(dst), kan]})
      elif label[i[0]][-1:] == '筒':
        melds.append({'KAN':['pin', ''.join(dst), kan]})
      elif label[i[0]][-1:] == '索':
        melds.append({'KAN':['sou', ''.join(dst), kan]})
      else:
        melds.append({'KAN':['honors', ''.join(dst), kan]})

  win_tile = {
    'man' : win_man,
    'pin' : win_pin,
    'sou' : win_sou,
    'honors' : win_honors,
  }
  
  return tiles, win_tile, melds
