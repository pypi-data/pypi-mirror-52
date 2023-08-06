# !usr/bin/env python
# coding=gbk
import math
import numpy
from scipy.fftpack import dct


# coding=utf-8
# ��������Ҫ���ĸ����������Ƿֱ��ǣ�
#    audio2frame:����Ƶת����֡����
#    deframesignal:��ÿһ֡��һ�����������ı任
#    spectrum_magnitude:����ÿһ֡����Ҷ�任�Ժ�ķ���
#    spectrum_power:����ÿһ֡����Ҷ�任�Ժ�Ĺ�����
#    log_spectrum_power:����ÿһ֡����Ҷ�任�Ժ�Ķ���������
#    pre_emphasis:��ԭʼ�źŽ���Ԥ���ش���



def audio2frame(signal, frame_length, frame_step, winfunc=lambda x: numpy.ones((x,))):
    '''����Ƶ�ź�ת��Ϊ֡��
	�������壺
	signal:ԭʼ��Ƶ�ͺ�
	frame_length:ÿһ֡�ĳ���(����ָ������ĳ��ȣ�������Ƶ�ʳ���ʱ����)
	frame_step:����֡�ļ����ͬ�϶��壩
	winfunc:lambda��������������һ������
    '''
    signal_length = len(signal)  # �ź��ܳ���
    frame_length = int(round(frame_length))  # ��֡֡ʱ�䳤��
    frame_step = int(round(frame_step))  # ����֮֡��Ĳ���
    if signal_length <= frame_length:  # ���źų���С��һ��֡�ĳ��ȣ���֡������Ϊ1
        frames_num = 1
    else:  # ���򣬼���֡���ܳ���
        frames_num = 1 + int(math.ceil((1.0 * signal_length - frame_length) / frame_step))
    pad_length = int((frames_num - 1) * frame_step + frame_length)  # ����֡�������ܵ���ƽ��ĳ���
    zeros = numpy.zeros((pad_length - signal_length,))  # �����ĳ���ʹ��0���������FFT�е������������
    pad_signal = numpy.concatenate((signal, zeros))  # �����źż�Ϊpad_signal
    indices = numpy.tile(numpy.arange(0, frame_length), (frames_num, 1)) + numpy.tile(
        numpy.arange(0, frames_num * frame_step, frame_step),
        (frame_length, 1)).T  # �൱�ڶ�����֡��ʱ�����г�ȡ���õ�frames_num*frame_length���ȵľ���
    indices = numpy.array(indices, dtype=numpy.int32)  # ��indicesת��Ϊ����
    frames = pad_signal[indices]  # �õ�֡�ź�
    win = numpy.tile(winfunc(frame_length), (frames_num, 1))  # window������������Ĭ��ȡ1
    return frames * win  # ����֡�źž���


def deframesignal(frames, signal_length, frame_length, frame_step, winfunc=lambda x: numpy.ones((x,))):
    '''���庯����ԭ�źŵ�ÿһ֡���б任��Ӧ����Ϊ������������
    �������壺
    frames:audio2frame�������ص�֡����
    signal_length:�źų���
    frame_length:֡����
    frame_step:֡���
    winfunc:��ÿһ֡��window�������з�����Ĭ�ϴ˴�����window
    '''
    # �Բ�������ȡ������
    signal_length = round(signal_length)  # �źŵĳ���
    frame_length = round(frame_length)  # ֡�ĳ���
    frames_num = numpy.shape(frames)[0]  # ֡������
    assert numpy.shape(frames)[1] == frame_length, '"frames"�����С����ȷ����������Ӧ�õ���һ֡����'  # �ж�framesά��
    indices = numpy.tile(numpy.arange(0, frame_length), (frames_num, 1)) + numpy.tile(
        numpy.arange(0, frames_num * frame_step, frame_step),
        (frame_length, 1)).T  # �൱�ڶ�����֡��ʱ�����г�ȡ���õ�frames_num*frame_length���ȵľ���
    indices = numpy.array(indices, dtype=numpy.int32)
    pad_length = (frames_num - 1) * frame_step + frame_length  # ��ƽ��������ź�
    if signal_length <= 0:
        signal_length = pad_length
    recalc_signal = numpy.zeros((pad_length,))  # ��������ź�
    window_correction = numpy.zeros((pad_length, 1))  # ������
    win = winfunc(frame_length)
    for i in range(0, frames_num):
        window_correction[indices[i, :]] = window_correction[indices[i, :]] + win + 1e-15  # ��ʾ�źŵ��ص��̶�
        recalc_signal[indices[i, :]] = recalc_signal[indices[i, :]] + frames[i, :]  # ԭ�źż����ص��̶ȹ��ɵ�������ź�
    recalc_signal = recalc_signal / window_correction  # �µĵ�������źŵ��ڵ����źŴ���ÿ�����ص��̶�
    return recalc_signal[0:signal_length]  # ���ظ��µĵ����ź�


def spectrum_magnitude(frames, NFFT):
    '''����ÿһ֡����FFY����Ժ��Ƶ�׵ķ��ȣ���frames�Ĵ�СΪN*L,�򷵻ؾ���Ĵ�СΪN*NFFT
    ����˵����
    frames:��audio2frame�����еķ���ֵ����֡����
    NFFT:FFT�任�������С,���֡����С��NFFT����֡�����ಿ����0�������
    '''
    complex_spectrum = numpy.fft.rfft(frames, NFFT)  # ��frames����FFT�任
    return numpy.absolute(complex_spectrum)  # ����Ƶ�׵ķ���ֵ


def spectrum_power(frames, NFFT):
    '''����ÿһ֡����Ҷ�任�Ժ�Ĺ�����
    ����˵����
    frames:audio2frame�������������֡����
    NFFT:FFT�Ĵ�С
    '''
    return 1.0 / NFFT * numpy.square(spectrum_magnitude(frames, NFFT))  # �����׵���ÿһ��ķ���ƽ��/NFFT


def log_spectrum_power(frames, NFFT, norm=1):
    '''����ÿһ֡�Ĺ����׵Ķ�����ʽ
    ����˵����
    frames:֡���󣬼�audio2frame���صľ���
    NFFT��FFT�任�Ĵ�С
    norm:����������һ��ϵ��
    '''
    spec_power = spectrum_power(frames, NFFT)
    spec_power[spec_power < 1e-30] = 1e-30  # Ϊ�˷�ֹ���ֹ����׵���0����Ϊ0�޷�ȡ����
    log_spec_power = 10 * numpy.log10(spec_power)
    if norm:
        return log_spec_power - numpy.max(log_spec_power)
    else:
        return log_spec_power


def pre_emphasis(signal, coefficient=0.95):
    '''���źŽ���Ԥ����
    �������壺
    signal:ԭʼ�ź�
    coefficient:����ϵ����Ĭ��Ϊ0.95
    '''
    return numpy.append(signal[0], signal[1:] - coefficient * signal[:-1])


# ����ÿһ֡��MFCCϵ��




def calcMFCC_delta_delta(signal, samplerate=16000, win_length=0.025, win_step=0.01, cep_num=13, filters_num=26,
                         NFFT=512, low_freq=0, high_freq=None, pre_emphasis_coeff=0.97, cep_lifter=22,
                         appendEnergy=True):
    '''����13��MFCC+13��һ��΢��ϵ��+13������ϵ��,һ��39��ϵ��
    '''
    feat = calcMFCC(signal, samplerate, win_length, win_step, cep_num, filters_num, NFFT, low_freq, high_freq,
                    pre_emphasis_coeff, cep_lifter, appendEnergy)  # ���Ȼ�ȡ13��һ��MFCCϵ��
    result1 = derivate(feat)
    result2 = derivate(result1)
    result3 = numpy.concatenate((feat, result1), axis=1)
    result = numpy.concatenate((result3, result2), axis=1)
    return result


def calcMFCC_delta(signal, samplerate=16000, win_length=0.025, win_step=0.01, cep_num=13, filters_num=26, NFFT=512,
                   low_freq=0, high_freq=None, pre_emphasis_coeff=0.97, cep_lifter=22, appendEnergy=True):
    '''����13��MFCC+13��һ��΢��ϵ��
    '''
    feat = calcMFCC(signal, samplerate, win_length, win_step, cep_num, filters_num, NFFT, low_freq, high_freq,
                    pre_emphasis_coeff, cep_lifter, appendEnergy)  # ���Ȼ�ȡ13��һ��MFCCϵ��
    result = derivate(feat)  # ����derivate����
    result = numpy.concatenate((feat, result), axis=1)
    return result


def derivate(feat, big_theta=2, cep_num=13):
    '''����һ��ϵ�����߼���ϵ����һ��任��ʽ
    ����˵��:
    feat:MFCC�������һ��ϵ������
    big_theta:��ʽ�еĴ�theta��Ĭ��ȡ2
    '''
    result = numpy.zeros(feat.shape)  # ���
    denominator = 0  # ��ĸ
    for theta in numpy.linspace(1, big_theta, big_theta):
        denominator = denominator + theta ** 2
    denominator = denominator * 2  # ����õ���ĸ��ֵ
    for row in numpy.linspace(0, feat.shape[0] - 1, feat.shape[0]):
        row = int(row)
        tmp = numpy.zeros((cep_num,))
        numerator = numpy.zeros((cep_num,))  # ����
        for t in numpy.linspace(1, cep_num, cep_num):
            t = int(t)
            a = 0
            b = 0
            s = 0
            for theta in numpy.linspace(1, big_theta, big_theta):
                theta = int(theta)
                if (t + theta) > cep_num:
                    a = 0
                else:

                    a = feat[row][t + theta - 1]
                if (t - theta) < 1:
                    b = 0
                else:
                    b = feat[row][t - theta - 1]
                s += theta * (a - b)
            numerator[t - 1] = s
        tmp = numerator * 1.0 / denominator
        result[row] = tmp
    return result


def calcMFCC(signal, samplerate=16000, win_length=0.025, win_step=0.01, cep_num=13, filters_num=26, NFFT=512,
             low_freq=0, high_freq=None, pre_emphasis_coeff=0.97, cep_lifter=22, appendEnergy=True):
    '''����13��MFCCϵ��
    �������壺
    signal:ԭʼ��Ƶ�źţ�һ��Ϊ.wav��ʽ�ļ�
    samplerate:����Ƶ�ʣ�����Ĭ��Ϊ16KHz
    win_length:�����ȣ�Ĭ�ϼ�һ֡Ϊ25ms
    win_step:�������Ĭ������¼�����֡��ʼʱ��֮�����10ms
    cep_num:����ϵ���ĸ�����Ĭ��Ϊ13
    filters_num:�˲����ĸ�����Ĭ��Ϊ26
    NFFT:����Ҷ�任��С��Ĭ��Ϊ512
    low_freq:���Ƶ�ʣ�Ĭ��Ϊ0
    high_freq:���Ƶ��
    pre_emphasis_coeff:Ԥ����ϵ����Ĭ��Ϊ0.97
    cep_lifter:���׵�����������
    appendEnergy:�Ƿ����������Ĭ�ϼ�
    '''

    feat, energy = fbank(signal, samplerate, win_length, win_step, filters_num, NFFT, low_freq, high_freq,
                         pre_emphasis_coeff)
    feat = numpy.log(feat)
    feat = dct(feat, type=2, axis=1, norm='ortho')[:, :cep_num]  # ������ɢ���ұ任,ֻȡǰ13��ϵ��
    feat = lifter(feat, cep_lifter)
    if appendEnergy:
        feat[:, 0] = numpy.log(energy)  # ֻȡ2-13��ϵ������һ���������Ķ���������
    return feat


def fbank(signal, samplerate=16000, win_length=0.025, win_step=0.01, filters_num=26, NFFT=512, low_freq=0,
          high_freq=None, pre_emphasis_coeff=0.97):
    '''������Ƶ�źŵ�MFCC
    ����˵����
    samplerate:����Ƶ��
    win_length:������
    win_step:�����
    filters_num:÷���˲�������
    NFFT:FFT��С
    low_freq:���Ƶ��
    high_freq:���Ƶ��
    pre_emphasis_coeff:Ԥ����ϵ��
    '''

    high_freq = high_freq or samplerate / 2  # ������Ƶ���������Ƶ��
    signal = pre_emphasis(signal, pre_emphasis_coeff)  # ��ԭʼ�źŽ���Ԥ���ش���
    frames = audio2frame(signal, win_length * samplerate, win_step * samplerate)  # �õ�֡����
    spec_power = spectrum_power(frames, NFFT)  # �õ�ÿһ֡FFT�Ժ��������
    energy = numpy.sum(spec_power, 1)  # ��ÿһ֡�������׽������
    energy = numpy.where(energy == 0, numpy.finfo(float).eps, energy)  # ������Ϊ0�ĵط�����Ϊeps���������ڽ��ж�������
    fb = get_filter_banks(filters_num, NFFT, samplerate, low_freq, high_freq)  # ���ÿһ���˲�����Ƶ�ʿ��
    feat = numpy.dot(spec_power, fb.T)  # ���˲����������׽��е��
    feat = numpy.where(feat == 0, numpy.finfo(float).eps, feat)  # ͬ�����ܳ���0
    return feat, energy


def log_fbank(signal, samplerate=16000, win_length=0.025, win_step=0.01, filters_num=26, NFFT=512, low_freq=0,
              high_freq=None, pre_emphasis_coeff=0.97):
    '''�������ֵ
    �������壺ͬ��
    '''
    feat, energy = fbank(signal, samplerate, win_length, win_step, filters_num, NFFT, low_freq, high_freq,
                         pre_emphasis_coeff)
    return numpy.log(feat)


def ssc(signal, samplerate=16000, win_length=0.025, win_step=0.01, filters_num=26, NFFT=512, low_freq=0, high_freq=None,
        pre_emphasis_coeff=0.97):
    '''
    ������
    '''
    high_freq = high_freq or samplerate / 2
    signal = pre_emphasis(signal, pre_emphasis_coeff)
    frames = audio2frame(signal, win_length * samplerate, win_step * samplerate)
    spec_power = spectrum_power(frames, NFFT)
    spec_power = numpy.where(spec_power == 0, numpy.finfo(float).eps, spec_power)  # ������
    fb = get_filter_banks(filters_num, NFFT, samplerate, low_freq, high_freq)
    feat = numpy.dot(spec_power, fb.T)  # ��������
    R = numpy.tile(numpy.linspace(1, samplerate / 2, numpy.size(spec_power, 1)), (numpy.size(spec_power, 0), 1))
    return numpy.dot(spec_power * R, fb.T) / feat


def hz2mel(hz):
    '''��Ƶ��hzת��Ϊ÷��Ƶ��
    ����˵����
    hz:Ƶ��
    '''
    return 2595 * numpy.log10(1 + hz / 700.0)


def mel2hz(mel):
    '''��÷��Ƶ��ת��Ϊhz
    ����˵����
    mel:÷��Ƶ��
    '''
    return 700 * (10 ** (mel / 2595.0) - 1)


def get_filter_banks(filters_num=20, NFFT=512, samplerate=16000, low_freq=0, high_freq=None):
    '''����÷�����Ǽ���˲��������˲����ڵ�һ��Ƶ�ʺ͵�����Ƶ�ʴ�Ϊ0���ڵڶ���Ƶ�ʴ�Ϊ1
    ����˵����
    filers_num:�˲�������
    NFFT:FFT��С
    samplerate:����Ƶ��
    low_freq:���Ƶ��
    high_freq:���Ƶ��
    '''
    # ���ȣ���Ƶ��hzת��Ϊ÷��Ƶ�ʣ���Ϊ�˶��ֱ������Ĵ�С��Ƶ�ʲ����������ȣ����Ի�Ϊ÷��Ƶ�������Էָ�
    low_mel = hz2mel(low_freq)
    high_mel = hz2mel(high_freq)
    # ��Ҫ��low_mel��high_mel֮��ȼ�����filters_num���㣬һ��filters_num+2����
    mel_points = numpy.linspace(low_mel, high_mel, filters_num + 2)
    # �ٽ�÷��Ƶ��ת��ΪhzƵ�ʣ������ҵ���Ӧ��hzλ��
    hz_points = mel2hz(mel_points)
    # ����������Ҫ֪����Щhz_points��Ӧ��fft�е�λ��
    bin = numpy.floor((NFFT + 1) * hz_points / samplerate)
    # �����������˲����ı��ʽ�ˣ�ÿ���˲����ڵ�һ���㴦�͵������㴦��Ϊ0���м�Ϊ��������״
    fbank = numpy.zeros([filters_num, NFFT / 2 + 1])
    for j in range(0, filters_num):
        for i in range(int(bin[j]), int(bin[j + 1])):
            fbank[j, i] = (i - bin[j]) / (bin[j + 1] - bin[j])
        for i in range(int(bin[j + 1]), int(bin[j + 2])):
            fbank[j, i] = (bin[j + 2] - i) / (bin[j + 2] - bin[j + 1])
    return fbank


def lifter(cepstra, L=22):
    '''�����׺���
    ����˵����
    cepstra:MFCCϵ��
    L����ϵ����Ĭ��Ϊ22
    '''
    if L > 0:
        nframes, ncoeff = numpy.shape(cepstra)
        n = numpy.arange(ncoeff)
        lift = 1 + (L / 2) * numpy.sin(numpy.pi * n / L)
        return lift * cepstra
    else:
        return cepstra