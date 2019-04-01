clear;
close all;
clc;
peek1 = []
peek2 = []
inexes1 = []
inexes2 = []
subplot(2,1,1);
steps = -pi:pi/24:pi;
Fs = 1000;
i = Fs;
T = 1/Fs;
L = Fs;
t = (0:L-1)*T;
for theta = steps
    S1 = sin(2*pi*50*t + 0);
    S2 = sin(2*pi*50*t + theta);
    N1 = randn(size(t));
    N2 = randn(size(t));
    X1 = S1 + N1;
    X2 = S2 + N1;

    Y = fft(X1 + X2);
    f = i*(0:(i/2))/i;
    P2 = abs(Y/i);
    P1 = 2*P2(1:floor(i/2)+1);
    [a1,b1] = max(P1);
    peek1 = [peek1 a1];
    inexes1 = [inexes1 b1];
    plot(f, P1 );
    hold on;
end
title("Sum of signals")
xlabel("F(Hz)")
ylabel("P1(f)")
xlim([50-2 50+2])

subplot(2,1,2)
plot(steps, peek1)
title("ampliteude of theta |P1(f)|")
xlabel("theta")
xticks([-pi:pi/2:pi])
ylabel("|P1(f)|")

