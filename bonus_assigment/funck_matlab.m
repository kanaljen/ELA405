clear all;
clc
close all;
Fs = 1;
T = 11;
t = 0:Fs:(T*100);
L = length(t);
Noize  = randn(size(t));
S = 2* sin(2*pi*t);
X = S + Noize;

[maxVal,indexMax] = max(abs(fft(X - mean(X))));
disp(maxVal);
disp(indexMax);


freqM1 = (indexMax - 1) * Fs / (L - 1);
freqM2 = (indexMax - 1) * Fs / (L - 0);

numbCyc1 = freqM1 * T;
numbCyc2 = freqM1 * T;

subplot(2,1,1);
plot(t, X);
subplot(2,1,2);
plot(abs(fft(X - mean(X))));
