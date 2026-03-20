"""PBP (play-by-play) statistics stubs.

These functions raise NotImplementedError until PBP data is available.
"""

from __future__ import annotations

import pandas as pd


def calc_ast_atb3(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The percentage of total assists that were assists on above the break 3s."""
    raise NotImplementedError("PBP data not yet available: %AST ATB3")


def calc_ast_atr2(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The percentage of total assists that were assists at the rim."""
    raise NotImplementedError("PBP data not yet available: %AST ATR2")


def calc_ast_rim_3s(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The percentage of total assists that were assists either at the rim or on 3-pointers."""
    raise NotImplementedError("PBP data not yet available: %AST RIM+3s")


def calc_ast_rim_paint(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The percentage of total assists that were assists in the paint (including shots at the rim)."""
    raise NotImplementedError("PBP data not yet available: %AST RIM+PAINT")


def calc_ast_c3(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The percentage of total assists that were assists on corner 3s."""
    raise NotImplementedError("PBP data not yet available: %AST C3")


def calc_ast_dunk(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The percentage of total assists that were assists on dunks."""
    raise NotImplementedError("PBP data not yet available: %AST DUNK")


def calc_ast_paint2(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The percentage of total assists that were assists in the paint (not at the rim)."""
    raise NotImplementedError("PBP data not yet available: %AST PAINT2")


def calc_ast_mid2(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The percentage of total assists that were assists in the midrange."""
    raise NotImplementedError("PBP data not yet available: %AST MID2")


def calc_ast2(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The percentage of total assists that were assists on made 2-pointers."""
    raise NotImplementedError("PBP data not yet available: %AST2")


def calc_ast3(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The percentage of total assists that were assists on made 3-pointers."""
    raise NotImplementedError("PBP data not yet available: %AST3")


def calc_hc_freq(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The percentage of the team's offensive chances that were marked as half court (as opposed to transition or putback) chances."""
    raise NotImplementedError("PBP data not yet available: HC FREQ")


def calc_tr_freq(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The percentage of the team's offensive chances that were marked as transition (as opposed to half court or putback) chances."""
    raise NotImplementedError("PBP data not yet available: TR FREQ")


def calc_pb_freq(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The percentage of the team's offensive chances that were marked as putback(as opposed to half court or transition ) chances."""
    raise NotImplementedError("PBP data not yet available: PB FREQ")


def calc_poss(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Of all time where either team has possession (so excluding time when neither team has possession), what percentage belongs to this team."""
    raise NotImplementedError("PBP data not yet available: POSS%")


def calc_dunk_fga(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The percentage of shots taken that were dunk attempts."""
    raise NotImplementedError("PBP data not yet available: DUNK FGA%")


def calc_layup_fga(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Percentage of the players shots taken as layups."""
    raise NotImplementedError("PBP data not yet available: LAYUP FGA%")


def calc_lay_dunk_fga(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Percentage of the players shots taken as layups and dunks."""
    raise NotImplementedError("PBP data not yet available: LAY+DUNK FGA%")


def calc_shots_center(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Percentage of shots taken from the center of the court. This includes all shots where the shooter is positioned within 1 foot in either direction of the imaginary centerline of the court connecting the two rims."""
    raise NotImplementedError("PBP data not yet available: % Shots Center")


def calc_shots_left(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Percentage of shots taken from the left side of the court. This includes all shots where the shooter is positioned more than 1 foot to the left of the court's imaginary centerline."""
    raise NotImplementedError("PBP data not yet available: % Shots Left")


def calc_shots_right(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Percentage of shots taken from the right side of the court. This includes all shots where the shooter is positioned more than 1 foot to the right of the court's imaginary centerline."""
    raise NotImplementedError("PBP data not yet available: % Shots Right")


def calc_tov_10_secs(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The total number of turnovers tagged by the scorer as a 10 second violation by the team."""
    raise NotImplementedError("PBP data not yet available: TOV 10 SECS")


def calc_strk_10(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The total number of scoring streaks of 10+ consecutive points scored by the team."""
    raise NotImplementedError("PBP data not yet available: STRK 10+")


def calc_agst_10(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The total number of scoring streaks allowed of 10+ consecutive points allowed by the team."""
    raise NotImplementedError("PBP data not yet available: AGST 10+")


def calc_strk_12(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The total number of scoring streaks of 12+ consecutive points scored by the team."""
    raise NotImplementedError("PBP data not yet available: STRK 12+")


def calc_agst_12(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The total number of scoring streaks allowed of 12+ consecutive points allowed by the team."""
    raise NotImplementedError("PBP data not yet available: AGST 12+")


def calc_fgm2_astd(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The percentage of 2P shots made that were assisted."""
    raise NotImplementedError("PBP data not yet available: FGM2 ASTD%")


def calc_2sfld(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The percentage of 2-point shot attempts where a foul was drawn."""
    raise NotImplementedError("PBP data not yet available: 2SFLD%")


def calc_2sfld_100(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The number of 2-point shooting fouls drawn per 100 possessions."""
    raise NotImplementedError("PBP data not yet available: 2SFLD/100")


def calc_2sfld_40(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The number of 2-point shooting fouls drawn per 40 minutes."""
    raise NotImplementedError("PBP data not yet available: 2SFLD/40")


def calc_2sfld_g(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The number of 2-point shooting fouls drawn per game."""
    raise NotImplementedError("PBP data not yet available: 2SFLD/G")


def calc_2sfld(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The total number of 2-point shooting fouls drawn."""
    raise NotImplementedError("PBP data not yet available: 2SFLD")


def calc_2p_shot_att(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The number of 2-point field goal attempts plus shooting fouls drawn on missied shots. Effectively, the number of 2-point shot attempts by the player."""
    raise NotImplementedError("PBP data not yet available: 2P SHOT ATT")


def calc_2p_0_10s(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Percentage of the player's 2-point field goal attempts taken with 0 - 10 seconds remaining on the shot clock that were made."""
    raise NotImplementedError("PBP data not yet available: 2P% (0-10s)")


def calc_2p_20_30s(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Percentage of the player's 2-point field goal attempts taken with 20 - 30 seconds remaining on the shot clock that were made."""
    raise NotImplementedError("PBP data not yet available: 2P% (20-30s)")


def calc_2p_10_20s(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Percentage of the player's 2-point field goal attempts taken with 10 - 20 seconds remaining on the shot clock that were made."""
    raise NotImplementedError("PBP data not yet available: 2P% (10-20s)")


def calc_2p_in_hc(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """An estimate of 2-point field goal percentage (makes / attempts) on shots in the context of half court offense (as opposed to transition or putback)."""
    raise NotImplementedError("PBP data not yet available: 2P% in HC")


def calc_2p_in_tr(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """An estimate of 2-point field goal percentage (makes / attempts) on shots in the context of transition offense (as opposed to half court or putback)."""
    raise NotImplementedError("PBP data not yet available: 2P% in TR")


def calc_2pa_0_10s(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The total number of 2-point field goal attempts taken with 0 - 10 seconds remaining on the shot clock."""
    raise NotImplementedError("PBP data not yet available: 2PA (0-10s)")


def calc_2pa_10_20s(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The total number of 2-point field goal attempts taken with 10 - 20 seconds remaining on the shot clock."""
    raise NotImplementedError("PBP data not yet available: 2PA (10-20s)")


def calc_2pa_20_30s(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The total number of 2-point field goal attempts taken with 20 - 30 seconds remaining on the shot clock."""
    raise NotImplementedError("PBP data not yet available: 2PA (20-30s)")


def calc_2pa_in_hc(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """An estimate of the total number of 2-point field goal attempts taken in the context of half court offense (as opposed to transition or putback)."""
    raise NotImplementedError("PBP data not yet available: 2PA in HC")


def calc_2pa_in_tr(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """An estimate of the total number of 2-point field goal attempts taken in the context of transition offense (as opposed to half court or putback)."""
    raise NotImplementedError("PBP data not yet available: 2PA in TR")


def calc_2pm_in_hc(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """An estimate of the total number of 2-point field goals made in the context of half court offense (as opposed to transition or putback)."""
    raise NotImplementedError("PBP data not yet available: 2PM in HC")


def calc_2pm_in_tr(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """An estimate of the total number of 2-point field goals made in the context of transition offense (as opposed to half court or putback)."""
    raise NotImplementedError("PBP data not yet available: 2PM in TR")


def calc_2pm_0_10s(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The total number of 2-point field goals made with 0 - 10 seconds remaining on the shot clock."""
    raise NotImplementedError("PBP data not yet available: 2PM (0-10s)")


def calc_2pm_10_20s(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The total number of 2-point field goals made with 10 - 20 seconds remaining on the shot clock."""
    raise NotImplementedError("PBP data not yet available: 2PM (10-20s)")


def calc_2pm_20_30s(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The total number of 2-point field goals made with 20 - 30 seconds remaining on the shot clock."""
    raise NotImplementedError("PBP data not yet available: 2PM (20-30s)")


def calc_tov_3_secs(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The total number of turnovers tagged by the scorer as a 3 second violation by the team."""
    raise NotImplementedError("PBP data not yet available: TOV 3 SECS")


def calc_fgm3_astd(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The percentage of 3P shots made that were assisted."""
    raise NotImplementedError("PBP data not yet available: FGM3 ASTD%")


def calc_3sfld(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The percentage of 3-point shot attempts where a foul was drawn."""
    raise NotImplementedError("PBP data not yet available: 3SFLD%")


def calc_3sfld_100(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The number of 3-point shooting fouls drawn per 100 possessions."""
    raise NotImplementedError("PBP data not yet available: 3SFLD/100")


def calc_3sfld_40(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The number of 3-point shooting fouls drawn per 40 minutes."""
    raise NotImplementedError("PBP data not yet available: 3SFLD/40")


def calc_3sfld_g(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The number of 3-point shooting fouls drawn per game."""
    raise NotImplementedError("PBP data not yet available: 3SFLD/G")


def calc_3sfld(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The total number of 3-point shooting fouls drawn."""
    raise NotImplementedError("PBP data not yet available: 3SFLD")


def calc_3p_shot_att(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The number of 3-point field goal attempts plus shooting fouls drawn on missied shots. Effectively, the number of 3-point shot attempts by the player."""
    raise NotImplementedError("PBP data not yet available: 3P SHOT ATT")


def calc_3p_0_10s(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Percentage of the player's 3-point field goal attempts taken with 0 - 10 seconds remaining on the shot clock that were made."""
    raise NotImplementedError("PBP data not yet available: 3P% (0-10s)")


def calc_3p_20_30s(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Percentage of the player's 3-point field goal attempts taken with 20 - 30 seconds remaining on the shot clock that were made."""
    raise NotImplementedError("PBP data not yet available: 3P% (20-30s)")


def calc_3p_10_20s(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Percentage of the player's 3-point field goal attempts taken with 10 - 20 seconds remaining on the shot clock that were made."""
    raise NotImplementedError("PBP data not yet available: 3P% (10-20s)")


def calc_3p_in_hc(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """An estimate of 3-point field goal percentage (makes / attempts) on shots in the context of half court offense (as opposed to transition or putback)."""
    raise NotImplementedError("PBP data not yet available: 3P% in HC")


def calc_3p_in_tr(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """An estimate of 3-point field goal percentage (makes / attempts) on shots in the context of transition offense (as opposed to half court or putback)."""
    raise NotImplementedError("PBP data not yet available: 3P% in TR")


def calc_3pa_0_10s(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The total number of 3-point field goal attempts taken with 0 - 10 seconds remaining on the shot clock."""
    raise NotImplementedError("PBP data not yet available: 3PA (0-10s)")


def calc_3pa_10_20s(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The total number of 3-point field goal attempts taken with 10 - 20 seconds remaining on the shot clock."""
    raise NotImplementedError("PBP data not yet available: 3PA (10-20s)")


def calc_3pa_20_30s(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The total number of 3-point field goal attempts taken with 20 - 30 seconds remaining on the shot clock."""
    raise NotImplementedError("PBP data not yet available: 3PA (20-30s)")


def calc_3pa_in_hc(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """An estimate of the total number of 3-point field goal attempts taken in the context of half court offense (as opposed to transition or putback)."""
    raise NotImplementedError("PBP data not yet available: 3PA in HC")


def calc_3pa_in_tr(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """An estimate of the total number of 3-point field goal attempts taken in the context of transition offense (as opposed to half court or putback)."""
    raise NotImplementedError("PBP data not yet available: 3PA in TR")


def calc_3pm_in_hc(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """An estimate of the total number of 3-point field goals made in the context of half court offense (as opposed to transition or putback)."""
    raise NotImplementedError("PBP data not yet available: 3PM in HC")


def calc_3pm_in_tr(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """An estimate of the total number of 3-point field goals made in the context of transition offense (as opposed to half court or putback)."""
    raise NotImplementedError("PBP data not yet available: 3PM in TR")


def calc_3pm_0_10s(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The total number of 3-point field goals made with 0 - 10 seconds remaining on the shot clock."""
    raise NotImplementedError("PBP data not yet available: 3PM (0-10s)")


def calc_3pm_10_20s(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The total number of 3-point field goals made with 10 - 20 seconds remaining on the shot clock."""
    raise NotImplementedError("PBP data not yet available: 3PM (10-20s)")


def calc_3pm_20_30s(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The total number of 3-point field goals made with 20 - 30 seconds remaining on the shot clock."""
    raise NotImplementedError("PBP data not yet available: 3PM (20-30s)")


def calc_tov_5_secs(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The total number of turnovers tagged by the scorer as a 5 second violation by the team."""
    raise NotImplementedError("PBP data not yet available: TOV 5 SECS")


def calc_strk_8(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The total number of scoring streaks of 8+ consecutive points scored by the team."""
    raise NotImplementedError("PBP data not yet available: STRK 8+")


def calc_agst_8(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The total number of scoring streaks allowed of 8+ consecutive points allowed by the team."""
    raise NotImplementedError("PBP data not yet available: AGST 8+")


def calc_atb3_astd(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The percentage of shots made on above the break 3s that were assisted."""
    raise NotImplementedError("PBP data not yet available: ATB3 ASTD%")


def calc_atb3_drb_chnc(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The total number of defensive rebounds chances (defensive rebounds grabbed plus opponent offensive rebounds) on opponent's missed above the break 3s."""
    raise NotImplementedError("PBP data not yet available: ATB3 DRB CHNC")


def calc_atb3_drb(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Percentage of the opponent's missed above the break 3s that were defensive rebounded by the team."""
    raise NotImplementedError("PBP data not yet available: ATB3 DRB%")


def calc_atb3_drb(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The total number of defensive rebounds grabbed on opponent's missed above the break 3s."""
    raise NotImplementedError("PBP data not yet available: ATB3 DRB")


def calc_atb3_fga_0_10s(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The total number of field goal attempts on above the break 3s taken with 0 - 10 seconds remaining on the shot clock."""
    raise NotImplementedError("PBP data not yet available: ATB3 FGA (0-10s)")


def calc_atb3_fga_10_20s(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The total number of field goal attempts on above the break 3s taken with 10 - 20 seconds remaining on the shot clock."""
    raise NotImplementedError("PBP data not yet available: ATB3 FGA (10-20s)")


def calc_atb3_fga_20_30s(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The total number of field goal attempts on above the break 3s taken with 20 - 30 seconds remaining on the shot clock."""
    raise NotImplementedError("PBP data not yet available: ATB3 FGA (20-30s)")


def calc_atb3_fga_100(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Field goal attempts on above the break 3s per 100 possessions played."""
    raise NotImplementedError("PBP data not yet available: ATB3 FGA/100")


def calc_atb3_fga_40(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Field goal attempts on above the break 3s per 40 minutes played."""
    raise NotImplementedError("PBP data not yet available: ATB3 FGA/40")


def calc_atb3_fga_g(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Field goal attempts on above the break 3s per game."""
    raise NotImplementedError("PBP data not yet available: ATB3 FGA/G")


def calc_atb3_fga_0_10s_a(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Percentage of all shots taken that were above the break 3s with 0 - 10 seconds remaining on the shot clock."""
    raise NotImplementedError("PBP data not yet available: ATB3 FGA% (0-10s) A")


def calc_atb3_fga_0_10s_z(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Percentage of all above the break 3s that were taken with 0 - 10 seconds remaining on the shot clock."""
    raise NotImplementedError("PBP data not yet available: ATB3 FGA% (0-10s) Z")


def calc_atb3_fga_0_10s_c(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Percentage of all shots taken with 0 - 10 seconds remaining on the shot clock that were above the break 3s."""
    raise NotImplementedError("PBP data not yet available: ATB3 FGA% (0-10s) C")


def calc_atb3_fga_10_20s_a(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Percentage of all shots taken that were above the break 3s with 10 - 20 seconds remaining on the shot clock."""
    raise NotImplementedError("PBP data not yet available: ATB3 FGA% (10-20s) A")


def calc_atb3_fga_10_20s_z(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Percentage of all above the break 3s that were taken with 10 - 20 seconds remaining on the shot clock."""
    raise NotImplementedError("PBP data not yet available: ATB3 FGA% (10-20s) Z")


def calc_atb3_fga_20_30s_a(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Percentage of all shots taken that were above the break 3s with 20 - 30 seconds remaining on the shot clock."""
    raise NotImplementedError("PBP data not yet available: ATB3 FGA% (20-30s) A")


def calc_atb3_fga_20_30s_z(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Percentage of all above the break 3s that were taken with 20 - 30 seconds remaining on the shot clock."""
    raise NotImplementedError("PBP data not yet available: ATB3 FGA% (20-30s) Z")


def calc_atb3_fga_20_30s_c(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Percentage of all shots taken with 20 - 30 seconds remaining on the shot clock that were above the break 3s."""
    raise NotImplementedError("PBP data not yet available: ATB3 FGA% (20-30s) C")


def calc_atb3_fgm(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The total number of field goals made on above the break 3s."""
    raise NotImplementedError("PBP data not yet available: ATB3 FGM")


def calc_atb3_fgm_0_10s(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The total number of field goals made on above the break 3s taken with 0 - 10 seconds remaining on the shot clock."""
    raise NotImplementedError("PBP data not yet available: ATB3 FGM (0-10s)")


def calc_atb3_fgm_10_20s(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The total number of field goals made on above the break 3s taken with 10 - 20 seconds remaining on the shot clock."""
    raise NotImplementedError("PBP data not yet available: ATB3 FGM (10-20s)")


def calc_atb3_fgm_20_30s(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The total number of field goals made on above the break 3s taken with 20 - 30 seconds remaining on the shot clock."""
    raise NotImplementedError("PBP data not yet available: ATB3 FGM (20-30s)")


def calc_atb3_orb_chnc(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The total number of offensive rebounds chances (offensive rebounds grabbed plus opponent defensive rebounds) on the team's missed above the break 3s."""
    raise NotImplementedError("PBP data not yet available: ATB3 ORB CHNC")


def calc_atb3_orb(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Percentage of the team's missed above the break 3s that were offensive rebounded by the team."""
    raise NotImplementedError("PBP data not yet available: ATB3 ORB%")


def calc_atb3_orb(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The total number of offensive rebounds grabbed on the team's missed above the break 3s."""
    raise NotImplementedError("PBP data not yet available: ATB3 ORB")


def calc_atb3_reb_chnc(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The total number of rebounds chances (rebounds grabbed plus opponent rebounds) on the team's and opponent's missed above the break 3s."""
    raise NotImplementedError("PBP data not yet available: ATB3 REB CHNC")


def calc_atb3_reb(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Percentage of the team's and opponent's missed above the break 3s that were rebounded by the team."""
    raise NotImplementedError("PBP data not yet available: ATB3 REB%")


def calc_atb3_reb(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The total number of rebounds grabbed on the team's and opponent's missed above the break 3s."""
    raise NotImplementedError("PBP data not yet available: ATB3 REB")


def calc_atb3_fga_10_20s_c(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Percentage of all shots taken with 10 - 20 seconds remaining on the shot clock that were above the break 3s."""
    raise NotImplementedError("PBP data not yet available: ATB3 FGA% (10-20s) C")


def calc_oop_fga(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The percentage of shots taken that were alley-oop dunk attempts."""
    raise NotImplementedError("PBP data not yet available: OOP FGA%")


def calc_oop_fg(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Field goal percentage on alley-oops."""
    raise NotImplementedError("PBP data not yet available: OOP FG%")


def calc_oop_fga_100(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The number of alley-oop field goal attempts by the player, per 100 possessions played."""
    raise NotImplementedError("PBP data not yet available: OOP FGA/100")


def calc_oop_fga_40(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The number of alley-oop field goal attempts by the player, per 40 minutes played."""
    raise NotImplementedError("PBP data not yet available: OOP FGA/40")


def calc_oop_fga_g(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The number of alley-oop field goal attempts by the player, per game."""
    raise NotImplementedError("PBP data not yet available: OOP FGA/G")


def calc_oop_fga(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The total number of alley-oop field goal attempts by the player."""
    raise NotImplementedError("PBP data not yet available: OOP FGA")


def calc_oop_fgm(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The total number of alley-oop field goals made by the player."""
    raise NotImplementedError("PBP data not yet available: OOP FGM")


def calc_and1(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The percentage of shooting fouls drawn where the shot was made."""
    raise NotImplementedError("PBP data not yet available: And1%")


def calc_3and1(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The percentage of 3-point shooting fouls drawn where the shot was made."""
    raise NotImplementedError("PBP data not yet available: 3And1%")


def calc_and_1s(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The total number of times a shot was made while being fouled by a defender from the opposing team (total number of And 1s)."""
    raise NotImplementedError("PBP data not yet available: And 1s")


def calc_and1_100(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The number of and 1s (made shot + foul drawn) per 100 possessions."""
    raise NotImplementedError("PBP data not yet available: And1/100")


def calc_and1_40(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The number of and 1s (made shot + foul drawn) per 40 minutes."""
    raise NotImplementedError("PBP data not yet available: And1/40")


def calc_and1_g(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The number of and 1s (made shot + foul drawn) per game."""
    raise NotImplementedError("PBP data not yet available: And1/G")


def calc_2p_and_1s(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The total number of times a 2-point shot was made while being fouled by a defender from the opposing team (total number of And 1s made on 2-point shooting fouls)."""
    raise NotImplementedError("PBP data not yet available: 2P And 1s")


def calc_3p_and_1s(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The total number of times a 3-point shot was made while being fouled by a defender from the opposing team (total number of And 1s made on 3-point shooting fouls)."""
    raise NotImplementedError("PBP data not yet available: 3P And 1s")


def calc_a2pm(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The total number of assisted 2-point field goals made by the player."""
    raise NotImplementedError("PBP data not yet available: a2PM")


def calc_a2pm_100(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The number of assisted 2-point field goals made by the player, per 100 possessions played."""
    raise NotImplementedError("PBP data not yet available: a2PM/100")


def calc_a2pm_40(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The number of assisted 2-point field goals made by the player, per 40 minutes played."""
    raise NotImplementedError("PBP data not yet available: a2PM/40")


def calc_a2pm_g(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The number of assisted 2-point field goals made by the player, per game."""
    raise NotImplementedError("PBP data not yet available: a2PM/G")


def calc_a3pm(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The total number of assisted 3-point field goals made by the player."""
    raise NotImplementedError("PBP data not yet available: a3PM")


def calc_a3pm_100(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The number of assisted 3-point field goals made by the player, per 100 possessions played."""
    raise NotImplementedError("PBP data not yet available: a3PM/100")


def calc_a3pm_40(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The number of assisted 3-point field goals made by the player, per 40 minutes played."""
    raise NotImplementedError("PBP data not yet available: a3PM/40")


def calc_a3pm_g(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The number of assisted 3-point field goals made by the player, per game."""
    raise NotImplementedError("PBP data not yet available: a3PM/G")


def calc_atb3_afgm(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The total number of assisted above the break 3s made by the player."""
    raise NotImplementedError("PBP data not yet available: ATB3 aFGM")


def calc_atb3_afgm_100(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The number of assisted above the break 3s made by the player, per 100 possessions played."""
    raise NotImplementedError("PBP data not yet available: ATB3 aFGM/100")


def calc_atb3_afgm_40(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The number of assisted above the break 3s made by the player, per 40 minutes played."""
    raise NotImplementedError("PBP data not yet available: ATB3 aFGM/40")


def calc_atb3_afgm_g(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The number of assisted above the break 3s made by the player, per game."""
    raise NotImplementedError("PBP data not yet available: ATB3 aFGM/G")


def calc_c3_afgm(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The total number of assisted corner 3-pointers made by the player."""
    raise NotImplementedError("PBP data not yet available: C3 aFGM")


def calc_c3_afgm_100(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The number of assisted corner 3-pointers made by the player, per 100 possessions played."""
    raise NotImplementedError("PBP data not yet available: C3 aFGM/100")


def calc_c3_afgm_40(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The number of assisted corner 3-pointers made by the player, per 40 minutes played."""
    raise NotImplementedError("PBP data not yet available: C3 aFGM/40")


def calc_c3_afgm_g(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The number of assisted corner 3-pointers made by the player, per game."""
    raise NotImplementedError("PBP data not yet available: C3 aFGM/G")


def calc_dunk_afgm(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The total number of assisted dunks made by the player."""
    raise NotImplementedError("PBP data not yet available: DUNK aFGM")


def calc_dunk_afgm_100(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The number of assisted dunks made by the player, per 100 possessions played."""
    raise NotImplementedError("PBP data not yet available: DUNK aFGM/100")


def calc_dunk_afgm_40(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The number of assisted dunks made by the player, per 40 minutes played."""
    raise NotImplementedError("PBP data not yet available: DUNK aFGM/40")


def calc_dunk_afgm_g(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The number of assisted dunks made by the player, per game."""
    raise NotImplementedError("PBP data not yet available: DUNK aFGM/G")


def calc_afgm(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The total number of assisted field goals made by the player."""
    raise NotImplementedError("PBP data not yet available: aFGM")


def calc_afgm_100(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The number of assisted field goals made by the player, per 100 possessions played."""
    raise NotImplementedError("PBP data not yet available: aFGM/100")


def calc_afgm_40(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The number of assisted field goals made by the player, per 40 minutes played."""
    raise NotImplementedError("PBP data not yet available: aFGM/40")


def calc_afgm_g(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The number of assisted field goals made by the player, per game."""
    raise NotImplementedError("PBP data not yet available: aFGM/G")


def calc_mid2_afgm(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The total number of assisted midrange 2s made by the player."""
    raise NotImplementedError("PBP data not yet available: MID2 aFGM")


def calc_mid2_afgm_100(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The number of assisted midrange 2s made by the player, per 100 possessions played."""
    raise NotImplementedError("PBP data not yet available: MID2 aFGM/100")


def calc_mid2_afgm_40(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The number of assisted midrange 2s made by the player, per 40 minutes played."""
    raise NotImplementedError("PBP data not yet available: MID2 aFGM/40")


def calc_mid2_afgm_g(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The number of assisted midrange 2s made by the player, per game."""
    raise NotImplementedError("PBP data not yet available: MID2 aFGM/G")


def calc_paint2_afgm(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The total number of assisted shots made in the paint (not at the rim) by the player."""
    raise NotImplementedError("PBP data not yet available: PAINT2 aFGM")


def calc_paint2_afgm_100(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The total number of assisted shots made in the paint (not at the rim) by the player, per 100 possessions played."""
    raise NotImplementedError("PBP data not yet available: PAINT2 aFGM/100")


def calc_paint2_afgm_40(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The total number of assisted shots made in the paint (not at the rim) by the player, per 40 minutes played."""
    raise NotImplementedError("PBP data not yet available: PAINT2 aFGM/40")


def calc_paint2_afgm_g(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The total number of assisted shots made in the paint (not at the rim) by the player, per game."""
    raise NotImplementedError("PBP data not yet available: PAINT2 aFGM/G")


def calc_atr2_afgm(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The total number of assisted shots at the rim made by the player."""
    raise NotImplementedError("PBP data not yet available: ATR2 aFGM")


def calc_atr2_afgm_100(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The number of assisted shots at the rim made by the player, per 100 possessions played."""
    raise NotImplementedError("PBP data not yet available: ATR2 aFGM/100")


def calc_atr2_afgm_40(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The number of assisted shots at the rim made by the player, per 40 minutes played."""
    raise NotImplementedError("PBP data not yet available: ATR2 aFGM/40")


def calc_atr2_afgm_g(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The number of assisted shots at the rim made by the player, per game."""
    raise NotImplementedError("PBP data not yet available: ATR2 aFGM/G")


def calc_rim_3s_afgm(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The total number of assisted shots made at the rim and on three pointers made by the player."""
    raise NotImplementedError("PBP data not yet available: Rim + 3s aFGM")


def calc_rim_3s_afgm_100(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The number of assisted shots made at the rim (within 4.5 feet of the basket) and on three pointers made by the player, per 100 possessions played."""
    raise NotImplementedError("PBP data not yet available: Rim + 3s aFGM/100")


def calc_rim_3s_afgm_40(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The number of assisted shots made at the rim (within 4.5 feet of the basket) and on three pointers made by the player, per 40 minutes played."""
    raise NotImplementedError("PBP data not yet available: Rim + 3s aFGM/40")


def calc_rim_3s_afgm_g(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The number of assisted shots made at the rim (within 4.5 feet of the basket) and on three pointers made by the player, per game."""
    raise NotImplementedError("PBP data not yet available: Rim + 3s aFGM/G")


def calc_rim_3s_astd(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The percentage of shots made either at the rim (within 4.5 feet of the basket) or on a three pointer that were assisted."""
    raise NotImplementedError("PBP data not yet available: Rim + 3s ASTD%")


def calc_rim_3s_efg(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Effective field goal percentage on shots at the rim (within 4.5 feet of the basket) as well as three pointers."""
    raise NotImplementedError("PBP data not yet available: Rim + 3s eFG%")


def calc_rim_3s_fg(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Field goal percentage on shots at the rim (within 4.5 feet of the basket) as well as three pointers."""
    raise NotImplementedError("PBP data not yet available: Rim + 3s FG%")


def calc_rim_3s_fga(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Field goal attempts at the rim (within 4.5 feet of the basket) and on three pointers."""
    raise NotImplementedError("PBP data not yet available: Rim + 3s FGA")


def calc_rim_3s_fga_100(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Field goal attempts either at the rim (within 4.5 feet of the basket) or on three pointers, per 100 possessions played."""
    raise NotImplementedError("PBP data not yet available: Rim + 3s FGA/100")


def calc_rim_3s_fga_40(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Field goal attempts either at the rim (within 4.5 feet of the basket) or on three pointers, per 40 minutes played."""
    raise NotImplementedError("PBP data not yet available: Rim + 3s FGA/40")


def calc_rim_3s_fga_g(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Field goal attempts either at the rim (within 4.5 feet of the basket) or on three pointers, per game."""
    raise NotImplementedError("PBP data not yet available: Rim + 3s FGA/G")


def calc_rim_3s_fga(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Percentage of shots taken either at the rim (within 4.5 feet of the basket) or as a three pointer."""
    raise NotImplementedError("PBP data not yet available: Rim + 3s FGA%")


def calc_rim_3s_fgm(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Field goals made either at the rim (within 4.5 feet of the basket) or on three pointers."""
    raise NotImplementedError("PBP data not yet available: Rim + 3s FGM")


def calc_rim_3s_ufgm(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The total number of unassisted shots made at the rim (within 4.5 feet of the basket) and on three pointers made by the player."""
    raise NotImplementedError("PBP data not yet available: Rim + 3s uFGM")


def calc_atr2_astd(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The percentage of shots made at the rim that were assisted, within 4.5 feet of the basket."""
    raise NotImplementedError("PBP data not yet available: ATR2 ASTD%")


def calc_atr2_drb_chnc(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The total number of defensive rebounds chances (defensive rebounds grabbed plus opponent offensive rebounds) on opponent's missed shots at the rim."""
    raise NotImplementedError("PBP data not yet available: ATR2 DRB CHNC")


def calc_atr2_drb(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Percentage of the opponent's missed shots at the rim that were defensive rebounded by the team."""
    raise NotImplementedError("PBP data not yet available: ATR2 DRB%")


def calc_atr2_drb(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The total number of defensive rebounds grabbed on opponent's missed shots at the rim."""
    raise NotImplementedError("PBP data not yet available: ATR2 DRB")


def calc_atr2_fg(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Field goal percentage at the rim, within 4.5 feet of the basket."""
    raise NotImplementedError("PBP data not yet available: ATR2 FG%")


def calc_atr2_fg_0_10s(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Field goal percentage on shots taken at the rim with 0 - 10 seconds remaining on the shot clock."""
    raise NotImplementedError("PBP data not yet available: ATR2 FG% (0-10s)")


def calc_atr2_fg_10_20s(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Field goal percentage on shots taken at the rim with 10 - 20 seconds remaining on the shot clock."""
    raise NotImplementedError("PBP data not yet available: ATR2 FG% (10-20s)")


def calc_atr2_fg_20_30s(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Field goal percentage on shots taken at the rim with 20 - 30 seconds remaining on the shot clock."""
    raise NotImplementedError("PBP data not yet available: ATR2 FG% (20-30s)")


def calc_atr2_fga(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Field goal attempts at the rim, within 4.5 feet of the basket."""
    raise NotImplementedError("PBP data not yet available: ATR2 FGA")


def calc_atr2_fga_0_10s(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The total number of field goal attempts at the rim taken with 0 - 10 seconds remaining on the shot clock."""
    raise NotImplementedError("PBP data not yet available: ATR2 FGA (0-10s)")


def calc_atr2_fga_10_20s(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The total number of field goal attempts at the rim taken with 10 - 20 seconds remaining on the shot clock."""
    raise NotImplementedError("PBP data not yet available: ATR2 FGA (10-20s)")


def calc_atr2_fga_20_30s(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The total number of field goal attempts at the rim taken with 20 - 30 seconds remaining on the shot clock."""
    raise NotImplementedError("PBP data not yet available: ATR2 FGA (20-30s)")


def calc_atr2_fga_100(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Field goal attempts at the rim (within 4.5 feet of the basket) per 100 possessions played."""
    raise NotImplementedError("PBP data not yet available: ATR2 FGA/100")


def calc_atr2_fga_40(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Field goal attempts at the rim (within 4.5 feet of the basket) per 40 minutes played."""
    raise NotImplementedError("PBP data not yet available: ATR2 FGA/40")


def calc_atr2_fga_g(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Field goal attempts at the rim (within 4.5 feet of the basket) per game."""
    raise NotImplementedError("PBP data not yet available: ATR2 FGA/G")


def calc_atr2_fga(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Percentage of shots taken at the rim, within 4.5 feet of the basket."""
    raise NotImplementedError("PBP data not yet available: ATR2 FGA%")


def calc_atr2_fga_0_10s_a(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Percentage of all shots taken that were at the rim with 0 - 10 seconds remaining on the shot clock."""
    raise NotImplementedError("PBP data not yet available: ATR2 FGA% (0-10s) A")


def calc_atr2_fga_0_10s_z(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Percentage of all shots at the rim that were taken with 0 - 10 seconds remaining on the shot clock."""
    raise NotImplementedError("PBP data not yet available: ATR2 FGA% (0-10s) Z")


def calc_atr2_fga_0_10s_c(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Percentage of all shots taken with 0 - 10 seconds remaining on the shot clock that were at the rim."""
    raise NotImplementedError("PBP data not yet available: ATR2 FGA% (0-10s) C")


def calc_atr2_fga_10_20s_a(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Percentage of all shots taken that were at the rim with 10 - 20 seconds remaining on the shot clock."""
    raise NotImplementedError("PBP data not yet available: ATR2 FGA% (10-20s) A")


def calc_atr2_fga_10_20s_z(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Percentage of all shots at the rim that were taken with 10 - 20 seconds remaining on the shot clock."""
    raise NotImplementedError("PBP data not yet available: ATR2 FGA% (10-20s) Z")


def calc_atr2_fga_10_20s_c(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Percentage of all shots taken with 10 - 20 seconds remaining on the shot clock that were at the rim."""
    raise NotImplementedError("PBP data not yet available: ATR2 FGA% (10-20s) C")


def calc_atr2_fga_20_30s_a(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Percentage of all shots taken that were at the rim with 20 - 30 seconds remaining on the shot clock."""
    raise NotImplementedError("PBP data not yet available: ATR2 FGA% (20-30s) A")


def calc_atr2_fga_20_30s_z(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Percentage of all shots at the rim that were taken with 20 - 30 seconds remaining on the shot clock."""
    raise NotImplementedError("PBP data not yet available: ATR2 FGA% (20-30s) Z")


def calc_atr2_fga_20_30s_c(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Percentage of all shots taken with 20 - 30 seconds remaining on the shot clock that were at the rim."""
    raise NotImplementedError("PBP data not yet available: ATR2 FGA% (20-30s) C")


def calc_atr2_fgm(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Field goals made at the rim (within 4.5 feet of the basket)."""
    raise NotImplementedError("PBP data not yet available: ATR2 FGM")


def calc_atr2_fgm_0_10s(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The total number of field goals made at the rim taken with 0 - 10 seconds remaining on the shot clock."""
    raise NotImplementedError("PBP data not yet available: ATR2 FGM (0-10s)")


def calc_atr2_fgm_10_20s(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The total number of field goals made at the rim taken with 10 - 20 seconds remaining on the shot clock."""
    raise NotImplementedError("PBP data not yet available: ATR2 FGM (10-20s)")


def calc_atr2_fgm_20_30s(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The total number of field goals made at the rim taken with 20 - 30 seconds remaining on the shot clock."""
    raise NotImplementedError("PBP data not yet available: ATR2 FGM (20-30s)")


def calc_atr2_orb_chnc(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The total number of offensive rebounds chances (offensive rebounds grabbed plus opponent defensive rebounds) on the team's missed shots at the rim."""
    raise NotImplementedError("PBP data not yet available: ATR2 ORB CHNC")


def calc_atr2_orb(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Percentage of the team's missed shots at the rim that were offensive rebounded by the team."""
    raise NotImplementedError("PBP data not yet available: ATR2 ORB%")


def calc_atr2_orb(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The total number of offensive rebounds grabbed on the team's missed shots at the rim."""
    raise NotImplementedError("PBP data not yet available: ATR2 ORB")


def calc_atr2_reb_chnc(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The total number of rebounds chances (rebounds grabbed plus opponent rebounds) on the team's and opponent's missed shots at the rim."""
    raise NotImplementedError("PBP data not yet available: ATR2 REB CHNC")


def calc_atr2_reb(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Percentage of the team's and opponent's missed shots at the rim that were rebounded by the team."""
    raise NotImplementedError("PBP data not yet available: ATR2 REB%")


def calc_atr2_reb(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The total number of rebounds grabbed on the team's and opponent's missed shots at the rim."""
    raise NotImplementedError("PBP data not yet available: ATR2 REB")


def calc_atb3_fg(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Field goal percentage on above the break 3s."""
    raise NotImplementedError("PBP data not yet available: ATB3 FG%")


def calc_atb3_fga(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The total number of field goal attempts on above the break 3s."""
    raise NotImplementedError("PBP data not yet available: ATB3 FGA")


def calc_atb3_fga(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Percentage of shots taken as above the break 3s."""
    raise NotImplementedError("PBP data not yet available: ATB3 FGA%")


def calc_atb3_fg_0_10s(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Field goal percentage on above the break 3s taken with 0 - 10 seconds remaining on the shot clock."""
    raise NotImplementedError("PBP data not yet available: ATB3 FG% (0-10s)")


def calc_atb3_fg_10_20s(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Field goal percentage on above the break 3s taken with 10 - 20 seconds remaining on the shot clock."""
    raise NotImplementedError("PBP data not yet available: ATB3 FG% (10-20s)")


def calc_atb3_fg_20_30s(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Field goal percentage on above the break 3s taken with 20 - 30 seconds remaining on the shot clock."""
    raise NotImplementedError("PBP data not yet available: ATB3 FG% (20-30s)")


def calc_atb3_ufgm(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """No description available"""
    raise NotImplementedError("PBP data not yet available: ATB3 uFGM")


def calc_s_chnc_d(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The average number of seconds per defensive chance. This number is identical to seconds / defensive possession, except with seconds after an offensive rebound excluded, and with putback chances excluded. This number effectively measures the average number of seconds from the start of a possession until a team's first shot, shooting foul or turnover."""
    raise NotImplementedError("PBP data not yet available: S/CHNC D")


def calc_s_poss_d(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The average number of seconds per defensive possession. This number measures the average length of entire defensive possessions, so added seconds from offensive rebounds count, as offensive rebounds extend a single possession."""
    raise NotImplementedError("PBP data not yet available: S/POSS D")


def calc_s_put_d(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The average number of seconds per defensive putback. This number measures the average length of chances (average seconds until the next shot, shooting foul or turnover) that start following an offensive rebound."""
    raise NotImplementedError("PBP data not yet available: S/PUT D")


def calc_s_chnc_o(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The average number of seconds per offensive chance. This number is identical to seconds / offensive possession, except with seconds after an offensive rebound excluded, and with putback chances excluded. This number effectively measures the average number of seconds from the start of a possession until a team's first shot, shooting foul or turnover."""
    raise NotImplementedError("PBP data not yet available: S/CHNC O")


def calc_s_poss_o(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The average number of seconds per offensive possession. This number measures the average length of entire offensive possessions, so added seconds from offensive rebounds count, as offensive rebounds extend a single possession."""
    raise NotImplementedError("PBP data not yet available: S/POSS O")


def calc_s_put_o(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The average number of seconds per offensive putback. This number measures the average length of chances (average seconds until the next shot, shooting foul or turnover) that start following an offensive rebound."""
    raise NotImplementedError("PBP data not yet available: S/PUT O")


def calc_2pa_avg_dist(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Average shot distance on 2-point field goal attempts. Shot distances are based on scorekeeper-tagged locations and may contain minor shot-location inaccuracies."""
    raise NotImplementedError("PBP data not yet available: 2PA Avg Dist")


def calc_3pa_avg_dist(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Average shot distance on 3-point field goal attempts. Shot distances are based on scorekeeper-tagged locations and may contain minor shot-location inaccuracies. Heaves (above 35 feet) are removed."""
    raise NotImplementedError("PBP data not yet available: 3PA Avg Dist")


def calc_atb3_avg_dist(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Average shot distance of above the break 3s attempts. Shot distances are based on scorekeeper-tagged locations and may contain minor shot-location inaccuracies. Heaves (above 35 feet) are removed."""
    raise NotImplementedError("PBP data not yet available: ATB3 Avg Dist")


def calc_fga_avg_dist(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Average shot distance on all field goal attempts. Shot distances are based on scorekeeper-tagged locations and may contain minor shot-location inaccuracies. Heaves (above 35 feet) are removed."""
    raise NotImplementedError("PBP data not yet available: FGA Avg Dist")


def calc_bc_poss_chlg(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Total number of head coach challenges on backcourt violations or whether team control (possession) was established before a foul or violation (women's basketball only)."""
    raise NotImplementedError("PBP data not yet available: BC/Poss CHLG")


def calc_tov_pass(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The total number of turnovers tagged by the scorer as a bad pass turnover by the team."""
    raise NotImplementedError("PBP data not yet available: TOV PASS")


def calc_bc_poss_chlg(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Percentage of coach challenges on backcourt violations or whether team control was established before a foul or violation that were successful (women's basketball only)."""
    raise NotImplementedError("PBP data not yet available: BC/Poss CHLG%")


def calc_bh_fg(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Field goal percentage on shots taken behind the hoop."""
    raise NotImplementedError("PBP data not yet available: BH FG%")


def calc_bh_fga(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Field goal attempts taken behind the hoop."""
    raise NotImplementedError("PBP data not yet available: BH FGA")


def calc_bh_fga_100(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Field goal attempts taken behind the hoop per 100 possessions played."""
    raise NotImplementedError("PBP data not yet available: BH FGA/100")


def calc_bh_fga_40(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Field goal attempts taken behind the hoop per 40 minutes played."""
    raise NotImplementedError("PBP data not yet available: BH FGA/40")


def calc_bh_fga_g(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Field goal attempts taken behind the hoop per game."""
    raise NotImplementedError("PBP data not yet available: BH FGA/G")


def calc_bh_fga(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Percentage of shots taken behind the hoop."""
    raise NotImplementedError("PBP data not yet available: BH FGA%")


def calc_bh_fgm(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Field goals made on shots taken behind the hoop."""
    raise NotImplementedError("PBP data not yet available: BH FGM")


def calc_blk2(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The total number of blocks by the player on opposing 2P shot attempts."""
    raise NotImplementedError("PBP data not yet available: BLK2")


def calc_blk2_100(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The number of blocks by the player on opposing 2P shot attempts, per 100 possessions played."""
    raise NotImplementedError("PBP data not yet available: BLK2/100")


def calc_blk2_40(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The number of blocks by the player on opposing 2P shot attempts, per 40 minutes played."""
    raise NotImplementedError("PBP data not yet available: BLK2/40")


def calc_blk2_g(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The number of blocks by the player on opposing 2P shot attempts, per game."""
    raise NotImplementedError("PBP data not yet available: BLK2/G")


def calc_blk3(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The total number of blocks by the player on opposing 3P shot attempts."""
    raise NotImplementedError("PBP data not yet available: BLK3")


def calc_blk3_100(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The number of blocks by the player on opposing 3P shot attempts, per 100 possessions played."""
    raise NotImplementedError("PBP data not yet available: BLK3/100")


def calc_blk3_40(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The number of blocks by the player on opposing 3P shot attempts, per 40 minutes played."""
    raise NotImplementedError("PBP data not yet available: BLK3/40")


def calc_blk3_g(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The number of blocks by the player on opposing 3P shot attempts, per game."""
    raise NotImplementedError("PBP data not yet available: BLK3/G")


def calc_c3_ufgm(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """No description available"""
    raise NotImplementedError("PBP data not yet available: C3 uFGM")


def calc_chlg(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Percentage of coach challenges that were successful."""
    raise NotImplementedError("PBP data not yet available: CHLG%")


def calc_challenge(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Total number of head coach challenges used."""
    raise NotImplementedError("PBP data not yet available: Challenge")


def calc_c3_astd(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The percentage of shots made on corner 3s that were assisted."""
    raise NotImplementedError("PBP data not yet available: C3 ASTD%")


def calc_c3_drb_chnc(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The total number of defensive rebounds chances (defensive rebounds grabbed plus opponent offensive rebounds) on opponent's missed corner 3s."""
    raise NotImplementedError("PBP data not yet available: C3 DRB CHNC")


def calc_c3_drb(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Percentage of the opponent's missed corner 3s that were defensive rebounded by the team."""
    raise NotImplementedError("PBP data not yet available: C3 DRB%")


def calc_c3_drb(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The total number of defensive rebounds grabbed on opponent's missed corner 3s."""
    raise NotImplementedError("PBP data not yet available: C3 DRB")


def calc_c3_fg(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Field goal percentage on corner 3-pointers."""
    raise NotImplementedError("PBP data not yet available: C3 FG%")


def calc_c3_fg_0_10s(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Field goal percentage on corner 3s taken with 0 - 10 seconds remaining on the shot clock."""
    raise NotImplementedError("PBP data not yet available: C3 FG% (0-10s)")


def calc_c3_fg_10_20s(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Field goal percentage on corner 3s taken with 10 - 20 seconds remaining on the shot clock."""
    raise NotImplementedError("PBP data not yet available: C3 FG% (10-20s)")


def calc_c3_fg_20_30s(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Field goal percentage on corner 3s taken with 20 - 30 seconds remaining on the shot clock."""
    raise NotImplementedError("PBP data not yet available: C3 FG% (20-30s)")


def calc_c3_fga(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Field goal attempts on corner 3-pointers."""
    raise NotImplementedError("PBP data not yet available: C3 FGA")


def calc_c3_fga_0_10s(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The total number of field goal attempts on corner 3s taken with 0 - 10 seconds remaining on the shot clock."""
    raise NotImplementedError("PBP data not yet available: C3 FGA (0-10s)")


def calc_c3_fga_10_20s(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The total number of field goal attempts on corner 3s taken with 10 - 20 seconds remaining on the shot clock."""
    raise NotImplementedError("PBP data not yet available: C3 FGA (10-20s)")


def calc_c3_fga_20_30s(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The total number of field goal attempts on corner 3s taken with 20 - 30 seconds remaining on the shot clock."""
    raise NotImplementedError("PBP data not yet available: C3 FGA (20-30s)")


def calc_c3_fga_100(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Field goal attempts on corner 3s per 100 possessions played."""
    raise NotImplementedError("PBP data not yet available: C3 FGA/100")


def calc_c3_fga_40(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Field goal attempts on corner 3s per 40 minutes played."""
    raise NotImplementedError("PBP data not yet available: C3 FGA/40")


def calc_c3_fga_g(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Field goal attempts on corner 3s per game."""
    raise NotImplementedError("PBP data not yet available: C3 FGA/G")


def calc_c3_fga(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Percentage of shots taken as corner 3-pointers."""
    raise NotImplementedError("PBP data not yet available: C3 FGA%")


def calc_c3_fga_0_10s_a(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Percentage of all shots taken that were corner 3s with 0 - 10 seconds remaining on the shot clock."""
    raise NotImplementedError("PBP data not yet available: C3 FGA% (0-10s) A")


def calc_c3_fga_0_10s_c(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Percentage of all shots taken with 0 - 10 seconds remaining on the shot clock that were corner 3s."""
    raise NotImplementedError("PBP data not yet available: C3 FGA% (0-10s) C")


def calc_c3_fga_0_10s_z(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Percentage of all corner 3s that were taken with 0 - 10 seconds remaining on the shot clock."""
    raise NotImplementedError("PBP data not yet available: C3 FGA% (0-10s) Z")


def calc_c3_fga_10_20s_a(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Percentage of all shots taken that were corner 3s with 10 - 20 seconds remaining on the shot clock."""
    raise NotImplementedError("PBP data not yet available: C3 FGA% (10-20s) A")


def calc_c3_fga_10_20s_c(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Percentage of all shots taken with 10 - 20 seconds remaining on the shot clock that were corner 3s."""
    raise NotImplementedError("PBP data not yet available: C3 FGA% (10-20s) C")


def calc_c3_fga_10_20s_z(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Percentage of all corner 3s that were taken with 10 - 20 seconds remaining on the shot clock."""
    raise NotImplementedError("PBP data not yet available: C3 FGA% (10-20s) Z")


def calc_c3_fga_20_30s_a(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Percentage of all shots taken that were corner 3s with 20 - 30 seconds remaining on the shot clock."""
    raise NotImplementedError("PBP data not yet available: C3 FGA% (20-30s) A")


def calc_c3_fga_20_30s_c(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Percentage of all shots taken with 20 - 30 seconds remaining on the shot clock that were corner 3s."""
    raise NotImplementedError("PBP data not yet available: C3 FGA% (20-30s) C")


def calc_c3_fga_20_30s_z(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Percentage of all corner 3s that were taken with 20 - 30 seconds remaining on the shot clock."""
    raise NotImplementedError("PBP data not yet available: C3 FGA% (20-30s) Z")


def calc_c3_fgm(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The total number of field goals made on corner 3s."""
    raise NotImplementedError("PBP data not yet available: C3 FGM")


def calc_c3_fgm_0_10s(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The total number of field goals made on corner 3s taken with 0 - 10 seconds remaining on the shot clock."""
    raise NotImplementedError("PBP data not yet available: C3 FGM (0-10s)")


def calc_c3_fgm_10_20s(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The total number of field goals made on corner 3s taken with 10 - 20 seconds remaining on the shot clock."""
    raise NotImplementedError("PBP data not yet available: C3 FGM (10-20s)")


def calc_c3_fgm_20_30s(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The total number of field goals made on corner 3s taken with 20 - 30 seconds remaining on the shot clock."""
    raise NotImplementedError("PBP data not yet available: C3 FGM (20-30s)")


def calc_c3_orb_chnc(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The total number of offensive rebounds chances (offensive rebounds grabbed plus opponent defensive rebounds) on the team's missed corner 3s."""
    raise NotImplementedError("PBP data not yet available: C3 ORB CHNC")


def calc_c3_orb(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Percentage of the team's missed corner 3s that were offensive rebounded by the team."""
    raise NotImplementedError("PBP data not yet available: C3 ORB%")


def calc_c3_orb(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The total number of offensive rebounds grabbed on the team's missed corner 3s."""
    raise NotImplementedError("PBP data not yet available: C3 ORB")


def calc_c3_reb_chnc(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The total number of rebounds chances (rebounds grabbed plus opponent rebounds) on the team's and opponent's missed corner 3s."""
    raise NotImplementedError("PBP data not yet available: C3 REB CHNC")


def calc_c3_reb(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Percentage of the team's and opponent's missed corner 3s that were rebounded by the team."""
    raise NotImplementedError("PBP data not yet available: C3 REB%")


def calc_c3_reb(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The total number of rebounds grabbed on the team's and opponent's missed corner 3s."""
    raise NotImplementedError("PBP data not yet available: C3 REB")


def calc_def_chnc(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """No description available"""
    raise NotImplementedError("PBP data not yet available: DEF CHNC")


def calc_def_chnc_stops(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """No description available"""
    raise NotImplementedError("PBP data not yet available: DEF CHNC STOPS")


def calc_def_chnc_stop(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """No description available"""
    raise NotImplementedError("PBP data not yet available: DEF CHNC STOP%")


def calc_def_poss(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """No description available"""
    raise NotImplementedError("PBP data not yet available: DEF POSS")


def calc_def_poss_stop(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """No description available"""
    raise NotImplementedError("PBP data not yet available: DEF POSS STOP%")


def calc_def_poss_stops(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """No description available"""
    raise NotImplementedError("PBP data not yet available: DEF POSS STOPS")


def calc_dfirstchnc(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """No description available"""
    raise NotImplementedError("PBP data not yet available: dFirstChnc")


def calc_dpbkchnc(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """No description available"""
    raise NotImplementedError("PBP data not yet available: dPbkChnc")


def calc_dpf(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The percentage of possessions with a defensive personal foul committed."""
    raise NotImplementedError("PBP data not yet available: DPF%")


def calc_drbfg_chnc(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Total number of defensive rebound opportunities (defensive rebounds plus opponent offensive rebounds) off missed field goals."""
    raise NotImplementedError("PBP data not yet available: DRBFG CHNC")


def calc_drbft_chnc(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Total number of defensive rebound opportunities (defensive rebounds plus opponent offensive rebounds) off missed free throws."""
    raise NotImplementedError("PBP data not yet available: DRBFT CHNC")


def calc_drbfg(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Total number of defensive rebounds (defensive rebounds plus opponent offensive rebounds) off missed field goals."""
    raise NotImplementedError("PBP data not yet available: DRBFG")


def calc_drbfg_100(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The number of defensive rebounds per 100 possessions (defensive rebounds plus opponent offensive rebounds) off missed field goals."""
    raise NotImplementedError("PBP data not yet available: DRBFG/100")


def calc_drbfg_40(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The number of defensive rebounds per 40 minutes (defensive rebounds plus opponent offensive rebounds) off missed field goals."""
    raise NotImplementedError("PBP data not yet available: DRBFG/40")


def calc_drbfg_g(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The number of defensive rebounds per game (defensive rebounds plus opponent offensive rebounds) off missed field goals."""
    raise NotImplementedError("PBP data not yet available: DRBFG/G")


def calc_drbft(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Total number of defensive rebounds (defensive rebounds plus opponent offensive rebounds) off missed free throws."""
    raise NotImplementedError("PBP data not yet available: DRBFT")


def calc_drbft_100(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The number of defensive rebounds per 100 possessions (defensive rebounds plus opponent offensive rebounds) off missed free throws."""
    raise NotImplementedError("PBP data not yet available: DRBFT/100")


def calc_drbft_40(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The number of defensive rebounds per 40 minutes (defensive rebounds plus opponent offensive rebounds) off missed free throws."""
    raise NotImplementedError("PBP data not yet available: DRBFT/40")


def calc_drbft_g(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The number of defensive rebounds per game (defensive rebounds plus opponent offensive rebounds) off missed free throws."""
    raise NotImplementedError("PBP data not yet available: DRBFT/G")


def calc_drbfg(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The percentage of opponent's missed field goals a player grabbed while he was on the floor."""
    raise NotImplementedError("PBP data not yet available: DRBFG%")


def calc_drbft(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The percentage of opponent's missed free throws a player grabbed while he was on the floor."""
    raise NotImplementedError("PBP data not yet available: DRBFT%")


def calc_tov_dribbling(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The total number of turnovers tagged by the scorer as a dribbling turnover by the team."""
    raise NotImplementedError("PBP data not yet available: TOV DRIBBLING")


def calc_dsecsfirstchnc(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """No description available"""
    raise NotImplementedError("PBP data not yet available: dSecsFirstChnc")


def calc_dsecspbkchnc(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """No description available"""
    raise NotImplementedError("PBP data not yet available: dSecsPbkChnc")


def calc_dsecsposs(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """No description available"""
    raise NotImplementedError("PBP data not yet available: dSecsPoss")


def calc_dunk_astd(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The percentage of a player's dunks that were assisted."""
    raise NotImplementedError("PBP data not yet available: DUNK ASTD%")


def calc_dunk_fga(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The total number of dunk attempts by the player."""
    raise NotImplementedError("PBP data not yet available: DUNK FGA")


def calc_dunk_fga_100(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The number of dunks attempted by the player, per 100 possessions played."""
    raise NotImplementedError("PBP data not yet available: DUNK FGA/100")


def calc_dunk_fga_40(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The number of dunks attempted by the player, per 40 minutes played."""
    raise NotImplementedError("PBP data not yet available: DUNK FGA/40")


def calc_dunk_fga_g(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The number of dunks attempted by the player, per game."""
    raise NotImplementedError("PBP data not yet available: DUNK FGA/G")


def calc_dunk_fgm(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The total number of dunks made by the player."""
    raise NotImplementedError("PBP data not yet available: DUNK FGM")


def calc_efgpcts01(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """No description available"""
    raise NotImplementedError("PBP data not yet available: efgPctS01")


def calc_efgpcts12(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """No description available"""
    raise NotImplementedError("PBP data not yet available: efgPctS12")


def calc_efgpcts23(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """No description available"""
    raise NotImplementedError("PBP data not yet available: efgPctS23")


def calc_bc_poss_chlg_fail(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Total number of unsuccessful coach challenges on backcourt violations or whether team control was established before a foul or violation (women's basketball only)."""
    raise NotImplementedError("PBP data not yet available: BC/Poss CHLG Fail")


def calc_chlg_fail(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Total number of unsuccessful coach challenges."""
    raise NotImplementedError("PBP data not yet available: CHLG Fail")


def calc_foul_chlg_fail(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Total number of unsuccessful coach challenges on foul-related plays. Men: restricted-area block/charge positioning. Women: correct player charged with the foul."""
    raise NotImplementedError("PBP data not yet available: Foul CHLG Fail")


def calc_goi_chlg_fail(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Total number of unsuccessful coach challenges on goaltending or basket interference calls, whether the ball was illegally touched on or above the rim (men's basketball only)."""
    raise NotImplementedError("PBP data not yet available: GOI CHLG Fail")


def calc_oob_chlg_fail(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Total number of unsuccessful coach challenges on out-of-bounds calls (which team last touched the ball before it went out)."""
    raise NotImplementedError("PBP data not yet available: OOB CHLG Fail")


def calc_flp2_fg(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Field goal percentage on far left paint 2-pointers."""
    raise NotImplementedError("PBP data not yet available: FLP2 FG%")


def calc_flp2_fga(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Field goal attempts on far left paint 2-pointers."""
    raise NotImplementedError("PBP data not yet available: FLP2 FGA")


def calc_flp2_fga_100(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Field goal attempts on far left paint 2-pointers per 100 possessions played."""
    raise NotImplementedError("PBP data not yet available: FLP2 FGA/100")


def calc_flp2_fga_40(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Field goal attempts on far left paint 2-pointers per 40 minutes played."""
    raise NotImplementedError("PBP data not yet available: FLP2 FGA/40")


def calc_flp2_fga_g(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Field goal attempts on far left paint 2-pointers per game."""
    raise NotImplementedError("PBP data not yet available: FLP2 FGA/G")


def calc_flp2_fga(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Percentage of shots taken as far left paint 2-pointers."""
    raise NotImplementedError("PBP data not yet available: FLP2 FGA%")


def calc_flp2_fgm(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Field goals made on far left paint 2-pointers."""
    raise NotImplementedError("PBP data not yet available: FLP2 FGM")


def calc_frp2_fg(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Field goal percentage on far right paint 2-pointers."""
    raise NotImplementedError("PBP data not yet available: FRP2 FG%")


def calc_frp2_fga(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Field goal attempts on far right paint 2-pointers."""
    raise NotImplementedError("PBP data not yet available: FRP2 FGA")


def calc_frp2_fga_100(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Field goal attempts on far right paint 2-pointers per 100 possessions played."""
    raise NotImplementedError("PBP data not yet available: FRP2 FGA/100")


def calc_frp2_fga_40(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Field goal attempts on far right paint 2-pointers per 40 minutes played."""
    raise NotImplementedError("PBP data not yet available: FRP2 FGA/40")


def calc_frp2_fga_g(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Field goal attempts on far right paint 2-pointers per game."""
    raise NotImplementedError("PBP data not yet available: FRP2 FGA/G")


def calc_frp2_fga(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Percentage of shots taken as far right paint 2-pointers."""
    raise NotImplementedError("PBP data not yet available: FRP2 FGA%")


def calc_frp2_fgm(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Field goals made on far right paint 2-pointers."""
    raise NotImplementedError("PBP data not yet available: FRP2 FGM")


def calc_ffl_100(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The number of defensive floor fouls committed per 100 possessions."""
    raise NotImplementedError("PBP data not yet available: FFL/100")


def calc_ffl_40(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The number of defensive floor fouls committed per 40 minutes."""
    raise NotImplementedError("PBP data not yet available: FFL/40")


def calc_ffl_g(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The number of defensive floor fouls committed per game."""
    raise NotImplementedError("PBP data not yet available: FFL/G")


def calc_ffl(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The percentage of possessions where a defensive floor foul was committed."""
    raise NotImplementedError("PBP data not yet available: FFL%")


def calc_ffl(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The total number of defensive floor fouls committed."""
    raise NotImplementedError("PBP data not yet available: FFL")


def calc_ffld(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The total number of floor fouls drawn."""
    raise NotImplementedError("PBP data not yet available: FFLD")


def calc_ffld_100(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The number of floor fouls drawn per 100 possessions."""
    raise NotImplementedError("PBP data not yet available: FFLD/100")


def calc_ffld_40(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The number of floor fouls drawn per 40 minutes."""
    raise NotImplementedError("PBP data not yet available: FFLD/40")


def calc_ffld_g(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The number of floor fouls drawn per game."""
    raise NotImplementedError("PBP data not yet available: FFLD/G")


def calc_fg_0_10s(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Percentage of the player's field goal attempts taken with 0 - 10 seconds remaining on the shot clock that were made."""
    raise NotImplementedError("PBP data not yet available: FG% 0-10s")


def calc_fg_20_30s(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Percentage of the player's field goal attempts taken with 20 - 30 seconds remaining on the shot clock that were made."""
    raise NotImplementedError("PBP data not yet available: FG% 20-30s")


def calc_fg_10_20s(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Percentage of the player's field goal attempts taken with 10 - 20 seconds remaining on the shot clock that were made."""
    raise NotImplementedError("PBP data not yet available: FG% 10-20s")


def calc_fg_center(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Field goal percentage on shots taken from the center of the court. This includes all shots where the shooter is positioned within 1 foot in either direction of the imaginary centerline of the court connecting the two rims."""
    raise NotImplementedError("PBP data not yet available: FG% Center")


def calc_fg_left(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Field goal percentage on shots taken from the left side of the court. This includes all shots where the shooter is positioned more than 1 foot to the left of the court's imaginary centerline."""
    raise NotImplementedError("PBP data not yet available: FG% Left")


def calc_fg_right(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Field goal percentage on shots taken from the right side of the court. This includes all shots where the shooter is positioned more than 1 foot to the right of the court's imaginary centerline."""
    raise NotImplementedError("PBP data not yet available: FG% Right")


def calc_fg_in_hc(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """An estimate of overall field goal percentage (makes / attempts) on shots in the context of half court offense (as opposed to transition or putback)."""
    raise NotImplementedError("PBP data not yet available: FG% in HC")


def calc_fg_in_tr(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """An estimate of overall field goal percentage (makes / attempts) on shots in the context of transition offense (as opposed to half court or putback)."""
    raise NotImplementedError("PBP data not yet available: FG% in TR")


def calc_dunk_fg(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Field goal percentage on dunks."""
    raise NotImplementedError("PBP data not yet available: DUNK FG%")


def calc_layup_fg(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Field goal percentage on layups attempted."""
    raise NotImplementedError("PBP data not yet available: LAYUP FG%")


def calc_lay_dunk_fg(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Field goal percentage on layups and dunks attempted."""
    raise NotImplementedError("PBP data not yet available: LAY+DUNK FG%")


def calc_fg_on_pb(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """An estimate of overall field goal percentage (makes / attempts) on shots in the context of putback attempts (as opposed to transition or half court)."""
    raise NotImplementedError("PBP data not yet available: FG% on PB")


def calc_fga_center(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Total field goal attempts taken from the center of the court. This includes all shots where the shooter is positioned within 1 foot in either direction of the imaginary centerline of the court connecting the two rims."""
    raise NotImplementedError("PBP data not yet available: FGA Center")


def calc_fga_left(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Total field goal attempts taken from the left side of the court. This includes all shots where the shooter is positioned more than 1 foot to the left of the court's imaginary centerline."""
    raise NotImplementedError("PBP data not yet available: FGA Left")


def calc_fga_right(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Total field goal attempts taken from the right side of the court. This includes all shots where the shooter is positioned more than 1 foot to the right of the court's imaginary centerline."""
    raise NotImplementedError("PBP data not yet available: FGA Right")


def calc_fga_0_10s_2s(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Percentage of all 2s that were taken with 0 - 10 seconds remaining on the shot clock."""
    raise NotImplementedError("PBP data not yet available: FGA% (0-10s) 2s")


def calc_fga_0_10s_3s(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Percentage of all 3s that were taken with 0 - 10 seconds remaining on the shot clock."""
    raise NotImplementedError("PBP data not yet available: FGA% (0-10s) 3s")


def calc_fga_0_10s_a(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Percentage of all shots that were taken with 0 - 10 seconds remaining on the shot clock."""
    raise NotImplementedError("PBP data not yet available: FGA% (0-10s) A")


def calc_fga_10_20s_2s(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Percentage of all 2s that were taken with 10 - 20 seconds remaining on the shot clock."""
    raise NotImplementedError("PBP data not yet available: FGA% (10-20s) 2s")


def calc_fga_10_20s_3s(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Percentage of all 3s that were taken with 10 - 20 seconds remaining on the shot clock."""
    raise NotImplementedError("PBP data not yet available: FGA% (10-20s) 3s")


def calc_fga_10_20s_a(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Percentage of all shots that were taken with 10 - 20 seconds remaining on the shot clock."""
    raise NotImplementedError("PBP data not yet available: FGA% (10-20s) A")


def calc_fga_20_30s_2s(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Percentage of all 2s that were taken with 20 - 30 seconds remaining on the shot clock."""
    raise NotImplementedError("PBP data not yet available: FGA% (20-30s) 2s")


def calc_fga_20_30s_3s(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Percentage of all 3s that were taken with 20 - 30 seconds remaining on the shot clock."""
    raise NotImplementedError("PBP data not yet available: FGA% (20-30s) 3s")


def calc_fga_20_30s_a(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Percentage of all shots that were taken with 20 - 30 seconds remaining on the shot clock."""
    raise NotImplementedError("PBP data not yet available: FGA% (20-30s) A")


def calc_fga_in_hc(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """An estimate of the percentage of all shots that were taken in the context of half court offense (as opposed to transition or putback)."""
    raise NotImplementedError("PBP data not yet available: FGA% in HC")


def calc_fga_in_tr(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """An estimate of the percentage of all shots that were taken in the context of transition offense (as opposed to half court or putback)."""
    raise NotImplementedError("PBP data not yet available: FGA% in TR")


def calc_fga_on_pb(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """An estimate of the percentage of all shots that were taken in the context of putback offense (as opposed to transition or half court)."""
    raise NotImplementedError("PBP data not yet available: FGA% on PB")


def calc_fga2pb(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """No description available"""
    raise NotImplementedError("PBP data not yet available: fga2Pb")


def calc_fga3pb(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """No description available"""
    raise NotImplementedError("PBP data not yet available: fga3Pb")


def calc_fgabox(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """No description available"""
    raise NotImplementedError("PBP data not yet available: fgaBox")


def calc_fga_0_10s(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The total number of field goal attempts taken with 0 - 10 seconds remaining on the shot clock."""
    raise NotImplementedError("PBP data not yet available: FGA (0-10s)")


def calc_fga_10_20s(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The total number of field goal attempts taken with 10 - 20 seconds remaining on the shot clock."""
    raise NotImplementedError("PBP data not yet available: FGA (10-20s)")


def calc_fga_20_30s(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The total number of field goal attempts taken with 20 - 30 seconds remaining on the shot clock."""
    raise NotImplementedError("PBP data not yet available: FGA (20-30s)")


def calc_fga_in_hc(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """An estimate of the total number of field goal attempts taken in the context of half court offense (as opposed to transition or putback)."""
    raise NotImplementedError("PBP data not yet available: FGA in HC")


def calc_fga_in_tr(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """An estimate of the total number of field goal attempts taken in the context of transition offense (as opposed to half court or putback)."""
    raise NotImplementedError("PBP data not yet available: FGA in TR")


def calc_fga_on_pb(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """An estimate of the total number of field goal attempts taken in the context of putback offense (as opposed to half court or transition)."""
    raise NotImplementedError("PBP data not yet available: FGA on PB")


def calc_fgm_astd(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The percentage of all fields goals made that were assisted."""
    raise NotImplementedError("PBP data not yet available: FGM ASTD%")


def calc_fgm_center(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Total field goals made from the center of the court. This includes all shots where the shooter is positioned within 1 foot in either direction of the imaginary centerline of the court connecting the two rims."""
    raise NotImplementedError("PBP data not yet available: FGM Center")


def calc_fgm_left(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Total field goals made from the left side of the court. This includes all shots where the shooter is positioned more than 1 foot to the left of the court's imaginary centerline."""
    raise NotImplementedError("PBP data not yet available: FGM Left")


def calc_fgm_right(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Total field goals made from the right side of the court. This includes all shots where the shooter is positioned more than 1 foot to the left of the court's imaginary centerline."""
    raise NotImplementedError("PBP data not yet available: FGM Right")


def calc_fgm_in_hc(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """An estimate of the total number of field goals made in the context of half court offense (as opposed to transition or putback)."""
    raise NotImplementedError("PBP data not yet available: FGM in HC")


def calc_fgm_in_tr(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """An estimate of the total number of field goals made in the context of transition offense (as opposed to half court or putback)."""
    raise NotImplementedError("PBP data not yet available: FGM in TR")


def calc_fgm_on_pb(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """An estimate of the total number of field goals made in the context of putback offense (as opposed to half court or transition)."""
    raise NotImplementedError("PBP data not yet available: FGM on PB")


def calc_fgm2pb(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """No description available"""
    raise NotImplementedError("PBP data not yet available: fgm2Pb")


def calc_fgm3pb(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """No description available"""
    raise NotImplementedError("PBP data not yet available: fgm3Pb")


def calc_fgm_0_10s(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The total number of field goals made, taken with 0 - 10 seconds remaining on the shot clock."""
    raise NotImplementedError("PBP data not yet available: FGM (0-10s)")


def calc_fgm_10_20s(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The total number of field goals made, taken with 10 - 20 seconds remaining on the shot clock."""
    raise NotImplementedError("PBP data not yet available: FGM (10-20s)")


def calc_fgm_20_30s(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The total number of field goals made, taken with 20 - 30 seconds remaining on the shot clock."""
    raise NotImplementedError("PBP data not yet available: FGM (20-30s)")


def calc_ffld(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The percentage of possessions where a floor foul was drawn."""
    raise NotImplementedError("PBP data not yet available: FFLD%")


def calc_foul_chlg(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Percentage of coach challenges on foul-related plays that were successful."""
    raise NotImplementedError("PBP data not yet available: Foul CHLG%")


def calc_foul_challenge(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Total number of head coach challenges on foul-related plays. Men: restricted-area block/charge positioning only. Women: correct player charged with the foul."""
    raise NotImplementedError("PBP data not yet available: Foul Challenge")


def calc_ft1(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Free throw percentage on the first free throw attempt."""
    raise NotImplementedError("PBP data not yet available: FT1%")


def calc_ft2(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Free throw percentage on the second free throw attempt."""
    raise NotImplementedError("PBP data not yet available: FT2%")


def calc_ft3(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Free throw percentage on the third free throw attempt."""
    raise NotImplementedError("PBP data not yet available: FT3%")


def calc_fta1(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The total number of first free throw attempts."""
    raise NotImplementedError("PBP data not yet available: FTA1")


def calc_ft1a1pct(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """No description available"""
    raise NotImplementedError("PBP data not yet available: ft1a1Pct")


def calc_ftm1(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The total number of first free throws made."""
    raise NotImplementedError("PBP data not yet available: FTM1")


def calc_fta2(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The total number of second free throw attempts."""
    raise NotImplementedError("PBP data not yet available: FTA2")


def calc_ftm2(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The total number of second free throw attempts made."""
    raise NotImplementedError("PBP data not yet available: FTM2")


def calc_fta3(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The total number of third free throw attempts."""
    raise NotImplementedError("PBP data not yet available: FTA3")


def calc_ftm3(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The total number of third free throw attempts made."""
    raise NotImplementedError("PBP data not yet available: FTM3")


def calc_fta1a1(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """No description available"""
    raise NotImplementedError("PBP data not yet available: fta1a1")


def calc_ftm1a1(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """No description available"""
    raise NotImplementedError("PBP data not yet available: ftm1a1")


def calc_ftratio(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """No description available"""
    raise NotImplementedError("PBP data not yet available: ftRatio")


def calc_goi_chlg(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Percentage of coach challenges on goaltending or basket interference calls that were successful (men's basketball only)."""
    raise NotImplementedError("PBP data not yet available: GOI CHLG%")


def calc_goi_challenge(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Total number of head coach challenges on goaltending or basket interference calls, whether the ball was illegally touched on or above the rim (men's basketball only)."""
    raise NotImplementedError("PBP data not yet available: GOI Challenge")


def calc_gtk(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The percentage of true shot attempts (FGAs + 0.44 * FTA) that were shots at the rim, from 3P range, or trips to the FT line."""
    raise NotImplementedError("PBP data not yet available: gTk%")


def calc_hc_chnc(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The total number of chances in the context of half court offense."""
    raise NotImplementedError("PBP data not yet available: HC CHNC")


def calc_hc_ppc(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """For half court offense, the total number of points scored divided by the total number of half court chances."""
    raise NotImplementedError("PBP data not yet available: HC PPC")


def calc_h3_fg(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Field goal percentage on heaves (35+ feet)."""
    raise NotImplementedError("PBP data not yet available: H3 FG%")


def calc_h3_fga(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Field goal attempts on heaves (35+ feet)."""
    raise NotImplementedError("PBP data not yet available: H3 FGA")


def calc_h3_fga_100(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Field goal attempts on heaves (35+ feet) per 100 possessions played."""
    raise NotImplementedError("PBP data not yet available: H3 FGA/100")


def calc_h3_fga_40(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Field goal attempts on heaves (35+ feet) per 40 minutes played."""
    raise NotImplementedError("PBP data not yet available: H3 FGA/40")


def calc_h3_fga_g(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Field goal attempts on heaves (35+ feet) per game."""
    raise NotImplementedError("PBP data not yet available: H3 FGA/G")


def calc_h3_fga(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Percentage of shots taken as heaves (35+ feet)."""
    raise NotImplementedError("PBP data not yet available: H3 FGA%")


def calc_h3_fgm(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Field goals made on heaves (35+ feet)."""
    raise NotImplementedError("PBP data not yet available: H3 FGM")


def calc_paint2_drb_chnc(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The total number of defensive rebounds chances (defensive rebounds grabbed plus opponent offensive rebounds) on opponent's missed shots in the paint (but not at the rim)."""
    raise NotImplementedError("PBP data not yet available: PAINT2 DRB CHNC")


def calc_paint2_drb(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Percentage of the opponent's missed shots in the paint (but not at the rim) that were defensive rebounded by the team."""
    raise NotImplementedError("PBP data not yet available: PAINT2 DRB%")


def calc_paint2_drb(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The total number of defensive rebounds grabbed on opponent's missed shots in the paint (but not at the rim)."""
    raise NotImplementedError("PBP data not yet available: PAINT2 DRB")


def calc_paint2_astd(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The percentage of shots made in the paint (but not at the rim) that were assisted."""
    raise NotImplementedError("PBP data not yet available: PAINT2 ASTD%")


def calc_lay_dunk_fga_100(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The number of layups and dunks attempted by the player, per 100 possessions played."""
    raise NotImplementedError("PBP data not yet available: LAY+DUNK FGA/100")


def calc_lay_dunk_fga_40(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The number of layups and dunks attempted by the player, per 40 minutes played."""
    raise NotImplementedError("PBP data not yet available: LAY+DUNK FGA/40")


def calc_lay_dunk_fga_g(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The number of layups and dunks attempted by the player, per game."""
    raise NotImplementedError("PBP data not yet available: LAY+DUNK FGA/G")


def calc_lay_dunk_fga(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The total combined number of layups and dunks attempted by the player."""
    raise NotImplementedError("PBP data not yet available: LAY+DUNK FGA")


def calc_lay_dunk_fgm(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The total number of layups and dunks made by the player."""
    raise NotImplementedError("PBP data not yet available: LAY+DUNK FGM")


def calc_layup_fga(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The total number of layups attempted by the player."""
    raise NotImplementedError("PBP data not yet available: LAYUP FGA")


def calc_layup_fga_100(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The number of layups attempted by the player per 100 possessions played."""
    raise NotImplementedError("PBP data not yet available: LAYUP FGA/100")


def calc_layup_fga_40(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The number of layups attempted by the player per 40 minutes played."""
    raise NotImplementedError("PBP data not yet available: LAYUP FGA/40")


def calc_layup_fga_g(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The number of layups attempted by the player per game."""
    raise NotImplementedError("PBP data not yet available: LAYUP FGA/G")


def calc_layup_fgm(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The total number of layups made by the player."""
    raise NotImplementedError("PBP data not yet available: LAYUP FGM")


def calc_lb2_fg(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Field goal percentage on left baseline 2-pointers."""
    raise NotImplementedError("PBP data not yet available: LB2 FG%")


def calc_lb2_fga(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Field goal attempts on left baseline 2-pointers."""
    raise NotImplementedError("PBP data not yet available: LB2 FGA")


def calc_lb2_fga_100(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Field goal attempts on left baseline 2-pointers per 100 possessions played."""
    raise NotImplementedError("PBP data not yet available: LB2 FGA/100")


def calc_lb2_fga_40(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Field goal attempts on left baseline 2-pointers per 40 minutes played."""
    raise NotImplementedError("PBP data not yet available: LB2 FGA/40")


def calc_lb2_fga_g(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Field goal attempts on left baseline 2-pointers per game."""
    raise NotImplementedError("PBP data not yet available: LB2 FGA/G")


def calc_lb2_fga(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Percentage of shots taken as left baseline 2-pointers."""
    raise NotImplementedError("PBP data not yet available: LB2 FGA%")


def calc_lb2_fgm(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Field goals made on left baseline 2-pointers."""
    raise NotImplementedError("PBP data not yet available: LB2 FGM")


def calc_lc3_fg(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Field goal percentage on left corner 3-pointers."""
    raise NotImplementedError("PBP data not yet available: LC3 FG%")


def calc_lc3_fga(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Field goal attempts on left corner 3-pointers."""
    raise NotImplementedError("PBP data not yet available: LC3 FGA")


def calc_lc3_fga_100(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Field goal attempts on left corner 3-pointers per 100 possessions played."""
    raise NotImplementedError("PBP data not yet available: LC3 FGA/100")


def calc_lc3_fga_40(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Field goal attempts on left corner 3-pointers per 40 minutes played."""
    raise NotImplementedError("PBP data not yet available: LC3 FGA/40")


def calc_lc3_fga_g(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Field goal attempts on left corner 3-pointers per game."""
    raise NotImplementedError("PBP data not yet available: LC3 FGA/G")


def calc_lc3_fga(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Percentage of shots taken as left corner 3-pointers."""
    raise NotImplementedError("PBP data not yet available: LC3 FGA%")


def calc_lc3_fgm(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Field goals made on left corner 3-pointers."""
    raise NotImplementedError("PBP data not yet available: LC3 FGM")


def calc_le2_fg(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Field goal percentage on left elbow 2-pointers."""
    raise NotImplementedError("PBP data not yet available: LE2 FG%")


def calc_le2_fga(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Field goal attempts on left elbow 2-pointers."""
    raise NotImplementedError("PBP data not yet available: LE2 FGA")


def calc_le2_fga_100(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Field goal attempts on left elbow 2-pointers per 100 possessions played."""
    raise NotImplementedError("PBP data not yet available: LE2 FGA/100")


def calc_le2_fga_40(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Field goal attempts on left elbow 2-pointers per 40 minutes played."""
    raise NotImplementedError("PBP data not yet available: LE2 FGA/40")


def calc_le2_fga_g(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Field goal attempts on left elbow 2-pointers per game."""
    raise NotImplementedError("PBP data not yet available: LE2 FGA/G")


def calc_le2_fga(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Percentage of shots taken as left elbow 2-pointers."""
    raise NotImplementedError("PBP data not yet available: LE2 FGA%")


def calc_le2_fgm(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Field goals made on left elbow 2-pointers."""
    raise NotImplementedError("PBP data not yet available: LE2 FGM")


def calc_l_r_fg(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Left side FG% minus Right side FG%. Positive values indicate better shooting from the left side of the court."""
    raise NotImplementedError("PBP data not yet available: L-R FG%")


def calc_l_r_fga(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Left side % of shots minus right side % of shots. Positive values indicate a higher share of attempts from the left side of the court."""
    raise NotImplementedError("PBP data not yet available: L-R FGA%")


def calc_lw3_fg(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Field goal percentage on left wing 3-pointers."""
    raise NotImplementedError("PBP data not yet available: LW3 FG%")


def calc_lw3_fga(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Field goal attempts on left wing 3-pointers."""
    raise NotImplementedError("PBP data not yet available: LW3 FGA")


def calc_lw3_fga_100(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Field goal attempts on left wing 3-pointers per 100 possessions played."""
    raise NotImplementedError("PBP data not yet available: LW3 FGA/100")


def calc_lw3_fga_40(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Field goal attempts on left wing 3-pointers per 40 minutes played."""
    raise NotImplementedError("PBP data not yet available: LW3 FGA/40")


def calc_lw3_fga_g(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Field goal attempts on left wing 3-pointers per game."""
    raise NotImplementedError("PBP data not yet available: LW3 FGA/G")


def calc_lw3_fga(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Percentage of shots taken as left wing 3-pointers."""
    raise NotImplementedError("PBP data not yet available: LW3 FGA%")


def calc_lw3_fgm(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Field goals made on left wing 3-pointers."""
    raise NotImplementedError("PBP data not yet available: LW3 FGM")


def calc_lng2_fg(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Field goal percentage on 15+ foot 2-pointers."""
    raise NotImplementedError("PBP data not yet available: LNG2 FG%")


def calc_lng2_fga(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Field goal attempts on 15+ foot 2-pointers."""
    raise NotImplementedError("PBP data not yet available: LNG2 FGA")


def calc_lng2_fga_100(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Field goal attempts on 15+ foot 2-pointers per 100 possessions played."""
    raise NotImplementedError("PBP data not yet available: LNG2 FGA/100")


def calc_lng2_fga_40(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Field goal attempts on 15+ foot 2-pointers per 40 minutes played."""
    raise NotImplementedError("PBP data not yet available: LNG2 FGA/40")


def calc_lng2_fga_g(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Field goal attempts on 15+ foot 2-pointers per game."""
    raise NotImplementedError("PBP data not yet available: LNG2 FGA/G")


def calc_lng2_fga(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Percentage of shots taken as 15+ foot 2-pointers."""
    raise NotImplementedError("PBP data not yet available: LNG2 FGA%")


def calc_lng2_fgm(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Field goals made on 15+ foot 2-pointers."""
    raise NotImplementedError("PBP data not yet available: LNG2 FGM")


def calc_lng3_fg(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Field goal percentage on 25+ foot 3-pointers."""
    raise NotImplementedError("PBP data not yet available: LNG3 FG%")


def calc_lng3_fga(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Field goal attempts on 25+ foot 3-pointers."""
    raise NotImplementedError("PBP data not yet available: LNG3 FGA")


def calc_lng3_fga_100(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Field goal attempts on 25+ foot 3-pointers per 100 possessions played."""
    raise NotImplementedError("PBP data not yet available: LNG3 FGA/100")


def calc_lng3_fga_40(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Field goal attempts on 25+ foot 3-pointers per 40 minutes played."""
    raise NotImplementedError("PBP data not yet available: LNG3 FGA/40")


def calc_lng3_fga_g(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Field goal attempts on 25+ foot 3-pointers per game."""
    raise NotImplementedError("PBP data not yet available: LNG3 FGA/G")


def calc_lng3_fga(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Percentage of shots taken as 25+ foot 3-pointers."""
    raise NotImplementedError("PBP data not yet available: LNG3 FGA%")


def calc_lng3_fgm(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Field goals made on 25+ foot 3-pointers."""
    raise NotImplementedError("PBP data not yet available: LNG3 FGM")


def calc_tov_lost(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The total number of turnovers tagged by the scorer as a lost ball turnover by the team."""
    raise NotImplementedError("PBP data not yet available: TOV LOST")


def calc_med2_fg(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Field goal percentage on 10-15 foot 2-pointers."""
    raise NotImplementedError("PBP data not yet available: MED2 FG%")


def calc_med2_fga(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Field goal attempts on 10-15 foot 2-pointers."""
    raise NotImplementedError("PBP data not yet available: MED2 FGA")


def calc_med2_fga_100(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Field goal attempts on 10-15 foot 2-pointers per 100 possessions played."""
    raise NotImplementedError("PBP data not yet available: MED2 FGA/100")


def calc_med2_fga_40(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Field goal attempts on 10-15 foot 2-pointers per 40 minutes played."""
    raise NotImplementedError("PBP data not yet available: MED2 FGA/40")


def calc_med2_fga_g(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Field goal attempts on 10-15 foot 2-pointers per game."""
    raise NotImplementedError("PBP data not yet available: MED2 FGA/G")


def calc_med2_fga(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Percentage of shots taken as 10-15 foot 2-pointers."""
    raise NotImplementedError("PBP data not yet available: MED2 FGA%")


def calc_med2_fgm(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Field goals made on 10-15 foot 2-pointers."""
    raise NotImplementedError("PBP data not yet available: MED2 FGM")


def calc_mid2_fg(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Field goal percentage on midrange 2s."""
    raise NotImplementedError("PBP data not yet available: MID2 FG%")


def calc_mid2_fg_0_10s(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Field goal percentage on midrange 2s taken with 0 - 10 seconds remaining on the shot clock."""
    raise NotImplementedError("PBP data not yet available: MID2 FG% (0-10s)")


def calc_mid2_fg_10_20s(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Field goal percentage on midrange 2s taken with 10 - 20 seconds remaining on the shot clock."""
    raise NotImplementedError("PBP data not yet available: MID2 FG% (10-20s)")


def calc_mid2_fg_20_30s(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Field goal percentage on midrange 2s taken with 20 - 30 seconds remaining on the shot clock."""
    raise NotImplementedError("PBP data not yet available: MID2 FG% (20-30s)")


def calc_mid2_fga(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Field goal attempts on midrange 2s."""
    raise NotImplementedError("PBP data not yet available: MID2 FGA")


def calc_mid2_fga_0_10s(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The total number of field goal attempts on midrange 2s taken with 0 - 10 seconds remaining on the shot clock."""
    raise NotImplementedError("PBP data not yet available: MID2 FGA (0-10s)")


def calc_mid2_fga_10_20s(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The total number of field goal attempts on midrange 2s taken with 10 - 20 seconds remaining on the shot clock."""
    raise NotImplementedError("PBP data not yet available: MID2 FGA (10-20s)")


def calc_mid2_fga_20_30s(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The total number of field goal attempts on midrange 2s taken with 20 - 30 seconds remaining on the shot clock."""
    raise NotImplementedError("PBP data not yet available: MID2 FGA (20-30s)")


def calc_mid2_fga_100(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Field goal attempts on midrange 2s per 100 possessions played."""
    raise NotImplementedError("PBP data not yet available: MID2 FGA/100")


def calc_mid2_fga_40(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Field goal attempts on midrange 2s per 40 minutes played."""
    raise NotImplementedError("PBP data not yet available: MID2 FGA/40")


def calc_mid2_fga_g(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Field goal attempts on midrange 2s per game."""
    raise NotImplementedError("PBP data not yet available: MID2 FGA/G")


def calc_mid2_fga(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Percentage of shots taken as midrange 2s."""
    raise NotImplementedError("PBP data not yet available: MID2 FGA%")


def calc_mid2_fga_0_10s_a(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Percentage of all shots taken that were midrange 2s with 0 - 10 seconds remaining on the shot clock."""
    raise NotImplementedError("PBP data not yet available: MID2 FGA% (0-10s) A")


def calc_mid2_fga_0_10s_c(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Percentage of all shots taken with 0 - 10 seconds remaining on the shot clock that were midrange 2s."""
    raise NotImplementedError("PBP data not yet available: MID2 FGA% (0-10s) C")


def calc_mid2_fga_0_10s_z(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Percentage of all midrange 2s that were taken with 0 - 10 seconds remaining on the shot clock."""
    raise NotImplementedError("PBP data not yet available: MID2 FGA% (0-10s) Z")


def calc_mid2_fga_10_20s_a(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Percentage of all shots taken that were midrange 2s with 10 - 20 seconds remaining on the shot clock."""
    raise NotImplementedError("PBP data not yet available: MID2 FGA% (10-20s) A")


def calc_mid2_fga_10_20s_c(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Percentage of all shots taken with 10 - 20 seconds remaining on the shot clock that were midrange 2s."""
    raise NotImplementedError("PBP data not yet available: MID2 FGA% (10-20s) C")


def calc_mid2_fga_10_20s_z(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Percentage of all midrange 2s that were taken with 10 - 20 seconds remaining on the shot clock."""
    raise NotImplementedError("PBP data not yet available: MID2 FGA% (10-20s) Z")


def calc_mid2_fga_20_30s_a(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Percentage of all shots taken that were midrange 2s with 20 - 30 seconds remaining on the shot clock."""
    raise NotImplementedError("PBP data not yet available: MID2 FGA% (20-30s) A")


def calc_mid2_fga_20_30s_c(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Percentage of all shots taken with 20 - 30 seconds remaining on the shot clock that were midrange 2s."""
    raise NotImplementedError("PBP data not yet available: MID2 FGA% (20-30s) C")


def calc_mid2_fga_20_30s_z(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Percentage of all midrange 2s that were taken with 20 - 30 seconds remaining on the shot clock."""
    raise NotImplementedError("PBP data not yet available: MID2 FGA% (20-30s) Z")


def calc_mid2_fgm(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Field goals made on midrange 2s."""
    raise NotImplementedError("PBP data not yet available: MID2 FGM")


def calc_mid2_fgm_0_10s(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The total number of field goals made on midrange 2s taken with 0 - 10 seconds remaining on the shot clock."""
    raise NotImplementedError("PBP data not yet available: MID2 FGM (0-10s)")


def calc_mid2_fgm_10_20s(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The total number of field goals made on midrange 2s taken with 10 - 20 seconds remaining on the shot clock."""
    raise NotImplementedError("PBP data not yet available: MID2 FGM (10-20s)")


def calc_mid2_fgm_20_30s(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The total number of field goals made on midrange 2s taken with 20 - 30 seconds remaining on the shot clock."""
    raise NotImplementedError("PBP data not yet available: MID2 FGM (20-30s)")


def calc_mid2_ufgm(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """No description available"""
    raise NotImplementedError("PBP data not yet available: MID2 uFGM")


def calc_mid2_orb_chnc(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The total number of offensive rebounds chances (offensive rebounds grabbed plus opponent defensive rebounds) on the team's missed midrange 2s."""
    raise NotImplementedError("PBP data not yet available: MID2 ORB CHNC")


def calc_mid2_orb(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Percentage of the team's missed midrange 2s that were offensive rebounded by the team."""
    raise NotImplementedError("PBP data not yet available: MID2 ORB%")


def calc_mid2_orb(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The total number of offensive rebounds grabbed on the team's missed midrange 2s."""
    raise NotImplementedError("PBP data not yet available: MID2 ORB")


def calc_mid2_reb_chnc(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The total number of rebounds chances (rebounds grabbed plus opponent rebounds) on the team's and opponent's missed midrange 2s."""
    raise NotImplementedError("PBP data not yet available: MID2 REB CHNC")


def calc_mid2_reb(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Percentage of the team's and opponent's missed midrange 2s that were rebounded by the team."""
    raise NotImplementedError("PBP data not yet available: MID2 REB%")


def calc_paint2_reb(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Percentage of the team's and opponent's missed shots in the paint (but not at the rim) that were rebounded by the team."""
    raise NotImplementedError("PBP data not yet available: PAINT2 REB%")


def calc_mid2_reb(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The total number of rebounds grabbed on the team's and opponent's missed midrange 2s."""
    raise NotImplementedError("PBP data not yet available: MID2 REB")


def calc_mid2_astd(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The percentage of shots made from the midrange that were assisted."""
    raise NotImplementedError("PBP data not yet available: MID2 ASTD%")


def calc_mid2_drb_chnc(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The total number of defensive rebounds chances (defensive rebounds grabbed plus opponent offensive rebounds) on opponent's missed midrange 2s."""
    raise NotImplementedError("PBP data not yet available: MID2 DRB CHNC")


def calc_mid2_drb(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Percentage of the opponent's missed midrange 2s that were defensive rebounded by the team."""
    raise NotImplementedError("PBP data not yet available: MID2 DRB%")


def calc_mid2_drb(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The total number of defensive rebounds grabbed on opponent's missed midrange 2s."""
    raise NotImplementedError("PBP data not yet available: MID2 DRB")


def calc_in_poss(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Number of minutes when the team is with possession. Due to minutes where neither team is in possession, team minutes + opponent minutes in possession do not add up to total game minutes."""
    raise NotImplementedError("PBP data not yet available: IN POSS")


def calc_in_poss_g(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Number of minutes when the team is with possession, per game. Due to minutes where neither team is in possession, team minutes + opponent minutes in possession do not add up to total game minutes."""
    raise NotImplementedError("PBP data not yet available: IN POSS/G")


def calc_out_poss(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Number of minutes when the opposing team is with possession. Due to minutes where neither team is in possession, team minutes + opponent minutes in possession do not add up to total game minutes."""
    raise NotImplementedError("PBP data not yet available: OUT POSS")


def calc_out_poss_g(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Number of minutes when the opposing team is with possession, per game. Due to minutes where neither team is in possession, team minutes + opponent minutes in possession do not add up to total game minutes."""
    raise NotImplementedError("PBP data not yet available: OUT POSS/G")


def calc_3par_nba(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Percentage of the player's field goal attempts that were NBA-distance 3-point field goal attempts."""
    raise NotImplementedError("PBP data not yet available: 3PAr**NBA")


def calc_3pa_nba(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The total number of NBA-distance 3-point field goal attempts taken."""
    raise NotImplementedError("PBP data not yet available: 3PA**NBA")


def calc_3p_nba(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Percentage of the player's NBA-distance 3-point field goal attempts that were made."""
    raise NotImplementedError("PBP data not yet available: 3P%**NBA")


def calc_3pm_nba(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The total number of NBA-distance 3-point field goals made."""
    raise NotImplementedError("PBP data not yet available: 3PM**NBA")


def calc_3pa_nba(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Percentage of the player's 3-point attempts that were NBA-distance 3-point field goal attempts."""
    raise NotImplementedError("PBP data not yet available: 3PA%**NBA")


def calc_tov_offensive(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The total number of turnovers tagged by the scorer as an offensive foul turnover by the team."""
    raise NotImplementedError("PBP data not yet available: TOV OFFENSIVE")


def calc_opfd(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The total number of offensive personal fouls drawn by the player."""
    raise NotImplementedError("PBP data not yet available: OPFD")


def calc_ofirstchnc(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """No description available"""
    raise NotImplementedError("PBP data not yet available: oFirstChnc")


def calc_oob_chlg(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Percentage of coach challenges on out-of-bounds calls that were successful."""
    raise NotImplementedError("PBP data not yet available: OOB CHLG%")


def calc_opbkchnc(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """No description available"""
    raise NotImplementedError("PBP data not yet available: oPbkChnc")


def calc_opfd_100(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The total number of offensive personal fouls drawn by the player, per 100 possessions played."""
    raise NotImplementedError("PBP data not yet available: OPFD/100")


def calc_opfd_40(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The total number of offensive personal fouls drawn by the player, per 40 minutes played."""
    raise NotImplementedError("PBP data not yet available: OPFD/40")


def calc_opfd_g(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The total number of offensive personal fouls drawn by the player, per game."""
    raise NotImplementedError("PBP data not yet available: OPFD/G")


def calc_opfd(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The percentage of defensive possessions with an offensive personal foul drawn by the player."""
    raise NotImplementedError("PBP data not yet available: OPFD%")


def calc_opf(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The percentage of possessions with an offensive personal foul committed."""
    raise NotImplementedError("PBP data not yet available: OPF%")


def calc_orbfg_chnc(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Total number of offensive rebound opportunities (offensive rebounds plus opponent defensive rebounds) off missed field goals."""
    raise NotImplementedError("PBP data not yet available: ORBFG CHNC")


def calc_orbft_chnc(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Total number of offensive rebound opportunities (offensive rebounds plus opponent defensive rebounds) off missed free throws."""
    raise NotImplementedError("PBP data not yet available: ORBFT CHNC")


def calc_orbfg(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Total number of offensive rebounds (offensive rebounds plus opponent defensive rebounds) off missed field goals."""
    raise NotImplementedError("PBP data not yet available: ORBFG")


def calc_orbfg_100(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The number of offensive rebounds per 100 possessions (offensive rebounds plus opponent defensive rebounds) off missed field goals."""
    raise NotImplementedError("PBP data not yet available: ORBFG/100")


def calc_orbfg_40(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The number of offensive rebounds per 40 minutes (offensive rebounds plus opponent defensive rebounds) off missed field goals."""
    raise NotImplementedError("PBP data not yet available: ORBFG/40")


def calc_orbfg_g(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The number of offensive rebounds per game (offensive rebounds plus opponent defensive rebounds) off missed field goals."""
    raise NotImplementedError("PBP data not yet available: ORBFG/G")


def calc_orbft(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Total number of offensive rebounds (offensive rebounds plus opponent defensive rebounds) off missed free throws."""
    raise NotImplementedError("PBP data not yet available: ORBFT")


def calc_orbft_100(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The number of offensive rebounds per 100 possessions (offensive rebounds plus opponent defensive rebounds) off missed free throws."""
    raise NotImplementedError("PBP data not yet available: ORBFT/100")


def calc_orbft_40(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The number of offensive rebounds per 40 minutes (offensive rebounds plus opponent defensive rebounds) off missed free throws."""
    raise NotImplementedError("PBP data not yet available: ORBFT/40")


def calc_orbft_g(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The number of offensive rebounds per game (offensive rebounds plus opponent defensive rebounds) off missed free throws."""
    raise NotImplementedError("PBP data not yet available: ORBFT/G")


def calc_orbfg(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The percentage of team's missed field goals a player grabbed while he was on the floor."""
    raise NotImplementedError("PBP data not yet available: ORBFG%")


def calc_orbft(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The percentage of team's missed free throws a player grabbed while he was on the floor."""
    raise NotImplementedError("PBP data not yet available: ORBFT%")


def calc_osecsfirstchnc(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """No description available"""
    raise NotImplementedError("PBP data not yet available: oSecsFirstChnc")


def calc_osecspbkchnc(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """No description available"""
    raise NotImplementedError("PBP data not yet available: oSecsPbkChnc")


def calc_secs_poss(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """No description available"""
    raise NotImplementedError("PBP data not yet available: SECS POSS")


def calc_tov_other(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The total number of turnovers tagged by the scorer as some other turnover type (lane violation, offensive goal tending, other) by the team."""
    raise NotImplementedError("PBP data not yet available: TOV OTHER")


def calc_tov_oob(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The total number of turnovers tagged by the scorer as an out of bounds turnover by the team."""
    raise NotImplementedError("PBP data not yet available: TOV OOB")


def calc_oob_challenge(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Total number of head coach challenges used on out-of-bounds calls (which team last touched the ball before it went out)."""
    raise NotImplementedError("PBP data not yet available: OOB Challenge")


def calc_paint2_fg(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Field goal percentage on shots taken in the paint (but not at the rim)."""
    raise NotImplementedError("PBP data not yet available: PAINT2 FG%")


def calc_paint2_fg_0_10s(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Field goal percentage on shots taken in the paint (but not at the rim) with 0 - 10 seconds remaining on the shot clock."""
    raise NotImplementedError("PBP data not yet available: PAINT2 FG% (0-10s)")


def calc_paint2_fg_10_20s(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Field goal percentage on shots taken in the paint (but not at the rim) with 10 - 20 seconds remaining on the shot clock."""
    raise NotImplementedError("PBP data not yet available: PAINT2 FG% (10-20s)")


def calc_paint2_fg_20_30s(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Field goal percentage on shots taken in the paint (but not at the rim) with 20 - 30 seconds remaining on the shot clock."""
    raise NotImplementedError("PBP data not yet available: PAINT2 FG% (20-30s)")


def calc_paint2_fga(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The total number of field goal attempts on shots taken in the paint (but not at the rim)."""
    raise NotImplementedError("PBP data not yet available: PAINT2 FGA")


def calc_paint2_fga_0_10s(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The total number of field goal attempts on shots taken in the paint (but not at the rim) with 0 - 10 seconds remaining on the shot clock."""
    raise NotImplementedError("PBP data not yet available: PAINT2 FGA (0-10s)")


def calc_paint2_fga_10_20s(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The total number of field goal attempts on shots taken in the paint (but not at the rim) with 10 - 20 seconds remaining on the shot clock."""
    raise NotImplementedError("PBP data not yet available: PAINT2 FGA (10-20s)")


def calc_paint2_fga_20_30s(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The total number of field goal attempts on shots taken in the paint (but not at the rim) with 20 - 30 seconds remaining on the shot clock."""
    raise NotImplementedError("PBP data not yet available: PAINT2 FGA (20-30s)")


def calc_paint2_fga_100(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Field goal attempts on shots taken in the paint (but not at the rim) per 100 possessions played."""
    raise NotImplementedError("PBP data not yet available: PAINT2 FGA/100")


def calc_paint2_fga_40(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Field goal attempts on shots taken in the paint (but not at the rim) per 40 minutes played."""
    raise NotImplementedError("PBP data not yet available: PAINT2 FGA/40")


def calc_paint2_fga_g(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Field goal attempts on shots taken in the paint (but not at the rim) per game."""
    raise NotImplementedError("PBP data not yet available: PAINT2 FGA/G")


def calc_paint2_fga(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Percentage of shots taken in the paint (not at the rim)."""
    raise NotImplementedError("PBP data not yet available: PAINT2 FGA%")


def calc_paint2_fga_0_10s_a(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Percentage of all shots taken that were in the paint (but not at the rim) with 0 - 10 seconds remaining on the shot clock."""
    raise NotImplementedError("PBP data not yet available: PAINT2 FGA% (0-10s) A")


def calc_paint2_fga_0_10s_c(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Percentage of all shots taken with 0 - 10 seconds remaining on the shot clock that were in the paint (but not at the rim)."""
    raise NotImplementedError("PBP data not yet available: PAINT2 FGA% (0-10s) C")


def calc_paint2_fga_0_10s_z(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Percentage of all shots in the paint (but not at the rim) that were taken with 0 - 10 seconds remaining on the shot clock."""
    raise NotImplementedError("PBP data not yet available: PAINT2 FGA% (0-10s) Z")


def calc_paint2_fga_10_20s_a(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Percentage of all shots taken that were in the paint (but not at the rim) with 10 - 20 seconds remaining on the shot clock."""
    raise NotImplementedError("PBP data not yet available: PAINT2 FGA% (10-20s) A")


def calc_paint2_fga_10_20s_c(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Percentage of all shots taken with 10 - 20 seconds remaining on the shot clock that were in the paint (but not at the rim)."""
    raise NotImplementedError("PBP data not yet available: PAINT2 FGA% (10-20s) C")


def calc_paint2_fga_10_20s_z(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Percentage of all shots in the paint (but not at the rim) that were taken with 10 - 20 seconds remaining on the shot clock."""
    raise NotImplementedError("PBP data not yet available: PAINT2 FGA% (10-20s) Z")


def calc_paint2_fga_20_30s_a(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Percentage of all shots taken that were in the paint (but not at the rim) with 20 - 30 seconds remaining on the shot clock."""
    raise NotImplementedError("PBP data not yet available: PAINT2 FGA% (20-30s) A")


def calc_paint2_fga_20_30s_c(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Percentage of all shots taken with 20 - 30 seconds remaining on the shot clock that were in the paint (but not at the rim)."""
    raise NotImplementedError("PBP data not yet available: PAINT2 FGA% (20-30s) C")


def calc_paint2_fga_20_30s_z(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Percentage of all shots in the paint (but not at the rim) that were taken with 20 - 30 seconds remaining on the shot clock."""
    raise NotImplementedError("PBP data not yet available: PAINT2 FGA% (20-30s) Z")


def calc_paint2_fgm(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The total number of field goals made on shots taken in the paint (but not at the rim)."""
    raise NotImplementedError("PBP data not yet available: PAINT2 FGM")


def calc_paint2_fgm_0_10s(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The total number of field goals made on shots taken in the paint (but not at the rim) with 0 - 10 seconds remaining on the shot clock."""
    raise NotImplementedError("PBP data not yet available: PAINT2 FGM (0-10s)")


def calc_paint2_fgm_10_20s(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The total number of field goals made on shots taken in the paint (but not at the rim) with 10 - 20 seconds remaining on the shot clock."""
    raise NotImplementedError("PBP data not yet available: PAINT2 FGM (10-20s)")


def calc_paint2_fgm_20_30s(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The total number of field goals made on shots taken in the paint (but not at the rim) with 20 - 30 seconds remaining on the shot clock."""
    raise NotImplementedError("PBP data not yet available: PAINT2 FGM (20-30s)")


def calc_paint2_orb_chnc(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The total number of offensive rebounds chances (offensive rebounds grabbed plus opponent defensive rebounds) on the team's missed shots in the paint (but not at the rim)."""
    raise NotImplementedError("PBP data not yet available: PAINT2 ORB CHNC")


def calc_paint2_orb(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Percentage of the team's missed shots in the paint (but not at the rim) that were offensive rebounded by the team."""
    raise NotImplementedError("PBP data not yet available: PAINT2 ORB%")


def calc_paint2_orb(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The total number of offensive rebounds grabbed on the team's missed shots in the paint (but not at the rim)."""
    raise NotImplementedError("PBP data not yet available: PAINT2 ORB")


def calc_paint2_reb_chnc(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The total number of rebounds chances (rebounds grabbed plus opponent rebounds) on the team's and opponent's missed shots in the paint (but not at the rim)."""
    raise NotImplementedError("PBP data not yet available: PAINT2 REB CHNC")


def calc_paint2_reb(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The total number of rebounds grabbed on the team's and opponent's missed shots in the paint (but not at the rim)."""
    raise NotImplementedError("PBP data not yet available: PAINT2 REB")


def calc_paint2_ufgm(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """No description available"""
    raise NotImplementedError("PBP data not yet available: PAINT2 uFGM")


def calc_pf(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The percentage of possessions with a personal foul committed."""
    raise NotImplementedError("PBP data not yet available: PF%")


def calc_pts_astd(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The total number of teammate points scored that were assisted by the player."""
    raise NotImplementedError("PBP data not yet available: PTS ASTD")


def calc_pts_astd(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The percentage of points scored by the player that were assisted by teammates."""
    raise NotImplementedError("PBP data not yet available: PTS ASTD%")


def calc_hc_pts(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The total number of points scored in the context of half court offense (as opposed to in transition, or on putbacks)."""
    raise NotImplementedError("PBP data not yet available: HC PTS")


def calc_tr_pts(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The total number of points scored in the context of transition offense (as opposed to in the half court, or on putbacks)."""
    raise NotImplementedError("PBP data not yet available: TR PTS")


def calc_pb_pts(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The total number of points scored in the context of putback offense (as opposed to in the half court, or in transition)."""
    raise NotImplementedError("PBP data not yet available: PB PTS")


def calc_ptsagstbox(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """No description available"""
    raise NotImplementedError("PBP data not yet available: ptsAgstBox")


def calc_ptsscoredbox(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """No description available"""
    raise NotImplementedError("PBP data not yet available: ptsScoredBox")


def calc_ptsscoredwb(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """No description available"""
    raise NotImplementedError("PBP data not yet available: ptsScoredWb")


def calc_pb_chnc(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The total number of chances in the context of putback offense."""
    raise NotImplementedError("PBP data not yet available: PB CHNC")


def calc_pb_ppc(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """For putback offense, the total number of points scored divided by the total number of putback chances."""
    raise NotImplementedError("PBP data not yet available: PB PPC")


def calc_rb2_fg(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Field goal percentage on right baseline 2-pointers."""
    raise NotImplementedError("PBP data not yet available: RB2 FG%")


def calc_rb2_fga(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Field goal attempts on right baseline 2-pointers."""
    raise NotImplementedError("PBP data not yet available: RB2 FGA")


def calc_rb2_fga_100(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Field goal attempts on right baseline 2-pointers per 100 possessions played."""
    raise NotImplementedError("PBP data not yet available: RB2 FGA/100")


def calc_rb2_fga_40(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Field goal attempts on right baseline 2-pointers per 40 minutes played."""
    raise NotImplementedError("PBP data not yet available: RB2 FGA/40")


def calc_rb2_fga_g(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Field goal attempts on right baseline 2-pointers per game."""
    raise NotImplementedError("PBP data not yet available: RB2 FGA/G")


def calc_rb2_fga(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Percentage of shots taken as right baseline 2-pointers."""
    raise NotImplementedError("PBP data not yet available: RB2 FGA%")


def calc_rb2_fgm(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Field goals made on right baseline 2-pointers."""
    raise NotImplementedError("PBP data not yet available: RB2 FGM")


def calc_rc3_fg(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Field goal percentage on right corner 3-pointers."""
    raise NotImplementedError("PBP data not yet available: RC3 FG%")


def calc_rc3_fga(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Field goal attempts on right corner 3-pointers."""
    raise NotImplementedError("PBP data not yet available: RC3 FGA")


def calc_rc3_fga_100(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Field goal attempts on right corner 3-pointers per 100 possessions played."""
    raise NotImplementedError("PBP data not yet available: RC3 FGA/100")


def calc_rc3_fga_40(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Field goal attempts on right corner 3-pointers per 40 minutes played."""
    raise NotImplementedError("PBP data not yet available: RC3 FGA/40")


def calc_rc3_fga_g(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Field goal attempts on right corner 3-pointers per game."""
    raise NotImplementedError("PBP data not yet available: RC3 FGA/G")


def calc_rc3_fga(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Percentage of shots taken as right corner 3-pointers."""
    raise NotImplementedError("PBP data not yet available: RC3 FGA%")


def calc_rc3_fgm(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Field goals made on right corner 3-pointers."""
    raise NotImplementedError("PBP data not yet available: RC3 FGM")


def calc_re2_fg(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Field goal percentage on right elbow 2-pointers."""
    raise NotImplementedError("PBP data not yet available: RE2 FG%")


def calc_re2_fga(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Field goal attempts on right elbow 2-pointers."""
    raise NotImplementedError("PBP data not yet available: RE2 FGA")


def calc_re2_fga_100(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Field goal attempts on right elbow 2-pointers per 100 possessions played."""
    raise NotImplementedError("PBP data not yet available: RE2 FGA/100")


def calc_re2_fga_40(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Field goal attempts on right elbow 2-pointers per 40 minutes played."""
    raise NotImplementedError("PBP data not yet available: RE2 FGA/40")


def calc_re2_fga_g(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Field goal attempts on right elbow 2-pointers per game."""
    raise NotImplementedError("PBP data not yet available: RE2 FGA/G")


def calc_re2_fga(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Percentage of shots taken as right elbow 2-pointers."""
    raise NotImplementedError("PBP data not yet available: RE2 FGA%")


def calc_re2_fgm(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Field goals made on right elbow 2-pointers."""
    raise NotImplementedError("PBP data not yet available: RE2 FGM")


def calc_rw3_fg(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Field goal percentage on right wing 3-pointers."""
    raise NotImplementedError("PBP data not yet available: RW3 FG%")


def calc_rw3_fga(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Field goal attempts on right wing 3-pointers."""
    raise NotImplementedError("PBP data not yet available: RW3 FGA")


def calc_rw3_fga_100(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Field goal attempts on right wing 3-pointers per 100 possessions played."""
    raise NotImplementedError("PBP data not yet available: RW3 FGA/100")


def calc_rw3_fga_40(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Field goal attempts on right wing 3-pointers per 40 minutes played."""
    raise NotImplementedError("PBP data not yet available: RW3 FGA/40")


def calc_rw3_fga_g(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Field goal attempts on right wing 3-pointers per game."""
    raise NotImplementedError("PBP data not yet available: RW3 FGA/G")


def calc_rw3_fga(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Percentage of shots taken as right wing 3-pointers."""
    raise NotImplementedError("PBP data not yet available: RW3 FGA%")


def calc_rw3_fgm(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Field goals made on right wing 3-pointers."""
    raise NotImplementedError("PBP data not yet available: RW3 FGM")


def calc_rim_paint_afgm(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The total number of assisted shots made in the paint (including shots at the rim) by the player."""
    raise NotImplementedError("PBP data not yet available: RIM+PAINT aFGM")


def calc_rim_paint_afgm_100(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The total number of assisted shots made in the paint (including shots at the rim) by the player, per 100 possessions played."""
    raise NotImplementedError("PBP data not yet available: RIM+PAINT aFGM/100")


def calc_rim_paint_afgm_40(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The total number of assisted shots made in the paint (including shots at the rim) by the player, per 40 minutes played."""
    raise NotImplementedError("PBP data not yet available: RIM+PAINT aFGM/40")


def calc_rim_paint_afgm_g(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The total number of assisted shots made in the paint (including shots at the rim) by the player, per game."""
    raise NotImplementedError("PBP data not yet available: RIM+PAINT aFGM/G")


def calc_rim_paint_astd(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The percentage of shots made in the paint (including shots at the rim) that were assisted."""
    raise NotImplementedError("PBP data not yet available: RIM+PAINT ASTD%")


def calc_rim_paint_fg(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Field goal percentage on shots taken in the paint (including shots at the rim)."""
    raise NotImplementedError("PBP data not yet available: RIM+PAINT FG%")


def calc_rim_paint_fga(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The total number of field goal attempts on shots taken in the paint (including shots at the rim)."""
    raise NotImplementedError("PBP data not yet available: RIM+PAINT FGA")


def calc_rim_paint_fga_100(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Field goal attempts on shots taken in the paint (including shots at the rim) per 100 possessions played."""
    raise NotImplementedError("PBP data not yet available: RIM+PAINT FGA/100")


def calc_rim_paint_fga_40(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Field goal attempts on shots taken in the paint (including shots at the rim) per 40 minutes played."""
    raise NotImplementedError("PBP data not yet available: RIM+PAINT FGA/40")


def calc_rim_paint_fga_g(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Field goal attempts on shots taken in the paint (including shots at the rim) per game."""
    raise NotImplementedError("PBP data not yet available: RIM+PAINT FGA/G")


def calc_rim_paint_fga(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Percentage of shots taken in the paint (including shots at the rim)."""
    raise NotImplementedError("PBP data not yet available: RIM+PAINT FGA%")


def calc_rim_paint_fgm(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The total number of field goals made on shots taken in the paint (including shots at the rim)."""
    raise NotImplementedError("PBP data not yet available: RIM+PAINT FGM")


def calc_rim_paint_ufgm(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The total number of unassisted shots made in the paint (including shots at the rim) by the player."""
    raise NotImplementedError("PBP data not yet available: RIM+PAINT uFGM")


def calc_sfl(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The total number of shooting fouls committed."""
    raise NotImplementedError("PBP data not yet available: SFL")


def calc_sfl2pts(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """No description available"""
    raise NotImplementedError("PBP data not yet available: sfl2Pts")


def calc_sfl3pts(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """No description available"""
    raise NotImplementedError("PBP data not yet available: sfl3Pts")


def calc_sfland1(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """No description available"""
    raise NotImplementedError("PBP data not yet available: sflAnd1")


def calc_sfld(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The percentage of shot attempts where a shooting foul was drawn."""
    raise NotImplementedError("PBP data not yet available: SFLD%")


def calc_sfld(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The total number of shooting fouls drawn."""
    raise NotImplementedError("PBP data not yet available: SFLD")


def calc_sfld_100(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The number of shooting fouls drawn per 100 possessions."""
    raise NotImplementedError("PBP data not yet available: SFLD/100")


def calc_sfld_40(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The number of shooting fouls drawn per 40 minutes."""
    raise NotImplementedError("PBP data not yet available: SFLD/40")


def calc_sfld_g(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The number of shooting fouls drawn per game."""
    raise NotImplementedError("PBP data not yet available: SFLD/G")


def calc_sfl_100(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The total number of shooting fouls committed per 100 possessions."""
    raise NotImplementedError("PBP data not yet available: SFL/100")


def calc_sfl_40(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The total number of shooting fouls committed per 40 minutes."""
    raise NotImplementedError("PBP data not yet available: SFL/40")


def calc_sfl_game(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The total number of shooting fouls committed per game."""
    raise NotImplementedError("PBP data not yet available: SFL/Game")


def calc_sfl(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The percentage of possessions where a shooting foul was committed."""
    raise NotImplementedError("PBP data not yet available: SFL%")


def calc_sht2_fg(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Field goal percentage on 4-10 foot 2-pointers."""
    raise NotImplementedError("PBP data not yet available: SHT2 FG%")


def calc_sht2_fga(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Field goal attempts on 4-10 foot 2-pointers."""
    raise NotImplementedError("PBP data not yet available: SHT2 FGA")


def calc_sht2_fga_100(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Field goal attempts on 4-10 foot 2-pointers per 100 possessions played."""
    raise NotImplementedError("PBP data not yet available: SHT2 FGA/100")


def calc_sht2_fga_40(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Field goal attempts on 4-10 foot 2-pointers per 40 minutes played."""
    raise NotImplementedError("PBP data not yet available: SHT2 FGA/40")


def calc_sht2_fga_g(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Field goal attempts on 4-10 foot 2-pointers per game."""
    raise NotImplementedError("PBP data not yet available: SHT2 FGA/G")


def calc_sht2_fga(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Percentage of shots taken as 4-10 foot 2-pointers."""
    raise NotImplementedError("PBP data not yet available: SHT2 FGA%")


def calc_sht2_fgm(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Field goals made on 4-10 foot 2-pointers."""
    raise NotImplementedError("PBP data not yet available: SHT2 FGM")


def calc_sht3_fg(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Field goal percentage on under 25-foot 3-pointers."""
    raise NotImplementedError("PBP data not yet available: SHT3 FG%")


def calc_sht3_fga(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Field goal attempts on under 25-foot 3-pointers."""
    raise NotImplementedError("PBP data not yet available: SHT3 FGA")


def calc_sht3_fga_100(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Field goal attempts on under 25-foot 3-pointers per 100 possessions played."""
    raise NotImplementedError("PBP data not yet available: SHT3 FGA/100")


def calc_sht3_fga_40(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Field goal attempts on under 25-foot 3-pointers per 40 minutes played."""
    raise NotImplementedError("PBP data not yet available: SHT3 FGA/40")


def calc_sht3_fga_g(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Field goal attempts on under 25-foot 3-pointers per game."""
    raise NotImplementedError("PBP data not yet available: SHT3 FGA/G")


def calc_sht3_fga(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Percentage of shots taken as under 25-foot 3-pointers."""
    raise NotImplementedError("PBP data not yet available: SHT3 FGA%")


def calc_sht3_fgm(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Field goals made on under 25-foot 3-pointers."""
    raise NotImplementedError("PBP data not yet available: SHT3 FGM")


def calc_slp2_fg(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Field goal percentage on short left paint 2-pointers."""
    raise NotImplementedError("PBP data not yet available: SLP2 FG%")


def calc_slp2_fga(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Field goal attempts on short left paint 2-pointers."""
    raise NotImplementedError("PBP data not yet available: SLP2 FGA")


def calc_slp2_fga_100(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Field goal attempts on short left paint 2-pointers per 100 possessions played."""
    raise NotImplementedError("PBP data not yet available: SLP2 FGA/100")


def calc_slp2_fga_40(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Field goal attempts on short left paint 2-pointers per 40 minutes played."""
    raise NotImplementedError("PBP data not yet available: SLP2 FGA/40")


def calc_slp2_fga_g(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Field goal attempts on short left paint 2-pointers per game."""
    raise NotImplementedError("PBP data not yet available: SLP2 FGA/G")


def calc_slp2_fga(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Percentage of shots taken as short left paint 2-pointers."""
    raise NotImplementedError("PBP data not yet available: SLP2 FGA%")


def calc_slp2_fgm(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Field goals made on short left paint 2-pointers."""
    raise NotImplementedError("PBP data not yet available: SLP2 FGM")


def calc_srp2_fg(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Field goal percentage on short right paint 2-pointers."""
    raise NotImplementedError("PBP data not yet available: SRP2 FG%")


def calc_srp2_fga(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Field goal attempts on short right paint 2-pointers."""
    raise NotImplementedError("PBP data not yet available: SRP2 FGA")


def calc_srp2_fga_100(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Field goal attempts on short right paint 2-pointers per 100 possessions played."""
    raise NotImplementedError("PBP data not yet available: SRP2 FGA/100")


def calc_srp2_fga_40(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Field goal attempts on short right paint 2-pointers per 40 minutes played."""
    raise NotImplementedError("PBP data not yet available: SRP2 FGA/40")


def calc_srp2_fga_g(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Field goal attempts on short right paint 2-pointers per game."""
    raise NotImplementedError("PBP data not yet available: SRP2 FGA/G")


def calc_srp2_fga(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Percentage of shots taken as short right paint 2-pointers."""
    raise NotImplementedError("PBP data not yet available: SRP2 FGA%")


def calc_srp2_fgm(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Field goals made on short right paint 2-pointers."""
    raise NotImplementedError("PBP data not yet available: SRP2 FGM")


def calc_shot_att(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The number of field goal attempts plus shooting fouls drawn on missied shots. Effectively, the number of shot attempts by the player."""
    raise NotImplementedError("PBP data not yet available: SHOT ATT")


def calc_tov_shot_clock(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The total number of turnovers tagged by the scorer as a shot clock violation by the team."""
    raise NotImplementedError("PBP data not yet available: TOV SHOT CLOCK")


def calc_stl3(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The total number of steals by the player beyond the opposing team's 3P line (i.e. in 3P shooting range)."""
    raise NotImplementedError("PBP data not yet available: STL3")


def calc_stl3_100(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The number of steals by the player beyond the opposing team's 3P line (i.e. in 3P shooting range), per 100 possessions played."""
    raise NotImplementedError("PBP data not yet available: STL3/100")


def calc_stl3_40(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The number of steals by the player beyond the opposing team's 3P line (i.e. in 3P shooting range), per 40 minutes played."""
    raise NotImplementedError("PBP data not yet available: STL3/40")


def calc_stl3_g(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The number of steals by the player beyond the opposing team's 3P line (i.e. in 3P shooting range), per game."""
    raise NotImplementedError("PBP data not yet available: STL3/G")


def calc_stl2(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The total number of steals by the player inside the opposing team's 3P line (i.e. in 2P shooting range)."""
    raise NotImplementedError("PBP data not yet available: STL2")


def calc_stl2_100(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The number of steals by the player inside the opposing team's 3P line (i.e. in 2P shooting range), per 100 possessions played."""
    raise NotImplementedError("PBP data not yet available: STL2/100")


def calc_stl2_40(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The number of steals by the player inside the opposing team's 3P line (i.e. in 2P shooting range), per 40 minutes played."""
    raise NotImplementedError("PBP data not yet available: STL2/40")


def calc_stl2_g(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The number of steals by the player inside the opposing team's 3P line (i.e. in 2P shooting range), per game."""
    raise NotImplementedError("PBP data not yet available: STL2/G")


def calc_bc_poss_chlg_pass(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Total number of successful coach challenges on backcourt violations or whether team control was established before a foul or violation (women's basketball only)."""
    raise NotImplementedError("PBP data not yet available: BC/Poss CHLG Pass")


def calc_chlg_pass(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Total number of successful coach challenges."""
    raise NotImplementedError("PBP data not yet available: CHLG Pass")


def calc_foul_chlg_pass(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Total number of successful coach challenges on foul-related plays. Men: restricted-area block/charge positioning. Women: correct player charged with the foul."""
    raise NotImplementedError("PBP data not yet available: Foul CHLG Pass")


def calc_goi_chlg_pass(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Total number of successful coach challenges on goaltending or basket interference calls, whether the ball was illegally touched on or above the rim (men's basketball only)."""
    raise NotImplementedError("PBP data not yet available: GOI CHLG Pass")


def calc_oob_chlg_pass(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Total number of successful coach challenges on out-of-bounds calls (which team last touched the ball before it went out)."""
    raise NotImplementedError("PBP data not yet available: OOB CHLG Pass")


def calc_2pa_sum_of_dist(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Sum of shot distances on all 2-point field goal attemps."""
    raise NotImplementedError("PBP data not yet available: 2PA Sum of Dist")


def calc_3pa_sum_of_dist(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Sum of shot distances on all 3-point field goal attemps."""
    raise NotImplementedError("PBP data not yet available: 3PA Sum of Dist")


def calc_atb_sum_of_dist(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Sum of shot distances for all above the break 3s attempted."""
    raise NotImplementedError("PBP data not yet available: ATB Sum of Dist")


def calc_fga_sum_of_dist(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Sum of shot distances on all field goal attemps."""
    raise NotImplementedError("PBP data not yet available: FGA Sum of Dist")


def calc_tok3_fg(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Field goal percentage on top of key 3-pointers."""
    raise NotImplementedError("PBP data not yet available: TOK3 FG%")


def calc_tok3_fga(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Field goal attempts on top of key 3-pointers."""
    raise NotImplementedError("PBP data not yet available: TOK3 FGA")


def calc_tok3_fga_100(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Field goal attempts on top of key 3-pointers per 100 possessions played."""
    raise NotImplementedError("PBP data not yet available: TOK3 FGA/100")


def calc_tok3_fga_40(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Field goal attempts on top of key 3-pointers per 40 minutes played."""
    raise NotImplementedError("PBP data not yet available: TOK3 FGA/40")


def calc_tok3_fga_g(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Field goal attempts on top of key 3-pointers per game."""
    raise NotImplementedError("PBP data not yet available: TOK3 FGA/G")


def calc_tok3_fga(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Percentage of shots taken as top of key 3-pointers."""
    raise NotImplementedError("PBP data not yet available: TOK3 FGA%")


def calc_tok3_fgm(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Field goals made on top of key 3-pointers."""
    raise NotImplementedError("PBP data not yet available: TOK3 FGM")


def calc_tr_chnc(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The total number of chances in the context of transition offense."""
    raise NotImplementedError("PBP data not yet available: TR CHNC")


def calc_tr_ppc(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """For transition offense, the total number of points scored divided by the total number of transition chances."""
    raise NotImplementedError("PBP data not yet available: TR PPC")


def calc_tov_travel(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The total number of turnovers tagged by the scorer as a traveling violation by the team."""
    raise NotImplementedError("PBP data not yet available: TOV TRAVEL")


def calc_ttspct(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """No description available"""
    raise NotImplementedError("PBP data not yet available: ttsPct")


def calc_2pmu(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The total number of unassisted 2-point field goals made by the player."""
    raise NotImplementedError("PBP data not yet available: 2PMu")


def calc_u2pm_100(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The number of unassisted 2-point field goals made by the player, per 100 possessions played."""
    raise NotImplementedError("PBP data not yet available: u2PM/100")


def calc_u2pm_40(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The number of unassisted 2-point field goals made by the player, per 40 minutes played."""
    raise NotImplementedError("PBP data not yet available: u2PM/40")


def calc_u2pm_g(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The number of unassisted 2-point field goals made by the player, per game."""
    raise NotImplementedError("PBP data not yet available: u2PM/G")


def calc_u3pm(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The total number of unassisted 3-point field goals made by the player."""
    raise NotImplementedError("PBP data not yet available: u3PM")


def calc_u3pm_100(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The number of unassisted 3-point field goals made by the player, per 100 possessions played."""
    raise NotImplementedError("PBP data not yet available: u3PM/100")


def calc_u3pm_40(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The number of unassisted 3-point field goals made by the player, per 40 minutes played."""
    raise NotImplementedError("PBP data not yet available: u3PM/40")


def calc_u3pm_g(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The number of unassisted 3-point field goals made by the player, per game."""
    raise NotImplementedError("PBP data not yet available: u3PM/G")


def calc_dunk_ufgm(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The total number of unassisted dunks made by the player."""
    raise NotImplementedError("PBP data not yet available: DUNK uFGM")


def calc_dunk_ufgm_100(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The number of unassisted dunks made by the player, per 100 possessions played."""
    raise NotImplementedError("PBP data not yet available: DUNK uFGM/100")


def calc_dunk_ufgm_40(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The number of unassisted dunks made by the player, per 40 minutes played."""
    raise NotImplementedError("PBP data not yet available: DUNK uFGM/40")


def calc_dunk_ufgm_g(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The number of unassisted dunks made by the player, per game."""
    raise NotImplementedError("PBP data not yet available: DUNK uFGM/G")


def calc_ufgm(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The total number of unassisted field goals made by the player."""
    raise NotImplementedError("PBP data not yet available: uFGM")


def calc_ufgm_100(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The number of unassisted field goals made by the player, per 100 possessions played."""
    raise NotImplementedError("PBP data not yet available: uFGM/100")


def calc_ufgm_40(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The number of unassisted field goals made by the player, per 40 minutes played."""
    raise NotImplementedError("PBP data not yet available: uFGM/40")


def calc_ufgm_g(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The number of unassisted field goals made by the player, per game."""
    raise NotImplementedError("PBP data not yet available: uFGM/G")


def calc_upts(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The total number of unassisted points scored by the player. Includes all points from free throws, as well as points on unassisted 2-point and 3-point shots made."""
    raise NotImplementedError("PBP data not yet available: uPTS")


def calc_upts_100(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The number of unassisted points scored by the player, per 100 possessions played. Includes all points from free throws, as well as points on unassisted 2-point and 3-point shots made."""
    raise NotImplementedError("PBP data not yet available: uPTS/100")


def calc_upts_40(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The number of unassisted points scored by the player, per 40 minutes played. Includes all points from free throws, as well as points on unassisted 2-point and 3-point shots made."""
    raise NotImplementedError("PBP data not yet available: uPTS/40")


def calc_upts_g(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The number of unassisted points scored by the player, per game. Includes all points from free throws, as well as points on unassisted 2-point and 3-point shots made."""
    raise NotImplementedError("PBP data not yet available: uPTS/G")


def calc_atr2_ufgm(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The total number of unassisted shots at the rim made by the player."""
    raise NotImplementedError("PBP data not yet available: ATR2 uFGM")


def calc_atr2_ufgm_100(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The number of unassisted shots at the rim made by the player, per 100 possessions played."""
    raise NotImplementedError("PBP data not yet available: ATR2 uFGM/100")


def calc_atr2_ufgm_40(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The number of unassisted shots at the rim made by the player, per 40 minutes played."""
    raise NotImplementedError("PBP data not yet available: ATR2 uFGM/40")


def calc_atr2_ufgm_g(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """The number of unassisted shots at the rim made by the player, per game."""
    raise NotImplementedError("PBP data not yet available: ATR2 uFGM/G")


