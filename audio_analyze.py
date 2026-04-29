import os
import numpy as np
from pydub import AudioSegment
from scipy.signal import find_peaks, welch
from pydub.silence import detect_nonsilent

#I did tried to use Librosa, but maybe because Arch Linux's package issue, it didn't worked out on my system. so decided resort on something else.
#While I say its tolorable running with shorter dialogue and/or running with powerful CPUs, but nature of Python, this part of code can get really slow sometimes, thus I should consider rewriting this bit with C/C++ someday.


def analyze_voice_segments(audio_file_path, input_threshold, window_size):
    try:
        # 0. Defining the list
        lists = []
        lists_unperiodic = []

        # 1. Load and Normalize
        sound = AudioSegment.from_file(audio_file_path).set_channels(1).set_frame_rate(22050)
        sr = sound.frame_rate
        samples = np.array(sound.get_array_of_samples(), dtype=np.float32)
        y = samples / 32768.0

        # 2. Energy-based Activity Detection
        window_size = int(sr * window_size) # 0.1ms windows
        energy = np.array([np.sqrt(np.mean(y[i:i+window_size]**2)) for i in range(0, len(y), window_size)])

        # Sensitivity: lower threshold (e.g., 0.01) finds quieter sounds
        threshold = 0.3 # 0.3 db
        is_active = (energy > input_threshold).astype(int)

        # 3. Find Contiguous Clusters (Grouping the 1s)
        # We look for where the activity status changes
        diff = np.diff(is_active)
        starts = np.where(diff == 1)[0] + 1
        ends = np.where(diff == -1)[0] + 1

        # Handle edge cases (starts with sound or ends with sound)
        if is_active[0] == 1:
            starts = np.insert(starts, 0, 0)
        if is_active[-1] == 1:
            ends = np.append(ends, len(is_active))

        print(f"Found {len(starts)} distinct segments.")
        print("-" * 40)

        # 4. Loop through each detected segment
        for i, (s_win, e_win) in enumerate(zip(starts, ends)):
            # Convert window indices back to sample indices
            start_samp = s_win * window_size
            end_samp = e_win * window_size

            # Skip segments that are too short (e.g., shorter than 100ms) to be a scream/yawn
            if (end_samp - start_samp) < (sr * 0.1):
                continue

            segment = y[start_samp:end_samp]

            # --- ANALYSIS LOGIC ---

            # Zero Crossing Rate
            zcr = np.mean(np.abs(np.diff(np.sign(segment)))) / 2

            # Periodicity (Autocorrelation)
            # Normalize the segment first to prevent math explosions. Fuck you Librosa, eat my arse.
            seg_norm = segment / (np.max(np.abs(segment)) + 1e-6)
            corr = np.correlate(seg_norm, seg_norm, mode='full')[len(seg_norm)-1:]
            corr = corr / (np.max(corr) + 1e-6)

            # Find peaks in the autocorrelation (human pitch range)
            peaks, _ = find_peaks(corr[20:500], height=0.3)
            periodicity_score = len(peaks)

            # Classification
            if periodicity_score > 5 and zcr < 0.15:
                label = "Periodic (Yawn/Tonal)"
            elif zcr > 0.18:
                label = "Standard Speech/Noise"
            else:
                label = "High-Freq/Breathy (Unperiodic. Likely Screaming)"

            start_sec = start_samp / sr
            end_sec = end_samp / sr

            #Final Steps. Showing the seconds in Terminal, as well as add the start_sec, end_sec onto list.
            print(f"[{i+1}] {start_sec:.2f}s - {end_sec:.2f}s")
            if(label == "Standard Speech/Noise"):
                lists.append(f"{start_sec:.2f}")
                lists.append(f"{end_sec:.2f}")
            elif(label == "High-Freq/Breathy (Unperiodic. Likely Screaming)"):
                lists_unperiodic.append(f"{start_sec:.2f}")
                lists_unperiodic.append(f"{end_sec:.2f}")
            print(f"    ZCR: {zcr:.4f} | Periodicity: {periodicity_score}")
            print(f"    Result: {label}")
            print("-" * 20)

        print(f"Standard Speech: {lists}")
        print(f"Unperiodic Speech: {lists_unperiodic}")
        list_to_return = list_to_string_list(lists)
        lists_to_return_unperiodic = list_to_string_list(lists_unperiodic)
        return list_to_return, lists_to_return_unperiodic

    except Exception as e:
        print(f"Error: {e}")


def list_to_string_list(input_list):
    """Converts　[0.3, 0.7, 1.2]  into '0.3, 0.7, 1.2'"""
    string_list = ""

    try:
        for i in range(0, len(input_list)):
            blank_insert = (", ") if (i != len(input_list) - 1) else ("")
            string_list = string_list + (f"{input_list[i]}") + blank_insert
        return string_list
    except ValueError:
        raise ValueError("Process at parse_mouth_list_opposite on audio_analyze.py failed!")
