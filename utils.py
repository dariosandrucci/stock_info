#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
Description: utils.py
    File that contains some useful functions to the well-functioning of main.py
License_info: Licensed to Portfolio Management Club Nova SBE; Daniel Gonçalves
'''
# --------------------------------------------------------------------------- #
#                                  Imports                                    #
# --------------------------------------------------------------------------- #
import yfinance as yf
import requests as rq
import pandas as pd
import numpy as np
from scipy.stats import norm
from datetime import datetime as dt
# --------------------------------------------------------------------------- #
#                             Portfolio Metrics                               #
# --------------------------------------------------------------------------- #
# Inspired on QuantStats - Simply Vectorized the functions!
def volatility(df_to_calc_risk_metrics: pd.DataFrame):
    return df_to_calc_risk_metrics["Close"].std() * np.sqrt(252)

def sharpe(df_to_calc_risk_metrics: pd.DataFrame, min_periods=1):
    return (df_to_calc_risk_metrics["Close"].mean() * 252)/(df_to_calc_risk_metrics["Close"].std() * np.sqrt(252))

def skew(df_to_calc_risk_metrics: pd.DataFrame, min_periods=1):
    return df_to_calc_risk_metrics["Close"].skew()

def kurtosis(df_to_calc_risk_metrics: pd.DataFrame, min_periods=1):
    return df_to_calc_risk_metrics["Close"].kurt()

def expected_return(df_to_calc_risk_metrics: pd.DataFrame, min_periods=1):
    return df_to_calc_risk_metrics["Close"].mean() * 252
    
#def sortino_ratio(df_to_calc_risk_metrics: pd.DataFrame, min_periods=1):
#    downside_df = (df_to_calc_risk_metrics["Close"].mask(df_to_calc_risk_metrics["Close"]>0,0) ** 2).sum()
#    downside = downside_df.divide(np.arange(1,len(downside_df)+1),axis=0)
#    res = df_to_calc_risk_metrics["Close"].mean() / downside
#    return res

def var(df_to_calc_risk_metrics: pd.DataFrame, min_periods=1):
    mu = df_to_calc_risk_metrics.expanding(min_periods=min_periods).mean()
    std = df_to_calc_risk_metrics.expanding(min_periods=min_periods).std()
    with np.errstate(invalid='ignore'):
        return pd.DataFrame(norm.ppf(0.05, mu, std), index=mu.index, columns=mu.columns)

def cvar(df_to_calc_risk_metrics: pd.DataFrame, min_periods=1):
    var_df = var(df_to_calc_risk_metrics,min_periods)
    cvar_result = pd.DataFrame()
    for df, var_ in zip(df_to_calc_risk_metrics.expanding(), var_df.expanding()):
        df : pd.DataFrame() = df
        cvar_value = df.mask(df >= var_,np.nan).mean().to_frame().T
        cvar_value.index = [df.index[-1]]
        cvar_result=pd.concat([cvar_result,cvar_value],axis=0)
    return cvar_result

def win_rate(df_to_calc_risk_metrics: pd.DataFrame, min_periods=1):
    return (df_to_calc_risk_metrics["Close"] > 0).mean()

def tail_ratio(df_to_calc_risk_metrics: pd.DataFrame, cutoff=0.95, min_periods=1):
    """
    Measures the ratio between the right
    (95%) and left tail (5%).
    """
    return abs(df_to_calc_risk_metrics["Close"].quantile(cutoff) / df_to_calc_risk_metrics["Close"].quantile(1-cutoff))

def kelly_criterion(df_to_calc_risk_metrics: pd.DataFrame):
    win_prob = win_rate(df_to_calc_risk_metrics["Close"])
    avg_win = df_to_calc_risk_metrics["Close"].mask(df_to_calc_risk_metrics["Close"] <= 0,np.nan).mean()
    avg_loss = df_to_calc_risk_metrics["Close"].mask(df_to_calc_risk_metrics["Close"] >= 0,np.nan).mean()
    win_loss_ratio = avg_win/avg_loss
    lose_prob = 1 - win_prob
    return ((win_loss_ratio * win_prob) - lose_prob) / win_loss_ratio

def period_finder(current_date : dt, months_to_reverse = 3):
    cm = current_date.month
    nm =  cm - months_to_reverse
    if nm >= 1:
        return dt(current_date.year, nm, current_date.day)

    elif nm + 12 >= 1:
        return dt(current_date.year - 1, nm + 12 , current_date.day)

    elif nm + 24 >= 1:
        return dt(current_date.year - 1, nm + 24 , current_date.day)

    else:
        print("Operations this far are not possible.")
