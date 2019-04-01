close all
% Assigment 1b
% Generate a signal 1 second long with 1000 sampling frequency
% Generate noise
% Plot signal, noise, and their sum (a noisy signal)
% plot their fourier transforms

%Fs = 1000;             % Sampling frequency
Fs = 150*1;             % Sampling frequency
T = 1/Fs;             % Sampling period
L = Fs;               % Length of signal (Always one second long)
%L = 1000;               % Length of signal (Always one second long)
t = (0:L-1)*T;        % Time vector
stemp = 1:150;

w0 = 50;      % Hz

%k = (1-0)/(0-150);
f = @(t) -1*t + 1;

%Form a signal containing a 49 to 50 Hz sinusoid of amplitude 1.
S =  cos(2*pi.*t.*(2.*t + 49));

%Noise
N = randn(size(t));
%Noisy Signal
X = S + N;

%FIG 1 PURE SIGNAL
figure(1), subplot(2,1,1)
plot(1000*t,S, '-*')
title('Pure Signal')
xlabel('t (milliseconds)')
ylabel('X(t)')
ylim([-2 2])



%FIG 4 PURE SIGNAL FFT
Y = fft(S);
f = Fs*(0:(L/2))/L;
P2 = abs(Y/L);
P1 = P2(1:L/2+1);
P1(2:end-1) = 2*P1(2:end-1);
subplot(2,1,2)
plot(f, P1)
title('fft(Pure Signal)') %Single-Sided Amplitude Spectrum of S(t)
xlabel('f (Hz)')
ylabel('|P1(f)|')
ylim([0, 1])



function x = mytestplot()
    figure(1), subplot(1,2,1)
    plot(1000*t(stemp),f(stemp), '-*')
    figure(1), subplot(1,2,2)
    plot(1000*t(stemp),fS(stemp), '-*')
end
