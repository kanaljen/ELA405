clear;

pas_freq = 55;
stop_freq = 60;
filter_order = [10 50 100];
plots = []
for i = filter_order
    lpFilt = designfilt('lowpassfir','FilterOrder',i,'PassbandFrequency',pas_freq, 'StopbandFrequency',stop_freq, 'SampleRate', 200)
    %plots = [plots freqz(lpFilt)];
    freqz(lpFilt)
end


pas_freq = 55;
filter_order = [2 5 8];
for i = filter_order
    lpFilt = designfilt('lowpassiir','FilterOrder',i,'PassbandFrequency',pas_freq, 'SampleRate', 200)
    %plots = [plots freqz(lpFilt)];
    freqz(lpFilt)
end

