#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 29 19:48:05 2018

@author: andrew
"""

import numpy as np
from scipy.optimize import curve_fit
from scipy.special import iv
from astropy.io import fits
import glob
import sys
from scipy.stats import chisquare
from scipy.stats import skellam as skell
from astropy.stats import sigma_clip
import initialize
from astropy.stats import biweight_midcorrelation
from filters import stamp

def corr(image, N=100, dim=0, opt=True):
    name = image.split('/')[-1]
    location = image.replace('/data/' + name,'')
    residual = location + '/' + 'residuals/' + name[:-5] + 'residual_.fits'
    mask = fits.getdata(residual, 1)
    if opt == True:
        residual = "%s/temp/conv.fits" % (location)
    data = fits.getdata(residual)
    try: weight_check = fits.getval(residual, 'WEIGHT')
    except: weight_check = 'N'
    if weight_check == 'Y':
        mask = (mask-1)*-1
    center = (int((data.shape[0])/2), int((data.shape[1])/2))
    if dim == 0:
        stamp1 = data[center[0]:center[0]+N, center[1]]
        stamp2 = data[center[0]:center[0]+N, center[1]+1]
        mask1 = mask[center[0]:center[0]+N, center[1]]
        mask2 = mask[center[0]:center[0]+N, center[1]+1]
    elif dim == 1:
        stamp1 = data[center[0], center[1]:center[1]+N]
        stamp2 = data[center[0]+1, center[1]:center[1]+N]
        mask1 = data[center[0], center[1]:center[1]+N]
        mask2 = data[center[0]+1, center[1]:center[1]+N]
    else:
        print("-> Error: Dimension number dim exceeds the 2D image\n-> Exiting...")
        sys.exit()
    if ((mask1==1).sum()) + ((mask2==1).sum()) > round(N*0.1):
        return 0
    else:
        return biweight_midcorrelation(stamp1, stamp2)

def get_res_data(image, numStamps=5, split=4, stampSize=(300,300), clipped_sigma=3, 
                 sim_x=0, sim_y=0, sim_size=30, sim=False, opt=True, real=True,
                 real_X=[], real_Y=[], real_stamp_size=25, X2_default=np.nan):
    name = image.split('/')[-1]
    location = image.replace('/data/' + name,'')
    residual = location + '/' + 'residuals/' + name[:-5] + 'residual_.fits'
    template = glob.glob(location + '/templates/*.fits')
    try: weight_check = fits.getval(residual, 'WEIGHT')
    except: weight_check = 'N'
    if opt == True:
        res = '%s/temp/conv.fits' % (location)
        try: X2norm = np.max(((float(fits.getval(res, 'FSIG00')), float(fits.getval(res, 'SSSIG00')), float(fits.getval(res, 'X2NRM00')))))
        except: X2norm = X2_default
        if real == True:
            res_data = np.ma.MaskedArray((fits.getdata(res))*-1, mask=np.zeros((fits.getdata(res)).shape))
        else:
            if weight_check == 'N':
                res_data = np.ma.masked_array((fits.getdata(res))*-1, mask=fits.getdata(residual, 1))
            else:
                res_data = np.ma.masked_array((fits.getdata(res))*-1, mask=((fits.getdata(residual, 1)-1)*-1))
    else:
        try: X2norm = np.max(((float(fits.getval(residual, 'FSIG00')), float(fits.getval(residual, 'SSSIG00')), float(fits.getval(residual, 'X2NRM00')))))
        except: X2norm = X2_default
        if real == True:
            res_data = np.ma.MaskedArray((fits.getdata(residual))*-1, mask=np.zeros((fits.getdata(residual)).shape))
        else:
            if weight_check == 'N':
                res_data = np.ma.masked_array(fits.getdata(residual), mask=fits.getdata(residual, 1))
            else:
                res_data = np.ma.masked_array(fits.getdata(residual), mask=((fits.getdata(residual, 1)-1)*-1))
    res_data_clipped = sigma_clip(res_data.data, sigma=clipped_sigma)
    res_data_master_mask = np.logical_or(res_data.mask, res_data_clipped.mask)
    res_data = np.ma.MaskedArray(res_data.data, mask=res_data_master_mask)
    if len(template) == 1:
        im_data = fits.getdata(image)
        temp_data = fits.getdata(template[0])
        im_data = (im_data).byteswap().newbyteorder()
        temp_data = (temp_data).byteswap().newbyteorder()
        image_data = np.ma.masked_array(im_data, mask=np.logical_not(fits.getdata(image, 1)))
        template_data = np.ma.masked_array(temp_data, mask=np.logical_not(fits.getdata(template[0], 1)))
        if real == True:
            res_stamps = [stamp(res_data, int(real_Y[i])-1, int(real_X[i])-1, int(real_stamp_size/2), int(real_stamp_size/2)) for i in range(len(real_X))]
            res_stamps.append(res_data)
        else:
            res_stamps = []
            if sim == False:
                res_data = np.array_split(res_data, split, axis=1)
                for r in res_data:
                    resStamp = np.array_split(r, numStamps, axis=0)
                    res_stamps += resStamp
            elif sim == True:
                res_data = stamp(res_data, sim_x, sim_y, sim_size, sim_size)
                res_data = np.array_split(res_data, split, axis=1)
                for r in res_data:
                    resStamp = np.array_split(r, numStamps, axis=0)
                    res_stamps += resStamp
            else:
                print("\n-> Error: 'sim' keyword must be boolean\n-> Exiting...")
                sys.exit()
        if real == True:
            image_median = [np.ma.median(image_data)] * 6
            template_median = [np.ma.median(template_data)] * 6
        else:
            image_stamps = []
            template_stamps = []
            image_data = np.array_split(image_data, split, axis=1)
            template_data = np.array_split(template_data, split, axis=1)
            for i in range(len(image_data)): 
                imageStamps = np.array_split(image_data[i], numStamps, axis=0)
                templateStamps = np.array_split(template_data[i], numStamps, axis=0)
                image_stamps += imageStamps
                template_stamps += templateStamps
            image_median = [np.ma.median(i) for i in image_stamps]
            template_median = [np.ma.median(j) for j in template_stamps]
        del res_data, name, location, residual, template
        return res_stamps, image_median, template_median, X2norm
    elif len(template) > 1:
        print("\n-> Error: Too many template images in 'templates' directory\n")
        sys.exit()
    else:
        print("\n-> Error: Problem with number of template images\n")
        sys.exit()

def get_res_hist(res_data, image_median_list, template_median_list):
    image_median = np.mean(image_median_list)
    template_median = np.mean(template_median_list)
    medianAvg = np.mean([image_median, template_median])
    res_median = np.ma.median(res_data)
    res_median_theoretical = image_median - template_median
    if np.ma.is_masked(np.ma.median(res_data)):
        res_median = 0
    rangeRes = abs((-1*5*medianAvg)+res_median_theoretical) + abs(res_median_theoretical+(5*medianAvg))
    expected_interval = skell.interval(0.99999999, image_median, template_median)
    bns = int(round((rangeRes/400)*2*(len((res_data.data).flatten()))**(1/3))/2)
    return np.histogram(res_data.data, weights=(np.logical_not(res_data.mask)).astype(int), bins=bns, range=expected_interval, density=True), res_median, np.ma.std(res_data), bns

def fit(image, stamp_num=3, stamp_size=(300,300), clipped_sig=3, Qthresh=0.25, 
        corr_thresh=0.50, s_x=0, s_y=0, s_width=30, stdThresh=1000, real_psf=True,
        real_x=[], real_y=[], real_stamp=25, optimize=True, distribution='skellam',
        method='curvefit', simulate=False, corr_check=True, use_config_file=True):
    if use_config_file == True:
        location = image.split('/')[:-2]
        location = '/'.join(location)
        stamp_num = initialize.get_config_value('stamp_num', file_loc=location+'/configs')
        clipped_sig = initialize.get_config_value('clipped_sig', file_loc=location+'/configs')
        Qthresh = initialize.get_config_value('qThresh', file_loc=location+'/configs')
        method = initialize.get_config_value('fit_method', file_loc=location+'/configs')
        corr_thresh = initialize.get_config_value('corr_thresh', file_loc=location+'/configs')
        corr_check = initialize.get_config_value('corr_check', file_loc=location+'/configs')
        stdThresh = initialize.get_config_value('stdThresh', file_loc=location+'/configs')
        real_psf = initialize.get_config_value('real_psf', file_loc=location+'/configs')
        real_stamp = initialize.get_config_value('real_stamp', file_loc=location+'/configs')
    if corr_check == True:
        biweight_corr_0 = corr(image, opt=optimize, dim=0)
        biweight_corr_1 = corr(image, opt=optimize, dim=1)
        biweight_corr = np.max((biweight_corr_0, biweight_corr_1))
        if biweight_corr >= corr_thresh:
            return 0
    res_stamps, image_median, template_median, X2 = get_res_data(image, numStamps=stamp_num, 
                                                             stampSize=stamp_size, 
                                                             clipped_sigma=clipped_sig,
                                                             sim_x=s_x, sim_y=s_y, sim_size=s_width,
                                                             sim=simulate, opt=optimize, real=real_psf,
                                                             real_X=real_x, real_Y=real_y,
                                                             real_stamp_size=real_stamp)
    if method == 'chi2':
        Qs = []
        Qs_norm = []
        qFloor = float(initialize.get_config_value('qFloor'))
        for i in range(len(res_stamps)):
            Qs.append(fit_chi2(res_stamps[i], image_median[0], template_median[0], std_thresh=stdThresh))
        if np.min(Qs) < Qthresh:
            Q = np.min(Qs)
        else:
            Q = np.max(Qs)
        if Q < qFloor:
            for i in range(len(res_stamps)):
                Qs_norm.append(fit_chi2(res_stamps[i], image_median[0], template_median[0], std_thresh=stdThresh, normalize=False))
            if np.min(Qs_norm) < Qthresh:
                Q_norm = np.min(Qs_norm)
            else:
                Q_norm = np.max(Qs_norm)
            if Q_norm > Q:
                Q = Q_norm
        return np.round(Q, decimals=2)
    elif method == 'curvefit':
        Q = fit_curvefit(res_stamps, image_median, template_median, X2, dist=distribution, qThresh=Qthresh, std_thresh=stdThresh)
        return np.round(Q, decimals=2)
    

def fit_chi2(res_data, median1, median2, conf_level=0.995, dx=100, dy=100, std_thresh=1000, normalize=True):
    if np.std(res_data) == 0:
        Q = 0
    elif (res_data.mask==True).all() == True:
        Q = 0
    elif np.std(res_data) >= std_thresh:
        Q = 0
    else:
        if normalize == True:
            res_data = (res_data - (median1 - median2)) / np.sqrt(median1 + median2)
        expected_iter = len(res_data.flatten())
        expected_interval = skell.interval(0.99999999, median1, median2)
        medianAvg = np.mean([median1, median2])
        bns = int((np.log2(expected_iter) + 1))
        expected = skell.rvs(median1, median2, size=(expected_iter))
        if medianAvg >= 0:
            data_hist = np.histogram(res_data.data, weights=(res_data.mask-1)*-1, bins=bns, range=expected_interval, density=False)
            expected_hist = np.histogram(expected, bins=bns, range=expected_interval, density=False)
        elif medianAvg < 0:
            data_hist = np.histogram(res_data.data, weights=(np.logical_not(res_data.mask)).astype(int), bins=bns, range=expected_interval, density=False)
        data_freq = list(data_hist[0])
        expected_freq = list(expected_hist[0])
        data_zeroind = [i for i in range(len(data_freq)) if expected_freq[i] == 0]
        expected_zeroind = [i for i in range(len(expected_freq)) if expected_freq[i] == 0]
        for i in expected_zeroind:
            if i not in data_zeroind:
                data_zeroind.append(i)
        data_freq_new = []
        expected_freq_new = []
        data_hist_new = []
        for ind in range(len(data_freq)):
            if ind not in data_zeroind:
                data_freq_new.append(data_freq[ind])
                expected_freq_new.append(expected_freq[ind])
                data_hist_new.append(data_hist[1][ind])
        del data_freq, expected_freq
        data_hist_new = np.array(data_hist_new, dtype=np.float64)
        chi2_test = chisquare(data_freq_new, f_exp=expected_freq_new)
        Q = 1 / (1 + (chi2_test[0] / (1 * expected_iter)))
        b_mid = 0.5*(data_hist_new[1:]+data_hist_new[:-1])
        b_mid = b_mid.astype(np.float64)
    return Q

def fit_curvefit(res_stamps, median1, median2, X2, dist='skellam', qThresh=0.35, std_thresh=1000):
    Qs = []
    for i in range(len(res_stamps)):
        try:
            hist, dataMean, stdev, bns = get_res_hist(res_stamps[i], median1, median2)
            if stdev >= std_thresh or stdev == 0:
                Q = 0
            else:
                a, b = hist[0], hist[1]
                b_mid = 0.5*(b[1:]+b[:-1])
                b_mid = b_mid.astype(np.float64)
                if dist == 'skellam':
                    params, covars = curve_fit(skellam,b_mid,a,[median1[i], median2[i]], maxfev=2000)
                    residuals = a - skellam(b_mid,*params)
                if dist == 'gauss':
                    params, covars = curve_fit(gauss,b_mid,a, maxfev=2000)
                    residuals = a - gauss(b_mid,*params)
                residuals = residuals[~np.isnan(residuals)]
                residuals = residuals[~np.isinf(residuals)]
                residuals = np.array(residuals)
                ss_res = np.sum(residuals**2)
                ss_tot = np.sum((a-np.mean(a))**2)
                rSquared = (1-(ss_res/ss_tot))
                if X2 != np.nan:
                    Q = rSquared/(1+(abs(X2/4)))
                else:
                    res_fitMean = abs(params[0] - params[1])
                    res_realMean = abs(median1[i] - median2[i])
                    Q = rSquared/(1+abs(res_fitMean-res_realMean))
                if list(residuals) == []:
                    Q = 0
                del params, residuals
        except Exception as e:
                Q = 0
                print(e)
        Qs.append(Q)
    if Qs == []:
        Q = 0
    if np.min(Qs) < qThresh:
        Q_final = np.min(Qs)
    else:
        Q_final = np.mean(Qs)
    del Qs, res_stamps, median1, median2
    try:
        del hist, residuals, dataMean, stdev, a, b, b_mid
    except:
        pass
    return Q_final

def skellam(k,u1,u2):
    return np.exp(-1*(u1+u2))*(u1/u2)**(k/2)*iv(k, 2*np.sqrt(u1*u2))

def gauss(x,mean,sig):
    return (1/np.sqrt((2*np.pi*sig**2)))*np.exp(-1*(x-mean)**2/(2*sig**2))