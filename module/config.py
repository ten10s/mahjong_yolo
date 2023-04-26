from mahjong.hand_calculating.hand_config import HandConfig, OptionalRules
from mahjong.constants import EAST, SOUTH, WEST, NORTH

#アガリオプション
def agari_option(config={}):
  #場風の判別
  if config.get('round_wind') == 'EAST':
    round = EAST
  elif config.get('round_wind') == 'SOUTH':
    round = SOUTH
  elif config.get('round_wind') == 'WEST':
    round = WEST
  elif config.get('round_wind') == 'NORTH':
    round = NORTH

  #自風の判別
  if config.get('player_wind') == 'EAST':
    player = EAST
  elif config.get('player_wind') == 'SOUTH':
    player = SOUTH
  elif config.get('player_wind') == 'WEST':
    player = WEST
  elif config.get('player_wind') == 'NORTH':
    player = NORTH

  #喰いタン
  tanyao = True
  if 'has_open_tanyao' in config:
    tanyao = config.get('has_open_tanyao')

  return HandConfig(
      # ツモ
      is_tsumo          = config.get("is_tsumo"),
      # リーチ
      is_riichi         = config.get("is_riichi"),
      # イッパツ
      is_ippatsu        = config.get("is_ippatsu"),
      # リンシャンカイホウ
      is_rinshan        = config.get("is_rinshan"),
      # チャンカン
      is_chankan        = config.get("is_chankan"),
      # ハイテイ
      is_haitei         = config.get("is_haitei"),
      # ホウテイ
      is_houtei         = config.get("is_houtei"),
      # ダブルリーチ
      is_daburu_riichi  = config.get("is_daburu_riichi"),
      # 流しマンガン
      is_nagashi_mangan = config.get("is_nagashi_mangan"),
      # テンホー
      is_tenhou         = config.get("is_tenhou"),
      # レンホー
      is_renhou         = config.get("is_renhou"),
      # チーホー
      is_chiihou        = config.get("is_chiihou"),
      #場風
      round_wind        = round,
      #自風
      player_wind       = player,
      #ルール追加
      options=OptionalRules(has_open_tanyao = tanyao, has_aka_dora = config.get('has_aka_dora'))
    )
