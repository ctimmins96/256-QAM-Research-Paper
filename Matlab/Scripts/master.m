%% 256-QAM Master File
%|-----------------------------------------------------------------------------------------------------------------------
%|      Author: Chase Timmins
%|  Instructor: Dr. Tofighi
%|      Course: EE 460
%| Create Date: December 10, 2020
%|-----------------------------------------------------------------------------------------------------------------------
%
% Description:
%        The purpose of this script is to act as a master file that references functions 
% used in the generation and detection of 256-QAM. This script will strictly generate a vector of
% pseudo-random data, translate it into 256-QAM symbols, generate the
% corresponding sinusoid, transmit and receive the sinusoid with some
% programmed noise, decode the received sine into the base symbols and
% demonstrate to the user the sent symbols, the received symbols as well as
% the number of errors. This script will be used in a larger script that
% will generate statistics relative to the SNR, BER, and other notable
%

%% Setup Statements
do_clear = 0;                   % Clear Flag: Set to 0 if the user wishes not to clear the variables in the command window during runtime.

if (do_clear == 1)
    clear all;
end
%clc;
close all;

%% Constant Definitions
t_s = 1e-9;                     % 1ns sample time
fs = 1/t_s;                     % 1 GHz sample frequency
fc = 0.1*fs;                    % 100 MHz RF carrier frequency
fc_QAM = 0.001*fs;              % 1 MHz QAM carrier frequency
order = 3;                      % Low Pass Filter order

noise_flag  = 1;                % Noise Flag: If set to 1, the noise power, NP, is set inside this script
random_flag = 0;                % Random Flag: Set to 1 if the user withes to generate a random sequence of inputs
fdev_flag   = 0;                % Fdev Flag:  If set to 1, the Frequency Deviation, fdev, is set inside this script

if (noise_flag == 1)
    NP = 15;                     % Noise Power (dBW)
end

a = mod((0:255),16) - 7.5;      % In-Phase
b = 7.5 - floor((0:255)/16);    % Quadrature
iq = a + b*1j;                  % IQ - Constellation / LUT

L = 16;                         % Length of Symbol Vector (Data)

if (fdev_flag == 1)
    fdev = 1.333e6*3;
end

%% Generate Random Input
in_data = round(255*rand(1,L));

%% Encode Input as 256-QAM
% Translate array to symbols
symb = zeros(size(in_data));
for ii = 1:length(symb)
    symb(ii) = iq(in_data(ii) + 1);
end

% Create Sinusoid from symbols
n = 0:(round(fs/fc_QAM) - 1);
sin_base = sin(2*pi*fc_QAM*n*t_s);

tx_QAM = zeros([1 length(sin_base)*length(symb)]);

tx_len = length(sin_base);

for ii = 1:length(symb)
    tx_QAM((ii-1)*tx_len + 1:ii*tx_len) = symb(ii)*sin_base;
end

%% FM Transmit

tx_r = 10*fmmod(real(tx_QAM),fc,fs,fdev);
tx_i = 10*fmmod(imag(tx_QAM),fc,fs,fdev);

%% Add Noise to the transmission
gauss = wgn(1,length(tx_r),NP);

gauss = gauss - mean(gauss);

rx_r = tx_r + 0.5*gauss;
rx_i = tx_i + 0.5*gauss;

%% FM Recieve

for ii = 1:order
    if (ii == 1)
        a = lowpass(fmdemod(rx_r,fc,fs,fdev)*(7.5/max(fmdemod(rx_r,fc,fs,fdev))),1.1e6,fs);
        b = lowpass(fmdemod(rx_i,fc,fs,fdev)*(7.5/max(fmdemod(rx_i,fc,fs,fdev))),1.1e6,fs);
    else
        a = lowpass(a,1.1e6,fs);
        b = lowpass(b,1.1e6,fs);
    end
end

% Find a constant to minimized the distance between the input and ouput
% waveforms

c_a = ((sum(real(tx_QAM).*a))/(sum(a.*a)));
c_b = ((sum(imag(tx_QAM).*b))/(sum(b.*b)));

% b = b*(max(imag(tx_QAM))/(max(b)));
% a = a*(max(real(tx_QAM))/(max(a)));
b = b*c_b;
a = a*c_a;

rx_QAM = a + b*1i;

t = 0:t_s:t_s*(length(rx_QAM)-1);

figure(1);
plot(t,real(tx_QAM),t,imag(tx_QAM),t,real(rx_QAM),t,imag(rx_QAM));
grid on;
xlabel('Time [s]');
ylabel('Voltage [V]');
ylim([-9 9]);
title('Transmitted and Received QAM Signals');
legend('TX - In Phase','TX - Quadrature','RX - In Phase','RX - Quadrature');

%% QAM-Decode
% Partition each symbol and determine the incoming symbol via nearest
% neighbor approximation (minimized variance)

in_symb = zeros(size(symb));
for ii = 1:length(symb)
    tmp = rx_QAM((ii-1)*tx_len + 1:ii*tx_len);
    mn = 9999;
    for jj = 1:256
        if (var(tmp - iq(jj)*sin_base) < mn)
            mn = var(tmp - iq(jj)*sin_base);
            in_symb(ii) = iq(jj);
        end
    end
end

%% Display Results

% Find total errors in calculation
errors = 0;
for ii = 1:length(symb)
    if (in_symb(ii) ~= symb(ii))
        errors = errors + 1;
    end
end

sent = '0x';
recv = '0x';

for ii = 1:length(symb)
    jj = 0;
    found1 = 0;
    found2 = 0;
    
    while (found1 == 0 || found2 == 0)
        jj = jj + 1;
        if (symb(ii) == iq(jj))
            found1 = 1;
            sent = strcat(sent,dec2hex(jj-1,2));
        end
        
        if (in_symb(ii) == iq(jj))
            found2 = 1;
            recv = strcat(recv,dec2hex(jj-1,2));
        end
    end
end

disp(['Sent Bit Stream:        ', sent]);
disp(['Received Bit Stream:    ', recv]);
disp(['Total Number of Errors: ', num2str(errors)]);
disp(['BER:                    ', num2str(errors*100/L), '%']);