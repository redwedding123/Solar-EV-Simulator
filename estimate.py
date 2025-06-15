import math
import matplotlib.pyplot as plt

def simulate_soc_range():
    print("\n Solar EV SOC + Range Estimation (with Graphs) \n")

    # User Inputs
    battery_capacity_kwh = float(input("Battery capacity (in kWh): "))
    voltage = float(input("Battery nominal voltage (in V): "))
    initial_soc = float(input("Initial SOC (in %, 0–100): "))
    energy_consumption = float(input("Energy consumption (in Wh/km): "))
    speed = float(input("Vehicle speed (in km/h): "))
    panel_area = float(input("Solar panel area (in m²): "))
    panel_efficiency = float(input("Panel efficiency (in %, e.g., 20): ")) / 100
    peak_irradiance = float(input("Peak solar irradiance (in W/m², e.g., 1000): "))
    drive_duration_min = int(input("Simulation time (in minutes): "))

    # Derived values
    battery_capacity_ah = (battery_capacity_kwh * 1000) / voltage
    soc_ah = (initial_soc / 100) * battery_capacity_ah
    power_motor_watts = (energy_consumption * speed)
    total_time = drive_duration_min * 60
    time_step = 1

    # Logging data for plots
    time_log = []
    soc_log = []
    range_log = []
    solar_log = []

    print("\n Simulating...\n")
    print("Time(min) \t SOC(%) \t \tRange(km)")

    for t in range(0, total_time + 1, time_step):
        # Simulate irradiance curve (e.g., sine from sunrise to sunset)
        irradiance = peak_irradiance * math.sin(math.pi * t / total_time)
        irradiance = max(0, irradiance) # ensuring irradiance is never negative (defaults to 0 when no light)

        # Solar power from irradiance
        solar_power = irradiance * panel_area * panel_efficiency

        # Current calculations
        i_motor = power_motor_watts / voltage
        i_solar = solar_power / voltage
        net_current = i_motor - i_solar

        # SOC update using Couloumb Counting
        delta_soc_ah = (net_current * time_step) / 3600
        soc_ah -= delta_soc_ah
        soc_ah = max(soc_ah, 0)

        # Metrics
        soc_percent = (soc_ah / battery_capacity_ah) * 100
        remaining_energy_wh = soc_ah * voltage
        remaining_range_km = remaining_energy_wh / energy_consumption

        # Store for graphing
        time_log.append(t / 60)  # in minutes
        soc_log.append(soc_percent)
        range_log.append(remaining_range_km)
        solar_log.append(solar_power)

        # Print every 5 minutes or when battery dies
        if t % 300 == 0 or soc_ah <= 0:
            print(f"{t//60:>5}\t\t{soc_percent:6.2f}\t\t{remaining_range_km:7.2f}")

        if soc_ah <= 0:
            print("\n Battery fully depleted. Vehicle stopped.")
            break

    print("\n Simulation complete. Generating plots...\n")

    # --- Plotting ---
    plt.figure(figsize=(12, 8))

    # SOC Plot
    plt.subplot(3, 1, 1)
    plt.plot(time_log, soc_log, color='green')
    plt.ylabel("SOC (%)")
    plt.title("State of Charge Over Time")
    plt.grid(True)

    # Range Plot
    plt.subplot(3, 1, 2)
    plt.plot(time_log, range_log, color='blue')
    plt.ylabel("Remaining Range (km)")
    plt.title("Remaining Range Over Time")
    plt.grid(True)

    # Solar Power Plot
    plt.subplot(3, 1, 3)
    plt.plot(time_log, solar_log, color='orange')
    plt.xlabel("Time (min)")
    plt.ylabel("Solar Power (W)")
    plt.title("Solar Input Over Time")
    plt.grid(True)

    plt.tight_layout()
    plt.show()

# Run the simulation
if __name__ == "__main__":
    simulate_soc_range()
