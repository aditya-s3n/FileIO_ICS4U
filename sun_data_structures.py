import csv

def interpret_validity_num_sunspots(num_of_sunspots):
    if num_of_sunspots > -1:
        return False
    
    return True

def get_all_sunspot_data():
    all_sunspots = []

    with open("sunspot_data.csv", "r") as file_sunspots:
        file_sunspots.readline()
        file_sunspots = csv.reader(file_sunspots)

        for line in file_sunspots:
            year = int(line[1])
            month = int(line[2])
            day = int(line[3])
            num_sunspots = int(line[5])

            valid_sunspot_data = interpret_validity_num_sunspots(num_sunspots)

            if year >= 2002 and year <= 2018 and valid_sunspot_data:
                date = f"{year}-{month:02d}-{day:02d}" #EXPLAIN :02D IN REPORT, AND DELETE

                all_sunspots.append((date, num_sunspots))

    return all_sunspots


def get_all_flare_data():
    all_flares = {}

    with open("hessi.solar.flare.UP_To_2018.csv", "r") as file_flares:
        file_flares.readline()
        file_flares = csv.reader(file_flares)

        for line in file_flares:
            date = line[1]
            duration = int(line[5])
            number_of_flares = float(line[7]) # some values are in scientific notation (e.g 2e+05) - float required
                                              # ADD TO REPORT, AND DELETE

            energy_range = line[8].split("-")
            low_energy = int(energy_range[0])
            high_energy = int(energy_range[1])

            if date not in all_flares:
                all_flares[date] = []

            all_flares[date].append(((low_energy, high_energy), duration, number_of_flares))

    return all_flares


def time_series_analysis(sun_spot_list, flare_dict):
    sunspot_flare_dict = {}

    for day in sun_spot_list:
        date = day[0]
        num_sunspots = day[1]

        if date in flare_dict:
            flare_day = flare_dict[date]
            peak_flare_energy = 0
            for flares in flare_day:
                high_flare_energy = flares[0][1]
                
                if high_flare_energy > peak_flare_energy:
                    peak_flare_energy = high_flare_energy

            sunspot_flare_dict[date] = (num_sunspots, peak_flare_energy)

    return sunspot_flare_dict

def correlation_sunspots_flare(sunspot_list, flare_dict):
    correlation_sunspot_flare_dict = {}

    for day in sunspot_list:
        date = day[0]
        num_sunspots = day[1]

        if date in flare_dict:
            flares = flare_dict[date]
            
            num_flares = 0
            for flare in flares:
                num_flares += flare[2]

            correlation_sunspot_flare_dict[date] = (num_sunspots, num_flares)

    return correlation_sunspot_flare_dict


def main():
    # all_flares = { date: [((low_energy_value, high_energy_value), Duration, number_of_flares), …], … }
    # all_sunspots_daily = [(date, num_of_sunspots), … ]
    all_flares = get_all_flare_data()
    all_sunspots = get_all_sunspot_data()

    # time_series_sunspots_flare_energy_dict = { date: (num_of_sunspots, peak_flare_energy), … }
    time_series_dict = time_series_analysis(all_sunspots, all_flares)

    # flares_sunspots_daily = { date: (num_of_sunspots, num_of_flares), … }
    correlation_dict = correlation_sunspots_flare(all_sunspots, all_flares)

main()