from mahjong.hand_calculating.hand import HandCalculator
from mahjong.tile import TilesConverter
from mahjong.meld import Meld
from mahjong.shanten import Shanten
from module.config import agari_option

class mahjong_calculation:
  def __init__(self, tiles, win_tile, meld=None, dora={}, config={}, debug=False):
    #手牌
    self.tiles_136 = TilesConverter.string_to_136_array(man=tiles['man'], pin=tiles['pin'], sou=tiles['sou'], honors=tiles['honors'], has_aka_dora=tiles.get('has_aka_dora'))
    self.tiles_34 = TilesConverter.string_to_34_array(man=tiles['man'], pin=tiles['pin'], sou=tiles['sou'], honors=tiles['honors'])
    #アガリ牌
    self.win_tile = TilesConverter.string_to_136_array(man=win_tile['man'], pin=win_tile['pin'], sou=win_tile['sou'], honors=win_tile['honors'])[0]
    #鳴き
    self.melds = []
    for key in meld[0]:
      hai = {
        key : meld[0][key]
      }
      if hai.get('KAN'):
        self.melds.append(
          Meld(Meld.KAN, TilesConverter.string_to_136_array(
              man    = hai[key][1] if hai[key][0] == 'man' else '',
              pin    = hai[key][1] if hai[key][0] == 'pin' else '',
              sou    = hai[key][1] if hai[key][0] == 'sou' else '',
              honors = hai[key][1] if hai[key][0] == 'honors' else '',
            ), hai[key][2] if hai[key][2] else ''
          )
        )
      else:
        self.melds.append(
          Meld(Meld.KAN if list(hai.keys())[0] == 'KAN' else Meld.PON if list(hai.keys())[0] == 'PON' else Meld.CHI,
            TilesConverter.string_to_136_array(
              man    = hai[key][1] if hai[key][0] == 'man' else '',
              pin    = hai[key][1] if hai[key][0] == 'pin' else '',
              sou    = hai[key][1] if hai[key][0] == 'sou' else '',
              honors = hai[key][1] if hai[key][0] == 'honors' else '',
            )
          )
        )

    #ドラ
    self.dora_indicators = []
    for key in dora:
      hai = {
        key : dora[key]
        }
      self.dora_indicators.append(TilesConverter.string_to_136_array(man=hai.get('man'), pin=hai.get('pin'), sou=hai.get('sou'), honors=hai.get('honors'))[0])
    
    #オプション
    self.config = agari_option(config)
    #ロンかツモか
    self.is_tsumo = config.get("is_tsumo", False)
    #親や子か
    self.is_dealer = config["player_wind"] == "EAST"
    #点数詳細表示
    self.debug = debug

    # #場風
    # self.round_wind = config['round_wind']
    # #自風
    # self.player_wind = config['player_wind']

  #点数計算
  def print_hand_result(self):
    calculator = HandCalculator()
    #計算結果
    result = calculator.estimate_hand_value(self.tiles_136, self.win_tile, self.melds, self.dora_indicators, self.config)
    if result.han and result.han != 1:
      if result.han <= 5:
          basic_score = result.fu * 2 ** (result.han + 2)
          if basic_score > 2000:
              hansu = "満貫"
          else:
              hansu = ""
      elif result.han <= 7:
          hansu = "跳満"
      elif result.han <= 10:
          hansu = "倍満"
      elif result.han <= 12:
          hansu = "三倍満"
      else:
          n = result.han // 13
          if n == 1:
              hansu = "役満"
          else:
              hansu = "{} 倍役満".format(n)

      if result.han < 1:
          all_cost = "1 飜縛りを満たしていません"
      elif self.is_tsumo:
          if self.is_dealer:
              all_cost = "{}点 オール".format(result.cost["additional"])
          else:
              all_cost = "親 {}点 / 子 {}点".format(result.cost["additional"], result.cost["main"])

      print(hansu)
      print(all_cost)

      #詳細表示
      if self.debug:
        # 翻数, 符数
        print(f'{result.han}藩 {result.fu}符')
        # 役
        print(result.yaku)
        # 符数の詳細
        for fu_item in result.fu_details:
            print(fu_item)
        print('')

    #テンパっていない場合シャンテン数
    else:
      shanten = Shanten()
      try:
        result = shanten.calculate_shanten(self.tiles_34)
        print('{}シャンテン'.format(result+1))
      except:
        print('無役')


# #(honors=1:東, 2:南, 3:西, 4:北, 5:白, 6:發, 7:中)
# #(赤ドラは0,またはrを用いる(並び順はなんでもOK), 'has_aka_dora' : Trueを設定)
# tiles = {
#   'man' : '111',
#   'pin' : '7777',
#   'sou' : '045565',
#   'honors' : '11',
#   'has_aka_dora' : True
#   }
# win_tile = {
#   'man' : '',
#   'pin' : '',
#   'sou' : '',
#   'honors' : '1'
#   }
# #鳴き(チー:CHI, ポン:PON, カン:KAN(True:ミンカン,False:アンカン), カカン:CHANKAN, ヌキドラ:NUKI)
# melds = [{
#   'KAN' : ['pin', '7777', False],
# }]
# dora = {
# }

# #(赤ドラの場合は、'has_aka_dora' : Trueを追加)
# #デフォルトは喰いタン、赤ドラ無効
# config = {
#   'is_tsumo' : True,
#   'round_wind' : 'EAST',
#   'player_wind' : 'EAST',
#   'has_aka_dora' : True
# }


# if __name__ == '__main__':
#   a = mahjong_calculation(tiles, win_tile, melds, dora, config, debug=True)
#   a.print_hand_result()
