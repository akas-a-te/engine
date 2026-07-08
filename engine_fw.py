def calculate_performance():
    print("\n--- Vehicle Performance Calculator ---\n")
    print("Select vehicle type: 1) Combustion  2) EV")
    choice = input("Enter choice (1/2): ")
    name = input("Enter vehicle name: ")

    # Defaults
    b_s_type, power_type, nature, tweak_level = "N/A", "N/A", "N/A", "N/A"
    bore_stroke_ratio = 0.0

    hp = float(input("Enter peak HP: "))
    torque = float(input("Enter peak Torque (Nm): "))
    weight_tonne = float(input("Enter weight (in kg): ")) / 1000

    hp_torque_ratio = hp / torque if torque != 0 else 0

    if choice == '2':  # EV
        b_s_type, power_type, nature, tweak_level = "Electric", "Direct", "EV Character", "N/A"
    else:  # Combustion
        bore = float(input("Enter bore (mm): "))
        stroke = float(input("Enter stroke (mm): "))
        bore_stroke_ratio = bore / stroke

        # B/S Classification
        if bore_stroke_ratio < 0.9:
            b_s_type = "Under-square"
        elif bore_stroke_ratio > 1.1:
            b_s_type = "Over-square"
        else:
            b_s_type = "Square"

        # HP/Torque Ratio Classification
        if hp_torque_ratio < 0.9:
            power_type = "Slow-revving"
        elif hp_torque_ratio > 1.1:
            power_type = "Fast-revving"
        else:
            power_type = "Mid-revving"

        # Determine "True to nature" or "Against nature"
        b_idx = 0 if bore_stroke_ratio < 0.9 else (1 if bore_stroke_ratio <= 1.1 else 2)
        p_idx = 0 if hp_torque_ratio < 0.9 else (1 if hp_torque_ratio <= 1.1 else 2)
        nature = "True to nature" if b_idx == p_idx else "Against nature"

        # Tweak Level based on Gap
        gap = abs(bore_stroke_ratio - hp_torque_ratio)
        if gap < 0.15:
            tweak_level = "Honest"
        elif gap <= 0.3:
            tweak_level = "Slightly tweaked"
        else:
            tweak_level = "Highly tweaked"

    norm_hp = hp / weight_tonne
    norm_torque = torque / weight_tonne

    print(f"\n--- {name} Results ---\n")
    if choice == '1':
        print(
            f"Gap: {abs(bore_stroke_ratio - hp_torque_ratio):.3f} | B/S: {bore_stroke_ratio:.3f} | HP/Torq: {hp_torque_ratio:.3f}\n")

    print(f"Norm. BHP: {norm_hp:.2f} HP/tonne | Norm. Torque: {norm_torque:.2f} Nm/tonne\n")
    print(f"Build: {b_s_type} | Delivery: {power_type}\n")
    print(f"Character: {nature} | Tweak Level: {tweak_level}")


if __name__ == "__main__":
    calculate_performance()