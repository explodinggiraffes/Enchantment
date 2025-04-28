Instructions for setting up the Enchantment project on macOS.

* Step 1: Install Simple Direct Media Layer (SDL2) using brew:
brew install SDL2
brew install SDL2_image
brew install SDL2_ttf

Update your shell's resrouce file:
export LD_LIBRARY_PATH=/opt/homebrew/lib:$LD_LIBRARY_PATH

* Step 2: Create the Enchantment project directory and cd to it

* Step 3: Obtain a copy of dejavu10x10_gs_tc.png and put it at the top level of the project directory

* Step 4: Create a virtual Python environment using venv:
python3 -m venv .venv
source ./.venv/bin/activate

* Step 5: Install project requirements

In the project root directory, create requirements.txt with the following entries:
tcod>=18.0.0
numpy>=2.2.4

pip3 install -r requirements.txt

To update: pip3 install --upgrade -r requirements.txt
