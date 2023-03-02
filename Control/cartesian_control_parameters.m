%
%
%               KUKA  RSI
%
%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


%% initialise
clear all;
close all;
clc;
format long


%% parameters
% k_p = 5;
% k_i = 5;
% k_d = 0;
% a_max = 0.2  % m s ^-2
a_max = 0.6e3  % mm s ^-2
a_min = -a_max % mm s ^-2
% v_max = 0.2 % m s ^-1
v_max = 0.25e3 % mm s ^-1
v_min = -v_max % m s^-1
% step_value = 0.400e3 % m
sin_freq = 0.05 % Hz
sin_omega =  sin_freq * 2 * pi 

% k_nenner = [1 3] ;   % koprime Faktorisierung
% k_zaehler = [3 1];   % koprime Faktorisierung


% v_factor = 4
% vorfilter = tf([1, 1], [3, 1])
% GK = 1/()

% tf1 = tf([1], [1, 2, 1])
% tf2 = tf([1, 1], [0.5, 1]) * tf([1, 1], [0.5, 1])
% tf3 = tf([1, 1], [0.1, 1]) * tf([1, 1], [0.1, 1])
% bode(tf2 * tf1)
% hold on
% bode(tf1)
% bode(tf3 * tf1)
% grid on

