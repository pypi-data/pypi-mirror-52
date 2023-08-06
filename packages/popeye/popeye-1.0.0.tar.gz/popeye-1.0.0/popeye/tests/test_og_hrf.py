import os
import sharedmem
import ctypes

import numpy as np
import numpy.testing as npt
import nose.tools as nt
from scipy.signal import fftconvolve

import popeye.utilities as utils
import popeye.og_hrf as og
from popeye.visual_stimulus import VisualStimulus, simulate_bar_stimulus, resample_stimulus
from popeye.spinach import generate_og_receptive_field

def test_og_fit():
    
    # stimulus features
    viewing_distance = 38
    screen_width = 25
    thetas = np.arange(0,360,90)
    thetas = np.insert(thetas,0,-1)
    thetas = np.append(thetas,-1)
    num_blank_steps = 30
    num_bar_steps = 30
    ecc = 12
    tr_length = 1.0
    frames_per_tr = 1.0
    scale_factor = 1.0
    pixels_across = 100
    pixels_down = 100
    dtype = ctypes.c_int16
    
    # create the sweeping bar stimulus in memory
    bar = simulate_bar_stimulus(pixels_across, pixels_down, viewing_distance, 
                                screen_width, thetas, num_bar_steps, num_blank_steps, ecc)
                                
    # create an instance of the Stimulus class
    stimulus = VisualStimulus(bar, viewing_distance, screen_width, scale_factor, tr_length, dtype)
    
    # initialize the gaussian model
    model = og.GaussianModel(stimulus, utils.spm_hrf)
    model.hrf_delay = 0
    model.mask_size = 5
    
    # generate a random pRF estimate
    x = -5.24
    y = 2.58
    sigma = 1.24
    hrf_delay = 0.66
    beta = 2.5
    baseline = -0.25
    
    # create the "data"
    data = model.generate_prediction(x, y, sigma, hrf_delay, beta, baseline)
    
    # set search grid
    x_grid = (-10,10)
    y_grid = (-10,10)
    s_grid = (0.25,5.25)
    h_grid = (-1.0,1.0)
    
    # set search bounds
    x_bound = (-12.0,12.0)
    y_bound = (-12.0,12.0)
    s_bound = (0.001,12.0)
    h_bound = (-1.5,1.5)
    b_bound = (1e-8,None)
    m_bound = (None,None)
    
    # loop over each voxel and set up a GaussianFit object
    grids = (x_grid, y_grid, s_grid, h_grid,)
    bounds = (x_bound, y_bound, s_bound, h_bound, b_bound, m_bound)
    
    # fit the response
    fit = og.GaussianFit(model, data, grids, bounds, Ns=5)
    
    # coarse fit
    npt.assert_almost_equal(fit.x0, -5.0)
    npt.assert_almost_equal(fit.y0, 5.0)
    npt.assert_almost_equal(fit.s0, 2.75)
    npt.assert_almost_equal(fit.hrf0, 0.5)
    # the baseline/beta should be 0/1 when regressed data vs. estimate
    (m,b) = np.polyfit(fit.scaled_ballpark_prediction, data, 1)
    npt.assert_almost_equal(m, 1.0)
    npt.assert_almost_equal(b, 0.0)

    # assert equivalence
    npt.assert_almost_equal(fit.x, x)
    npt.assert_almost_equal(fit.y, y)
    npt.assert_almost_equal(fit.hrf_delay, hrf_delay)
    npt.assert_almost_equal(fit.sigma, sigma)
    npt.assert_almost_equal(fit.beta, beta)
    
    # test receptive field
    rf = generate_og_receptive_field(x, y, sigma, fit.model.stimulus.deg_x, fit.model.stimulus.deg_y)
    rf /= (2 * np.pi * sigma**2) * 1/np.diff(model.stimulus.deg_x[0,0:2])**2
    npt.assert_almost_equal(np.round(rf.sum()), np.round(fit.receptive_field.sum())) 
    
    # test model == fit RF
    npt.assert_almost_equal(np.round(fit.model.generate_receptive_field(x,y,sigma).sum()), np.round(fit.receptive_field.sum()))

# def test_og_nuisance_fit():
#     
#     # stimulus features
#     viewing_distance = 38
#     screen_width = 25
#     thetas = np.arange(0,360,90)
#     thetas = np.insert(thetas,0,-1)
#     thetas = np.append(thetas,-1)
#     num_blank_steps = 30
#     num_bar_steps = 30
#     ecc = 12
#     tr_length = 1.0
#     frames_per_tr = 1.0
#     scale_factor = 1.0
#     pixels_across = 200
#     pixels_down = 200
#     dtype = ctypes.c_int16
#     
#     # create the sweeping bar stimulus in memory
#     bar = simulate_bar_stimulus(pixels_across, pixels_down, viewing_distance, 
#                                 screen_width, thetas, num_bar_steps, num_blank_steps, ecc)
#                                 
#     # create an instance of the Stimulus class
#     stimulus = VisualStimulus(bar, viewing_distance, screen_width, scale_factor, tr_length, dtype)
#     
#     # initialize the gaussian model
#     model = og.GaussianModel(stimulus, utils.double_gamma_hrf)
#     model.hrf_delay = 0
#     
#     # generate a random pRF estimate
#     x = -5.24
#     y = 2.58
#     sigma = 0.98
#     beta = 2.5
#     baseline = 0.0
#     
#     # create the "data"
#     data = model.generate_prediction(x, y, sigma, beta, baseline)
#     
#     # create nuisance signal
#     step = np.zeros(len(data))
#     step[30:-30] = 1
#     
#     # add to data
#     data += step
#     
#     # create design matrix
#     nuisance = sm.add_constant(step)
#     
#     # recreate model with nuisance
#     model = og.GaussianModel(stimulus, utils.double_gamma_hrf, nuisance)
#     model.hrf_delay = 0
#     
#     # set search grid
#     x_grid = (-7,7)
#     y_grid = (-7,7)
#     s_grid = (0.25,3.25)
#     
#     # set search bounds
#     x_bound = (-10.0,10.0)
#     y_bound = (-10.0,10.0)
#     s_bound = (0.001,10.0)
#     b_bound = (1e-8,None)
#     m_bound = (None, None)
#     
#     # loop over each voxel and set up a GaussianFit object
#     grids = (x_grid, y_grid, s_grid,)
#     bounds = (x_bound, y_bound, s_bound, b_bound, m_bound)
#     
#     # fit the response
#     fit = og.GaussianFit(model, data, grids, bounds, Ns=3)
#     
#     # assert equivalence
#     nt.assert_almost_equal(fit.x, x, 1)
#     nt.assert_almost_equal(fit.y, y, 1)
#     nt.assert_almost_equal(fit.sigma, sigma, 1)
#     nt.assert_almost_equal(fit.beta, beta, 1)
    
