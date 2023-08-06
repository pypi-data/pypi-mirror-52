import pickle
import numpy as np
from emulchem.network import NeuralNet
import torch
import torch.nn as nn
import torchvision
import torchvision.transforms as transforms
import glob
import os


path_emulchem = os.path.dirname(__file__)
print(path_emulchem)

def molecule_list():
    """Returns an array containing a list of all of the molecules included in the emulator"""
    query = os.path.join(path_emulchem,"data","chem","scaler*.p")
    files = glob.glob(query)
    molecules = [f.split(".")[0][6:] for f in files]
    return molecules

class Emulator():
    def __init__(self,specie):
        self.specie = specie

    def get_prediction_list(self,x):
        x = np.array(x)
        x_val = self.input_scaler.transform(x.reshape(1,-1))
        y_val = self.neural_network(torch.FloatTensor(x_val)).detach().numpy()[0]
        y_val = self.output_scaler.inverse_transform(y_val.reshape(1,-1))
        return y_val[0][0]        




class ChemistryEmulator(Emulator):
    def __init__(self,specie):
        Emulator.__init__(self,specie)
        self.neural_network = NeuralNet(input_size=6,hidden_size=200,hidden_size2=100,hidden_size3=50,num_outputs=1)
        path_chem = os.path.join(path_emulchem,"data","chem")
        #self.neural_network.load_state_dict(torch.load(os.path.join(path_emulchem,"data/chem/network{}".format(self.specie))))
        self.neural_network.load_state_dict(torch.load(os.path.join(path_chem,"network{}".format(self.specie))))
        with open(os.path.join(path_chem,"minMaxScaler.p"),"rb") as f:
            self.input_scaler = pickle.load(f)
        with open(os.path.join(path_chem,"scaler{}.p".format(self.specie)),"rb") as f:
            self.output_scaler= pickle.load(f)
    
    def get_prediction(self,radfield,zeta,density,av,temperature,metallicity):
        """radfield
        zeta
        density
        av 
        temperature kelvin
        metallicity """
        self.check_bounds(radfield,zeta,density,av,temperature,metallicity)
        x = [radfield,zeta,density,av,temperature,metallicity]
        y = np.exp(self.get_prediction_list(x))
        return y

    def check_bounds(self,radfield,zeta,density,av,temperature,metallicity):
        """raises an error if the supplied parameter values are outside emulator range"""
        av_bounds = [1,100]
        density_bounds = [10**4,10**6]
        temperature_bounds = [10,200]
        metallicity_bounds = [0,2]
        radfield_bounds = [1,10**3]
        zeta_bounds = [1,10**3]

        out_of_bounds = []
        bounds_msg = "{} was {} which is outside of the emulator bounds of {} to {}\n"

        if av<av_bounds[0] or av>av_bounds[1]:
            out_of_bounds.append(bounds_msg.format("av",av,av_bounds[0],av_bounds[1]))
        if density<density_bounds[0] or density>10**6:
            out_of_bounds.append(bounds_msg.format("density",density,density_bounds[0],density_bounds[1]))
        if temperature<temperature_bounds[0] or temperature>temperature_bounds[1]:
            out_of_bounds.append(bounds_msg.format("temperature",temperature,temperature_bounds[0],temperature_bounds[1]))
        if metallicity<metallicity_bounds[0] or metallicity>metallicity_bounds[1]:
            out_of_bounds.append(bounds_msg.format("metallicity",metallicity,metallicity_bounds[0],metallicity_bounds[1]))
        if radfield<radfield_bounds[0] or radfield>radfield_bounds[1]:
            out_of_bounds.append(bounds_msg.format("radfield",radfield,radfield_bounds[0],radfield_bounds[1]))
        if zeta<zeta_bounds[0] or zeta>zeta_bounds[1]:
            out_of_bounds.append(bounds_msg.format("zeta",zeta,zeta_bounds[0],zeta_bounds[1]))

        if len(out_of_bounds) !=0:
            raise Exception("".join(out_of_bounds))
            #raise Exception(", ".join(out_of_bounds)+ " out of emulator usable bounds")





class RadexEmulator(Emulator):
    def __init__(self,specie,transition):
        Emulator.__init__(self,specie)
        self.transition  = transition
        self.neural_network = NeuralNet(input_size=3,hidden_size=200,hidden_size2=100,hidden_size3=50,num_outputs=1)
        path_rad = os.path.join(path_emulchem,"data","rad")
        self.neural_network.load_state_dict(torch.load(os.path.join(path_rad,"network{}{}".format(self.specie,self.transition))))
        with open(os.path.join(path_rad,"minMaxScaler{}{}.p".format(self.specie,self.transition)),"rb") as f:
            self.input_scaler = pickle.load(f)
        with open(os.path.join(path_rad,"scaler{}{}.p".format(self.specie,self.transition)),"rb") as f:
            self.output_scaler= pickle.load(f)

    def get_prediction(self,temperature,density,column_density,line_width=1):
        """Temperature:Kelvin
        Density:...
        column_density:
        line-width:
        """
        self.check_bounds(temperature,density,column_density,line_width)
        x = [temperature,density,np.log10(column_density/line_width)]
        y = self.get_prediction_list(x)*line_width
        return y

    def check_bounds(self,temperature,density,column_density,line_width):
        density_bounds = [10**4,10**6]
        temperature_bounds = [10,200]
        CO_bounds = [10**13,10**19]
        CS_bounds = [10**10,10**18]
        HCOplus_bounds = [10**8,10**15]
        HCN_bounds = [10**9,10**17]

        out_of_bounds = []
        scaled_column_density = column_density/line_width

        bounds_msg = "{} was {} which is outside of the emulator bounds of {} to {}\n"

        if density<density_bounds[0] or density>10**6:
            out_of_bounds.append(bounds_msg.format("density",density,density_bounds[0],density_bounds[1]))
        if temperature<temperature_bounds[0] or temperature>temperature_bounds[1]: 
            out_of_bounds.append(bounds_msg.format("temperature",temperature,temperature_bounds[0],temperature_bounds[1]))
        if self.specie=="CO":
            if scaled_column_density<CO_bounds[0] or scaled_column_density>CO_bounds[1]:
                out_of_bounds.append(bounds_msg.format("scaled column density",scaled_column_density,CO_bounds[0],CO_bounds[1]))
        elif self.specie=="CS":
            if scaled_column_density<CS_bounds[0] or scaled_column_density>CS_bounds[1]:
                out_of_bounds.append(bounds_msg.format("scaled column density",scaled_column_density,CS_bounds[0],CS_bounds[1]))
        elif self.specie=="HCO+":
            if scaled_column_density<HCOplus_bounds[0] or scaled_column_density>HCOplus_bounds[1]:
                out_of_bounds.append(bounds_msg.format("scaled column density",scaled_column_density,HCOplus_bounds[0],HCOplus_bounds[1]))
        elif self.specie=="HCN":
            if scaled_column_density<HCN_bounds[0] or scaled_column_density>HCN_bounds[1]:
                out_of_bounds.append(bounds_msg.format("scaled column density",scaled_column_density,HCN_bounds[0],HCN_bounds[1]))

        if len(out_of_bounds) !=0:
            raise Exception("".join(out_of_bounds))




"""
    def check_bounds(self,temperature,density,column_density,line_width):
        out_of_bounds = []
        scaled_column_density = column_density/line_width
        if temperature<10 or temperature>200:
            out_of_bounds.append("temperature")
        if density<10**4 or density>10**6:
            out_of_bounds.append("density")

        if self.specie=="CO":
            if scaled_column_density<10**13 or scaled_column_density>10**19:
                out_of_bounds.append("column_density to line-width ratio")
        elif self.specie=="CS":
            if scaled_column_density<10**10 or scaled_column_density>10**18:
                out_of_bounds.append("column_density to line-width ratio")
        elif self.specie=="HCO+":
            if scaled_column_density<10**8 or scaled_column_density>10**15:
                out_of_bounds.append("column_density to line-width ratio")
        elif self.specie=="HCN":
            if scaled_column_density<10**9 or scaled_column_density>10**17:
                out_of_bounds.append("column_density to line-width ratio")


        if len(out_of_bounds) !=0:
            raise Exception(", ".join(out_of_bounds)+ " out of emulator usable bounds")

"""

