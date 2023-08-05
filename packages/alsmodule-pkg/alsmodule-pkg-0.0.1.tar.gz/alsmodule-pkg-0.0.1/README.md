# Ambient Light Sensor (ALS) Package
# Copyright (C) 2019 Jean-Jacques Puig

This module implements a trivial interface to access ambient light sensors
available on some Apple computers (iMac...).

Usage is very simple; the 'als' module exports only one module method,
getSensorReadings(), which returns raw samples values as a list of two (Long)
integers.

import als
print(als.getSensorReadings())
