
# Bancho Loadtesting

This is a tool I have been using to test the performane of my bancho server.
I decided to rewrite it and release it to the public, to benefit others who may find it useful somehow.

## Usage

To use this tool, ensure you have Python installed on your system along with `pip`.
Then, follow these steps:

1. Clone the repository:

    ```shell
    git clone https://github.com/Lekuruu/bancho-loadtesting.git
    cd bancho-loadtesting
    ```

2. Install the required dependencies:

    ```shell
    pip install -r requirements.txt
    ```

3. Set up the configuration:

    ```shell
    cp config.example.json config.json
    # Open and edit the config.json with your preferred editor...
    ```

4. Run the tool:

    ```shell
    python main.py
    ```

Have fun destroying your server!
