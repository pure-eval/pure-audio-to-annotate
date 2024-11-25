# pure-audio-to-annotate

This repository contains scripts to prepare and maintain the audio
data repository for the PURE (Perceptual Universal Reconstruction
Evaluation) audio annotation system.

## Overview

The main script (`generate_config.py`) scans a directory of audio
files and generates a configuration file that maps the relationships
between reference and transformed audio files. This configuration
is used by the PURE annotation system to present audio pairs for
evaluation.

## Prerequisites

- Python 3.7+
- Git LFS (Large File Storage)

## Setting up Git LFS

Git LFS is required for handling audio files efficiently. To set up:

1. Install Git LFS:
   ```bash
   # macOS (with Homebrew)
   brew install git-lfs

   # Ubuntu/Debian
   sudo apt install git-lfs

   # Windows (with Chocolatey)
   choco install git-lfs
   ```

2. Enable Git LFS:
   ```bash
   git lfs install
   ```

3. Track WAV files:
   ```bash
   git lfs track "*.wav"
   ```

4. Make sure .gitattributes is committed:
   ```bash
   git add .gitattributes
   git commit -m "Configure Git LFS for audio files"
   ```

## Usage

1. Clone this repository:
   ```bash
   git clone https://github.com/pure-eval/pure-audio-to-annotate
   cd pure-audio-to-annotate
   ```

2. Run the configuration generator:
   ```bash
   python generate_config.py experiment_dir
   ```

The script will:
- Scan the `{experiment_dir}` directory
- Generate `config/{experiment_dir}.json`

## Directory Structure

Expected input structure:
```
experiment_dir/
└──.../
    ├── id.wav           # Transformed audio
    ├── id-reference.wav # Reference audio
    └── id.json          # Metadata
```

## Audio License

The audio files in this repository are derived from the FSD50K dataset. Usage is subject to the license terms of FSD50K. For more information, see:
- [FSD50K Dataset](https://zenodo.org/record/4060432)
- [FSD50K License](https://creativecommons.org/licenses/by/4.0/)

## Tips for Working with Git LFS

1. Checking LFS status:
   ```bash
   git lfs status
   ```

2. Pulling audio files:
   ```bash
   git lfs pull
   ```

3. Verifying tracked files:
   ```bash
   git lfs ls-files
   ```

4. If you need to clear local LFS cache:
   ```bash
   git lfs prune
   ```

Remember to always pull LFS files after cloning:
```bash
git clone https://github.com/pure-eval/pure-audio-to-annotate
cd pure-audio-to-annotate
git lfs pull
```

## Contributing

1. When adding new audio files:
   - Place them in the correct directory structure
   - Run the configuration generator
   - Commit both the files and the updated config
   - Push using regular git commands (Git LFS handles the files automatically)

2. Verify file tracking:
   ```bash
   git lfs status
   git status
   ```
