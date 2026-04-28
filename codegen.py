def calculate_tics(seconds):
    """Converts seconds to ZDoom tics (35 tics per second)."""
    return int(float(seconds) * 35)

def generate_zscript(frame_label, normal_frame, blink_frame, openmouth_frame, openmouth_eyeclosed_frame, goto_label, seconds, mouth_input_string, mouth_input_string_unperiodic):
    """Pure logic to build the script string."""
    mouth_times = parse_mouth_list(mouth_input_string)
    mouth_times_unperiodic = parse_mouth_list(mouth_input_string_unperiodic)
    mouth_tics = [int(t * 35) for t in mouth_times]
    mouth_tics_unperiodic = [int(t * 35) for t in mouth_times_unperiodic]
    IsSpeaking = False
    IsSpeaking_unperiodic = False

    print(mouth_tics)

    count = calculate_tics(seconds)
    lines = []

    if(len(frame_label) != 4):
        raise ValueError("frame_label needs to be 4 letter long!")
        return

    # Lead-in
    lines.append(f'TNT1 A 0 CB_SpeakDialogue(#DialogueNumber1, #DialogueNumber2, "Villy", "Very_Angry" );')
    #lines.append(f'{frame_label} {normal_frame} 9 CB_DialogueSkipPrevent;')
    #lines.append(f'{frame_label} {normal_frame} 1 CB_DialogueSkipPrevent;')

    # Main Loop
    for i in range(0, count):
        if(i > 10):
            zscript_func = f'A_JumpIfInTargetInventory("SkipDialogue", 1, "{goto_label}");'
        else:
            zscript_func = "CB_DialogueSkipPrevent;"

        if i in mouth_tics:
            IsSpeaking = not IsSpeaking
            print(IsSpeaking)

        if i in mouth_tics_unperiodic:
            IsSpeaking_unperiodic = not IsSpeaking_unperiodic
            print(IsSpeaking_unperiodic)

        if IsSpeaking:
            current_frame = blink_frame_func(i, openmouth_frame, openmouth_eyeclosed_frame) if (i % 8 < 4) else blink_frame_func(i, normal_frame, blink_frame)
        elif IsSpeaking_unperiodic:
            current_frame = openmouth_eyeclosed_frame
        else:
            current_frame = blink_frame_func(i, normal_frame, blink_frame)

        command = f'{frame_label} {current_frame} 1 {zscript_func}'
        lines.append(command)

    lines.append(f"\n{goto_label}:")
    return "\n".join(lines)

def parse_mouth_list(input_string):
    """Converts '0.3, 0.7, 1.2' into [0.3, 0.7, 1.2]"""
    if not input_string.strip():
        return []

    try:
        # 1. Replace commas with spaces so we have one consistent separator
        # 2. Split by whitespace
        # 3. Convert every valid chunk into a float
        raw_list = input_string.replace(',', ' ').split()
        return [float(x) for x in raw_list]
    except ValueError:
        raise ValueError("Mouth Movements must be a list of numbers separated by commas!")

def blink_frame_func(i, normal_frame, blink_frame):
    if (i % 60 < 3) and (i > 10):
        return blink_frame
    else:
        return normal_frame
