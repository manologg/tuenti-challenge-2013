/*	This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>. */

package com.nonoo.rttydecoder.fft.dpll;

import java.io.BufferedReader;
import java.io.ByteArrayInputStream;
import java.io.ByteArrayOutputStream;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.InputStreamReader;

import javax.sound.sampled.AudioFileFormat;
import javax.sound.sampled.AudioFormat;
import javax.sound.sampled.AudioInputStream;
import javax.sound.sampled.AudioSystem;
import javax.sound.sampled.DataLine;
import javax.sound.sampled.LineUnavailableException;
import javax.sound.sampled.TargetDataLine;

import edu.emory.mathcs.jtransforms.fft.DoubleFFT_1D;

public class RTTYDecoder implements Runnable {
	private final static int SAMPLERATE = 48000;
	private final static int BUFFERSIZE = SAMPLERATE;
	private final static int FREQ0 = 915;
	private final static int FREQ1 = 1085;
	private final static double BITSPERSEC = 45.45;
	private final static double PWRTHRESHOLD = 5;
	private final static int CHUNKCOUNTPERBIT = 4;

	private static enum RTTYMode { letters, symbols };
	private static RTTYMode mode = RTTYMode.letters;
    private static char[] RTTYLetters = ("<" + "E" + "\n" + "A" + " " + "S" + "I" + "U" + "\n" + "D" + "R" + "J" + "N" + "F" + "C" + "K" + "T" + "Z" + "L" + "W" + "H" + "Y" + "P" + "Q" + "O" + "B" + "G" + "^" + "M" + "X" + "V" + "^").toCharArray();
    private static char[] RTTYSymbols = ("<" + "3" + "\n" + "-" + " " + "," + "8" + "7" + "\n" + "$" + "4" + "#" + "," + "." + ":" + "(" + "5" + "+" + ")" + "2" + "." + "6" + "0" + "1" + "9" + "7" + "." + "^" + "." + "/" + "=" + "^").toCharArray();

	private TargetDataLine tdl;
	private double[] chunkBuffer;
	private DoubleFFT_1D fft;
	private double[] fftData;
	private int oneChunkSampleCount;
	private int binOfFreq0, binOfFreq1;
	private int oldChunkVal = 0;
	private ByteArrayOutputStream baos;

	public RTTYDecoder(TargetDataLine tdl) {
		this.tdl = tdl;

		int oneBitSampleCount = (int)Math.round(SAMPLERATE/BITSPERSEC);
		oneChunkSampleCount = (int)Math.round(oneBitSampleCount/CHUNKCOUNTPERBIT);
		System.out.println("One bit length: " + 1/BITSPERSEC + " seconds, " + oneBitSampleCount + " samples");
		System.out.println("One chunk length: " + (1/BITSPERSEC)/CHUNKCOUNTPERBIT + " seconds, " + oneChunkSampleCount + " samples");

		chunkBuffer = new double[oneChunkSampleCount];

		fft = new DoubleFFT_1D(oneChunkSampleCount);
		// we need to initialize a buffer where we store our samples as complex numbers. first value is the real part, second is the imaginary.
		fftData = new double[oneChunkSampleCount*2];
		binOfFreq0 = (int)Math.round((FREQ0/(double)SAMPLERATE)*fftData.length);
		binOfFreq1 = (int)Math.round((FREQ1/(double)SAMPLERATE)*fftData.length);

		System.out.println("FFT bin of freq. 0 (" + FREQ0 + "Hz): " + binOfFreq0);
		System.out.println("FFT bin of freq. 1 (" + FREQ1 + "Hz): " + binOfFreq1);

		baos = new ByteArrayOutputStream(); // this will store output sound data for debugging purposes 
	}

	// converts double samples to byte pairs
	private byte[] getBytesFromDoubles(final double[] audioData, final int storedSamples) {
		byte[] audioDataBytes = new byte[storedSamples * 2];

		for (int i = 0; i < storedSamples; i++) {
			// saturation
			audioData[i] = Math.min(1.0, Math.max(-1.0, audioData[i]));

			// scaling and conversion to integer
			int sample = (int) Math.round((audioData[i] + 1.0) * 32767.5) - 32768;

			byte high = (byte) ((sample >> 8) & 0xFF);
			byte low = (byte) (sample & 0xFF);
			audioDataBytes[i * 2] = low;
			audioDataBytes[i * 2 + 1] = high;
		}

		return audioDataBytes;
	}

	// saves the audio data given in audioDataBytes to a .wav file
	private void writeWavFile(final byte[] audioDataBytes, final int storedSamples, final String fileName) {
		AudioFormat audioFormat = new AudioFormat(AudioFormat.Encoding.PCM_SIGNED, SAMPLERATE, 16, 1, 2, SAMPLERATE, false);
		AudioInputStream audioInputStream = new AudioInputStream(new ByteArrayInputStream(audioDataBytes), audioFormat, storedSamples);

		try {
			FileOutputStream fileOutputStream = new FileOutputStream(fileName);
			AudioSystem.write(audioInputStream, AudioFileFormat.Type.WAVE, fileOutputStream);
			audioInputStream.close();
		} catch (Exception e) {
			e.printStackTrace();
		}
	}

	// reads a chunk from the sound device
	public int getChunk(double[] chunkBuffer) {
		byte[] abBuffer = new byte[oneChunkSampleCount*2];
		int samplesRead = 0;

		// waiting for the buffer to get filled
		try {
			while (tdl.available() < abBuffer.length)
				Thread.sleep(0, 1); // without this, the audio will be choppy

			int bytesRead = tdl.read(abBuffer, 0, abBuffer.length);

			// converting frames stored as bytes to double values
			samplesRead = bytesRead / 2;
			for (int i = 0; i < samplesRead; i++) {
				chunkBuffer[i] = ((abBuffer[i * 2] & 0xFF) | (abBuffer[i * 2 + 1] << 8)) / 32768.0;
			}
		} catch (InterruptedException e) {
		}
		return samplesRead;
	}

	// analyzes a chunk with FFT and returns the bit value based on the averaged spectral power at the mark and space freqs
	public int demodulator() {
		int samplesRead = getChunk(chunkBuffer);

		baos.write(getBytesFromDoubles(chunkBuffer, samplesRead), 0, samplesRead * 2);  // writing to the output wav for debugging purposes

		for (int i = 0; i < fftData.length; i++)
			fftData[i] = 0;
		for (int i = 0; i < samplesRead; i++) {
			// copying audio data to the fft data buffer, imaginary part is 0
			fftData[2 * i] = chunkBuffer[i];
			fftData[2 * i + 1] = 0;
		}

		// calculating the fft of the data, so we will have spectral power of each frequency component
		// fft resolution (number of bins) is samplesNum, because we initialized with that value
		fft.complexForward(fftData);

		double PWRFreq0 = Math.sqrt(fftData[binOfFreq0] * fftData[binOfFreq0] + fftData[binOfFreq0+1] * fftData[binOfFreq0+1]);
		double PWRFreq1 = Math.sqrt(fftData[binOfFreq1] * fftData[binOfFreq1] + fftData[binOfFreq1+1] * fftData[binOfFreq1+1]);

		if (PWRFreq0 > PWRTHRESHOLD || PWRFreq1 > PWRTHRESHOLD) {
			if (PWRFreq0-PWRFreq1 < 0)
				return 1; 
			else
				return 0; 
		}
		return -1;
	}

	// this function returns at the half of a bit with the bit's value
	public int getBitDPLL() {
		boolean chunkPhaseChanged = false;
		int chunkVal = -1;
		int chunkPhase = 0;

		while (chunkPhase < CHUNKCOUNTPERBIT) {
			chunkVal = demodulator();
			if (chunkVal == -1)
				break;

			if (!chunkPhaseChanged && chunkVal != oldChunkVal) {
				if (chunkPhase < CHUNKCOUNTPERBIT/2)
					chunkPhase++; // early
				else
					chunkPhase--; // late
				chunkPhaseChanged = true;
			}
			oldChunkVal = chunkVal;
			chunkPhase++;
		}

		// putting a tick to the output wav signing the moment when the DPLL returned
		baos.write(100);
		baos.write(100);
		baos.write(100);
		baos.write(100);
		baos.write(100);
		baos.write(100);
		return chunkVal;
	}
	
	// this function returns only when the start bit is successfully received
	public void waitForStartBit() {
		int bitResult;

		while (!Thread.interrupted()) {
			do {
				bitResult = demodulator();
			} while ((bitResult == 0 || bitResult == -1) && !Thread.interrupted());
			
			//System.out.println("sb0: 1");
			
			do {
				bitResult = demodulator();
			} while ((bitResult == 1 || bitResult == -1) && !Thread.interrupted());
			
			//System.out.println("sb1: 0");

			// waiting half bit time
			for (int i = 0; i < CHUNKCOUNTPERBIT/2; i++)
				bitResult = demodulator();

			//System.out.println("sb2: " + bitResult);

			if (bitResult == 0)
				break;
		}
		//System.out.println("start bit ok");
	}

	@Override
	public void run() {
		tdl.start();

		int byteResult = 0;
		int byteResultp = 0;
		int bitResult;
		
		while (!Thread.interrupted()) {
			waitForStartBit();
			
			System.out.print("0 "); // first bit is the start bit, it's zero
			
			// reading 7 more bits
			for (byteResultp = 1, byteResult = 0; byteResultp < 8; byteResultp++) {
				bitResult = getBitDPLL();
				if (bitResult == -1) {
					byteResult = -1;
					break;
				}

				switch (byteResultp) {
					case 6: // stop bit 1
						System.out.print(" " + bitResult);
						break;
					case 7: // stop bit 2
						System.out.print(bitResult);
						break;
					default:
						System.out.print(bitResult);
						byteResult += bitResult << (byteResultp-1);
				}
			}

			if (byteResult == -1)
				continue;

			switch (byteResult) {
				case 31:
					mode = RTTYMode.letters;
					System.out.println(" ^L^");
					break;
				case 27:
					mode = RTTYMode.symbols;
					System.out.println(" ^F^");
					break;
				default:
					switch (mode) {
					case letters:
						System.out.println(" *** " + RTTYLetters[byteResult] + "(" + byteResult + ")");
						break;
					case symbols:
						System.out.println(" *** " + RTTYSymbols[byteResult] + "(" + byteResult + ")");
						break;
					}
			}
		}

		tdl.stop();
		tdl.close();
	}

	public static void main(String[] args) {
		AudioFormat audioFormat = new AudioFormat(AudioFormat.Encoding.PCM_SIGNED, SAMPLERATE, 16, 1, 2, SAMPLERATE, false);
		DataLine.Info info = new DataLine.Info(TargetDataLine.class, audioFormat, BUFFERSIZE);

		TargetDataLine targetDataLine = null;
		try {
			targetDataLine = (TargetDataLine) AudioSystem.getLine(info);
			targetDataLine.open(audioFormat, BUFFERSIZE);
			System.out.println("Buffer size: " + targetDataLine.getBufferSize());
		} catch (LineUnavailableException e1) {
			e1.printStackTrace();
		}

		// creating the recorder thread from this class' instance
		RTTYDecoder rttyDecoder = new RTTYDecoder(targetDataLine);
		Thread rttyDecoderThread = new Thread(rttyDecoder);

		// we use this to read line from the standard input
		BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
		rttyDecoderThread.setPriority(Thread.MAX_PRIORITY);
		rttyDecoderThread.start();

		System.out.println("Recording... press ENTER to stop recording!");
		try {
			br.readLine();
		} catch (IOException e) {
			e.printStackTrace();
		}
		System.out.println("Stopping...");
		rttyDecoder.writeWavFile(rttyDecoder.baos.toByteArray(), rttyDecoder.baos.size() / 2, "output.wav");

		rttyDecoderThread.interrupt();

		try {
			// waiting for the recorder thread to stop
			rttyDecoderThread.join();
		} catch (InterruptedException e) {
			e.printStackTrace();
		}
		System.out.println("Recording stopped.");
	}
}
