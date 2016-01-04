import sys
import os

sys.path.append("/Users/Bya/git/predictEPL/config/")
sys.path.append("/Users/Bya/git/predictEPL/utils/")

import paths
import useful_methods


# Show Base Model Results
# return dfNB
def BaseRes():
    # Read as DF
    os.chdir(paths.READ_PATH_GAME_INFO)
    dfNB = useful_methods.csv_dic_df("Predict-NB-63min.csv")

    # Convert strings to Integer & Float
    dfNB['score_ht_home'] = [int(st) for st in dfNB['score_ht_home']]
    dfNB['score_ht_away'] = [int(st) for st in dfNB['score_ht_away']]
    dfNB['score_ft_home'] = [int(st) for st in dfNB['score_ft_home']]
    dfNB['score_ft_away'] = [int(st) for st in dfNB['score_ft_away']]

    dfNB['nb_pos_home'] = [float(st) for st in dfNB['nb_pos_home']]
    dfNB['nb_neg_home'] = [float(st) for st in dfNB['nb_neg_home']]
    dfNB['nb_pos_away'] = [float(st) for st in dfNB['nb_pos_away']]
    dfNB['nb_neg_away'] = [float(st) for st in dfNB['nb_neg_away']]

    # Use only Twitter data Games
    dfNB = dfNB[(dfNB['nb_neg_home'] != -1)].copy().reset_index(drop=True)

    # Print results
    BaseAnalyze(dfNB)

    return dfNB


# Show Odds Model Results
# return dfOdds
def OddsRes():
    # Data Read as DF
    dfOdds = useful_methods.OddsPortalDf()

    # Convert strings to Integer & Float
    dfOdds['score_ft_home'] = [int(st) for st in dfOdds['score_ft_home']]
    dfOdds['score_ft_away'] = [int(st) for st in dfOdds['score_ft_away']]

    dfOdds['odds_home'] = [float(st) for st in dfOdds['odds_home']]
    dfOdds['odds_away'] = [float(st) for st in dfOdds['odds_away']]
    dfOdds['odds_draw'] = [float(st) for st in dfOdds['odds_draw']]

    # Use only Twitter data Games
    dfOdds = dfOdds[
        # GW != [1, 2, 3, 12], index != [37, 68, 120, 159]
        (dfOdds['GW'] >= 4) & (dfOdds['GW'] != 12) &
        (dfOdds.index != 37) & (dfOdds.index != 68) & (dfOdds.index != 120) &
        (dfOdds.index != 159)
        ].copy().reset_index(drop=True)

    OddsAnalyze(dfOdds)

    return dfOdds


# Show Review Model Results
# return dfNB
def ReviewRes():
    # Read as DF
    os.chdir(paths.READ_PATH_GAME_INFO)
    dfNB = useful_methods.csv_dic_df("Predict-NB-63min.csv")

    # Convert strings to Integer & Float
    dfNB['score_ht_home'] = [int(st) for st in dfNB['score_ht_home']]
    dfNB['score_ht_away'] = [int(st) for st in dfNB['score_ht_away']]
    dfNB['score_ft_home'] = [int(st) for st in dfNB['score_ft_home']]
    dfNB['score_ft_away'] = [int(st) for st in dfNB['score_ft_away']]

    dfNB['nb_pos_home'] = [float(st) for st in dfNB['nb_pos_home']]
    dfNB['nb_neg_home'] = [float(st) for st in dfNB['nb_neg_home']]
    dfNB['nb_pos_away'] = [float(st) for st in dfNB['nb_pos_away']]
    dfNB['nb_neg_away'] = [float(st) for st in dfNB['nb_neg_away']]

    # Use only Twitter data Games
    dfNB = dfNB[(dfNB['nb_neg_home'] != -1)].copy().reset_index(drop=True)

    # Print resulst
    ReviewAnalyze(dfNB)

    return dfNB


# Emolex Model Results
# return dfEmolex
def EmolexRes():
    # Read as DF
    os.chdir(paths.READ_PATH_GAME_INFO)
    dfEmolex = useful_methods.csv_dic_df("Predict-Emolex-63min-NonRT.csv")

    # Convert strings to Integer & Float
    dfEmolex['score_ht_home'] = [int(st) for st in dfEmolex['score_ht_home']]
    dfEmolex['score_ht_away'] = [int(st) for st in dfEmolex['score_ht_away']]
    dfEmolex['score_ft_home'] = [int(st) for st in dfEmolex['score_ft_home']]
    dfEmolex['score_ft_away'] = [int(st) for st in dfEmolex['score_ft_away']]

    dfEmolex['pn_home'] = [float(st) for st in dfEmolex['pn_home']]
    dfEmolex['pn_away'] = [float(st) for st in dfEmolex['pn_away']]

    # Use only Twitter data Games
    dfEmolex = dfEmolex[(dfEmolex['pn_home'] != -1)].copy().reset_index(drop=True)

    # Show Resulst
    EmolexAnalyze(dfEmolex)

    return dfEmolex


# All Model Results
# return all models result as one dfAll
def AllRes():
    # Combine all DFs
    dfBase = BaseRes()
    dfOdds = OddsRes()
    dfReview = ReviewRes()
    dfEmolex = EmolexRes()

    # Copying Review Res
    dfAll = dfBase.copy()
    dfAll = dfReview.copy()

    # Adding Odds Res columns
    dfAll['odds_away'] = dfOdds['odds_away']
    dfAll['odds_home'] = dfOdds['odds_home']

    # Adding Emolex Res columns
    dfAll['pn_away'] = dfEmolex['pn_away']
    dfAll['pn_home'] = dfEmolex['pn_home']

    return dfAll


# Base Model Result Analyzer
def BaseAnalyze(df):
    # As Predicted
    predict_good = len(
        df[
            # HT: (h > a) & FT: (h > a)
            ((df['score_ht_home'] > df['score_ht_away']) & (df['score_ft_home'] > df['score_ft_away'])) |

            # HT: (h < a) & FT: (h < a)
            ((df['score_ht_home'] < df['score_ht_away']) & (df['score_ft_home'] < df['score_ft_away']))
        ]
    )

    # Predic Failed
    predict_ng = len(
        df[
            # HT: (h > a) & FT: (h < a)
            ((df['score_ht_home'] > df['score_ht_away']) & (df['score_ft_home'] < df['score_ft_away'])) |

            # HT: (h < a) & FT: (h > a)
            ((df['score_ht_home'] < df['score_ht_away']) & (df['score_ft_home'] > df['score_ft_away']))
        ]
    )

    # Can't Predict, HT:DRAW
    ht_draw = len(
        df[
            # FT: (h = a)
            (df['score_ht_home'] == df['score_ht_away'])
        ]
    )

    # Not Our Concern, FT: DRAW
    ft_draw = len(
        df[
            # FT: (h = a)
            (df['score_ft_home'] == df['score_ft_away'])
        ]
    )

    print("*************************")
    print("Base Model Resulst:\n")
    # Show Results
    print("[GOOD]: {0}\n[NG]: {1}\n[HT DRAW]:{2}\n[FT DRAW]:{3}".format(
            predict_good, predict_ng, ht_draw, ft_draw))

    return (predict_good, predict_ng, ht_draw, ft_draw)


# Odds Model Result Analyzer
def OddsAnalyze(df):
    # NOTE: Lower odds score are WIN

    # As Predicted
    predict_good = len(
        df[
            # Odds: (h < a) & FT: (h > a)
            ((df['odds_home'] < df['odds_away']) & (df['score_ft_home'] > df['score_ft_away'])) |

            # Odds: (h > a) & FT: (h < a)
            ((df['odds_home'] > df['odds_away']) & (df['score_ft_home'] < df['score_ft_away']))
        ]
    )

    # Predict Failed
    predict_ng = len(
        df[
            # Odds: (h < a) & FT: (h > a)
            ((df['odds_home'] > df['odds_away']) & (df['score_ft_home'] > df['score_ft_away'])) |

            # Odds: (h < a) & FT: (h < a)
            ((df['odds_home'] < df['odds_away']) & (df['score_ft_home'] < df['score_ft_away']))
        ]
    )

    # Not Our Concern, FT: DRAW
    ft_draw = len(
        df[
            # FT: (h = a)
            (df['score_ft_home'] == df['score_ft_away'])
        ]
    )

    print("*************************")
    print("Odds Model Resulst:\n")
    print("[GOOD]: {0}\n[NG]: {1} \n[FT DRAW]:{2}".format(
            predict_good, predict_ng, ft_draw))

    return (predict_good, predict_ng, ft_draw)


# Base Model Result Analyzer
def ReviewAnalyze(df):
    # As Predicted
    predict_good = len(
        df[
            # HT: (h > a) & FT: (h > a)
            ((df['nb_pos_home'] > df['nb_pos_away']) & (df['score_ft_home'] > df['score_ft_away'])) |

            # HT: (h < a) & FT: (h < a)
            ((df['nb_pos_home'] < df['nb_pos_away']) & (df['score_ft_home'] < df['score_ft_away']))
        ]
    )

    # Predict Failed
    predict_ng = len(
        df[
            # HT: (h > a) & FT: (h > a)
            ((df['nb_pos_home'] > df['nb_pos_away']) & (df['score_ft_home'] < df['score_ft_away'])) |

            # HT: (h < a) & FT: (h < a)
            ((df['nb_pos_home'] < df['nb_pos_away']) & (df['score_ft_home'] > df['score_ft_away']))
        ]
    )

    # Not Our Concern, FT: DRAW
    ft_draw = len(
        df[
            # FT: (h = a)
            (df['score_ft_home'] == df['score_ft_away'])
        ]
    )

    print("*************************")
    print("Review Model Resulst:\n")
    # Show Results
    print("[GOOD]: {0}\n[NG]:{1} \n[FT DRAW]:{2}".format(
            predict_good, predict_ng, ft_draw))

    return (predict_good, predict_ng, ft_draw)


# Emolex Model Result Analyzer
def EmolexAnalyze(df):
    # NOTE: Lower odds score are WIN

    # As Predicted
    predict_good = len(
        df[
            # Emolex: (h > a) & FT: (h > a)
            ((df['pn_home'] > df['pn_away']) & (df['score_ft_home'] > df['score_ft_away'])) |

            # Emolex: (h < a) & FT: (h < a)
            ((df['pn_home'] < df['pn_away']) & (df['score_ft_home'] < df['score_ft_away']))
        ]
    )

    # Predict Failed
    predict_ng = len(
        df[
            # Emolex: (h > a) & FT: (h < a)
            ((df['pn_home'] > df['pn_away']) & (df['score_ft_home'] < df['score_ft_away'])) |

            # Emolex: (h < a) & FT: (h > a)
            ((df['pn_home'] < df['pn_away']) & (df['score_ft_home'] > df['score_ft_away']))
        ]
    )

    # Not Our Concern, FT: DRAW
    ft_draw = len(
        df[
            # FT: (h = a)
            (df['score_ft_home'] == df['score_ft_away'])
        ]
    )

    print("*************************")
    print("Emolex Model Resulst:\n")
    print("[GOOD]: {0}\n[NG]: {1} \n[FT DRAW]:{2}".format(
            predict_good, predict_ng, ft_draw))

    return (predict_good, predict_ng, ft_draw)
