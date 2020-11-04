#bin/bash bash

black monolith
python3 -m pytest --cov-config .coveragerc --cov monolith monolith/tests/test_booking_services.py