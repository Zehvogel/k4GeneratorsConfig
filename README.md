# k4Generators


## k4Generators


## Description
A python based module for the automatic generation of inputfiles for  Monte-Carlo(MC) generators.

## Requirements
`Python >= 3.7`\
`PyYaml`  

Check your python version
```
python --version
```

you can install pyYaml as user with:
```
pip3 install pyyaml --user
```

## Usage
Before begining, you should setup the environment by: 
```
source /path/to/k4generators/setup.(tc)(z)sh
```
The setup script will check that python3 is available on your machine.

Once you have written your own inputfile(`input.yaml`), as seen in the [examples](https://gitlab.com/aprice/k4generators/-/tree/main/Examples?ref_type=heads), execute the following:\

`k4gen -f input.yaml`

This will create a directory containing the desired runcards. The directory can be set in the inputfile as:\
`OutDir: /path/to/out`
