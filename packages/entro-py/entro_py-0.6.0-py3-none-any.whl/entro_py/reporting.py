from .entrolib import compute_shannon, compute_monte_carlo_pi, get_pi_deviation, compute_chi_squared, compute_entropy_graph
from os import walk, path
"""
reporting.py: A set of functions to create entropy reports.
"""
__author__    = "Pavel Chikul"
__copyright__ = "Copyright 2018, REGLabs"


class report:
    def __init__(self, quite = False):
        self.mute_console = quite


    def console_out(self, message):
        if not self.mute_console:
            print(message)


    def process_directory_report(self, in_path, out_file_name):
        """
        Creates an entropy report for a list of files in directory and saves it in a CSV spreadsheet.
        """
        (_, _, file_list) = next(walk(in_path), (None, None, []))
        if out_file_name != "":
            with open(out_file_name, "w") as file_out:
                file_out.write("File Name;File Size (B);Entropy;Pi;Pi Deviation (%);Chi-Squared\r")

        self.console_out("%30s %15s %15s %15s %15s %15s" % ("File Name", "File Size (B)", "Entropy", "Pi", "Pi Deviation (%)", "Chi-Squared"))

        for file_name in file_list:
            byte_array = []
            with open(path.join(in_path, file_name), "rb") as f:
                byte_array = f.read()

            file_size = len(byte_array)
            entropy = compute_shannon(byte_array)
            new_pi = compute_monte_carlo_pi(byte_array)
            pi_deviation = get_pi_deviation(new_pi)
            chi_squared = compute_chi_squared(byte_array)

            if out_file_name != "":
                with open(out_file_name, "a") as file_out:
                    file_out.write("%s;%d;%f;%f;%f;%f\r" % (file_name, file_size, entropy, new_pi, pi_deviation, chi_squared))

            self.console_out("%30s %15d %15f %15f %15f %15f" % (file_name, file_size, entropy, new_pi, pi_deviation, chi_squared))


    def process_directory_graphs(self, in_path, step):
        """
        Calculates entropy oscillations for every file in a passed directory and writes 
        separate graph reports into CSV spreadsheets named <in_path>/<filename>.csv.
        """
        (_, _, file_list) = next(walk(in_path), (None, None, []))

        for file_name in file_list:
            self.console_out(f"Processing file: {file_name}")
            self.write_file_graph(path.join(in_path, file_name), path.join(in_path, file_name) + ".csv", step)


    def write_file_report(self, in_file_name, out_file_name):
        """
        Creates an entropy report for a single file and saves it in a CSV spreadsheet.
        """
        byte_array = []
        with open(in_file_name, "rb") as f:
            byte_array = f.read()

        file_size = len(byte_array)
        entropy = compute_shannon(byte_array)
        new_pi = compute_monte_carlo_pi(byte_array)
        pi_deviation = get_pi_deviation(new_pi)
        chi_squared = compute_chi_squared(byte_array)

        if out_file_name != "":
            with open(out_file_name, "w") as file_out:
                file_out.write("File Name;File Size (B);Entropy;Pi;Pi Deviation (%);Chi-Squared\r")
                file_out.write("%s;%d;%f;%f;%f;%f\r" % (in_file_name, file_size, entropy, new_pi, pi_deviation, chi_squared))
            
        self.console_out("%30s %15s %15s %15s %15s %15s" % ("File Name", "File Size (B)", "Entropy", "Pi", "Pi Deviation (%)", "Chi-Squared"))
        self.console_out("%30s %15d %15f %15f %15f %15f" % (in_file_name, file_size, entropy, new_pi, pi_deviation, chi_squared))
    
    
    def write_file_graph(self, in_file_name, out_file_name, step, start=0, end=0):
        """
        Calculates entropy oscillations for a file and writes it to CSV spreadsheet.
        """
        byte_array = []
        with open(in_file_name, "rb") as f:
            byte_array = f.read()

        if start != 0 or end != 0:
            byte_array = byte_array[start:end]

        shannons, chis, _ = compute_entropy_graph(byte_array, step)
        self.console_out("%10s %15s" % ("Entropy", "Chi-Squared"))

        if out_file_name != "":
            with open(out_file_name, "w") as file_out:
                file_out.write("Entropy (per %d bytes);Chi-Squared (per %d bytes)\r" % (step, step))
                for i in range(len(shannons)):
                    self.console_out("%10f %15f" % (shannons[i], chis[i]))
                    file_out.write("%f;%f\r" % (shannons[i], chis[i]))
        else:
            for i in range(len(shannons)):
                self.console_out("%10f %15f" % (shannons[i], chis[i]))
