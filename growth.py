from datetime import date, datetime
#from kivy.clock import Clock
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.properties import ObjectProperty, StringProperty
import pandas as pd
import scipy.interpolate as spi
import bisect
#import matplotlib.pyplot as plt
#import datetime as dt
#from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelHeader
from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
#from kivy.uix.boxlayout import BoxLayout
from matplotlib.figure import Figure

def calculate_percentile_from_table(table_file_path,tab_path, target_age_in_days, percentile_values, target_measure_value, value_description):
    # read the Excel file and extract the age in days from the first column of each row
    df = pd.read_excel(table_file_path, tab_path, skiprows=[0], usecols='A,E:S')
    ages = df.iloc[:, 0]
    
    # read the percentiles and measure values for the row corresponding to the target age
    percentiles_and_measures = df[df.iloc[:, 0] == target_age_in_days].iloc[0, 1:]

    # extract the percentiles and measure values
    percentiles = percentile_values
    measures = percentiles_and_measures.values

    # perform cubic spline interpolation on the percentiles and measure values
    tck = spi.splrep(percentiles, measures, s=0)

    # find the percentile value corresponding to the target measure value using inverse interpolation
    idx = bisect.bisect_left(measures, target_measure_value)
    if idx == 0:
        percentile = percentiles[0]
    elif idx == len(measures):
        percentile = percentiles[-1]
    else:
        # interpolate between the two nearest percentiles
        y0, y1 = measures[idx-1], measures[idx]
        p0, p1 = percentiles[idx-1], percentiles[idx]
        percentile = p0 + (p1-p0) * (target_measure_value-y0) / (y1-y0)
    #print("Percentile at {}: {}".format(value_description, target_measure_value))
    #print("Percentile: {}".format(percentile))
    return percentile

def plot_growth_chart(table_file_path,tab_path, age_in_days, height, Y_axis_label, Gender):

    data = pd.read_excel(table_file_path,tab_path)
    # Extract data from input
    age = data['Day']
    Normal = data['SD0']
    sD2 = data['SD2']
    sD3 = data['SD3']
    sD2neg = data['SD2neg']
    sD3neg = data['SD3neg']

    # Create plot
    figure = Figure()
    ax = figure.add_subplot()
    ax.plot(age, Normal, label='Normal')
    ax.plot(age, sD2, label='+2')
    ax.plot(age, sD3, label='+3')
    ax.plot(age, sD2neg, label='-2')
    ax.plot(age, sD3neg, label='-3')

    # Enter age in days as the X coordinate of the plt.scatter and height as Y
    ax.scatter(age_in_days, height, color='green', label='Child height', s=50)

    # Add title and axis labels
    ax.set_title('WHO Growth Charts' + Gender + '(0-5 years)')
    ax.set_xlabel('Age (Days)')
    ax.set_ylabel( Y_axis_label + '(cm)')

    # Add legend
    ax.legend()

    # Add grid
    ax.grid(True, which='both', linestyle='dashdot', color='grey', alpha=0.9)

    # Set size of grid cells
    ax.minorticks_on()
    ax.grid(True, which='minor', linestyle='--', color='grey', alpha=0.5)
    ax.tick_params(axis='both', which='both', length=0)

    return figure


class MainScreen(Screen):
    dob = ObjectProperty(None)
    height_input = ObjectProperty(None)
    weight_input = ObjectProperty(None)
    head_circumference_input = ObjectProperty(None)
    height_percentile_text = StringProperty('N/A')
    weight_percentile_text = StringProperty('N/A')
    H_C_percentile_text = StringProperty('N/A')
    
    
    #calculate the age from the dob and today's date
    def calculate_age(self):
        today = date.today()
        try :
            birth_date = datetime.strptime(self.dob.text, '%Y%m%d').date()
            age_in_days = (today - birth_date).days
        except ValueError:
            self.dob.text = ''
            self.dob.hint_text_color = (1,0,0,1) # Set hint text color to red
            return None
        else:
            self.dob.hint_text_color = (1,1,1,1)
            age_in_years = age_in_days / 365.25
            return age_in_days
    
    def print_toggle_state(self):
        male_button = self.ids.male_button
        female_button = self.ids.female_button
        if male_button.state == 'down':
            self.gender = 'Boy'
            print(f'Gender : {self.gender}')
        elif female_button.state == 'down':
            self.gender = 'Girl'
            print(f'Gender : {self.gender}')
        return self.gender
        

        #Error handling on input and assinging to variable names
    def press(self):
        self.age_in_days = self.calculate_age() 
        if self.age_in_days is None:
            return  # return early if age_in_days is None
    
        
        height_input = self.ids.height_input
        try:
            height = float(height_input.text)
        except ValueError:
            height_input.text = ''
            height = 0
        weight_input = self.ids.weight_input
        try:
            weight = float(weight_input.text)
        except ValueError:
            weight_input.text = ''
            weight = 0
        head_circumference_input = self.ids.head_circumference_input
        try:
            head_circumference = float(head_circumference_input.text)
        except ValueError:
            head_circumference_input.text = ''
            head_circumference = 0 
        
        print(f'Age: {self.age_in_days}, Height: {height}, Weight: {weight}, Head Circumference: {head_circumference}')

        if self.ids.male_button.state == 'down':
             # Call the function to calculate percentile using boy's table
            h_eight_percentile = calculate_percentile_from_table('C:\\Users\\munya\\Downloads\\lhfa-boys-percentiles-expanded-tables (1).xlsx','lhfa_boys_p_exp', self.age_in_days, 
                               [0.001, 0.01, 0.03, 0.05, 0.1, 0.15, 0.25, 0.5, 0.75, 0.85, 0.9, 0.95, 0.97, 0.99, 0.999],
                                 height, "h_eight")
            W_eight_percentile = calculate_percentile_from_table('C:\\Users\\munya\\Downloads\\Who boys percentile charts\\wfa-boys-percentiles-expanded-tables.xlsx','wfa_boys_p_exp',  self.age_in_days,
                                [0.001, 0.01, 0.03, 0.05, 0.1, 0.15, 0.25, 0.5, 0.75, 0.85, 0.9, 0.95, 0.97, 0.99, 0.999],
                                weight, "W_eight")
            H_C_Percentile = calculate_percentile_from_table('C:\\Users\\munya\Downloads\\Who boys percentile charts\\hcfa-boys-percentiles-expanded-tables.xlsx','hcfa_boys_p_exp', self.age_in_days,
                                [0.001, 0.01, 0.03, 0.05, 0.1, 0.15, 0.25, 0.5, 0.75, 0.85, 0.9, 0.95, 0.97, 0.99, 0.999],
                                head_circumference, "H_C")
            
        elif self.ids.female_button.state == 'down':
            h_eight_percentile = calculate_percentile_from_table('C:\\Users\\munya\\OneDrive\\Desktop\\coding stuff\\New folder\\Who charts\\Girls percentile tables.xlsx','Girls_Height_Age',  self.age_in_days, 
                                [0.001, 0.01, 0.03, 0.05, 0.1, 0.15, 0.25, 0.5, 0.75, 0.85, 0.9, 0.95, 0.97, 0.99, 0.999],
                                  height, "h_eight")
            W_eight_percentile = calculate_percentile_from_table('C:\\Users\\munya\\OneDrive\\Desktop\\coding stuff\\New folder\\Who charts\\Girls percentile tables.xlsx','Girls_Weight_Age',   self.age_in_days,
                                [0.001, 0.01, 0.03, 0.05, 0.1, 0.15, 0.25, 0.5, 0.75, 0.85, 0.9, 0.95, 0.97, 0.99, 0.999],
                                 weight, "W_eight")
            H_C_Percentile = calculate_percentile_from_table('C:\\Users\\munya\\OneDrive\\Desktop\\coding stuff\\New folder\\Who charts\\Girls percentile tables.xlsx','Girls_HC_Age',  self.age_in_days,
                                [0.001, 0.01, 0.03, 0.05, 0.1, 0.15, 0.25, 0.5, 0.75, 0.85, 0.9, 0.95, 0.97, 0.99, 0.999],
                                head_circumference,"H_C")
            
        
        else : return
             
         # Set the percentile value to the property
        if  h_eight_percentile is not None:
            self.height_percentile_text = str( h_eight_percentile)
        if  W_eight_percentile is not None:
            self.weight_percentile_text = str(W_eight_percentile)
        if  H_C_Percentile is not None:
            self.H_C_percentile_text = str(H_C_Percentile)
             
        #print("Percentile at {}: {}".format(value_description, target_measure_value))
        print("Percentile: {}".format(h_eight_percentile))
            
        # Switch to the new screen
        self.manager.current = "result_screen"
       
        

class ResultScreen(Screen):

    head_circumference_label_text = StringProperty("")
    weight_label_text = StringProperty("")
    height_label_text = StringProperty("")
    age_label_text = StringProperty("")  # Define the age_label_text attribute as a StringProperty with an initial value of ""
    gender_label_text = StringProperty("")
    height_percentile_text = StringProperty("")
    weight_percentile_text = StringProperty("")
    head_circumference_percentile_text = StringProperty("")
    
    def back(self):
        self.manager.current = "main_screen"
    
    def press(self, value):
        self.manager.switch_to(self.manager.get_screen("main_screen"))
    
    def reset(self):
        main_screen = self.manager.get_screen("main_screen")
        main_screen.ids.dob.text = ''
        main_screen.ids.height_input.text = ''
        main_screen.ids.weight_input.text = ''
        main_screen.ids.head_circumference_input.text = ''

    # Access the gender variable from MainScreen
    def on_enter(self, *args):
        main_screen = self.manager.get_screen("main_screen")
        Age = main_screen.age_in_days
        gender = main_screen.gender
        height = main_screen.ids.height_input.text
        weight = main_screen.ids.weight_input.text
        head_circumference = main_screen.ids.head_circumference_input.text
        heightpercentile = main_screen.height_percentile_text   
        weightpercentile = main_screen.weight_percentile_text
        HCpercentile = main_screen.H_C_percentile_text


        self.gender_label_text =  f"Gender: {gender}"
        self.age_label_text = str(Age)
        self.height_label_text = height
        self.weight_label_text = weight
        self.head_circumference_label_text= head_circumference
        self.height_percentile_text = heightpercentile
        self.weight_percentile_text = weightpercentile
        self.head_circumference_percentile_text = HCpercentile


class ChartScreen(Screen):
    
    def back(self):
        self.manager.current = "result_screen"

    def on_enter(self):

    # access variables from MainScreen
        main_screen = self.manager.get_screen("main_screen")
        male_button = main_screen.ids.male_button
        female_button = main_screen.ids.female_button
        Age = main_screen.age_in_days
        height = main_screen.ids.height_input.text
        weight = main_screen.ids.weight_input.text
        HC = main_screen.ids.head_circumference_input.text

        if male_button.state == 'down':
           
            height_plot = plot_growth_chart('C:\\Users\\munya\\Downloads\\lhfa-boys-zscore-expanded-tables.xlsx', 'LFA_boys_z_exp',Age,float(height), 'height', ' Boy ')
            weight_plot = plot_growth_chart('C:\\Users\\munya\\Downloads\\wfa-boys-zscore-expanded-tables (1).xlsx', 'WFA_boys_z_exp',Age,float(weight), 'Weight', ' Boy ')
            HC_plot = plot_growth_chart('C:\\Users\\munya\\Downloads\\hcfa-boys-zscore-expanded-tables.xlsx', 'HCFA_boys_z_exp',Age,float(HC), 'Head Cirumference', ' Boy ')

        elif female_button.state == 'down':
            
            height_plot = plot_growth_chart('C:\\Users\\munya\\Downloads\\lhfa-girls-zscore-expanded-tables (1).xlsx', 'LFA_girls_z_exp',Age,float(height), 'height', ' Girl ')
            weight_plot = plot_growth_chart('C:\\Users\\munya\\Downloads\\lhfa-girls-zscore-expanded-tables (1).xlsx', 'WFA_girls',Age,float(weight), 'Weight', ' Girl ')
            HC_plot = plot_growth_chart('C:\\Users\\munya\\Downloads\\lhfa-girls-zscore-expanded-tables (1).xlsx', 'HCFA_girls',Age,float(HC), 'Head Cirumference', ' Girl ')

        chart_box1 = self.ids.box1 # Reference to the BoxLayout for Chart 1
        chart_box1.clear_widgets()  # Clear existing widgets in the box
        chart_box1.add_widget(FigureCanvasKivyAgg(figure=height_plot))

        chart_box2 = self.ids.box2
        chart_box2.clear_widgets()
        chart_box2.add_widget(FigureCanvasKivyAgg(figure=weight_plot))

        chart_box3 = self.ids.box3
        chart_box3.clear_widgets()
        chart_box3.add_widget(FigureCanvasKivyAgg(figure=HC_plot))

       
class WindowManager(ScreenManager):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(MainScreen(name='main_screen'))
        self.add_widget(ResultScreen(name='result_screen'))
        self.add_widget(ChartScreen(name='charts_screen'))
        self.current = "main_screen"
       

# Designate Our .kv design file
kv = Builder.load_file('C:\\Users\\munya\\OneDrive\\Desktop\\coding stuff\\Kivy\\Paeds\\gre.kv')

class growth(App):
    def build(self):
        return kv
    
if __name__ == '__main__':
    growth().run()
