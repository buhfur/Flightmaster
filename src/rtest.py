#!/usr/bin/env python3
import yaml
import os
import pathlib
'''
with open("profile.yml") as f:
        data = yaml.safe_load(f)
        installed_addons = data[0]["install-directories"]
        #installed_addons["vanilla"].append({"AtlasLoot":"/tmp/addons/vanilla/Interface/AddOns/AtlasLoot"})
        #installed_addons["vanilla"].append({"Bagnon":"/tmp/addons/vanilla/Interface/AddOns/Bagnon"})

#with open("test_profile.yml", 'w') as f:
        #yaml.dump(data, f, default_flow_style=False)
'''

with open("test_profile.yml") as f:
        data = yaml.safe_load(f)
        installed_addons = data[1]["installed-addons"]
        for addon in installed_addons["vanilla"]:
            print(addon.keys())
