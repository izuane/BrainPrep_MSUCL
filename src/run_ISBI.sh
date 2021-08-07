echo "Running reorganize..."
python reorganize.py
echo "Running registration..."
python registration.py
echo "Running skull_stripping..."
python skull_stripping.py
echo "Running bias_correction..."
python bias_correction.py
echo "Finished."
