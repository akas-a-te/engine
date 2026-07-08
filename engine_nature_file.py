import csv
import os


def process_and_export_bikes(input_file="bikes.csv", output_file="bikes_analyzed.csv"):
    if not os.path.exists(input_file):
        print(f"Error: '{input_file}' not found. Please create it first.")
        return

    print(f"Processing '{input_file}' and saving results to '{output_file}'...\n")

    with open(input_file, mode="r", newline="", encoding="utf-8") as infile:
        reader = csv.DictReader(infile)

        # Define fieldnames for the new output file
        fieldnames = reader.fieldnames + ["norm_torque", "ratio", "energy_feel", "movement_motion", "full_profile"]

        with open(output_file, mode="w", newline="", encoding="utf-8") as outfile:
            writer = csv.DictWriter(outfile, fieldnames=fieldnames)
            writer.writeheader()

            for row in reader:
                hp = float(row["power_hp"])
                torque = float(row["torque_nm"])
                weight = float(row["weight_kg"]) / 1000

                norm_torque = torque / weight
                norm_hp = hp / weight
                ratio = norm_hp / norm_torque if norm_torque != 0 else 0

                # 1. Feel Vocabulary (Torque Substance)
                if norm_torque < 75:
                    feel = "Dead"
                elif 75 <= norm_torque < 150:
                    feel = "Calm"
                elif 150 <= norm_torque < 225:
                    feel = "Alive"
                elif 225 <= norm_torque <= 300:
                    feel = "Unapologetic"
                else:
                    feel = "Wild"

                # 2. Motion Vocabulary (Ratio Delivery)
                if ratio < 0.60:
                    motion = "Shrinked"
                elif 0.60 <= ratio < 0.85:
                    motion = "Open-Hearted"
                elif 0.85 <= ratio <= 1.10:
                    motion = "Steady"
                elif 1.10 < ratio <= 1.35:
                    motion = "Electric"
                else:
                    motion = "Chaotic"

                # Format the custom philosophy string
                profile_string = f"ENERGY - {feel} ( {norm_torque:.2f} )   |   MOVEMENT - {motion} ( {ratio:.3f} )"

                # Add new analytical values to the row data
                row["norm_torque"] = f"{norm_torque:.2f}"
                row["ratio"] = f"{ratio:.3f}"
                row["energy_feel"] = feel
                row["movement_motion"] = motion
                row["full_profile"] = profile_string

                writer.writerow(row)

    print(f"Success! Analysis complete. Check '{output_file}' for the results.")


if __name__ == "__main__":
    process_and_export_bikes()
