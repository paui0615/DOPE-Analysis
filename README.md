# Outline
### This project uses [DOP-E method](https://academic.oup.com/gji/article/216/3/1817/5222650), which is an open source code on [Github](https://github.com/berbellini/DOP-E) that estimates Rayleigh wave properties and constructs underground velocity structures, to perform data analysis on the mountainous area of ​​Kaohsiung City in Taiwan.
### This project uses python for data processing and analysis, and the package "matplotlib" is utilized for data visualization. Through these analyses, we have a breakthrough understanding of Rayleigh wave characteristics in the Chulin landslide area of ​​Taiwan, which will be helpful for future landslide remediation and prevention.

# Prerequisites
* python >= 3.6

# Install
`pip install -r requirements.txt`

# Usage
`python Polarization.py`
### (Or other python scripts)

# Results
`python Polarization.py`
### Plotting the polarization attribute for 4 months to check how do the Rayleigh waves distribute.
![Polarization example.](https://github.com/paui0615/DOPE-Analysis/assets/125962545/3d5ef861-19c3-4ebc-8f85-bbefac39f1ac)

`python BAZ_HV.py`
### Plotting H/V ratios and back of azimuth of rayleigh waves for 4 months to understand the changes of the ambient noise source.
![BAZ_HV example.](https://github.com/paui0615/DOPE-Analysis/assets/125962545/eaf38755-3a5a-454e-aff8-2e86803658d4)

`python Weather_HVdiff.py`
### Plot the H/V difference throughout the year to see if there is any relationship between climate change or GPS data and H/V.
![Weather_HVdiff example.](https://github.com/paui0615/DOPE-Analysis/assets/125962545/c917a4b2-9b62-47c2-a765-f2f696f19819)

`python Spectrogram_Lupit.py`
### Plot the ambient noise spectorgram during Typhoon Lupit.
![Spectrogram_Lupit example.](https://github.com/paui0615/DOPE-Analysis/assets/125962545/a09e2a42-a5ca-4e42-8d3f-f840a5e89f6f)

# Citations
- [Constraining S-wave velocity using Rayleigh wave ellipticity from polarization analysis of seismic noise.(Berbellin et al., 2019)](https://academic.oup.com/gji/article/216/3/1817/5222650)
- [Polarized Earth's ambient microseismic noise.(Schimmel et al., 2011)](https://agupubs.onlinelibrary.wiley.com/doi/full/10.1029/2011GC003661)
- [Constraining Chulin deep-seated landslide velocity structure with Rayleigh wave ellipticity.(Huang, 2022)](http://tdr.lib.ntu.edu.tw/jspui/handle/123456789/86194)
