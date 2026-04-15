def calculate_tics(seconds):
    """Converts seconds to ZDoom tics (35 tics per second)."""
    return int(float(seconds) * 35)

def generate_zscript(frame_label, normal_frame, blink_frame, goto_label, seconds):
    """Pure logic to build the script string."""
    count = calculate_tics(seconds)
    lines = []

    # Lead-in
    lines.append(f'TNT1 A 0 CB_SpeakDialogue(#DialogueNumber1, #DialogueNumber2, "Villy", "Very_Angry" );')
    lines.append(f'{frame_label} {normal_frame} 9 CB_DialogueSkipPrevent;')
    lines.append(f'{frame_label} {normal_frame} 1 CB_DialogueSkipPrevent;')

    # Main Loop
    for i in range(10, count):
        current_frame = blink_frame if (i % 10 == 0) else normal_frame

        command = f'{frame_label} {current_frame} 1 A_JumpIfInTargetInventory("SkipDialogue", 1, "{goto_label}");'
        lines.append(command)

    lines.append(f"\n{goto_label}:")
    return "\n".join(lines)
