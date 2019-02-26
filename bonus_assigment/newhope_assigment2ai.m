close all
clc

peek = []
inexes = []
subplot(3,1,1);
steps = 10:5:1000;
for i = steps
    Fs = 1000;
    T = 1/Fs;
    L = Fs;
    t = (0:L-1)*T;
    what = 1:150;
    S = cos(2*pi*50*t);
    N = randn(size(t));
    X = S + N;
    Y = fft(X);
    %f = Fs*(0:(L/2))/L;
    f = i*(0:(i/2))/i;
    %P2 = abs(Y/L);
    P2 = abs(Y/i);
    %P1 = P2(1:L/2+1);
    P1 = P2(1:floor(i/2)+1);
    %peek = [peek max(P1)];
    [a,b] = max(P1);
    peek = [peek a];
    inexes = [inexes b];
    plot(f, P1 );
    hold on;
end
title("Sum of signals")
xlabel("F(Hz)")
ylabel("P1(f)")

subplot(3,2,3)
plot(steps, peek)
title("Max amplitude |P1(f)|")
xlabel("Fs(Hz)")
ylabel("|P1(f)|")

subplot(3,2,4)
plot(steps, inexes)
title("Center frequensy based on sample frequensy")
xlabel("F(Hz)")
ylabel("Fs(Hz)")


% AssigmentB
count = 5
N = randn(size(t));
for i = [97 104]
    Fs = 1000;
    T = 1/Fs;
    L = Fs;
    t = (0:L-1)*T;
    what = 1:150;
    S = sin(2*pi*50*t);
    X = S + N;
    Y = fft(X);
    %f = Fs*(0:(L/2))/L;
    f = i*(0:(i/2))/i;
    %P2 = abs(Y/L);
    P2 = abs(Y/i);
    %P1 = P2(1:L/2+1);
    P1 = P2(1:floor(i/2)+1);
    subplot(3,2,count)
    plot(f, P1 );
    ylim([0 5])
    xlim([0 60])
    xlabel("f(Hz)")
    ylabel("P1(f)")
    if count == 5
        title("Sampling frequensy 99")
    else
        title("Samplinf freuensy 104")
    end
    count = count  + 1
end




