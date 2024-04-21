#!/usr/bin/env python3
import yaml
import os
import pathlib
import pyaml

with open("test_profile.yml") as f:
        data = yaml.safe_load(f)
        installed_addons = data[1]["installed-addons"]
        installed_addons["vanilla"].append({"name":"dir"})
        



with open("test_profile.yml", 'w') as f:
        yaml.dump(data, f, default_flow_style=False)




with open("test_profile.yml") as f:
        data = yaml.safe_load(f)

        installed_addons = data[1]["installed-addons"]
        for x in installed_addons:
            for y in installed_addons[x]:
                print(y)



def p_profile(profile='profile.yml'):
    with open(profile) as f:
        yam = yaml.safe_load(f)
        print(pyaml.dump(yam))



p_profile(profile='test_profile.yml')
