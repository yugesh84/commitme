# Python CLI for Generating Commit Messages

This tool is a Python-based Command Line Interface (CLI) designed to generate meaningful commit messages automatically. It leverages a language model to understand the changes made in a commit and suggests a commit message that summarizes those changes effectively.

## Features

- **Automatic Commit Message Generation:** Automatically generates commit messages based on the staged changes in your git repository.
- **Language Model Integration:** Utilizes a state-of-the-art language model to understand and summarize the changes.
- **Easy to Use:** Simple CLI interface for generating commit messages with a single command.

## Local Development

To use this tool locally, you need to have Python installed on your system. Follow these steps to set up the CLI:

1. Clone the repository to your local machine.
2. Navigate to the cloned directory.
3. Type the following commands to setup python environment
```
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
4. Make a copy of `commitme.properties.json.template` and rename it to `commitme.properties.json`. Fill in the required fields in the file.
5. Run the tool using the command `python commitme.py`


## Usage

Linux and macos binaries are also attached as assets to the latest release. An [example release](https://github.com/seriesfi/commitMe/releases/tag/0.0.2)

Steps to use the binary:

_NOTE: This will not fully work now as you'll need to carry over a properties file wherever you use the binary. This is a known issue and will be fixed in the next release._
1. Download the binary for your OS from the latest release
2. Rename the downloaded binary to `commitMe`
3. Make the binary executable using `chmod +x commitMe`
4. Add the binary to your path
5. Run the binary using `commitMe` in your git repository. The binary will automatically detect the changes and suggest a commit message.

## Contributing

Contributions to improve the tool are welcome. Please feel free to fork the repository, make your changes, and submit a pull request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
